from playwright.sync_api import sync_playwright
from user_utils import get_random_user
import time
from logger import setup_logger
import pytest

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

            time.sleep(3)
            browser.close()
    
    except Exception as e:
        logger.error(f"Test faild due to an exception: {e}")

if __name__ == "__main__":
    test_register_new_user()