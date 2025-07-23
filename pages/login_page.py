"""
Login Page Object for SauceDemo Test Automation Framework.

This module contains the Login page object with all login-related
functionality, element locators, and validation methods.
"""

from typing import Optional
from loguru import logger

from core.base_page import BasePage
from core.config_loader import config, UserConfig


class LoginPage(BasePage):
    """
    Login page object containing all login-related functionality.
    
    Handles user authentication, input validation, and navigation
    to the inventory page upon successful login.
    """
    
    # Page URL
    LOGIN_URL = config.environment.base_url
    
    # Element Locators
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    ERROR_BUTTON = '[data-test="error-button"]'
    
    # Page Elements
    SWAG_LABS_LOGO = '.login_logo'
    LOGIN_CONTAINER = '.login_container'
    LOGIN_WRAPPER = '.login_wrapper'
    
    def __init__(self):
        """Initialize Login page object."""
        super().__init__()
        logger.info("Login page object initialized")
    
    def navigate_to_login_page(self) -> None:
        """
        Navigate to the login page.
        
        Opens the SauceDemo login page and waits for it to load completely.
        """
        logger.info(f"Navigating to login page: {self.LOGIN_URL}")
        self.navigate_to(self.LOGIN_URL)
        self.wait_for_login_page_loaded()
    
    def wait_for_login_page_loaded(self) -> None:
        """Wait for login page to load completely."""
        self.wait_for_element_visible(self.LOGIN_CONTAINER)
        self.wait_for_element_visible(self.USERNAME_INPUT)
        self.wait_for_element_visible(self.PASSWORD_INPUT)
        self.wait_for_element_visible(self.LOGIN_BUTTON)
        logger.debug("Login page loaded successfully")
    
    def enter_username(self, username: str) -> None:
        """
        Enter username in the username field.
        
        Args:
            username: Username to enter
        """
        logger.debug(f"Entering username: {username}")
        self.fill_input(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter
        """
        logger.debug("Entering password")
        self.fill_input(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click the login button to submit the form."""
        logger.debug("Clicking login button")
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """
        Perform complete login process.
        
        Args:
            username: Username for login
            password: Password for login
        """
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def login_with_user_config(self, user_config: UserConfig) -> None:
        """
        Login using UserConfig object.
        
        Args:
            user_config: User configuration containing credentials
        """
        logger.info(f"Logging in with user: {user_config.username}")
        self.login(user_config.username, user_config.password)
    
    def login_with_standard_user(self) -> None:
        """Login with standard user credentials from configuration."""
        user_config = config.get_user("standard_user")
        self.login_with_user_config(user_config)
    
    def login_with_locked_user(self) -> None:
        """Login with locked out user credentials from configuration."""
        user_config = config.get_user("locked_out_user")
        self.login_with_user_config(user_config)
    
    def login_with_problem_user(self) -> None:
        """Login with problem user credentials from configuration."""
        user_config = config.get_user("problem_user")
        self.login_with_user_config(user_config)
    
    def login_with_performance_user(self) -> None:
        """Login with performance glitch user credentials from configuration."""
        user_config = config.get_user("performance_glitch_user")
        self.login_with_user_config(user_config)
    
    def get_error_message(self) -> str:
        """
        Get error message text from the login page.
        
        Returns:
            Error message text, or empty string if no error is displayed
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.debug(f"Error message displayed: {error_text}")
            return error_text
        return ""
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed on the page.
        
        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def close_error_message(self) -> None:
        """Close error message by clicking the error button."""
        if self.is_element_visible(self.ERROR_BUTTON):
            logger.debug("Closing error message")
            self.click_element(self.ERROR_BUTTON)
    
    def clear_username_field(self) -> None:
        """Clear the username input field."""
        logger.debug("Clearing username field")
        self.fill_input(self.USERNAME_INPUT, "")
    
    def clear_password_field(self) -> None:
        """Clear the password input field."""
        logger.debug("Clearing password field")
        self.fill_input(self.PASSWORD_INPUT, "")
    
    def clear_login_form(self) -> None:
        """Clear both username and password fields."""
        logger.debug("Clearing login form")
        self.clear_username_field()
        self.clear_password_field()
    
    def get_username_value(self) -> str:
        """
        Get current value from username field.
        
        Returns:
            Current username field value
        """
        return self.get_attribute(self.USERNAME_INPUT, "value") or ""
    
    def get_password_value(self) -> str:
        """
        Get current value from password field.
        
        Returns:
            Current password field value
        """
        return self.get_attribute(self.PASSWORD_INPUT, "value") or ""
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.
        
        Returns:
            True if login button is enabled, False otherwise
        """
        return self.is_element_enabled(self.LOGIN_BUTTON)
    
    def get_page_title(self) -> str:
        """
        Get the login page title.
        
        Returns:
            Page title
        """
        return super().get_page_title()
    
    def is_login_page_displayed(self) -> bool:
        """
        Verify that login page is currently displayed.
        
        Returns:
            True if login page is displayed, False otherwise
        """
        return (
            self.is_element_visible(self.LOGIN_CONTAINER) and
            self.is_element_visible(self.USERNAME_INPUT) and
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
    
    # Assertion Methods
    def assert_login_page_displayed(self) -> None:
        """Assert that login page is displayed correctly."""
        self.assert_element_visible(self.LOGIN_CONTAINER)
        self.assert_element_visible(self.USERNAME_INPUT)
        self.assert_element_visible(self.PASSWORD_INPUT)
        self.assert_element_visible(self.LOGIN_BUTTON)
        logger.info("Login page display assertion passed")
    
    def assert_error_message_displayed(self, expected_message: Optional[str] = None) -> None:
        """
        Assert that error message is displayed.
        
        Args:
            expected_message: Expected error message text (optional)
        """
        self.assert_element_visible(self.ERROR_MESSAGE)
        if expected_message:
            self.assert_text_contains(self.ERROR_MESSAGE, expected_message)
        logger.info("Error message assertion passed")
    
    def assert_no_error_message_displayed(self) -> None:
        """Assert that no error message is displayed."""
        self.assert_element_hidden(self.ERROR_MESSAGE)
        logger.info("No error message assertion passed")
    
    def assert_login_successful(self) -> None:
        """Assert that login was successful by checking URL change."""
        self.assert_url_contains("/inventory.html")
        logger.info("Login success assertion passed") 