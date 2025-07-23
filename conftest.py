"""
Pytest configuration and fixtures for SauceDemo Test Automation Framework.

This module provides centralized test fixtures, browser management,
logging configuration, and test data setup for the entire test suite.
"""

import pytest
import allure
from pathlib import Path
from loguru import logger
from typing import Generator, Dict, Any

from core.browser_handler import browser_handler
from core.config_loader import config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


def pytest_configure(config) -> None:
    """
    Configure pytest settings and logging.
    
    Args:
        config: Pytest configuration object
    """
    # Setup logging configuration
    logger.remove()  # Remove default handler
    
    # Import config here to avoid circular import
    from core.config_loader import config as test_config
    # TODO: make logging configuration more flexible
    
    logger.add(
        "logs/test_execution.log",
        level=test_config.logging.level,
        format=test_config.logging.format,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Add console logging for test execution
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
        colorize=True
    )
    
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("reports/screenshots").mkdir(exist_ok=True)
    Path("reports/allure-results").mkdir(exist_ok=True)
    
    logger.info("Test framework initialized successfully")


def pytest_unconfigure(config) -> None:
    """
    Cleanup after test execution.
    
    Args:
        config: Pytest configuration object
    """
    logger.info("Test framework cleanup completed")


@pytest.fixture(scope="session", autouse=True)
def test_session_setup() -> Generator[None, None, None]:
    """
    Session-level setup and teardown.
    
    Yields:
        None
    """
    logger.info("=== Starting Test Session ===")
    yield
    logger.info("=== Test Session Completed ===")


@pytest.fixture(scope="function")
def browser() -> Generator[None, None, None]:
    """
    Browser fixture for test execution.
    
    Provides browser initialization and cleanup for each test.
    
    Yields:
        None
    """
    logger.info("Initializing browser for test")
    
    try:
        # Start browser
        browser_handler.start_browser()
        yield
        
    except Exception as e:
        logger.error(f"Browser initialization failed: {e}")
        raise
        
    finally:
        # Cleanup browser
        logger.info("Cleaning up browser after test")
        browser_handler.cleanup()


@pytest.fixture(scope="function")
def login_page() -> LoginPage:
    """
    Login page fixture.
    
    Returns:
        LoginPage instance
    """
    return LoginPage()


@pytest.fixture(scope="function")
def inventory_page() -> InventoryPage:
    """
    Inventory page fixture.
    
    Returns:
        InventoryPage instance
    """
    return InventoryPage()


@pytest.fixture(scope="function")
def cart_page() -> CartPage:
    """
    Cart page fixture.
    
    Returns:
        CartPage instance
    """
    return CartPage()


@pytest.fixture(scope="function")
def checkout_step_one_page() -> CheckoutStepOnePage:
    """
    Checkout step one page fixture.
    
    Returns:
        CheckoutStepOnePage instance
    """
    return CheckoutStepOnePage()


@pytest.fixture(scope="function")
def checkout_step_two_page() -> CheckoutStepTwoPage:
    """
    Checkout step two page fixture.
    
    Returns:
        CheckoutStepTwoPage instance
    """
    return CheckoutStepTwoPage()


@pytest.fixture(scope="function")
def checkout_complete_page() -> CheckoutCompletePage:
    """
    Checkout complete page fixture.
    
    Returns:
        CheckoutCompletePage instance
    """
    return CheckoutCompletePage()


@pytest.fixture(scope="function")
def logged_in_user(browser, login_page) -> Generator[str, None, None]:
    """
    Fixture that provides a logged-in standard user.
    
    Args:
        browser: Browser fixture
        login_page: Login page fixture
        
    Yields:
        Username of the logged-in user
    """
    logger.info("Logging in with standard user")
    
    # Navigate to login page and login
    login_page.navigate_to_login_page()
    login_page.login_with_standard_user()
    
    # Verify login success
    login_page.assert_login_successful()
    
    yield "standard_user"
    
    logger.info("Logged in user session completed")


@pytest.fixture(scope="function")
def cart_with_items(browser, logged_in_user, inventory_page) -> Generator[Dict[str, Any], None, None]:
    """
    Fixture that provides a cart with predefined items.
    
    Args:
        browser: Browser fixture
        logged_in_user: Logged in user fixture
        inventory_page: Inventory page fixture
        
    Yields:
        Dictionary containing cart information
    """
    logger.info("Setting up cart with items")
    
    # Wait for inventory page to load
    inventory_page.wait_for_inventory_page_loaded()
    
    # Add items to cart
    inventory_page.add_sauce_labs_backpack()
    inventory_page.add_sauce_labs_bike_light()
    
    # Verify items were added
    inventory_page.assert_cart_badge_count("2")
    
    cart_info = {
        "items": ["Sauce Labs Backpack", "Sauce Labs Bike Light"],
        "count": 2
    }
    
    yield cart_info
    
    logger.info("Cart with items fixture completed")


@pytest.fixture(scope="function", autouse=True)
def test_logging(request) -> Generator[None, None, None]:
    """
    Automatic test logging fixture.
    
    Args:
        request: Pytest request object
        
    Yields:
        None
    """
    test_name = request.node.name
    test_class = request.node.cls.__name__ if request.node.cls else "TestFunction"
    
    logger.info(f"🚀 Starting test: {test_class}::{test_name}")
    
    yield
    
    logger.info(f"✅ Completed test: {test_class}::{test_name}")


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, browser) -> Generator[None, None, None]:
    """
    Automatic screenshot capture on test failure.
    
    Args:
        request: Pytest request object
        browser: Browser fixture
        
    Yields:
        None
    """
    yield
    
    # Check if test failed and browser is available
    if request.node.rep_call.failed and browser_handler.is_initialized:
        test_name = request.node.name
        timestamp = browser_handler.page.evaluate("Date.now()")
        screenshot_name = f"failure_{test_name}_{timestamp}"
        
        try:
            screenshot_path = browser_handler.take_screenshot(screenshot_name)
            logger.error(f"Test failed - Screenshot saved: {screenshot_path}")
            
            # Attach screenshot to Allure report
            with open(screenshot_path, "rb") as screenshot_file:
                allure.attach(
                    screenshot_file.read(),
                    name=f"Failure Screenshot - {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for screenshot fixture.
    
    Args:
        item: Test item
        call: Test call information
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def test_data() -> Dict[str, Any]:
    """
    Test data fixture providing common test data.
    
    Returns:
        Dictionary containing test data
    """
    return {
        "valid_customer": config.test_data.customer_info,
        "invalid_credentials": config.test_data.invalid_credentials,
        "users": config.users,
        "base_url": config.environment.base_url
    }


# Pytest markers configuration
pytest_markers = [
    "smoke: Smoke tests for critical functionality",
    "regression: Regression tests for full coverage", 
    "negative: Negative test scenarios",
    "slow: Tests that take longer to execute",
    "login: Authentication related tests",
    "cart: Shopping cart functionality tests",
    "checkout: Checkout process tests"
] 