from playwright.sync_api import sync_playwright
from user_utils import get_random_user
import time
from logger import setup_logger
import pytest
import random
import logging

logger = logging.getLogger(__name__)

def select_random_dropdown_option(page, selector: str, description: str = "dropdown") -> None:
    """
    Select a random non-empty option from a dropdown.
    Args:
        page: Playwrite page instance.
        selector: CSS selector for the dropdown.
        description: Friendly name for logging (e.g., 'day', 'month', 'year').
    """
    logger.info(f"Selecting random{description} from dropdown: {selector}")

    #Get all available options
    options = page.query_selector_all(f"{selector} option")
    if not options:
        logger.error(f"No options found for {description} ({selector})")
        raise ValueError(f"No options found for {description} ({selector})")

    #Filter out placeholder/empty options
    valid_options = [opt for opt in options if opt.get_attribute('value')]
    if not valid_options:
        logger.error(f"No valid (non-empty) options found for {description} ({selector})")
        raise ValueError(f"No valid (non_empty) options found for {description} ({selector})")

    #Pick random option
    random_option = random.choice(valid_options)
    random_value = random_option.get_attribute('value')

    logger.info(f"Randomly selected {description}: {random_value}")

    #Select the option
    page.select_option(selector, random_value)

logger = setup_logger()

def test_register_new_user():
    logger.info("Starting test: Register a new user.")

    try:

        id, name, email, password, firstName, lastName, company, address, address2, state, city, zipcode, mobileNumber = get_random_user()
    
        with sync_playwright() as p:
            logger.info("Step 1: Launching browser")
            browser = p.chromium.launch(headless=False, slow_mo=100) #Run browser
            page = browser.new_page()

            logger.info("Step 2: Navigating to home page")
            page.goto('https://www.automationexercise.com')

            logger.info("Step 3: Verifying homepage logo is visible")
            page.wait_for_selector("img[alt='Website for automation practice']")
            assert page.is_visible("img[alt='Website for automation practice']")
            
            logger.info("Step 4: Click on 'Signup / Login' button")
            page.click("a[href = '/login']")

            logger.info("Step 5: Verify 'New User Signup!' is visible")
            page.wait_for_selector("div[class='signup-form']")
            assert page.is_visible("div[class='signup-form']")

            logger.info("Step 6: Enter name and email address")
            page.fill('[data-qa="signup-name"]', name)
            page.fill('[data-qa="signup-email"]', email)
            page.click('button[data-qa="signup-button"]')

            logger.info("Step 7: Verify 'ENTER ACCOUNT INFORMATION' is visible")
            page.wait_for_selector("div[class='login-form']")
            assert page.is_visible("div[class='login-form']")

            logger.info("Step 8: Fill details: Title, Name, Email, Password etc")
            page.wait_for_selector('[id="id_gender1"]')
            page.click('[id="id_gender1"]')
            page.wait_for_selector('[data-qa="name"]')
            page.fill('[data-qa="name"]', name)
            #page.wait_for_selector('[data-qa="email"]')
            #page.fill('[data-qa="email"]', email)
            page.wait_for_selector('[data-qa="password"]')
            page.fill('[data-qa="password"]', password)
            select_random_dropdown_option(page, 'select[data-qa="days"]', description="day")
            select_random_dropdown_option(page, 'select[data-qa="months"]', description="month")
            select_random_dropdown_option(page, 'select[data-qa="years"]', description="year")
            
            logger.info("Step 9: Select checkbox 'Sign up for our newsletter!'")
            page.click('[id="newsletter"]')
            
            logger.info("Step 10: Select checkbox 'Receive special offers from our partners!'")
            page.click('[id="optin"]')
            
            logger.info("Step 11: Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number")
            page.fill('[data-qa="first_name"]', firstName)
            page.fill('[data-qa="last_name"]', lastName)
            page.fill('[data-qa="company"]', company)
            page.fill('[data-qa="address"]', address)
            page.fill('[data-qa="address2"]', address2)
            select_random_dropdown_option(page, 'select[data-qa="country"]', description="country")
            page.fill('[data-qa="state"]', state)
            page.fill('[data-qa="city"]', city)
            page.fill('[data-qa="zipcode"]', zipcode)
            page.fill('[data-qa="mobile_number"]', mobileNumber)
            
            logger.info("Step 12: Click 'Create Account button'")
            page.click('[data-qa="create-account"]')

            logger.info("Step 13: Verify that 'ACCOUNT CREATED!' is visible")
            page.wait_for_selector('[data-qa="account-created"]')
            assert page.is_visible('[data-qa="account-created"]')

            logger.info("Step 14: Click 'Continue' button")
            page.click('[data-qa="continue-button"]')

            logger.info("Step 15: Verify that 'Logged in as username' is visible")
            page.wait_for_selector('[class="fa fa-user"]')
            assert page.is_visible('[class="fa fa-user"]')

            logger.info("Step 16: Click 'Delete Account' button")
            page.click('[href="/delete_account"]')

            logger.info("Step 17: Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button")
            page.wait_for_selector('[data-qa="account-deleted"]')
            assert page.is_visible('[data-qa="account-deleted"]')
            page.click('[data-qa="continue-button"]')

            logger.info("SUCCESS!!!")

            time.sleep(3)
            #browser.close()
    
    except Exception as e:
        logger.error(f"Test faild due to an exception: {e}")

if __name__ == "__main__":
    test_register_new_user()