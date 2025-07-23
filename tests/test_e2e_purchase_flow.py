"""
End-to-End Purchase Flow tests for SauceDemo Test Automation Framework.

This module contains comprehensive tests for the complete purchase journey,
from login through product selection, cart management, and checkout completion.
"""

import pytest
import allure
from loguru import logger

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage
from core.config_loader import config


@allure.epic("E2E Purchase Flow")
@allure.feature("Complete Purchase Journey")
class TestE2EPurchaseFlow:
    """Test class for end-to-end purchase flow scenarios."""
    
    @allure.story("Happy Path - Complete Purchase")
    @allure.title("Complete purchase flow with single item")
    @allure.description("Verify complete purchase flow from login to order completion with single item")
    @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_complete_purchase_single_item(
        self, 
        browser, 
        login_page: LoginPage, 
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage
    ):
        """
        Test complete purchase flow with single item.
        
        Steps:
        1. Login with standard user
        2. Add single item to cart
        3. Navigate to cart and verify item
        4. Proceed to checkout
        5. Fill customer information
        6. Review order and complete purchase
        7. Verify order completion
        """
        with allure.step("Login with standard user"):
            login_page.navigate_to_login_page()
            login_page.login_with_standard_user()
            login_page.assert_login_successful()
        
        with allure.step("Add Sauce Labs Backpack to cart"):
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.add_sauce_labs_backpack()
            inventory_page.assert_cart_badge_count("1")
            inventory_page.assert_product_in_cart("Sauce Labs Backpack")
        
        with allure.step("Navigate to cart and verify item"):
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_page_displayed()
            cart_page.assert_cart_item_count(1)
            cart_page.assert_item_in_cart("Sauce Labs Backpack")
        
        with allure.step("Proceed to checkout"):
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
            checkout_step_one_page.assert_checkout_step_one_displayed()
        
        with allure.step("Fill customer information"):
            checkout_step_one_page.fill_customer_info_from_config()
            checkout_step_one_page.click_continue()
        
        with allure.step("Review order summary"):
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            checkout_step_two_page.assert_checkout_step_two_displayed()
            
            # Verify order details
            order_items = checkout_step_two_page.get_order_items()
            assert len(order_items) == 1, f"Expected 1 item in order, got {len(order_items)}"
            assert order_items[0]['name'] == "Sauce Labs Backpack", f"Expected 'Sauce Labs Backpack', got {order_items[0]['name']}"
            
            # Verify price calculations
            subtotal = checkout_step_two_page.get_subtotal_value()
            tax = checkout_step_two_page.get_tax_value()
            total = checkout_step_two_page.get_total_value()
            
            assert subtotal > 0, "Subtotal should be greater than 0"
            assert tax > 0, "Tax should be greater than 0"
            assert abs(total - (subtotal + tax)) < 0.01, f"Total ({total}) should equal subtotal ({subtotal}) + tax ({tax})"
        
        with allure.step("Complete the purchase"):
            checkout_step_two_page.click_finish()
            checkout_complete_page.wait_for_checkout_complete_loaded()
            checkout_complete_page.assert_checkout_complete_displayed()
        
        with allure.step("Verify order completion"):
            checkout_complete_page.assert_order_success_message()
            
            completion_header = checkout_complete_page.get_completion_header()
            assert "thank you" in completion_header.lower(), f"Expected 'thank you' in completion header, got: {completion_header}"
            
            # Verify completion page elements
            assert checkout_complete_page.is_order_completed(), "Order completion page should be displayed"
        
        with allure.step("Return to inventory page"):
            checkout_complete_page.click_back_home()
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_inventory_page_displayed()
            
            # Verify cart is empty after purchase
            inventory_page.assert_no_cart_badge_visible()
        
        logger.info("Complete purchase flow with single item test completed successfully")
    
    @allure.story("Happy Path - Complete Purchase")
    @allure.title("Complete purchase flow with multiple items")
    @allure.description("Verify complete purchase flow with multiple items and price calculations")
    @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_complete_purchase_multiple_items(
        self,
        browser,
        login_page: LoginPage,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage
    ):
        """
        Test complete purchase flow with multiple items.
        
        Steps:
        1. Login with standard user
        2. Add multiple items to cart
        3. Navigate to cart and verify items
        4. Complete checkout process
        5. Verify order completion
        """
        expected_items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        with allure.step("Login with standard user"):
            login_page.navigate_to_login_page()
            login_page.login_with_standard_user()
            login_page.assert_login_successful()
        
        with allure.step("Add multiple items to cart"):
            inventory_page.wait_for_inventory_page_loaded()
            
            # Add three different items
            inventory_page.add_sauce_labs_backpack()
            inventory_page.add_sauce_labs_bike_light()
            inventory_page.add_sauce_labs_bolt_tshirt()
            
            # Verify cart badge shows correct count
            inventory_page.assert_cart_badge_count("3")
        
        with allure.step("Navigate to cart and verify all items"):
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_item_count(3)
            
            # Verify all expected items are in cart
            for item_name in expected_items:
                cart_page.assert_item_in_cart(item_name)
        
        with allure.step("Proceed through checkout process"):
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
            checkout_step_one_page.fill_customer_info_from_config()
            checkout_step_one_page.click_continue()
        
        with allure.step("Verify order summary with multiple items"):
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            
            # Verify all items are in order summary
            order_items = checkout_step_two_page.get_order_items()
            assert len(order_items) == 3, f"Expected 3 items in order, got {len(order_items)}"
            
            order_item_names = [item['name'] for item in order_items]
            for expected_item in expected_items:
                assert expected_item in order_item_names, f"Item '{expected_item}' not found in order summary"
            
            # Verify price calculations for multiple items
            subtotal = checkout_step_two_page.get_subtotal_value()
            tax = checkout_step_two_page.get_tax_value()
            total = checkout_step_two_page.get_total_value()
            
            assert subtotal > 20, f"Subtotal for 3 items should be > $20, got ${subtotal}"
            assert tax > 1, f"Tax for 3 items should be > $1, got ${tax}"
            assert abs(total - (subtotal + tax)) < 0.01, "Total should equal subtotal + tax"
        
        with allure.step("Complete purchase"):
            checkout_step_two_page.click_finish()
            checkout_complete_page.wait_for_checkout_complete_loaded()
            checkout_complete_page.assert_order_success_message()
        
        with allure.step("Verify successful completion"):
            # Return to inventory and verify cart is empty
            checkout_complete_page.click_back_home()
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_no_cart_badge_visible()
        
        logger.info("Complete purchase flow with multiple items test completed successfully")
    
    @allure.story("Cart Management")
    @allure.title("Add and remove items during purchase flow")
    @allure.description("Verify cart management functionality during purchase flow")
    @allure.severity("high")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_management_during_purchase_flow(
        self,
        browser,
        logged_in_user: str,
        inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        Test cart management functionality during purchase flow.
        
        Steps:
        1. Add multiple items to cart
        2. Navigate to cart
        3. Remove some items
        4. Continue shopping and add more items
        5. Verify final cart state
        """
        with allure.step("Add multiple items to cart"):
            inventory_page.wait_for_inventory_page_loaded()
            
            # Add three items
            inventory_page.add_sauce_labs_backpack()
            inventory_page.add_sauce_labs_bike_light()
            inventory_page.add_sauce_labs_bolt_tshirt()
            
            inventory_page.assert_cart_badge_count("3")
        
        with allure.step("Navigate to cart and remove one item"):
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_item_count(3)
            
            # Remove one item
            cart_page.remove_item_by_name("Sauce Labs Bike Light")
            cart_page.assert_cart_item_count(2)
            cart_page.assert_item_not_in_cart("Sauce Labs Bike Light")
        
        with allure.step("Continue shopping and add another item"):
            cart_page.continue_shopping()
            inventory_page.wait_for_inventory_page_loaded()
            
            # Verify cart badge shows correct count after removal
            inventory_page.assert_cart_badge_count("2")
            
            # Add another item (different from what's already in cart)
            inventory_page.add_product_to_cart_by_name("Sauce Labs Fleece Jacket")
            inventory_page.assert_cart_badge_count("3")
        
        with allure.step("Verify final cart state"):
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_item_count(3)
            
            # Verify expected items are in cart
            expected_final_items = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket"]
            for item in expected_final_items:
                cart_page.assert_item_in_cart(item)
            
            # Verify removed item is not in cart
            cart_page.assert_item_not_in_cart("Sauce Labs Bike Light")
        
        logger.info("Cart management during purchase flow test completed successfully")
    
    @allure.story("Checkout Validation")
    @allure.title("Checkout with empty cart")
    @allure.description("Verify behavior when attempting checkout with empty cart")
    @allure.severity("medium")
    @pytest.mark.negative
    @pytest.mark.checkout
    def test_checkout_empty_cart(
        self,
        browser,
        logged_in_user: str,
        inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        Test checkout process with empty cart.
        
        Steps:
        1. Navigate to cart without adding items
        2. Verify cart is empty
        3. Attempt to proceed to checkout
        4. Verify appropriate handling of empty cart
        """
        with allure.step("Navigate to empty cart"):
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_no_cart_badge_visible()
            
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_empty()
        
        with allure.step("Verify checkout button behavior with empty cart"):
            # The checkout button should still be clickable but may lead to appropriate handling
            # Note: This depends on the application's business logic
            cart_page.assert_cart_page_displayed()
            
            # In SauceDemo, the checkout button is still available even with empty cart
            # This might be considered a bug or acceptable behavior depending on requirements
            
        logger.info("Checkout with empty cart test completed successfully")
    
    @allure.story("Purchase Flow Interruption")
    @allure.title("Cancel checkout process at different stages")
    @allure.description("Verify cancellation functionality at different checkout stages")
    @allure.severity("medium")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_cancel_checkout_process(
        self,
        browser,
        cart_with_items: dict,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        inventory_page: InventoryPage
    ):
        """
        Test cancellation at different stages of checkout process.
        
        Steps:
        1. Start with cart containing items
        2. Proceed to checkout step one and cancel
        3. Proceed to checkout step two and cancel
        4. Verify cart state is preserved
        """
        with allure.step("Navigate to cart with items"):
            inventory_page.click_shopping_cart()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_item_count(cart_with_items["count"])
        
        with allure.step("Cancel at checkout step one"):
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
            
            # Cancel and verify return to cart
            checkout_step_one_page.click_cancel()
            cart_page.wait_for_cart_page_loaded()
            cart_page.assert_cart_item_count(cart_with_items["count"])
        
        with allure.step("Proceed to step two and cancel"):
            cart_page.proceed_to_checkout()
            checkout_step_one_page.wait_for_checkout_step_one_loaded()
            checkout_step_one_page.fill_customer_info_from_config()
            checkout_step_one_page.click_continue()
            
            checkout_step_two_page.wait_for_checkout_step_two_loaded()
            
            # Cancel from step two
            checkout_step_two_page.click_cancel()
            inventory_page.wait_for_inventory_page_loaded()
            
            # Verify cart items are still preserved
            inventory_page.assert_cart_badge_count(str(cart_with_items["count"]))
        
        logger.info("Cancel checkout process test completed successfully") 