"""
AI Prompt Processor
Handles interactions with various AI models and prompt processing
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import aiohttp
import time
from datetime import datetime

class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"
    GOOGLE_GEMINI = "google_gemini"
    HUGGINGFACE = "huggingface"
    LOCAL = "local"

@dataclass
class AIModelConfig:
    provider: AIProvider
    model_name: str
    temperature: float = 0.3
    max_tokens: int = 4000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 60
    retry_attempts: int = 3

@dataclass
class AIResponse:
    content: str
    model_used: str
    provider: str
    tokens_used: int
    processing_time: float
    metadata: Dict[str, Any]

class AIPromptProcessor:
    """AI Prompt Processor for handling various AI model interactions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize providers
        self.providers = {}
        self._initialize_providers()
        
        # Request tracking
        self.request_history = []
        self.token_usage = {}
        
    def _initialize_providers(self):
        """Initialize AI provider configurations"""
        
        # OpenAI Configuration
        if 'openai' in self.config:
            self.providers[AIProvider.OPENAI] = {
                'api_key': self.config['openai'].get('api_key'),
                'base_url': self.config['openai'].get('base_url', 'https://api.openai.com/v1'),
                'default_model': self.config['openai'].get('default_model', 'gpt-4'),
                'organization': self.config['openai'].get('organization')
            }
        
        # Anthropic Configuration
        if 'anthropic' in self.config:
            self.providers[AIProvider.ANTHROPIC] = {
                'api_key': self.config['anthropic'].get('api_key'),
                'base_url': self.config['anthropic'].get('base_url', 'https://api.anthropic.com'),
                'default_model': self.config['anthropic'].get('default_model', 'claude-3-sonnet-20240229')
            }
        
        # Azure OpenAI Configuration
        if 'azure_openai' in self.config:
            self.providers[AIProvider.AZURE_OPENAI] = {
                'api_key': self.config['azure_openai'].get('api_key'),
                'endpoint': self.config['azure_openai'].get('endpoint'),
                'api_version': self.config['azure_openai'].get('api_version', '2024-02-01'),
                'deployment_name': self.config['azure_openai'].get('deployment_name')
            }
        
        # Google Gemini Configuration
        if 'google_gemini' in self.config:
            self.providers[AIProvider.GOOGLE_GEMINI] = {
                'api_key': self.config['google_gemini'].get('api_key'),
                'base_url': self.config['google_gemini'].get('base_url', 'https://generativelanguage.googleapis.com'),
                'default_model': self.config['google_gemini'].get('default_model', 'gemini-1.5-flash')
            }
    
    async def process_prompt(
        self, 
        prompt: str, 
        model_config: Optional[Dict[str, Any]] = None, 
        context: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Process a prompt using specified AI model"""
        
        start_time = time.time()
        
        # Parse model configuration
        config = self._parse_model_config(model_config or {})
        
        try:
            # Select provider and process
            if config.provider == AIProvider.OPENAI:
                response = await self._process_openai(prompt, config)
            elif config.provider == AIProvider.ANTHROPIC:
                response = await self._process_anthropic(prompt, config)
            elif config.provider == AIProvider.AZURE_OPENAI:
                response = await self._process_azure_openai(prompt, config)
            else:
                raise ValueError(f"Unsupported AI provider: {config.provider}")
            
            # Track usage
            self._track_usage(response)
            
            # Log request
            self.logger.info(f"AI request completed: {response.model_used}, tokens: {response.tokens_used}")
            
            return {
                'generated_content': response.content,
                'model_info': {
                    'provider': response.provider,
                    'model': response.model_used,
                    'tokens_used': response.tokens_used,
                    'processing_time': response.processing_time
                },
                'metadata': response.metadata
            }
            
        except Exception as e:
            self.logger.error(f"AI processing failed: {str(e)}")
            raise
    
    def _parse_model_config(self, config: Dict[str, Any]) -> AIModelConfig:
        """Parse and validate model configuration"""
        
        provider_str = config.get('provider', 'openai')
        provider = AIProvider(provider_str) if provider_str in [p.value for p in AIProvider] else AIProvider.OPENAI
        
        model_name = config.get('model', self._get_default_model(provider))
        
        return AIModelConfig(
            provider=provider,
            model_name=model_name,
            temperature=config.get('temperature', 0.3),
            max_tokens=config.get('max_tokens', 4000),
            top_p=config.get('top_p', 1.0),
            frequency_penalty=config.get('frequency_penalty', 0.0),
            presence_penalty=config.get('presence_penalty', 0.0),
            timeout=config.get('timeout', 60),
            retry_attempts=config.get('retry_attempts', 3)
        )
    
    def _get_default_model(self, provider: AIProvider) -> str:
        """Get default model for provider"""
        if provider == AIProvider.OPENAI:
            return self.providers.get(provider, {}).get('default_model', 'gpt-4')
        elif provider == AIProvider.ANTHROPIC:
            return self.providers.get(provider, {}).get('default_model', 'claude-3-sonnet-20240229')
        elif provider == AIProvider.AZURE_OPENAI:
            return self.providers.get(provider, {}).get('deployment_name', 'gpt-4')
        else:
            return 'gpt-3.5-turbo'
    
    async def _process_openai(self, prompt: str, config: AIModelConfig) -> AIResponse:
        """Process prompt using OpenAI API"""
        
        provider_config = self.providers.get(AIProvider.OPENAI, {})
        if not provider_config.get('api_key'):
            raise ValueError("OpenAI API key not configured")
        
        headers = {
            'Authorization': f"Bearer {provider_config['api_key']}",
            'Content-Type': 'application/json'
        }
        
        if provider_config.get('organization'):
            headers['OpenAI-Organization'] = provider_config['organization']
        
        payload = {
            'model': config.model_name,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': config.temperature,
            'max_tokens': config.max_tokens,
            'top_p': config.top_p,
            'frequency_penalty': config.frequency_penalty,
            'presence_penalty': config.presence_penalty
        }
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout)) as session:
            for attempt in range(config.retry_attempts):
                try:
                    async with session.post(
                        f"{provider_config['base_url']}/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            processing_time = time.time() - start_time
                            
                            return AIResponse(
                                content=result['choices'][0]['message']['content'],
                                model_used=result['model'],
                                provider=AIProvider.OPENAI.value,
                                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                                processing_time=processing_time,
                                metadata={
                                    'finish_reason': result['choices'][0]['finish_reason'],
                                    'usage': result.get('usage', {}),
                                    'attempt': attempt + 1
                                }
                            )
                        else:
                            error_text = await response.text()
                            if attempt == config.retry_attempts - 1:
                                raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                            
                            # Wait before retry
                            await asyncio.sleep(2 ** attempt)
                            
                except asyncio.TimeoutError:
                    if attempt == config.retry_attempts - 1:
                        raise Exception("OpenAI API timeout")
                    await asyncio.sleep(2 ** attempt)
    
    async def _process_anthropic(self, prompt: str, config: AIModelConfig) -> AIResponse:
        """Process prompt using Anthropic Claude API"""
        
        provider_config = self.providers.get(AIProvider.ANTHROPIC, {})
        if not provider_config.get('api_key'):
            raise ValueError("Anthropic API key not configured")
        
        headers = {
            'x-api-key': provider_config['api_key'],
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': config.model_name,
            'max_tokens': config.max_tokens,
            'temperature': config.temperature,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout)) as session:
            for attempt in range(config.retry_attempts):
                try:
                    async with session.post(
                        f"{provider_config['base_url']}/v1/messages",
                        headers=headers,
                        json=payload
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            processing_time = time.time() - start_time
                            
                            content = result['content'][0]['text'] if result['content'] else ''
                            
                            return AIResponse(
                                content=content,
                                model_used=result['model'],
                                provider=AIProvider.ANTHROPIC.value,
                                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                                processing_time=processing_time,
                                metadata={
                                    'stop_reason': result.get('stop_reason'),
                                    'usage': result.get('usage', {}),
                                    'attempt': attempt + 1
                                }
                            )
                        else:
                            error_text = await response.text()
                            if attempt == config.retry_attempts - 1:
                                raise Exception(f"Anthropic API error: {response.status} - {error_text}")
                            
                            await asyncio.sleep(2 ** attempt)
                            
                except asyncio.TimeoutError:
                    if attempt == config.retry_attempts - 1:
                        raise Exception("Anthropic API timeout")
                    await asyncio.sleep(2 ** attempt)
    
    async def _process_azure_openai(self, prompt: str, config: AIModelConfig) -> AIResponse:
        """Process prompt using Azure OpenAI API"""
        
        provider_config = self.providers.get(AIProvider.AZURE_OPENAI, {})
        if not provider_config.get('api_key') or not provider_config.get('endpoint'):
            raise ValueError("Azure OpenAI configuration incomplete")
        
        headers = {
            'api-key': provider_config['api_key'],
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': config.temperature,
            'max_tokens': config.max_tokens,
            'top_p': config.top_p,
            'frequency_penalty': config.frequency_penalty,
            'presence_penalty': config.presence_penalty
        }
        
        url = f"{provider_config['endpoint']}/openai/deployments/{provider_config['deployment_name']}/chat/completions?api-version={provider_config['api_version']}"
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout)) as session:
            for attempt in range(config.retry_attempts):
                try:
                    async with session.post(url, headers=headers, json=payload) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            processing_time = time.time() - start_time
                            
                            return AIResponse(
                                content=result['choices'][0]['message']['content'],
                                model_used=provider_config['deployment_name'],
                                provider=AIProvider.AZURE_OPENAI.value,
                                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                                processing_time=processing_time,
                                metadata={
                                    'finish_reason': result['choices'][0]['finish_reason'],
                                    'usage': result.get('usage', {}),
                                    'attempt': attempt + 1
                                }
                            )
                        else:
                            error_text = await response.text()
                            if attempt == config.retry_attempts - 1:
                                raise Exception(f"Azure OpenAI API error: {response.status} - {error_text}")
                            
                            await asyncio.sleep(2 ** attempt)
                            
                except asyncio.TimeoutError:
                    if attempt == config.retry_attempts - 1:
                        raise Exception("Azure OpenAI API timeout")
                    await asyncio.sleep(2 ** attempt)
    
    def _track_usage(self, response: AIResponse):
        """Track AI model usage for monitoring and billing"""
        
        date_key = datetime.now().strftime('%Y-%m-%d')
        
        if date_key not in self.token_usage:
            self.token_usage[date_key] = {}
        
        provider_key = f"{response.provider}:{response.model_used}"
        
        if provider_key not in self.token_usage[date_key]:
            self.token_usage[date_key][provider_key] = {
                'requests': 0,
                'tokens': 0,
                'processing_time': 0.0
            }
        
        self.token_usage[date_key][provider_key]['requests'] += 1
        self.token_usage[date_key][provider_key]['tokens'] += response.tokens_used
        self.token_usage[date_key][provider_key]['processing_time'] += response.processing_time
    
    def get_usage_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get usage statistics for the specified number of days"""
        
        from datetime import datetime, timedelta
        
        stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_processing_time': 0.0,
            'daily_breakdown': {},
            'provider_breakdown': {}
        }
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_key = date.strftime('%Y-%m-%d')
            
            if date_key in self.token_usage:
                daily_data = self.token_usage[date_key]
                stats['daily_breakdown'][date_key] = daily_data
                
                for provider_key, usage in daily_data.items():
                    stats['total_requests'] += usage['requests']
                    stats['total_tokens'] += usage['tokens']
                    stats['total_processing_time'] += usage['processing_time']
                    
                    if provider_key not in stats['provider_breakdown']:
                        stats['provider_breakdown'][provider_key] = {
                            'requests': 0,
                            'tokens': 0,
                            'processing_time': 0.0
                        }
                    
                    stats['provider_breakdown'][provider_key]['requests'] += usage['requests']
                    stats['provider_breakdown'][provider_key]['tokens'] += usage['tokens']
                    stats['provider_breakdown'][provider_key]['processing_time'] += usage['processing_time']
        
        return stats
    
    async def validate_configuration(self) -> Dict[str, bool]:
        """Validate all configured AI providers"""
        
        validation_results = {}
        
        for provider, config in self.providers.items():
            try:
                if provider == AIProvider.OPENAI:
                    validation_results[provider.value] = await self._validate_openai(config)
                elif provider == AIProvider.ANTHROPIC:
                    validation_results[provider.value] = await self._validate_anthropic(config)
                elif provider == AIProvider.AZURE_OPENAI:
                    validation_results[provider.value] = await self._validate_azure_openai(config)
                elif provider == AIProvider.GOOGLE_GEMINI:
                    validation_results[provider.value] = await self._validate_google_gemini(config)
                else:
                    validation_results[provider.value] = False
            except Exception as e:
                self.logger.error(f"Validation failed for {provider.value}: {str(e)}")
                validation_results[provider.value] = False
        
        return validation_results
    
    async def _validate_openai(self, config: Dict[str, Any]) -> bool:
        """Validate OpenAI configuration"""
        
        if not config.get('api_key'):
            return False
        
        try:
            headers = {'Authorization': f"Bearer {config['api_key']}"}
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(f"{config['base_url']}/models", headers=headers) as response:
                    return response.status == 200
        except:
            return False
    
    async def _validate_anthropic(self, config: Dict[str, Any]) -> bool:
        """Validate Anthropic configuration"""
        
        if not config.get('api_key'):
            return False
        
        try:
            headers = {
                'x-api-key': config['api_key'],
                'anthropic-version': '2023-06-01'
            }
            
            # Test with a minimal request
            payload = {
                'model': config['default_model'],
                'max_tokens': 10,
                'messages': [{'role': 'user', 'content': 'Hello'}]
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(
                    f"{config['base_url']}/v1/messages", 
                    headers=headers, 
                    json=payload
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def _validate_azure_openai(self, config: Dict[str, Any]) -> bool:
        """Validate Azure OpenAI configuration"""
        
        if not all([config.get('api_key'), config.get('endpoint'), config.get('deployment_name')]):
            return False
        
        try:
            headers = {'api-key': config['api_key']}
            url = f"{config['endpoint']}/openai/deployments?api-version={config['api_version']}"
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url, headers=headers) as response:
                    return response.status == 200
        except:
            return False
    
    async def _validate_google_gemini(self, config: Dict[str, Any]) -> bool:
        """Validate Google Gemini configuration"""
        
        if not config.get('api_key'):
            return False
        
        try:
            # List models is a lightweight call; v1 endpoint generally available
            url = f"{config['base_url'].rstrip('/')}/v1/models?key={config['api_key']}"
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    return response.status == 200
        except:
            return False

# Export for easier imports
__all__ = ['AIPromptProcessor', 'AIProvider', 'AIModelConfig', 'AIResponse']
