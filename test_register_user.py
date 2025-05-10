from playwright.sync_api import sync_playwright
from user_utils import get_random_user
from logger import setup_logger
import time
import random
import logging

logger = setup_logger()


def wait_and_assert_visible(page, selector, description="element"):
    logger.info(f"Waiting for {description} to appear: {selector}")
    page.wait_for_selector(selector)
    assert page.is_visible(selector), f"{description} not visible: {selector}"


def select_random_dropdown_option(page, selector: str, description: str = "dropdown") -> None:
    logger.info(f"Selecting random {description} from dropdown: {selector}")
    options = page.query_selector_all(f"{selector} option")
    valid_options = [opt for opt in options if opt.get_attribute('value')]
    if not valid_options:
        raise ValueError(f"No valid options for {description}: {selector}")
    random_option = random.choice(valid_options)
    page.select_option(selector, random_option.get_attribute('value'))
    logger.info(f"Selected {description}: {random_option.get_attribute('value')}")


def fill_form_fields(page, field_data: dict):
    for selector, value in field_data.items():
        logger.info(f"Filling field {selector} with value: {value}")
        page.fill(selector, value)


def test_register_new_user():
    logger.info("Starting test: Register a new user")

    id, name, email, password, firstName, lastName, company, address, address2, state, city, zipcode, mobileNumber = get_random_user()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            page = browser.new_page()

            page.goto('https://www.automationexercise.com')
            wait_and_assert_visible(page, "img[alt='Website for automation practice']", "Homepage logo")

            page.click("a[href = '/login']")
            wait_and_assert_visible(page, "div[class='signup-form']", "Signup form")

            page.fill('[data-qa="signup-name"]', name)
            page.fill('[data-qa="signup-email"]', email)
            page.click('button[data-qa="signup-button"]')

            wait_and_assert_visible(page, "div[class='login-form']", "Account info form")

            page.click('[id="id_gender1"]')
            page.fill('[data-qa="name"]', name)
            page.fill('[data-qa="password"]', password)

            for selector, description in [
                ('select[data-qa="days"]', 'day'),
                ('select[data-qa="months"]', 'month'),
                ('select[data-qa="years"]', 'year')
            ]:
                select_random_dropdown_option(page, selector, description)

            page.click('[id="newsletter"]')
            page.click('[id="optin"]')

            fill_form_fields(page, {
                '[data-qa="first_name"]': firstName,
                '[data-qa="last_name"]': lastName,
                '[data-qa="company"]': company,
                '[data-qa="address"]': address,
                '[data-qa="address2"]': address2,
                '[data-qa="state"]': state,
                '[data-qa="city"]': city,
                '[data-qa="zipcode"]': zipcode,
                '[data-qa="mobile_number"]': mobileNumber
            })

            select_random_dropdown_option(page, 'select[data-qa="country"]', 'country')

            page.click('[data-qa="create-account"]')
            wait_and_assert_visible(page, '[data-qa="account-created"]', 'Account Created message')

            page.click('[data-qa="continue-button"]')
            wait_and_assert_visible(page, '[class="fa fa-user"]', 'Logged in user')

            page.click('[href="/delete_account"]')
            wait_and_assert_visible(page, '[data-qa="account-deleted"]', 'Account Deleted message')
            page.click('[data-qa="continue-button"]')

            logger.info("Test completed successfully.")
            time.sleep(5)
            browser.close()

    except Exception as e:
        logger.error(f"Test failed due to an exception: {e}")


if __name__ == "__main__":
    test_register_new_user()
