"""
Configuration Manager for SauceDemo Test Automation Framework.

This module provides centralized configuration management for test execution,
including environment settings, user credentials, and test data.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger


class ViewportConfig(BaseModel):
    """Browser viewport configuration."""
    width: int = Field(default=1920, description="Browser window width")
    height: int = Field(default=1080, description="Browser window height")


class EnvironmentConfig(BaseModel):
    """Environment configuration settings."""
    base_url: str = Field(description="Base URL of the application")
    timeout: int = Field(default=30000, description="Default timeout in milliseconds")
    headless: bool = Field(default=False, description="Run browser in headless mode")
    browser: str = Field(default="chromium", description="Browser type to use")
    viewport: ViewportConfig = Field(default_factory=ViewportConfig)


class UserConfig(BaseModel):
    """User credentials configuration."""
    username: str = Field(description="Username for login")
    password: str = Field(description="Password for login")
    description: str = Field(description="User description")


class CustomerInfo(BaseModel):
    """Customer information for checkout process."""
    first_name: str = Field(description="Customer first name")
    last_name: str = Field(description="Customer last name")
    postal_code: str = Field(description="Customer postal code")


class InvalidCredential(BaseModel):
    """Invalid credential combination for negative testing."""
    username: str = Field(description="Invalid username")
    password: str = Field(description="Invalid password")


class TestDataConfig(BaseModel):
    """Test data configuration."""
    customer_info: CustomerInfo = Field(description="Valid customer information")
    invalid_credentials: list[InvalidCredential] = Field(description="Invalid login combinations")


class ReportingConfig(BaseModel):
    """Reporting configuration settings."""
    screenshots_on_failure: bool = Field(default=True, description="Take screenshots on test failure")
    video_recording: bool = Field(default=False, description="Record video during test execution")
    trace_on_failure: bool = Field(default=True, description="Generate trace on test failure")


class LoggingConfig(BaseModel):
    """Logging configuration settings."""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(description="Log message format")


class ConfigLoader:
    """Loads and manages test configuration from YAML files."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file. Defaults to config/test_config.yaml
        """
        self.config_file = config_file or self._get_default_config_path()
        self._config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        project_root = Path(__file__).parent.parent
        return str(project_root / "config" / "test_config.yaml")
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self._config_data = yaml.safe_load(file)
            logger.info(f"Configuration loaded from: {self.config_file}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            raise
    
    @property
    def environment(self) -> EnvironmentConfig:
        """Get environment configuration."""
        return EnvironmentConfig(**self._config_data.get('environment', {}))
    
    @property
    def users(self) -> Dict[str, UserConfig]:
        """Get user configurations."""
        users_data = self._config_data.get('users', {})
        return {
            username: UserConfig(**user_data)
            for username, user_data in users_data.items()
        }
    
    @property
    def test_data(self) -> TestDataConfig:
        """Get test data configuration."""
        return TestDataConfig(**self._config_data.get('test_data', {}))
    
    @property
    def reporting(self) -> ReportingConfig:
        """Get reporting configuration."""
        return ReportingConfig(**self._config_data.get('reporting', {}))
    
    @property
    def logging(self) -> LoggingConfig:
        """Get logging configuration."""
        return LoggingConfig(**self._config_data.get('logging', {}))
    
    def get_user(self, username: str) -> UserConfig:
        """
        Get specific user configuration.
        
        Args:
            username: Username to retrieve configuration for
            
        Returns:
            UserConfig object for the specified user
            
        Raises:
            KeyError: If user is not found in configuration
        """
        users = self.users
        if username not in users:
            available_users = list(users.keys())
            raise KeyError(f"User '{username}' not found. Available users: {available_users}")
        return users[username]


# Global configuration instance
config = ConfigLoader() 