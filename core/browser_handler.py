"""
Browser Manager for SauceDemo Test Automation Framework.

This module provides centralized browser management using Playwright,
including browser lifecycle, page operations, and screenshot capabilities.
"""

from typing import Optional, Dict, Any
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from loguru import logger

from core.config_loader import config


class BrowserHandler:
    """Handles browser setup and cleanup for tests."""
    
    def __init__(self):
        """Initialize browser handler."""
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._is_initialized = False
    
    def start_browser(self) -> None:
        """Start browser with config settings."""
        if self._is_initialized:
            logger.warning("Browser already initialized. Skipping initialization.")
            return
        
        try:
            # Start Playwright
            self._playwright = sync_playwright().start()
            logger.info("Playwright started successfully")
            
            # Launch browser based on configuration
            # TODO: add support for more browser options
            browser_type = getattr(self._playwright, config.environment.browser)
            self._browser = browser_type.launch(
                headless=config.environment.headless,
                slow_mo=100 if not config.environment.headless else 0
            )
            logger.info(f"Browser '{config.environment.browser}' launched successfully")
            
            # Create browser context with viewport settings
            self._context = self._browser.new_context(
                viewport={
                    "width": config.environment.viewport.width,
                    "height": config.environment.viewport.height
                }
            )
            logger.info("Browser context created with viewport settings")
            
            # Create new page
            self._page = self._context.new_page()
            
            # Set default timeout
            self._page.set_default_timeout(config.environment.timeout)
            
            self._is_initialized = True
            logger.info("Browser initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            self.cleanup()
            raise
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to specified URL.
        
        Args:
            url: URL to navigate to
            
        Raises:
            RuntimeError: If browser is not initialized
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        try:
            self._page.goto(url)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise
    
    def take_screenshot(self, name: str, full_page: bool = True) -> str:
        """
        Take screenshot of current page.
        
        Args:
            name: Screenshot filename (without extension)
            full_page: Whether to capture full page or viewport only
            
        Returns:
            Path to saved screenshot
            
        Raises:
            RuntimeError: If browser is not initialized
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshots_dir / f"{name}.png"
        
        try:
            self._page.screenshot(path=str(screenshot_path), full_page=full_page)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """
        Wait for page to reach specified load state.
        
        Args:
            state: Load state to wait for ('load', 'domcontentloaded', 'networkidle')
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        try:
            self._page.wait_for_load_state(state)
            logger.debug(f"Page reached load state: {state}")
        except Exception as e:
            logger.error(f"Failed to wait for load state '{state}': {e}")
            raise
    
    def execute_javascript(self, script: str) -> Any:
        """
        Execute JavaScript in the current page context.
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Result of JavaScript execution
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        try:
            result = self._page.evaluate(script)
            logger.debug(f"JavaScript executed successfully: {script[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Failed to execute JavaScript: {e}")
            raise
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current page URL
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        return self._page.url
    
    def get_page_title(self) -> str:
        """
        Get current page title.
        
        Returns:
            Current page title
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        return self._page.title()
    
    def refresh_page(self) -> None:
        """Refresh current page."""
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        
        try:
            self._page.reload()
            logger.info("Page refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh page: {e}")
            raise
    
    def cleanup(self) -> None:
        """
        Clean up browser resources.
        
        Closes page, context, browser, and stops Playwright in proper order.
        """
        try:
            if self._page:
                self._page.close()
                logger.debug("Page closed")
            
            if self._context:
                self._context.close()
                logger.debug("Browser context closed")
            
            if self._browser:
                self._browser.close()
                logger.debug("Browser closed")
            
            if self._playwright:
                self._playwright.stop()
                logger.debug("Playwright stopped")
            
            self._is_initialized = False
            logger.info("Browser cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during browser cleanup: {e}")
    
    @property
    def page(self) -> Page:
        """
        Get current page instance.
        
        Returns:
            Current Playwright page instance
            
        Raises:
            RuntimeError: If browser is not initialized
        """
        if not self._is_initialized or not self._page:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        return self._page
    
    @property
    def context(self) -> BrowserContext:
        """
        Get current browser context.
        
        Returns:
            Current browser context
            
        Raises:
            RuntimeError: If browser is not initialized
        """
        if not self._is_initialized or not self._context:
            raise RuntimeError("Browser not initialized. Call start_browser() first.")
        return self._context
    
    @property
    def is_initialized(self) -> bool:
        """Check if browser is initialized."""
        return self._is_initialized


# Global browser manager instance
browser_handler = BrowserHandler() 