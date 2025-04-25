from playwright.sync_api import sync_playwright
from user_utils import get_random_user
import time
import pytest

def test_register_new_user():
    id, name, email, password, firstName, lastName, company, address, address2, state, city, zipcode, mobileNumber = get_random_user()
    with sync_playwright() as p:
        print( "Step 1: Launching browser")
        browser = p.chromium.launch(headless=False, slow_mo=100) #Run browser
        page = browser.new_page()

        print("Step 2: Navigating to home page")
        page.goto('https://www.automationexercise.com')

        print("Step 3: Verifying homepage logo is visible")
        page.wait_for_selector("img[alt='Website for automation practice']")
        assert page.is_visible("img[alt='Website for automation practice']")
        
        print("Step 4: Click on 'Signup / Login' button")
        page.click("a[href = '/login']")

        print("Step 5: Verify 'New User Signup!' is visible")
        page.wait_for_selector("div[class='signup-form']")
        assert page.is_visible("div[class='signup-form']")

        print("Step 6: Enter name and email address")
        page.fill('[data-qa="signup-name"]', name)
        page.fill('[data-qa="signup-email"]', email)
        page.click('button[data-qa="signup-button"]')

        time.sleep(3)
        browser.close()

test_register_new_user()