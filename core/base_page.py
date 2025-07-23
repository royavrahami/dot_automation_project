"""
Base Page class for SauceDemo Test Automation Framework.

This module provides the foundation for all page objects, implementing
common web element interactions and providing reusable methods.
"""

from typing import Optional, List, Any
from playwright.sync_api import Locator, expect
from loguru import logger

from core.browser_handler import browser_handler
from core.config_loader import config


class BasePage:
    """
    Base page class providing common page operations and element interactions.
    
    All page objects should inherit from this class to ensure consistent
    behavior and reusable functionality across the test suite.
    """
    
    def __init__(self):
        """Initialize base page with browser handler."""
        self.page = browser_handler.page
        self.timeout = config.environment.timeout
        # TODO: add support for custom timeouts per page
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to specified URL.
        
        Args:
            url: URL to navigate to
        """
        browser_handler.navigate_to(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, state: str = "networkidle") -> None:
        """
        Wait for page to load completely.
        
        Args:
            state: Load state to wait for
        """
        browser_handler.wait_for_load_state(state)
    
    def find_element(self, selector: str) -> Locator:
        """
        Find element by selector.
        
        Args:
            selector: CSS selector or data-test attribute
            
        Returns:
            Playwright Locator object
        """
        return self.page.locator(selector)
    
    def find_elements(self, selector: str) -> List[Locator]:
        """
        Find multiple elements by selector.
        
        Args:
            selector: CSS selector or data-test attribute
            
        Returns:
            List of Playwright Locator objects
        """
        return self.page.locator(selector).all()
    
    def click_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click on element identified by selector.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            element.click()
            logger.debug(f"Clicked element: {selector}")
        except Exception as e:
            logger.error(f"Failed to click element '{selector}': {e}")
            raise
    
    def fill_input(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Fill input field with specified value.
        
        Args:
            selector: CSS selector or data-test attribute
            value: Value to fill
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            element.clear()
            element.fill(value)
            logger.debug(f"Filled input '{selector}' with value: {value}")
        except Exception as e:
            logger.error(f"Failed to fill input '{selector}': {e}")
            raise
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of element.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
            
        Returns:
            Text content of the element
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            text = element.text_content() or ""
            logger.debug(f"Retrieved text from '{selector}': {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from '{selector}': {e}")
            raise
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get attribute value of element.
        
        Args:
            selector: CSS selector or data-test attribute
            attribute: Attribute name to retrieve
            timeout: Custom timeout for the operation
            
        Returns:
            Attribute value or None if not found
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="attached", timeout=timeout or self.timeout)
            value = element.get_attribute(attribute)
            logger.debug(f"Retrieved attribute '{attribute}' from '{selector}': {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute '{attribute}' from '{selector}': {e}")
            raise
    
    def is_element_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible on the page.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or 5000)  # Shorter timeout for visibility checks
            return element.is_visible()
        except Exception:
            return False
    
    def is_element_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled.
        
        Args:
            selector: CSS selector or data-test attribute
            
        Returns:
            True if element is enabled, False otherwise
        """
        try:
            element = self.find_element(selector)
            return element.is_enabled()
        except Exception:
            return False
    
    def wait_for_element_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Wait for element to become visible.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            logger.debug(f"Element became visible: {selector}")
        except Exception as e:
            logger.error(f"Element did not become visible within timeout '{selector}': {e}")
            raise
    
    def wait_for_element_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Wait for element to become hidden.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="hidden", timeout=timeout or self.timeout)
            logger.debug(f"Element became hidden: {selector}")
        except Exception as e:
            logger.error(f"Element did not become hidden within timeout '{selector}': {e}")
            raise
    
    def select_dropdown_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Select option from dropdown by value.
        
        Args:
            selector: CSS selector or data-test attribute for select element
            value: Value to select
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            element.select_option(value=value)
            logger.debug(f"Selected option '{value}' from dropdown '{selector}'")
        except Exception as e:
            logger.error(f"Failed to select option '{value}' from dropdown '{selector}': {e}")
            raise
    
    def hover_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over element.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the operation
        """
        try:
            element = self.find_element(selector)
            element.wait_for(state="visible", timeout=timeout or self.timeout)
            element.hover()
            logger.debug(f"Hovered over element: {selector}")
        except Exception as e:
            logger.error(f"Failed to hover over element '{selector}': {e}")
            raise
    
    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll element into view.
        
        Args:
            selector: CSS selector or data-test attribute
        """
        try:
            element = self.find_element(selector)
            element.scroll_into_view_if_needed()
            logger.debug(f"Scrolled to element: {selector}")
        except Exception as e:
            logger.error(f"Failed to scroll to element '{selector}': {e}")
            raise
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current page URL
        """
        return browser_handler.get_current_url()
    
    def get_page_title(self) -> str:
        """
        Get current page title.
        
        Returns:
            Current page title
        """
        return browser_handler.get_page_title()
    
    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot of current page.
        
        Args:
            name: Screenshot filename (without extension)
            
        Returns:
            Path to saved screenshot
        """
        return browser_handler.take_screenshot(name)
    
    def refresh_page(self) -> None:
        """Refresh current page."""
        browser_handler.refresh_page()
        self.wait_for_page_load()
    
    def assert_element_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element is visible on the page.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the assertion
        """
        element = self.find_element(selector)
        expect(element).to_be_visible(timeout=timeout or self.timeout)
        logger.debug(f"Assertion passed: Element is visible - {selector}")
    
    def assert_element_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element is hidden on the page.
        
        Args:
            selector: CSS selector or data-test attribute
            timeout: Custom timeout for the assertion
        """
        element = self.find_element(selector)
        expect(element).to_be_hidden(timeout=timeout or self.timeout)
        logger.debug(f"Assertion passed: Element is hidden - {selector}")
    
    def assert_text_equals(self, selector: str, expected_text: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element text equals expected value.
        
        Args:
            selector: CSS selector or data-test attribute
            expected_text: Expected text content
            timeout: Custom timeout for the assertion
        """
        element = self.find_element(selector)
        expect(element).to_have_text(expected_text, timeout=timeout or self.timeout)
        logger.debug(f"Assertion passed: Text equals '{expected_text}' - {selector}")
    
    def assert_text_contains(self, selector: str, expected_text: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element text contains expected value.
        
        Args:
            selector: CSS selector or data-test attribute
            expected_text: Expected text content to be contained
            timeout: Custom timeout for the assertion
        """
        element = self.find_element(selector)
        expect(element).to_contain_text(expected_text, timeout=timeout or self.timeout)
        logger.debug(f"Assertion passed: Text contains '{expected_text}' - {selector}")
    
    def assert_url_equals(self, expected_url: str) -> None:
        """
        Assert that current URL equals expected value.
        
        Args:
            expected_url: Expected URL
        """
        expect(self.page).to_have_url(expected_url)
        logger.debug(f"Assertion passed: URL equals '{expected_url}'")
    
    def assert_url_contains(self, expected_part: str) -> None:
        """
        Assert that current URL contains expected part.
        
        Args:
            expected_part: Expected URL part
        """
        current_url = self.get_current_url()
        assert expected_part in current_url, f"URL '{current_url}' does not contain '{expected_part}'"
        logger.debug(f"Assertion passed: URL contains '{expected_part}'") 