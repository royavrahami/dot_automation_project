"""
Login functionality tests for SauceDemo Test Automation Framework.

This module contains comprehensive tests for user authentication,
including positive and negative scenarios for all user types.
"""

import pytest
import allure
from loguru import logger

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from core.config_loader import config


@allure.epic("Authentication")
@allure.feature("User Login")
class TestLogin:
    """Test class for login functionality."""
    
    @allure.story("Successful Login")
    @allure.title("Login with standard user credentials")
    @allure.description("Verify that standard user can login successfully and access inventory page")
    @allure.severity("critical")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_standard_user_success(self, browser, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Test successful login with standard user.
        
        Steps:
        1. Navigate to login page
        2. Enter valid standard user credentials
        3. Click login button
        4. Verify successful login (redirect to inventory page)
        5. Verify inventory page elements are displayed
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Login with standard user credentials"):
            login_page.login_with_standard_user()
        
        with allure.step("Verify successful login"):
            login_page.assert_login_successful()
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_inventory_page_displayed()
        
        with allure.step("Verify inventory page functionality"):
            # Verify product count
            inventory_page.assert_product_count(6)
            
            # Verify cart badge is not visible (empty cart)
            inventory_page.assert_no_cart_badge_visible()
        
        logger.info("Standard user login test completed successfully")
    
    @allure.story("Failed Login")
    @allure.title("Login with locked out user")
    @allure.description("Verify that locked out user cannot login and appropriate error message is displayed")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.login
    def test_login_locked_out_user_failure(self, browser, login_page: LoginPage):
        """
        Test login failure with locked out user.
        
        Steps:
        1. Navigate to login page
        2. Enter locked out user credentials
        3. Click login button
        4. Verify error message is displayed
        5. Verify user remains on login page
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Attempt login with locked out user"):
            login_page.login_with_locked_user()
        
        with allure.step("Verify error message is displayed"):
            login_page.assert_error_message_displayed("Sorry, this user has been locked out")
            
            # Verify specific error message content
            error_message = login_page.get_error_message()
            assert "locked out" in error_message.lower(), f"Expected 'locked out' in error message, got: {error_message}"
        
        with allure.step("Verify user remains on login page"):
            assert login_page.is_login_page_displayed(), "User should remain on login page after failed login"
            
            # Verify URL hasn't changed
            current_url = login_page.get_current_url()
            assert "inventory.html" not in current_url, "User should not be redirected to inventory page"
        
        logger.info("Locked out user login test completed successfully")
    
    @allure.story("Failed Login")
    @allure.title("Login with invalid credentials")
    @allure.description("Verify that invalid credentials are rejected with appropriate error message")
    @allure.severity("high")
    @pytest.mark.negative
    @pytest.mark.login
    @pytest.mark.parametrize("username,password", [
        ("invalid_user", "wrong_password"),
        ("standard_user", "wrong_password"),
        ("", ""),
        ("", "secret_sauce"),
        ("standard_user", "")
    ])
    def test_login_invalid_credentials(self, browser, login_page: LoginPage, username: str, password: str):
        """
        Test login with various invalid credential combinations.
        
        Args:
            username: Username to test
            password: Password to test
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step(f"Attempt login with credentials: '{username}' / '{password}'"):
            login_page.login(username, password)
        
        with allure.step("Verify error message is displayed"):
            login_page.assert_error_message_displayed()
            
            # Verify error message contains relevant information
            error_message = login_page.get_error_message()
            
            if username == "" or password == "":
                assert any(word in error_message.lower() for word in ["required", "missing"]), \
                    f"Expected 'required' or 'missing' in error message for empty fields, got: {error_message}"
            else:
                assert any(word in error_message.lower() for word in ["username", "password", "not match"]), \
                    f"Expected authentication error message, got: {error_message}"
        
        with allure.step("Verify user remains on login page"):
            assert login_page.is_login_page_displayed(), "User should remain on login page after failed login"
        
        logger.info(f"Invalid credentials test completed for: {username}/{password}")
    
    @allure.story("Successful Login")
    @allure.title("Login with problem user")
    @allure.description("Verify that problem user can login but may have UI issues")
    @allure.severity("medium")
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_problem_user_success(self, browser, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Test login with problem user (user with various UI issues).
        
        Steps:
        1. Navigate to login page
        2. Login with problem user
        3. Verify login is successful
        4. Note: This user may have image and sorting issues
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Login with problem user credentials"):
            login_page.login_with_problem_user()
        
        with allure.step("Verify successful login"):
            login_page.assert_login_successful()
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_inventory_page_displayed()
        
        with allure.step("Verify basic inventory functionality"):
            # Problem user should still see products
            inventory_page.assert_product_count(6)
            
            # Note: Problem user may have image issues, but basic functionality should work
            product_names = inventory_page.get_product_names()
            assert len(product_names) > 0, "Problem user should still see product names"
        
        logger.info("Problem user login test completed successfully")
    
    @allure.story("Successful Login")
    @allure.title("Login with performance glitch user")
    @allure.description("Verify that performance glitch user can login with potential delays")
    @allure.severity("medium")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.slow
    def test_login_performance_glitch_user_success(self, browser, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Test login with performance glitch user (user with performance issues).
        
        Steps:
        1. Navigate to login page
        2. Login with performance glitch user
        3. Verify login is successful with potential delays
        4. Verify inventory page loads (may be slower)
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Login with performance glitch user credentials"):
            login_page.login_with_performance_user()
        
        with allure.step("Verify successful login (with potential performance delays)"):
            # Performance glitch user may take longer to redirect
            login_page.assert_login_successful()
            
            # Wait longer for inventory page to load due to performance issues
            inventory_page.wait_for_inventory_page_loaded()
            inventory_page.assert_inventory_page_displayed()
        
        with allure.step("Verify inventory functionality works despite performance issues"):
            inventory_page.assert_product_count(6)
            
            # Verify products are displayed
            product_names = inventory_page.get_product_names()
            assert len(product_names) == 6, f"Expected 6 products, got {len(product_names)}"
        
        logger.info("Performance glitch user login test completed successfully")
    
    @allure.story("Login Form Validation")
    @allure.title("Error message dismissal")
    @allure.description("Verify that error messages can be dismissed properly")
    @allure.severity("low")
    @pytest.mark.regression
    @pytest.mark.login
    def test_error_message_dismissal(self, browser, login_page: LoginPage):
        """
        Test error message dismissal functionality.
        
        Steps:
        1. Navigate to login page
        2. Trigger an error by invalid login
        3. Verify error message is displayed
        4. Dismiss error message
        5. Verify error message is hidden
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Trigger error message with invalid credentials"):
            login_page.login("invalid", "invalid")
            login_page.assert_error_message_displayed()
        
        with allure.step("Dismiss error message"):
            login_page.close_error_message()
        
        with allure.step("Verify error message is hidden"):
            login_page.assert_no_error_message_displayed()
        
        with allure.step("Verify form is still functional after error dismissal"):
            # Clear fields and try valid login
            login_page.clear_login_form()
            login_page.login_with_standard_user()
            login_page.assert_login_successful()
        
        logger.info("Error message dismissal test completed successfully")
    
    @allure.story("Login Form Validation")
    @allure.title("Form field validation")
    @allure.description("Verify login form field behavior and validation")
    @allure.severity("low")
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_form_field_validation(self, browser, login_page: LoginPage):
        """
        Test login form field validation and behavior.
        
        Steps:
        1. Navigate to login page
        2. Test field clearing functionality
        3. Test field value retrieval
        4. Test button state
        """
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            login_page.assert_login_page_displayed()
        
        with allure.step("Test field input and clearing"):
            # Enter values
            login_page.enter_username("test_user")
            login_page.enter_password("test_pass")
            
            # Verify values were entered
            assert login_page.get_username_value() == "test_user", "Username field should contain entered value"
            assert login_page.get_password_value() == "test_pass", "Password field should contain entered value"
            
            # Clear fields
            login_page.clear_login_form()
            
            # Verify fields are cleared
            assert login_page.get_username_value() == "", "Username field should be empty after clearing"
            assert login_page.get_password_value() == "", "Password field should be empty after clearing"
        
        with allure.step("Test login button state"):
            # Login button should be enabled
            assert login_page.is_login_button_enabled(), "Login button should be enabled"
        
        logger.info("Login form field validation test completed successfully") 