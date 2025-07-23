"""
Inventory Page Object for SauceDemo Test Automation Framework.

This module contains the Inventory page object with all product catalog
functionality, including product listing, sorting, and cart operations.
"""

from typing import List, Optional, Dict, Any
from loguru import logger

from core.base_page import BasePage
from core.config_loader import config


class InventoryPage(BasePage):
    """
    Inventory page object containing all product catalog functionality.
    
    Handles product display, sorting, filtering, and cart operations
    for the SauceDemo e-commerce application.
    """
    
    # Page URL
    INVENTORY_URL = f"{config.environment.base_url}/inventory.html"
    
    # Header Elements
    APP_LOGO = '.app_logo'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'
    MENU_BUTTON = '#react-burger-menu-btn'
    
    # Sorting and Filtering
    PRODUCT_SORT_CONTAINER = '[data-test="product-sort-container"]'
    
    # Product Container
    INVENTORY_CONTAINER = '[data-test="inventory-container"]'
    INVENTORY_LIST = '.inventory_list'
    INVENTORY_ITEM = '.inventory_item'
    
    # Product Item Elements
    INVENTORY_ITEM_NAME = '.inventory_item_name'
    INVENTORY_ITEM_DESC = '.inventory_item_desc'
    INVENTORY_ITEM_PRICE = '.inventory_item_price'
    INVENTORY_ITEM_IMG = '.inventory_item_img'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart"]'
    REMOVE_BUTTON = '[data-test^="remove"]'
    
    # Specific Product Buttons (for direct access)
    ADD_BACKPACK_BUTTON = '[data-test="add-to-cart-sauce-labs-backpack"]'
    ADD_BIKE_LIGHT_BUTTON = '[data-test="add-to-cart-sauce-labs-bike-light"]'
    ADD_BOLT_TSHIRT_BUTTON = '[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]'
    ADD_FLEECE_JACKET_BUTTON = '[data-test="add-to-cart-sauce-labs-fleece-jacket"]'
    ADD_ONESIE_BUTTON = '[data-test="add-to-cart-sauce-labs-onesie"]'
    ADD_RED_TSHIRT_BUTTON = '[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]'
    
    # Remove Product Buttons
    REMOVE_BACKPACK_BUTTON = '[data-test="remove-sauce-labs-backpack"]'
    REMOVE_BIKE_LIGHT_BUTTON = '[data-test="remove-sauce-labs-bike-light"]'
    REMOVE_BOLT_TSHIRT_BUTTON = '[data-test="remove-sauce-labs-bolt-t-shirt"]'
    REMOVE_FLEECE_JACKET_BUTTON = '[data-test="remove-sauce-labs-fleece-jacket"]'
    REMOVE_ONESIE_BUTTON = '[data-test="remove-sauce-labs-onesie"]'
    REMOVE_RED_TSHIRT_BUTTON = '[data-test="remove-test.allthethings()-t-shirt-(red)"]'
    
    # Menu Items (when menu is opened)
    MENU_ITEM_ALL_ITEMS = '#inventory_sidebar_link'
    MENU_ITEM_ABOUT = '#about_sidebar_link'
    MENU_ITEM_LOGOUT = '#logout_sidebar_link'
    MENU_ITEM_RESET = '#reset_sidebar_link'
    MENU_CLOSE_BUTTON = '#react-burger-cross-btn'
    
    def __init__(self):
        """Initialize Inventory page object."""
        super().__init__()
        logger.info("Inventory page object initialized")
    
    def wait_for_inventory_page_loaded(self) -> None:
        """Wait for inventory page to load completely."""
        self.wait_for_element_visible(self.INVENTORY_CONTAINER)
        self.wait_for_element_visible(self.INVENTORY_LIST)
        self.wait_for_element_visible(self.SHOPPING_CART_LINK)
        logger.debug("Inventory page loaded successfully")
    
    def get_product_names(self) -> List[str]:
        """
        Get list of all product names on the page.
        
        Returns:
            List of product names
        """
        product_elements = self.find_elements(self.INVENTORY_ITEM_NAME)
        product_names = [element.text_content() or "" for element in product_elements]
        logger.debug(f"Found {len(product_names)} products: {product_names}")
        return product_names
    
    def get_product_prices(self) -> List[str]:
        """
        Get list of all product prices on the page.
        
        Returns:
            List of product prices as strings
        """
        price_elements = self.find_elements(self.INVENTORY_ITEM_PRICE)
        prices = [element.text_content() or "" for element in price_elements]
        logger.debug(f"Found prices: {prices}")
        return prices
    
    def get_product_descriptions(self) -> List[str]:
        """
        Get list of all product descriptions on the page.
        
        Returns:
            List of product descriptions
        """
        desc_elements = self.find_elements(self.INVENTORY_ITEM_DESC)
        descriptions = [element.text_content() or "" for element in desc_elements]
        logger.debug(f"Found {len(descriptions)} product descriptions")
        return descriptions
    
    def get_product_count(self) -> int:
        """
        Get total number of products displayed.
        
        Returns:
            Number of products on the page
        """
        products = self.find_elements(self.INVENTORY_ITEM)
        count = len(products)
        logger.debug(f"Total products displayed: {count}")
        return count
    
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Add product to cart by product name.
        
        Args:
            product_name: Name of the product to add
        """
        logger.info(f"Adding product to cart: {product_name}")
        
        # Find the product by name and get its add to cart button
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                add_button = item.locator(self.ADD_TO_CART_BUTTON)
                add_button.click()
                logger.debug(f"Successfully added '{product_name}' to cart")
                return
        
        raise ValueError(f"Product '{product_name}' not found on the page")
    
    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """
        Remove product from cart by product name.
        
        Args:
            product_name: Name of the product to remove
        """
        logger.info(f"Removing product from cart: {product_name}")
        
        # Find the product by name and get its remove button
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                remove_button = item.locator(self.REMOVE_BUTTON)
                if remove_button.is_visible():
                    remove_button.click()
                    logger.debug(f"Successfully removed '{product_name}' from cart")
                    return
                else:
                    raise ValueError(f"Remove button not visible for product '{product_name}'")
        
        raise ValueError(f"Product '{product_name}' not found on the page")
    
    def add_sauce_labs_backpack(self) -> None:
        """Add Sauce Labs Backpack to cart."""
        # Quick method for common product
        logger.info("Adding Sauce Labs Backpack to cart")
        self.click_element(self.ADD_BACKPACK_BUTTON)
    
    def add_sauce_labs_bike_light(self) -> None:
        """Add Sauce Labs Bike Light to cart."""
        logger.info("Adding Sauce Labs Bike Light to cart")
        self.click_element(self.ADD_BIKE_LIGHT_BUTTON)
    
    def add_sauce_labs_bolt_tshirt(self) -> None:
        """Add Sauce Labs Bolt T-Shirt to cart."""
        logger.info("Adding Sauce Labs Bolt T-Shirt to cart")
        self.click_element(self.ADD_BOLT_TSHIRT_BUTTON)
    
    def remove_sauce_labs_backpack(self) -> None:
        """Remove Sauce Labs Backpack from cart."""
        logger.info("Removing Sauce Labs Backpack from cart")
        self.click_element(self.REMOVE_BACKPACK_BUTTON)
    
    def sort_products(self, sort_option: str) -> None:
        """
        Sort products by specified option.
        
        Args:
            sort_option: Sort option value ('az', 'za', 'lohi', 'hilo')
        """
        logger.info(f"Sorting products by: {sort_option}")
        self.select_dropdown_option(self.PRODUCT_SORT_CONTAINER, sort_option)
        self.wait_for_page_load()
    
    def sort_products_name_a_to_z(self) -> None:
        """Sort products by name A to Z."""
        self.sort_products('az')
    
    def sort_products_name_z_to_a(self) -> None:
        """Sort products by name Z to A."""
        self.sort_products('za')
    
    def sort_products_price_low_to_high(self) -> None:
        """Sort products by price low to high."""
        self.sort_products('lohi')
    
    def sort_products_price_high_to_low(self) -> None:
        """Sort products by price high to low."""
        self.sort_products('hilo')
    
    def click_shopping_cart(self) -> None:
        """Click on shopping cart icon to navigate to cart page."""
        logger.info("Clicking shopping cart")
        self.click_element(self.SHOPPING_CART_LINK)
    
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
    
    def open_menu(self) -> None:
        """Open the hamburger menu."""
        logger.debug("Opening hamburger menu")
        self.click_element(self.MENU_BUTTON)
        self.wait_for_element_visible(self.MENU_ITEM_LOGOUT)
    
    def close_menu(self) -> None:
        """Close the hamburger menu."""
        logger.debug("Closing hamburger menu")
        self.click_element(self.MENU_CLOSE_BUTTON)
    
    def logout(self) -> None:
        """Logout from the application."""
        logger.info("Logging out from application")
        self.open_menu()
        self.click_element(self.MENU_ITEM_LOGOUT)
    
    def reset_app_state(self) -> None:
        """Reset application state (clear cart)."""
        logger.info("Resetting application state")
        self.open_menu()
        self.click_element(self.MENU_ITEM_RESET)
        self.close_menu()
    
    def click_product_name(self, product_name: str) -> None:
        """
        Click on product name to navigate to product details.
        
        Args:
            product_name: Name of the product to click
        """
        logger.info(f"Clicking on product: {product_name}")
        
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                name_element.click()
                logger.debug(f"Clicked on product: {product_name}")
                return
        
        raise ValueError(f"Product '{product_name}' not found on the page")
    
    def get_product_details(self, product_name: str) -> Dict[str, Any]:
        """
        Get product details by product name.
        
        Args:
            product_name: Name of the product
            
        Returns:
            Dictionary containing product details
        """
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                details = {
                    'name': name_element.text_content(),
                    'description': item.locator(self.INVENTORY_ITEM_DESC).text_content(),
                    'price': item.locator(self.INVENTORY_ITEM_PRICE).text_content(),
                    'image_src': item.locator(self.INVENTORY_ITEM_IMG + ' img').get_attribute('src')
                }
                logger.debug(f"Retrieved details for product: {product_name}")
                return details
        
        raise ValueError(f"Product '{product_name}' not found on the page")
    
    # Assertion Methods
    def assert_inventory_page_displayed(self) -> None:
        """Assert that inventory page is displayed correctly."""
        self.assert_element_visible(self.INVENTORY_CONTAINER)
        self.assert_element_visible(self.INVENTORY_LIST)
        self.assert_element_visible(self.SHOPPING_CART_LINK)
        logger.info("Inventory page display assertion passed")
    
    def assert_product_count(self, expected_count: int) -> None:
        """
        Assert that the number of products matches expected count.
        
        Args:
            expected_count: Expected number of products
        """
        actual_count = self.get_product_count()
        assert actual_count == expected_count, f"Expected {expected_count} products, but found {actual_count}"
        logger.info(f"Product count assertion passed: {expected_count}")
    
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
    
    def assert_product_in_cart(self, product_name: str) -> None:
        """
        Assert that product has been added to cart (Remove button visible).
        
        Args:
            product_name: Name of the product to check
        """
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                remove_button = item.locator(self.REMOVE_BUTTON)
                assert remove_button.is_visible(), f"Remove button not visible for product '{product_name}'"
                logger.info(f"Product in cart assertion passed: {product_name}")
                return
        
        raise ValueError(f"Product '{product_name}' not found on the page")
    
    def assert_product_not_in_cart(self, product_name: str) -> None:
        """
        Assert that product is not in cart (Add to Cart button visible).
        
        Args:
            product_name: Name of the product to check
        """
        product_items = self.find_elements(self.INVENTORY_ITEM)
        
        for item in product_items:
            name_element = item.locator(self.INVENTORY_ITEM_NAME)
            if name_element.text_content() == product_name:
                add_button = item.locator(self.ADD_TO_CART_BUTTON)
                assert add_button.is_visible(), f"Add to cart button not visible for product '{product_name}'"
                logger.info(f"Product not in cart assertion passed: {product_name}")
                return
        
        raise ValueError(f"Product '{product_name}' not found on the page") 