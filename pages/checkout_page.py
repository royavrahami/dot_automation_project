"""
Checkout Page Object for SauceDemo Test Automation Framework.

This module contains the Checkout page objects for the complete checkout process,
including customer information, order review, and order completion.
"""

from typing import Dict, Any, List, Optional
from loguru import logger

from core.base_page import BasePage
from core.config_loader import config, CustomerInfo


class CheckoutStepOnePage(BasePage):
    """
    Checkout Step One page object for customer information entry.
    
    Handles customer information form validation and submission
    for the checkout process.
    """
    
    # Page URL
    CHECKOUT_STEP_ONE_URL = f"{config.environment.base_url}/checkout-step-one.html"
    
    # Form Elements
    CHECKOUT_INFO_CONTAINER = '.checkout_info_container'
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    
    # Buttons
    CONTINUE_BUTTON = '[data-test="continue"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    
    # Error Elements
    ERROR_MESSAGE = '[data-test="error"]'
    ERROR_BUTTON = '[data-test="error-button"]'
    
    def __init__(self):
        """Initialize Checkout Step One page object."""
        super().__init__()
        logger.info("Checkout Step One page object initialized")
    
    def wait_for_checkout_step_one_loaded(self) -> None:
        """Wait for checkout step one page to load completely."""
        self.wait_for_element_visible(self.CHECKOUT_INFO_CONTAINER)
        self.wait_for_element_visible(self.FIRST_NAME_INPUT)
        self.wait_for_element_visible(self.LAST_NAME_INPUT)
        self.wait_for_element_visible(self.POSTAL_CODE_INPUT)
        self.wait_for_element_visible(self.CONTINUE_BUTTON)
        logger.debug("Checkout step one page loaded successfully")
    
    def enter_first_name(self, first_name: str) -> None:
        """
        Enter first name in the first name field.
        
        Args:
            first_name: First name to enter
        """
        logger.debug(f"Entering first name: {first_name}")
        self.fill_input(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """
        Enter last name in the last name field.
        
        Args:
            last_name: Last name to enter
        """
        logger.debug(f"Entering last name: {last_name}")
        self.fill_input(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str) -> None:
        """
        Enter postal code in the postal code field.
        
        Args:
            postal_code: Postal code to enter
        """
        logger.debug(f"Entering postal code: {postal_code}")
        self.fill_input(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_customer_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Fill all customer information fields.
        
        Args:
            first_name: Customer first name
            last_name: Customer last name
            postal_code: Customer postal code
        """
        logger.info("Filling customer information")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def fill_customer_info_from_config(self) -> None:
        """Fill customer information using data from configuration."""
        customer_info = config.test_data.customer_info
        logger.info("Filling customer information from configuration")
        self.fill_customer_information(
            customer_info.first_name,
            customer_info.last_name,
            customer_info.postal_code
        )
    
    def fill_customer_info_object(self, customer_info: CustomerInfo) -> None:
        """
        Fill customer information using CustomerInfo object.
        
        Args:
            customer_info: CustomerInfo object containing customer data
        """
        logger.info("Filling customer information from CustomerInfo object")
        self.fill_customer_information(
            customer_info.first_name,
            customer_info.last_name,
            customer_info.postal_code
        )
    
    def click_continue(self) -> None:
        """Click continue button to proceed to checkout step two."""
        logger.info("Clicking continue button")
        self.click_element(self.CONTINUE_BUTTON)
    
    def click_cancel(self) -> None:
        """Click cancel button to return to cart page."""
        logger.info("Clicking cancel button")
        self.click_element(self.CANCEL_BUTTON)
    
    def get_error_message(self) -> str:
        """
        Get error message text from the checkout page.
        
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
    
    def clear_all_fields(self) -> None:
        """Clear all customer information fields."""
        logger.debug("Clearing all customer information fields")
        self.fill_input(self.FIRST_NAME_INPUT, "")
        self.fill_input(self.LAST_NAME_INPUT, "")
        self.fill_input(self.POSTAL_CODE_INPUT, "")
    
    # Assertion Methods
    def assert_checkout_step_one_displayed(self) -> None:
        """Assert that checkout step one page is displayed correctly."""
        self.assert_element_visible(self.CHECKOUT_INFO_CONTAINER)
        self.assert_element_visible(self.FIRST_NAME_INPUT)
        self.assert_element_visible(self.LAST_NAME_INPUT)
        self.assert_element_visible(self.POSTAL_CODE_INPUT)
        self.assert_element_visible(self.CONTINUE_BUTTON)
        logger.info("Checkout step one display assertion passed")
    
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


class CheckoutStepTwoPage(BasePage):
    """
    Checkout Step Two page object for order review and confirmation.
    
    Handles order summary display, price calculations, and order finalization.
    """
    
    # Page URL
    CHECKOUT_STEP_TWO_URL = f"{config.environment.base_url}/checkout-step-two.html"
    
    # Container Elements
    CHECKOUT_SUMMARY_CONTAINER = '.checkout_summary_container'
    SUMMARY_INFO = '.summary_info'
    
    # Order Summary Elements
    CART_LIST = '.cart_list'
    CART_ITEM = '.cart_item'
    CART_ITEM_NAME = '.inventory_item_name'
    CART_ITEM_DESC = '.inventory_item_desc'
    CART_ITEM_PRICE = '.inventory_item_price'
    CART_QUANTITY = '.cart_quantity'
    
    # Price Summary Elements
    SUMMARY_SUBTOTAL = '.summary_subtotal_label'
    SUMMARY_TAX = '.summary_tax_label'
    SUMMARY_TOTAL = '.summary_total_label'
    
    # Payment and Shipping Info
    PAYMENT_INFO = '.summary_value_label'
    SHIPPING_INFO = '.summary_value_label'
    
    # Buttons
    FINISH_BUTTON = '[data-test="finish"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    
    def __init__(self):
        """Initialize Checkout Step Two page object."""
        super().__init__()
        logger.info("Checkout Step Two page object initialized")
    
    def wait_for_checkout_step_two_loaded(self) -> None:
        """Wait for checkout step two page to load completely."""
        self.wait_for_element_visible(self.CHECKOUT_SUMMARY_CONTAINER)
        self.wait_for_element_visible(self.CART_LIST)
        self.wait_for_element_visible(self.SUMMARY_SUBTOTAL)
        self.wait_for_element_visible(self.FINISH_BUTTON)
        logger.debug("Checkout step two page loaded successfully")
    
    def get_order_items(self) -> List[Dict[str, Any]]:
        """
        Get list of all items in the order summary.
        
        Returns:
            List of dictionaries containing order item details
        """
        order_items = []
        item_elements = self.find_elements(self.CART_ITEM)
        
        for item in item_elements:
            item_details = {
                'name': item.locator(self.CART_ITEM_NAME).text_content() or "",
                'description': item.locator(self.CART_ITEM_DESC).text_content() or "",
                'price': item.locator(self.CART_ITEM_PRICE).text_content() or "",
                'quantity': item.locator(self.CART_QUANTITY).text_content() or "1"
            }
            order_items.append(item_details)
        
        logger.debug(f"Found {len(order_items)} items in order summary")
        return order_items
    
    def get_subtotal(self) -> str:
        """
        Get subtotal amount from order summary.
        
        Returns:
            Subtotal as string
        """
        subtotal_text = self.get_text(self.SUMMARY_SUBTOTAL)
        logger.debug(f"Order subtotal: {subtotal_text}")
        return subtotal_text
    
    def get_tax_amount(self) -> str:
        """
        Get tax amount from order summary.
        
        Returns:
            Tax amount as string
        """
        tax_text = self.get_text(self.SUMMARY_TAX)
        logger.debug(f"Order tax: {tax_text}")
        return tax_text
    
    def get_total_amount(self) -> str:
        """
        Get total amount from order summary.
        
        Returns:
            Total amount as string
        """
        total_text = self.get_text(self.SUMMARY_TOTAL)
        logger.debug(f"Order total: {total_text}")
        return total_text
    
    def get_subtotal_value(self) -> float:
        """
        Get subtotal as numeric value.
        
        Returns:
            Subtotal as float
        """
        subtotal_text = self.get_subtotal()
        # Extract numeric value from text like "Item total: $29.99"
        import re
        match = re.search(r'\$(\d+\.?\d*)', subtotal_text)
        if match:
            return float(match.group(1))
        return 0.0
    
    def get_tax_value(self) -> float:
        """
        Get tax as numeric value.
        
        Returns:
            Tax as float
        """
        tax_text = self.get_tax_amount()
        # Extract numeric value from text like "Tax: $2.40"
        import re
        match = re.search(r'\$(\d+\.?\d*)', tax_text)
        if match:
            return float(match.group(1))
        return 0.0
    
    def get_total_value(self) -> float:
        """
        Get total as numeric value.
        
        Returns:
            Total as float
        """
        total_text = self.get_total_amount()
        # Extract numeric value from text like "Total: $32.39"
        import re
        match = re.search(r'\$(\d+\.?\d*)', total_text)
        if match:
            return float(match.group(1))
        return 0.0
    
    def click_finish(self) -> None:
        """Click finish button to complete the order."""
        logger.info("Clicking finish button to complete order")
        self.click_element(self.FINISH_BUTTON)
    
    def click_cancel(self) -> None:
        """Click cancel button to return to inventory page."""
        logger.info("Clicking cancel button")
        self.click_element(self.CANCEL_BUTTON)
    
    def get_order_summary(self) -> Dict[str, Any]:
        """
        Get complete order summary information.
        
        Returns:
            Dictionary containing order summary details
        """
        summary = {
            'items': self.get_order_items(),
            'subtotal': self.get_subtotal_value(),
            'tax': self.get_tax_value(),
            'total': self.get_total_value()
        }
        logger.debug("Retrieved complete order summary")
        return summary
    
    # Assertion Methods
    def assert_checkout_step_two_displayed(self) -> None:
        """Assert that checkout step two page is displayed correctly."""
        self.assert_element_visible(self.CHECKOUT_SUMMARY_CONTAINER)
        self.assert_element_visible(self.CART_LIST)
        self.assert_element_visible(self.SUMMARY_SUBTOTAL)
        self.assert_element_visible(self.SUMMARY_TAX)
        self.assert_element_visible(self.SUMMARY_TOTAL)
        self.assert_element_visible(self.FINISH_BUTTON)
        logger.info("Checkout step two display assertion passed")
    
    def assert_order_total(self, expected_total: float, tolerance: float = 0.01) -> None:
        """
        Assert that order total matches expected value.
        
        Args:
            expected_total: Expected total amount
            tolerance: Acceptable difference for floating point comparison
        """
        actual_total = self.get_total_value()
        assert abs(actual_total - expected_total) <= tolerance, \
            f"Expected total ${expected_total:.2f}, but got ${actual_total:.2f}"
        logger.info(f"Order total assertion passed: ${expected_total:.2f}")


class CheckoutCompletePage(BasePage):
    """
    Checkout Complete page object for order completion confirmation.
    
    Handles order completion confirmation and navigation back to inventory.
    """
    
    # Page URL
    CHECKOUT_COMPLETE_URL = f"{config.environment.base_url}/checkout-complete.html"
    
    # Container Elements
    CHECKOUT_COMPLETE_CONTAINER = '.checkout_complete_container'
    
    # Success Elements
    COMPLETE_HEADER = '.complete-header'
    COMPLETE_TEXT = '.complete-text'
    PONY_EXPRESS = '.pony_express'
    
    # Button
    BACK_HOME_BUTTON = '[data-test="back-to-products"]'
    
    def __init__(self):
        """Initialize Checkout Complete page object."""
        super().__init__()
        logger.info("Checkout Complete page object initialized")
    
    def wait_for_checkout_complete_loaded(self) -> None:
        """Wait for checkout complete page to load completely."""
        self.wait_for_element_visible(self.CHECKOUT_COMPLETE_CONTAINER)
        self.wait_for_element_visible(self.COMPLETE_HEADER)
        self.wait_for_element_visible(self.BACK_HOME_BUTTON)
        logger.debug("Checkout complete page loaded successfully")
    
    def get_completion_header(self) -> str:
        """
        Get completion header text.
        
        Returns:
            Completion header text
        """
        header_text = self.get_text(self.COMPLETE_HEADER)
        logger.debug(f"Completion header: {header_text}")
        return header_text
    
    def get_completion_message(self) -> str:
        """
        Get completion message text.
        
        Returns:
            Completion message text
        """
        message_text = self.get_text(self.COMPLETE_TEXT)
        logger.debug(f"Completion message: {message_text}")
        return message_text
    
    def click_back_home(self) -> None:
        """Click back home button to return to inventory page."""
        logger.info("Clicking back home button")
        self.click_element(self.BACK_HOME_BUTTON)
    
    def is_order_completed(self) -> bool:
        """
        Check if order completion is displayed.
        
        Returns:
            True if order completion elements are visible, False otherwise
        """
        return (
            self.is_element_visible(self.CHECKOUT_COMPLETE_CONTAINER) and
            self.is_element_visible(self.COMPLETE_HEADER) and
            self.is_element_visible(self.BACK_HOME_BUTTON)
        )
    
    # Assertion Methods
    def assert_checkout_complete_displayed(self) -> None:
        """Assert that checkout complete page is displayed correctly."""
        self.assert_element_visible(self.CHECKOUT_COMPLETE_CONTAINER)
        self.assert_element_visible(self.COMPLETE_HEADER)
        self.assert_element_visible(self.COMPLETE_TEXT)
        self.assert_element_visible(self.BACK_HOME_BUTTON)
        logger.info("Checkout complete display assertion passed")
    
    def assert_order_success_message(self, expected_header: str = "Thank you for your order!") -> None:
        """
        Assert that order success message is displayed.
        
        Args:
            expected_header: Expected success header text
        """
        self.assert_text_contains(self.COMPLETE_HEADER, expected_header)
        logger.info("Order success message assertion passed") 