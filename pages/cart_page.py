"""
Cart Page Object for SauceDemo Test Automation Framework.

This module contains the Cart page object with all shopping cart
functionality, including item management and checkout navigation.
"""

from typing import List, Dict, Any, Optional
from loguru import logger

from core.base_page import BasePage
from core.config_loader import config


class CartPage(BasePage):
    """
    Cart page object containing all shopping cart functionality.
    
    Handles cart item display, quantity management, removal operations,
    and navigation to checkout process.
    """
    
    # Page URL
    CART_URL = f"{config.environment.base_url}/cart.html"
    
    # Header Elements
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'
    
    # Cart Container
    CART_CONTENTS_CONTAINER = '#cart_contents_container'
    CART_LIST = '.cart_list'
    CART_ITEM = '.cart_item'
    
    # Cart Item Elements
    CART_ITEM_NAME = '.inventory_item_name'
    CART_ITEM_DESC = '.inventory_item_desc'
    CART_ITEM_PRICE = '.inventory_item_price'
    CART_QUANTITY = '.cart_quantity'
    REMOVE_BUTTON = '[data-test^="remove"]'
    
    # Specific Remove Buttons
    REMOVE_BACKPACK_BUTTON = '[data-test="remove-sauce-labs-backpack"]'
    REMOVE_BIKE_LIGHT_BUTTON = '[data-test="remove-sauce-labs-bike-light"]'
    REMOVE_BOLT_TSHIRT_BUTTON = '[data-test="remove-sauce-labs-bolt-t-shirt"]'
    REMOVE_FLEECE_JACKET_BUTTON = '[data-test="remove-sauce-labs-fleece-jacket"]'
    REMOVE_ONESIE_BUTTON = '[data-test="remove-sauce-labs-onesie"]'
    REMOVE_RED_TSHIRT_BUTTON = '[data-test="remove-test.allthethings()-t-shirt-(red)"]'
    
    # Navigation Buttons
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    
    # Empty Cart Elements
    CART_DESC_LABEL = '.cart_desc_label'
    
    def __init__(self):
        """Initialize Cart page object."""
        super().__init__()
        logger.info("Cart page object initialized")
    
    def navigate_to_cart_page(self) -> None:
        """
        Navigate to the cart page.
        
        Opens the SauceDemo cart page and waits for it to load completely.
        """
        logger.info(f"Navigating to cart page: {self.CART_URL}")
        self.navigate_to(self.CART_URL)
        self.wait_for_cart_page_loaded()
    
    def wait_for_cart_page_loaded(self) -> None:
        """Wait for cart page to load completely."""
        self.wait_for_element_visible(self.CART_CONTENTS_CONTAINER)
        self.wait_for_element_visible(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_element_visible(self.CHECKOUT_BUTTON)
        logger.debug("Cart page loaded successfully")
    
    def get_cart_items(self) -> List[Dict[str, Any]]:
        """
        Get list of all items in the cart with their details.
        
        Returns:
            List of dictionaries containing cart item details
        """
        cart_items = []
        item_elements = self.find_elements(self.CART_ITEM)
        
        for item in item_elements:
            item_details = {
                'name': item.locator(self.CART_ITEM_NAME).text_content() or "",
                'description': item.locator(self.CART_ITEM_DESC).text_content() or "",
                'price': item.locator(self.CART_ITEM_PRICE).text_content() or "",
                'quantity': item.locator(self.CART_QUANTITY).text_content() or "1"
            }
            cart_items.append(item_details)
        
        logger.debug(f"Found {len(cart_items)} items in cart")
        return cart_items
    
    def get_cart_item_names(self) -> List[str]:
        """
        Get list of all product names in the cart.
        
        Returns:
            List of product names in cart
        """
        name_elements = self.find_elements(self.CART_ITEM_NAME)
        names = [element.text_content() or "" for element in name_elements]
        logger.debug(f"Cart item names: {names}")
        return names
    
    def get_cart_item_count(self) -> int:
        """
        Get total number of items in the cart.
        
        Returns:
            Number of items in cart
        """
        items = self.find_elements(self.CART_ITEM)
        count = len(items)
        logger.debug(f"Total items in cart: {count}")
        return count
    
    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty.
        
        Returns:
            True if cart is empty, False otherwise
        """
        return self.get_cart_item_count() == 0
    
    def remove_item_by_name(self, product_name: str) -> None:
        """
        Remove item from cart by product name.
        
        Args:
            product_name: Name of the product to remove
        """
        logger.info(f"Removing item from cart: {product_name}")
        
        item_elements = self.find_elements(self.CART_ITEM)
        
        for item in item_elements:
            name_element = item.locator(self.CART_ITEM_NAME)
            if name_element.text_content() == product_name:
                remove_button = item.locator(self.REMOVE_BUTTON)
                remove_button.click()
                logger.debug(f"Successfully removed '{product_name}' from cart")
                return
        
        raise ValueError(f"Product '{product_name}' not found in cart")
    
    def remove_sauce_labs_backpack(self) -> None:
        """Remove Sauce Labs Backpack from cart."""
        logger.info("Removing Sauce Labs Backpack from cart")
        self.click_element(self.REMOVE_BACKPACK_BUTTON)
    
    def remove_sauce_labs_bike_light(self) -> None:
        """Remove Sauce Labs Bike Light from cart."""
        logger.info("Removing Sauce Labs Bike Light from cart")
        self.click_element(self.REMOVE_BIKE_LIGHT_BUTTON)
    
    def remove_sauce_labs_bolt_tshirt(self) -> None:
        """Remove Sauce Labs Bolt T-Shirt from cart."""
        logger.info("Removing Sauce Labs Bolt T-Shirt from cart")
        self.click_element(self.REMOVE_BOLT_TSHIRT_BUTTON)
    
    def remove_all_items(self) -> None:
        """Remove all items from cart."""
        logger.info("Removing all items from cart")
        
        # Get current item names to avoid stale element references
        item_names = self.get_cart_item_names()
        
        for item_name in item_names:
            self.remove_item_by_name(item_name)
        
        logger.debug("All items removed from cart")
    
    def continue_shopping(self) -> None:
        """Click continue shopping button to return to inventory page."""
        logger.info("Clicking continue shopping button")
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def proceed_to_checkout(self) -> None:
        """Click checkout button to proceed to checkout process."""
        logger.info("Proceeding to checkout")
        self.click_element(self.CHECKOUT_BUTTON)
    
    def get_item_details(self, product_name: str) -> Dict[str, Any]:
        """
        Get details of specific item in cart.
        
        Args:
            product_name: Name of the product
            
        Returns:
            Dictionary containing item details
        """
        item_elements = self.find_elements(self.CART_ITEM)
        
        for item in item_elements:
            name_element = item.locator(self.CART_ITEM_NAME)
            if name_element.text_content() == product_name:
                details = {
                    'name': name_element.text_content(),
                    'description': item.locator(self.CART_ITEM_DESC).text_content(),
                    'price': item.locator(self.CART_ITEM_PRICE).text_content(),
                    'quantity': item.locator(self.CART_QUANTITY).text_content()
                }
                logger.debug(f"Retrieved details for cart item: {product_name}")
                return details
        
        raise ValueError(f"Product '{product_name}' not found in cart")
    
    def get_total_price(self) -> float:
        """
        Calculate total price of all items in cart.
        
        Returns:
            Total price as float
        """
        cart_items = self.get_cart_items()
        total = 0.0
        
        for item in cart_items:
            # Extract numeric value from price string (e.g., "$29.99" -> 29.99)
            price_text = item['price'].replace('$', '')
            quantity = int(item['quantity'])
            item_price = float(price_text) * quantity
            total += item_price
        
        logger.debug(f"Calculated total price: ${total:.2f}")
        return total
    
    def is_item_in_cart(self, product_name: str) -> bool:
        """
        Check if specific item is in cart.
        
        Args:
            product_name: Name of the product to check
            
        Returns:
            True if item is in cart, False otherwise
        """
        item_names = self.get_cart_item_names()
        return product_name in item_names
    
    def get_cart_badge_count(self) -> Optional[str]:
        """
        Get the number displayed on cart badge.
        
        Returns:
            Cart badge count as string, or None if badge is not visible
        """
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            count = self.get_text(self.SHOPPING_CART_BADGE)
            logger.debug(f"Cart badge count: {count}")
            return count
        return None
    
    def is_cart_badge_visible(self) -> bool:
        """
        Check if cart badge is visible.
        
        Returns:
            True if cart badge is visible, False otherwise
        """
        return self.is_element_visible(self.SHOPPING_CART_BADGE)
    
    # Assertion Methods
    def assert_cart_page_displayed(self) -> None:
        """Assert that cart page is displayed correctly."""
        self.assert_element_visible(self.CART_CONTENTS_CONTAINER)
        self.assert_element_visible(self.CONTINUE_SHOPPING_BUTTON)
        self.assert_element_visible(self.CHECKOUT_BUTTON)
        logger.info("Cart page display assertion passed")
    
    def assert_cart_item_count(self, expected_count: int) -> None:
        """
        Assert that cart contains expected number of items.
        
        Args:
            expected_count: Expected number of items in cart
        """
        actual_count = self.get_cart_item_count()
        assert actual_count == expected_count, f"Expected {expected_count} items in cart, but found {actual_count}"
        logger.info(f"Cart item count assertion passed: {expected_count}")
    
    def assert_cart_empty(self) -> None:
        """Assert that cart is empty."""
        assert self.is_cart_empty(), "Cart is not empty"
        logger.info("Cart empty assertion passed")
    
    def assert_cart_not_empty(self) -> None:
        """Assert that cart is not empty."""
        assert not self.is_cart_empty(), "Cart is empty"
        logger.info("Cart not empty assertion passed")
    
    def assert_item_in_cart(self, product_name: str) -> None:
        """
        Assert that specific item is in cart.
        
        Args:
            product_name: Name of the product to check
        """
        assert self.is_item_in_cart(product_name), f"Product '{product_name}' not found in cart"
        logger.info(f"Item in cart assertion passed: {product_name}")
    
    def assert_item_not_in_cart(self, product_name: str) -> None:
        """
        Assert that specific item is not in cart.
        
        Args:
            product_name: Name of the product to check
        """
        assert not self.is_item_in_cart(product_name), f"Product '{product_name}' found in cart but should not be"
        logger.info(f"Item not in cart assertion passed: {product_name}")
    
    def assert_cart_badge_count(self, expected_count: str) -> None:
        """
        Assert that cart badge shows expected count.
        
        Args:
            expected_count: Expected cart badge count
        """
        self.assert_element_visible(self.SHOPPING_CART_BADGE)
        self.assert_text_equals(self.SHOPPING_CART_BADGE, expected_count)
        logger.info(f"Cart badge count assertion passed: {expected_count}")
    
    def assert_no_cart_badge_visible(self) -> None:
        """Assert that cart badge is not visible (empty cart)."""
        self.assert_element_hidden(self.SHOPPING_CART_BADGE)
        logger.info("No cart badge assertion passed")
    
    def assert_total_price(self, expected_total: float, tolerance: float = 0.01) -> None:
        """
        Assert that total price matches expected value.
        
        Args:
            expected_total: Expected total price
            tolerance: Acceptable difference for floating point comparison
        """
        actual_total = self.get_total_price()
        assert abs(actual_total - expected_total) <= tolerance, \
            f"Expected total ${expected_total:.2f}, but got ${actual_total:.2f}"
        logger.info(f"Total price assertion passed: ${expected_total:.2f}") 