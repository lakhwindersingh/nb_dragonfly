#!/usr/bin/env python3
"""
Main entry point for the SDLC Pipeline Engine
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
import yaml
from typing import Dict, Any

# Import orchestrator from package
from sdlc_pipeline_engine.pipeline_orchestrator import SDLCPipelineOrchestrator

def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('pipeline_engine.log')
        ]
    )

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file or environment.
    Preference order:
    1) Explicit path argument
    2) CONFIG_PATH env var
    3) config.yml (engine dir -> CWD)
    4) config.yaml (fallback)
    """

    # Resolve candidate config path if not explicitly provided
    if not config_path:
        env_path = os.getenv('CONFIG_PATH')
        engine_dir = Path(__file__).resolve().parent
        candidates = [
            env_path if env_path else None,
            str(engine_dir / 'config.yml'),
            'config.yml',
            str(engine_dir / 'config.yaml'),
            'config.yaml',
        ]
        # pick the first existing candidate
        for cand in candidates:
            if cand and os.path.exists(cand):
                config_path = cand
                break

    # Default configuration (used as base)
    config = {
        'prompts_base_dir': os.getenv('PROMPTS_BASE_DIR') or str(Path(__file__).resolve().parent.parent / 'sdlc-pipeline'),
        'ai_config': {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'default_model': 'gpt-4'
            }
        },
        'artifact_config': {
            'storage_path': os.getenv('ARTIFACT_STORAGE_PATH', './artifacts'),
            'max_storage_size': int(os.getenv('MAX_STORAGE_SIZE', 10 * 1024 * 1024 * 1024)),
            'retention_days': int(os.getenv('RETENTION_DAYS', 365))
        },
        'repository_config': {
            'git': {
                'default_provider': 'github'
            },
            'confluence': {
                'base_url': os.getenv('CONFLUENCE_URL'),
                'username': os.getenv('CONFLUENCE_USERNAME'),
                'api_token': os.getenv('CONFLUENCE_API_TOKEN')
            },
            'sharepoint': {
                'tenant_id': os.getenv('SHAREPOINT_TENANT_ID'),
                'client_id': os.getenv('SHAREPOINT_CLIENT_ID'),
                'client_secret': os.getenv('SHAREPOINT_CLIENT_SECRET')
            }
        },
        'workflow_config': {
            'max_concurrent_nodes': int(os.getenv('MAX_CONCURRENT_NODES', 10)),
            'default_timeout_seconds': int(os.getenv('DEFAULT_TIMEOUT', 1800)),
            'cleanup_interval_hours': int(os.getenv('CLEANUP_INTERVAL', 24))
        },
        'validation_config': {
            'quality_thresholds': {
                'minimum_score': float(os.getenv('MIN_QUALITY_SCORE', 75.0)),
                'error_threshold': int(os.getenv('ERROR_THRESHOLD', 0)),
                'warning_threshold': int(os.getenv('WARNING_THRESHOLD', 5))
            }
        }
    }

    # Load from resolved config file if any
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                # Shallow merge: config file values override defaults
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Failed to load config file {config_path}: {e}")

    return config

async def main():
    """Main application entry point"""
    
    # Setup logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting SDLC Pipeline Engine")
    
    try:
        # Load configuration
        # Prefer config.yml by default; fall back to config.yaml if needed
        explicit_path = os.getenv('CONFIG_PATH')
        if explicit_path and not os.path.exists(explicit_path):
            logging.warning(f"CONFIG_PATH set to '{explicit_path}' but file does not exist; falling back to auto-detect")
            explicit_path = None
        config = load_config(explicit_path)
        
        # Create orchestrator
        orchestrator = SDLCPipelineOrchestrator(config)
        
        # Validate AI configuration
        logger.info("Validating AI configuration...")
        ai_validation = await orchestrator.ai_processor.validate_configuration()
        
        for provider, is_valid in ai_validation.items():
            status = "✓" if is_valid else "✗"
            logger.info(f"{status} {provider}: {'Available' if is_valid else 'Not configured'}")
        
        if not any(ai_validation.values()):
            logger.error("No AI providers configured. Please check configuration.")
            return
        
        # Example: Load and execute a pipeline
        pipeline_file = os.getenv('PIPELINE_FILE')
        if pipeline_file and os.path.exists(pipeline_file):
            logger.info(f"Loading pipeline from {pipeline_file}")
            
            with open(pipeline_file, 'r') as f:
                pipeline_def = yaml.safe_load(f)
            
            # Create pipeline
            pipeline_id = await orchestrator.create_pipeline(pipeline_def)
            logger.info(f"Created pipeline: {pipeline_id}")
            
            # Get user inputs from environment or config
            user_inputs = {
                'project_name': os.getenv('PROJECT_NAME', 'Sample Project'),
                'business_domain': os.getenv('BUSINESS_DOMAIN', 'Web Application'),
                'target_users': os.getenv('TARGET_USERS', 'End users'),
                'technology_preferences': os.getenv('TECH_PREFERENCES', 'Java Spring Boot, React'),
                'timeline_months': int(os.getenv('TIMELINE_MONTHS', 6)),
                'budget_range': os.getenv('BUDGET_RANGE', '$100K-$200K')
            }
            
            # Execute pipeline
            execution_id = await orchestrator.execute_pipeline(pipeline_id, user_inputs)
            logger.info(f"Started pipeline execution: {execution_id}")
            
            # Monitor execution
            while True:
                status = await orchestrator.get_execution_status(execution_id)
                logger.info(f"Execution Status: {status['status']}, Progress: {status['progress']:.1f}%")
                
                if status['status'] in ['completed', 'failed', 'cancelled']:
                    break
                
                await asyncio.sleep(10)
            
            logger.info(f"Pipeline execution completed with status: {status['status']}")
        
        else:
            logger.info("No pipeline file specified. Engine ready for API requests.")
            
            # Keep the engine running for API requests
            while True:
                await asyncio.sleep(60)
    
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Engine error: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("SDLC Pipeline Engine stopped")

if __name__ == "__main__":
    asyncio.run(main())
