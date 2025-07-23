"""
Checkout Validation tests for SauceDemo Test Automation Framework.

This module contains comprehensive tests for checkout form validation,
error handling, and negative scenarios during the checkout process.
"""

import pytest
import allure
from loguru import logger

from pages.checkout_page import CheckoutStepOnePage
from core.config_loader import config


@allure.epic("Checkout Process")
@allure.feature("Checkout Form Validation")
class TestCheckoutValidation:
    """Test class for checkout form validation and error handling."""
    
    @allure.story("Form Validation")
    @allure.title("Checkout with missing first name")
    @allure.description("Verify error handling when first name is missing")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_missing_first_name(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test checkout form validation with missing first name.
        
        Steps:
        1. Navigate to checkout step one with items in cart
        2. Fill only last name and postal code
        3. Attempt to continue
        4. Verify error message for missing first name
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Fill form with missing first name"):
            customer_info = config.test_data.customer_info
            checkout_step_one_page.enter_last_name(customer_info.last_name)
            checkout_step_one_page.enter_postal_code(customer_info.postal_code)
            # Intentionally leave first name empty
        
        with allure.step("Attempt to continue and verify error"):
            checkout_step_one_page.click_continue()
            
            # Verify error message is displayed
            checkout_step_one_page.assert_error_message_displayed("First Name is required")
            
            error_message = checkout_step_one_page.get_error_message()
            assert "first name" in error_message.lower(), f"Expected 'first name' in error message, got: {error_message}"
        
        with allure.step("Verify user remains on checkout step one"):
            checkout_step_one_page.assert_checkout_step_one_displayed()
            
            # Verify URL hasn't changed
            current_url = checkout_step_one_page.get_current_url()
            assert "checkout-step-one" in current_url, "User should remain on checkout step one page"
        
        logger.info("Checkout missing first name validation test completed successfully")
    
    @allure.story("Form Validation")
    @allure.title("Checkout with missing last name")
    @allure.description("Verify error handling when last name is missing")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_missing_last_name(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test checkout form validation with missing last name.
        
        Steps:
        1. Navigate to checkout step one with items in cart
        2. Fill only first name and postal code
        3. Attempt to continue
        4. Verify error message for missing last name
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Fill form with missing last name"):
            customer_info = config.test_data.customer_info
            checkout_step_one_page.enter_first_name(customer_info.first_name)
            checkout_step_one_page.enter_postal_code(customer_info.postal_code)
            # Intentionally leave last name empty
        
        with allure.step("Attempt to continue and verify error"):
            checkout_step_one_page.click_continue()
            
            # Verify error message is displayed
            checkout_step_one_page.assert_error_message_displayed("Last Name is required")
            
            error_message = checkout_step_one_page.get_error_message()
            assert "last name" in error_message.lower(), f"Expected 'last name' in error message, got: {error_message}"
        
        logger.info("Checkout missing last name validation test completed successfully")
    
    @allure.story("Form Validation")
    @allure.title("Checkout with missing postal code")
    @allure.description("Verify error handling when postal code is missing")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_missing_postal_code(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test checkout form validation with missing postal code.
        
        Steps:
        1. Navigate to checkout step one with items in cart
        2. Fill only first name and last name
        3. Attempt to continue
        4. Verify error message for missing postal code
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Fill form with missing postal code"):
            customer_info = config.test_data.customer_info
            checkout_step_one_page.enter_first_name(customer_info.first_name)
            checkout_step_one_page.enter_last_name(customer_info.last_name)
            # Intentionally leave postal code empty
        
        with allure.step("Attempt to continue and verify error"):
            checkout_step_one_page.click_continue()
            
            # Verify error message is displayed
            checkout_step_one_page.assert_error_message_displayed("Postal Code is required")
            
            error_message = checkout_step_one_page.get_error_message()
            assert any(word in error_message.lower() for word in ["postal", "zip"]), \
                f"Expected 'postal' or 'zip' in error message, got: {error_message}"
        
        logger.info("Checkout missing postal code validation test completed successfully")
    
    @allure.story("Form Validation")
    @allure.title("Checkout with all fields empty")
    @allure.description("Verify error handling when all required fields are empty")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_all_fields_empty(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test checkout form validation with all fields empty.
        
        Steps:
        1. Navigate to checkout step one with items in cart
        2. Leave all fields empty
        3. Attempt to continue
        4. Verify appropriate error message
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Attempt to continue with empty form"):
            # All fields are empty by default
            checkout_step_one_page.click_continue()
        
        with allure.step("Verify error message is displayed"):
            checkout_step_one_page.assert_error_message_displayed()
            
            error_message = checkout_step_one_page.get_error_message()
            # The error should mention the first required field that's missing
            assert any(word in error_message.lower() for word in ["first name", "required"]), \
                f"Expected error about required field, got: {error_message}"
        
        logger.info("Checkout all fields empty validation test completed successfully")
    
    @allure.story("Form Validation")
    @allure.title("Error message dismissal in checkout")
    @allure.description("Verify that checkout error messages can be dismissed")
    @allure.severity("medium")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_error_message_dismissal(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test error message dismissal in checkout form.
        
        Steps:
        1. Navigate to checkout step one
        2. Trigger validation error
        3. Dismiss error message
        4. Verify error is hidden
        5. Complete form successfully
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Trigger validation error"):
            checkout_step_one_page.click_continue()  # Submit empty form
            checkout_step_one_page.assert_error_message_displayed()
        
        with allure.step("Dismiss error message"):
            checkout_step_one_page.close_error_message()
        
        with allure.step("Verify error message is hidden"):
            assert not checkout_step_one_page.is_error_displayed(), "Error message should be hidden after dismissal"
        
        with allure.step("Complete form successfully after error dismissal"):
            checkout_step_one_page.fill_customer_info_from_config()
            checkout_step_one_page.click_continue()
            
            # Should proceed to step two without errors
            from pages.checkout_page import CheckoutStepTwoPage
            checkout_step_two_page = CheckoutStepTwoPage()
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            checkout_step_two_page.assert_checkout_step_two_displayed()
        
        logger.info("Checkout error message dismissal test completed successfully")
    
    @allure.story("Form Validation")
    @allure.title("Form field clearing and re-entry")
    @allure.description("Verify form field behavior during error correction")
    @allure.severity("low")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_form_field_correction(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test form field correction after validation errors.
        
        Steps:
        1. Navigate to checkout step one
        2. Fill form with partial data
        3. Trigger validation error
        4. Clear and re-fill form correctly
        5. Verify successful submission
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step("Fill form with partial data and trigger error"):
            checkout_step_one_page.enter_first_name("John")
            # Leave other fields empty
            checkout_step_one_page.click_continue()
            checkout_step_one_page.assert_error_message_displayed()
        
        with allure.step("Clear form and fill correctly"):
            checkout_step_one_page.close_error_message()
            checkout_step_one_page.clear_all_fields()
            checkout_step_one_page.fill_customer_info_from_config()
        
        with allure.step("Verify successful form submission"):
            checkout_step_one_page.click_continue()
            
            # Should proceed to step two
            from pages.checkout_page import CheckoutStepTwoPage
            checkout_step_two_page = CheckoutStepTwoPage()
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            checkout_step_two_page.assert_checkout_step_two_displayed()
        
        logger.info("Checkout form field correction test completed successfully")
    
    @allure.story("Data Validation")
    @allure.title("Checkout with various data formats")
    @allure.description("Verify checkout accepts various valid data formats")
    @allure.severity("medium")
    @pytest.mark.regression
    @pytest.mark.checkout
    @pytest.mark.parametrize("first_name,last_name,postal_code", [
        ("John", "Doe", "12345"),
        ("Mary-Jane", "Smith-Johnson", "K1A 0A6"),  # Canadian postal code
        ("José", "García", "28001"),  # Spanish names and postal code
        ("李", "小明", "100000"),  # Chinese names and postal code
        ("A", "B", "1"),  # Minimal valid input
        ("VeryLongFirstNameThatShouldStillBeAccepted", "VeryLongLastNameThatShouldStillBeAccepted", "12345-6789")
    ])
    def test_checkout_various_data_formats(
        self,
        browser,
        cart_with_items: dict,
        checkout_step_one_page: CheckoutStepOnePage,
        first_name: str,
        last_name: str,
        postal_code: str
    ):
        """
        Test checkout with various valid data formats.
        
        Args:
            first_name: First name to test
            last_name: Last name to test
            postal_code: Postal code to test
        """
        with allure.step("Navigate to checkout step one"):
            from pages.inventory_page import InventoryPage
            from pages.cart_page import CartPage
            
            inventory_page = InventoryPage()
            cart_page = CartPage()
            
            inventory_page.click_shopping_cart()
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
        
        with allure.step(f"Fill form with data: '{first_name}', '{last_name}', '{postal_code}'"):
            checkout_step_one_page.fill_customer_information(first_name, last_name, postal_code)
        
        with allure.step("Verify form accepts the data and proceeds"):
            checkout_step_one_page.click_continue()
            
            # Should proceed to step two if data is accepted
            from pages.checkout_page import CheckoutStepTwoPage
            checkout_step_two_page = CheckoutStepTwoPage()
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            checkout_step_two_page.assert_checkout_step_two_displayed()
        
        logger.info(f"Checkout data format test completed for: {first_name}/{last_name}/{postal_code}")
    
    @allure.story("Navigation Validation")
    @allure.title("Direct navigation to checkout without cart items")
    @allure.description("Verify behavior when accessing checkout directly without items in cart")
    @allure.severity("medium")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_direct_checkout_access_without_items(
        self,
        browser,
        logged_in_user: str,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """
        Test direct navigation to checkout without items in cart.
        
        Steps:
        1. Login and ensure cart is empty
        2. Navigate directly to checkout URL
        3. Verify appropriate handling (redirect or error)
        """
        with allure.step("Navigate directly to checkout step one URL"):
            checkout_step_one_page.navigate_to(checkout_step_one_page.CHECKOUT_STEP_ONE_URL)
        
        with allure.step("Verify page behavior with empty cart"):
            # The application might:
            # 1. Redirect to cart page
            # 2. Show checkout page but handle empty cart gracefully
            # 3. Show an error message
            
            current_url = checkout_step_one_page.get_current_url()
            
            if "checkout-step-one" in current_url:
                # If checkout page is shown, it should handle empty cart
                checkout_step_one_page.assert_checkout_step_one_displayed()
                logger.info("Checkout page displayed with empty cart - testing form submission")
                
                # Try to submit form
                checkout_step_one_page.fill_customer_info_from_config()
                checkout_step_one_page.click_continue()
                
                # Verify what happens - might redirect or show error
                # This depends on application business logic
                
            elif "cart" in current_url:
                # Application redirected to cart page
                logger.info("Application redirected to cart page for empty cart checkout")
                
            else:
                # Some other handling
                logger.info(f"Application handled empty cart checkout by navigating to: {current_url}")
        
        logger.info("Direct checkout access without items test completed successfully") 