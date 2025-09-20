"""
Validation Engine
Handles validation of artifacts, configurations, and quality gates
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import ast
import yaml

class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    score: float
    details: Dict[str, Any]

@dataclass
class ValidationRule:
    name: str
    description: str
    severity: ValidationSeverity
    rule_type: str
    parameters: Dict[str, Any]
    custom_validator: Optional[Callable] = None

class ValidationEngine:
    """Engine for validating artifacts and enforcing quality gates"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Built-in validators
        self.validators = {
            'contains_text': self._validate_contains_text,
            'regex_match': self._validate_regex_match,
            'json_valid': self._validate_json_valid,
            'yaml_valid': self._validate_yaml_valid,
            'length_check': self._validate_length_check,
            'required_fields': self._validate_required_fields,
            'code_quality': self._validate_code_quality,
            'documentation_quality': self._validate_documentation_quality,
            'security_check': self._validate_security_check,
            'performance_check': self._validate_performance_check
        }

        # Custom validators
        self.custom_validators: Dict[str, Callable] = {}

        # Quality thresholds
        self.quality_thresholds = config.get('quality_thresholds', {
            'minimum_score': 75.0,
            'error_threshold': 0,
            'warning_threshold': 5
        })

    def register_custom_validator(self, name: str, validator: Callable):
        """Register a custom validator function"""
        self.custom_validators[name] = validator
        self.logger.info(f"Registered custom validator: {name}")

    async def validate(
            self,
            outputs: Dict[str, Any],
            rules: List[Dict[str, Any]],
            quality_gates: Optional[List[Dict[str, Any]]] = None
    ) -> ValidationResult:
        """Validate outputs against specified rules"""

        result = ValidationResult(
            passed=True,
            errors=[],
            warnings=[],
            info=[],
            score=100.0,
            details={}
        )

        # Convert rule dictionaries to ValidationRule objects
        validation_rules = []
        for rule_dict in rules:
            rule = ValidationRule(
                name=rule_dict.get('name', rule_dict.get('rule', 'unnamed')),
                description=rule_dict.get('description', ''),
                severity=ValidationSeverity(rule_dict.get('severity', 'error')),
                rule_type=rule_dict.get('rule', rule_dict.get('type', 'contains_text')),
                parameters=rule_dict.get('parameters', {}),
                custom_validator=rule_dict.get('custom_validator')
            )
            validation_rules.append(rule)

        # Execute validation rules
        for rule in validation_rules:
            try:
                rule_result = await self._execute_validation_rule(rule, outputs)

                # Aggregate results
                if rule_result['passed']:
                    if rule_result.get('message'):
                        result.info.append(f"✓ {rule.name}: {rule_result['message']}")
                else:
                    message = f"✗ {rule.name}: {rule_result.get('message', 'Validation failed')}"

                    if rule.severity == ValidationSeverity.ERROR:
                        result.errors.append(message)
                        result.passed = False
                    elif rule.severity == ValidationSeverity.WARNING:
                        result.warnings.append(message)
                    else:
                        result.info.append(message)

                # Store detailed results
                result.details[rule.name] = rule_result

            except Exception as e:
                error_msg = f"✗ {rule.name}: Validation rule execution failed - {str(e)}"
                result.errors.append(error_msg)
                result.passed = False
                self.logger.error(f"Validation rule failed: {rule.name} - {str(e)}")

        # Calculate overall score
        result.score = self._calculate_quality_score(result)

        # Apply quality gates
        if quality_gates:
            gate_result = await self._apply_quality_gates(result, quality_gates)
            if not gate_result['passed']:
                result.passed = False
                result.errors.extend(gate_result.get('errors', []))

        # Apply global thresholds
        if (len(result.errors) > self.quality_thresholds['error_threshold'] or
                len(result.warnings) > self.quality_thresholds['warning_threshold'] or
                result.score < self.quality_thresholds['minimum_score']):
            result.passed = False

        return result

    async def _execute_validation_rule(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single validation rule"""

        # Check for custom validator first
        if rule.custom_validator:
            return await self._execute_custom_validator(rule, outputs)

        # Check custom validators registry
        if rule.rule_type in self.custom_validators:
            validator = self.custom_validators[rule.rule_type]
            return await self._execute_custom_validator_func(validator, rule, outputs)

        # Use built-in validator
        if rule.rule_type in self.validators:
            validator = self.validators[rule.rule_type]
            return validator(rule, outputs)
        else:
            raise ValueError(f"Unknown validation rule type: {rule.rule_type}")

    async def _execute_custom_validator(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute custom validator function"""

        try:
            if callable(rule.custom_validator):
                result = rule.custom_validator(outputs, rule.parameters)

                # Handle async validators
                if hasattr(result, '__await__'):
                    result = await result

                return self._normalize_validator_result(result)
            else:
                raise ValueError("Custom validator is not callable")

        except Exception as e:
            return {
                'passed': False,
                'message': f"Custom validator error: {str(e)}"
            }

    async def _execute_custom_validator_func(self, validator: Callable, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute registered custom validator function"""

        try:
            result = validator(outputs, rule.parameters)

            # Handle async validators
            if hasattr(result, '__await__'):
                result = await result

            return self._normalize_validator_result(result)

        except Exception as e:
            return {
                'passed': False,
                'message': f"Custom validator error: {str(e)}"
            }

    def _normalize_validator_result(self, result: Any) -> Dict[str, Any]:
        """Normalize validator result to standard format"""

        if isinstance(result, bool):
            return {'passed': result, 'message': ''}
        elif isinstance(result, dict):
            return {
                'passed': result.get('passed', False),
                'message': result.get('message', ''),
                'details': result.get('details', {})
            }
        else:
            return {'passed': bool(result), 'message': str(result)}

    def _validate_contains_text(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that output contains specified text"""

        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')
        required_text = rule.parameters.get('text', '')
        case_sensitive = rule.parameters.get('case_sensitive', False)

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key])

        if not case_sensitive:
            content = content.lower()
            required_text = required_text.lower()

        if required_text in content:
            return {'passed': True, 'message': f"Found required text: '{required_text}'"}
        else:
            return {'passed': False, 'message': f"Required text not found: '{required_text}'"}

    def _validate_regex_match(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that output matches regex pattern"""

        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')
        pattern = rule.parameters.get('pattern', '')
        flags = rule.parameters.get('flags', 0)

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key])

        try:
            if re.search(pattern, content, flags):
                return {'passed': True, 'message': f"Pattern matched: {pattern}"}
            else:
                return {'passed': False, 'message': f"Pattern not matched: {pattern}"}
        except re.error as e:
            return {'passed': False, 'message': f"Invalid regex pattern: {str(e)}"}

    def _validate_json_valid(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that output is valid JSON"""

        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = outputs[target_key]

        try:
            if isinstance(content, str):
                json.loads(content)
            elif isinstance(content, (dict, list)):
                json.dumps(content)  # Test serialization
            else:
                return {'passed': False, 'message': 'Content is not JSON serializable'}

            return {'passed': True, 'message': 'Valid JSON format'}
        except (json.JSONDecodeError, TypeError) as e:
            return {'passed': False, 'message': f'Invalid JSON: {str(e)}'}

    def _validate_yaml_valid(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that output is valid YAML"""

        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key])

        try:
            yaml.safe_load(content)
            return {'passed': True, 'message': 'Valid YAML format'}
        except yaml.YAMLError as e:
            return {'passed': False, 'message': f'Invalid YAML: {str(e)}'}

    def _validate_length_check(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content length"""

        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')
        min_length = rule.parameters.get('min_length', 0)
        max_length = rule.parameters.get('max_length', float('inf'))

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key])
        length = len(content)

        if length < min_length:
            return {'passed': False, 'message': f'Content too short: {length} < {min_length}'}
        elif length > max_length:
            return {'passed': False, 'message': f'Content too long: {length} > {max_length}'}
        else:
            return {'passed': True, 'message': f'Length valid: {length} characters'}

    def _validate_required_fields(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that required fields are present"""

        required_fields = rule.parameters.get('fields', [])
        target_key = rule.parameters.get('key', list(outputs.keys())[0] if outputs else '')

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = outputs[target_key]

        # Parse content if it's a string
        if isinstance(content, str):
            try:
                if content.strip().startswith('{') or content.strip().startswith('['):
                    content = json.loads(content)
                else:
                    content = yaml.safe_load(content)
            except:
                return {'passed': False, 'message': 'Cannot parse content to check fields'}

        missing_fields = []

        for field in required_fields:
            if isinstance(content, dict):
                if field not in content:
                    missing_fields.append(field)
            elif isinstance(content, str):
                if field not in content:
                    missing_fields.append(field)

        if missing_fields:
            return {'passed': False, 'message': f'Missing required fields: {missing_fields}'}
        else:
            return {'passed': True, 'message': f'All required fields present: {required_fields}'}

    def _validate_code_quality(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code quality metrics"""

        target_key = rule.parameters.get('key', 'generated_content')
        min_functions = rule.parameters.get('min_functions', 1)
        max_complexity = rule.parameters.get('max_complexity', 10)
        require_comments = rule.parameters.get('require_comments', True)

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        code = str(outputs[target_key])
        issues = []

        # Count functions
        function_patterns = [
            r'def\s+\w+\s*\(',  # Python
            r'function\s+\w+\s*\(',  # JavaScript
            r'public\s+\w+\s+\w+\s*\(',  # Java methods
        ]

        function_count = 0
        for pattern in function_patterns:
            function_count += len(re.findall(pattern, code))

        if function_count < min_functions:
            issues.append(f'Too few functions: {function_count} < {min_functions}')

        # Check for comments if required
        if require_comments:
            comment_patterns = [r'//', r'/\*', r'#', r'"""', r"'''"]
            has_comments = any(re.search(pattern, code) for pattern in comment_patterns)

            if not has_comments:
                issues.append('No comments found in code')

        # Basic complexity check (nested blocks)
        nesting_level = 0
        max_nesting = 0
        for char in code:
            if char in '{(':
                nesting_level += 1
                max_nesting = max(max_nesting, nesting_level)
            elif char in '})':
                nesting_level -= 1

        if max_nesting > max_complexity:
            issues.append(f'Code complexity too high: {max_nesting} > {max_complexity}')

        if issues:
            return {'passed': False, 'message': f'Code quality issues: {"; ".join(issues)}'}
        else:
            return {'passed': True, 'message': f'Code quality acceptable (functions: {function_count})'}

    def _validate_documentation_quality(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate documentation quality"""

        target_key = rule.parameters.get('key', 'generated_content')
        min_sections = rule.parameters.get('min_sections', 3)
        require_toc = rule.parameters.get('require_toc', False)
        min_words = rule.parameters.get('min_words', 100)

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key])
        issues = []

        # Count sections (headers)
        header_patterns = [r'^#+\s', r'^.*\n=+$', r'^.*\n-+$']
        section_count = 0
        for pattern in header_patterns:
            section_count += len(re.findall(pattern, content, re.MULTILINE))

        if section_count < min_sections:
            issues.append(f'Too few sections: {section_count} < {min_sections}')

        # Check for table of contents
        if require_toc:
            toc_indicators = ['table of contents', 'toc', '- [', '* [']
            has_toc = any(indicator in content.lower() for indicator in toc_indicators)

            if not has_toc:
                issues.append('No table of contents found')

        # Count words
        word_count = len(re.findall(r'\b\w+\b', content))
        if word_count < min_words:
            issues.append(f'Too few words: {word_count} < {min_words}')

        if issues:
            return {'passed': False, 'message': f'Documentation quality issues: {"; ".join(issues)}'}
        else:
            return {'passed': True, 'message': f'Documentation quality good (sections: {section_count}, words: {word_count})'}

    def _validate_security_check(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Basic security validation"""

        target_key = rule.parameters.get('key', 'generated_content')

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key]).lower()
        security_issues = []

        # Common security anti-patterns
        security_patterns = {
            'hardcoded_password': r'password\s*=\s*["\'][^"\']+["\']',
            'hardcoded_key': r'(api_?key|secret)\s*=\s*["\'][^"\']+["\']',
            'sql_injection': r'(select|insert|update|delete).*\+.*["\']',
            'eval_usage': r'\beval\s*\(',
            'exec_usage': r'\bexec\s*\(',
        }

        for issue_type, pattern in security_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                security_issues.append(issue_type.replace('_', ' '))

        if security_issues:
            return {'passed': False, 'message': f'Security issues found: {", ".join(security_issues)}'}
        else:
            return {'passed': True, 'message': 'No obvious security issues detected'}

    def _validate_performance_check(self, rule: ValidationRule, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Basic performance validation"""

        target_key = rule.parameters.get('key', 'generated_content')

        if target_key not in outputs:
            return {'passed': False, 'message': f"Output key '{target_key}' not found"}

        content = str(outputs[target_key]).lower()
        performance_issues = []

        # Common performance anti-patterns
        performance_patterns = {
            'nested_loops': r'for\s+.*for\s+.*for\s+',
            'inefficient_search': r'\.find\s*\(\s*.*\)\s*!=\s*-1',
            'string_concatenation_loop': r'for\s+.*\+=.*["\']',
            'no_caching': r'(database|db|query).*for\s+',
        }

        for issue_type, pattern in performance_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                performance_issues.append(issue_type.replace('_', ' '))

        if performance_issues:
            return {'passed': False, 'message': f'Potential performance issues: {", ".join(performance_issues)}'}
        else:
            return {'passed': True, 'message': 'No obvious performance issues detected'}

    def _calculate_quality_score(self, result: ValidationResult) -> float:
        """Calculate overall quality score"""

        base_score = 100.0

        # Deduct points for issues
        error_penalty = len(result.errors) * 20
        warning_penalty = len(result.warnings) * 5

        score = max(0.0, base_score - error_penalty - warning_penalty)

        return round(score, 2)

    async def _apply_quality_gates(self, result: ValidationResult, quality_gates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply quality gates to validation result"""

        gate_result = {'passed': True, 'errors': []}

        for gate in quality_gates:
            gate_type = gate.get('type', 'threshold')

            if gate_type == 'threshold':
                threshold = gate.get('threshold', 75.0)
                if result.score < threshold:
                    gate_result['passed'] = False
                    gate_result['errors'].append(f'Quality score {result.score} below threshold {threshold}')

            elif gate_type == 'no_errors':
                if result.errors:
                    gate_result['passed'] = False
                    gate_result['errors'].append('Quality gate failed: errors present')

            elif gate_type == 'max_warnings':
                max_warnings = gate.get('max_warnings', 0)
                if len(result.warnings) > max_warnings:
                    gate_result['passed'] = False
                    gate_result['errors'].append(f'Too many warnings: {len(result.warnings)} > {max_warnings}')

        return gate_result

# Export for easier imports
__all__ = ['ValidationEngine', 'ValidationResult', 'ValidationRule', 'ValidationSeverity']