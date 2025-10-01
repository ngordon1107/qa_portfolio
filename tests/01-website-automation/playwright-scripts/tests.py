import re, pytest
from multiprocessing.connection import address_type

from playwright.sync_api import Page, expect

test_data = {
    "login": {
        "first_name": "Test_Kelly",
        "last_name": "Test_King",
        "password": "<PASSWORD>",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
        "phone": "1234567890",
        "ssn": "123-45-6789",
        "username": "kelly_king"
    }
    
}

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("https://parabank.parasoft.com/")
    print("successfully loaded page")
    yield

    print("after the test runs")

def test_registration(page: Page):
    # Arrange
    # username_input_box = page.locator("input[name='username']")
    # password_input_box = page.locator("input[name='password']")
    # login_button = page.get_by_role("button", name= "Log in")
    # forgot_login_link = page.get_by_role("link", name="Forgot login info?")
    registration_link = page.get_by_role("link", name= "Register")
    first_name = page.locator("input[id='customer.firstName']")
    last_name = page.locator("input[id='customer.lastName']")
    address = page.locator("input[id='customer.address.street']")
    city = page.locator("input[id='customer.address.city']")
    state = page.locator("input[id='customer.address.state']")
    zip = page.locator("input[id='customer.address.zipCode']")
    phone = page.locator("input[id='customer.phoneNumber']")
    ssn = page.locator("input[id='customer.ssn']")
    username = page.locator("input[id='customer.username']")
    password = page.locator("input[id='customer.password']")
    repeated_password = page.locator("input[id='repeatedPassword']")
    submit_button = page.get_by_role("button", name = "Register")
    header = page.locator("h1")


    # Act
    registration_link.click()
    print("registration link clicked")
    first_name.fill(test_data["login"]["first_name"])
    last_name.fill(test_data["login"]["last_name"])
    address.fill(test_data["login"]["address"])
    city.fill(test_data["login"]["city"])
    state.fill(test_data["login"]["state"])
    zip.fill(test_data["login"]["zip"])
    phone.fill(test_data["login"]["phone"])
    ssn.fill(test_data["login"]["ssn"])
    username.fill(test_data["login"]["username"])
    password.fill(test_data["login"]["password"])
    repeated_password.fill(test_data["login"]["password"])
    submit_button.click()

    # Assert
    # Expect a homepage to have login elements
    expect(header).to_contain_text(f"Welcome {test_data["login"]["username"]}")

@pytest.mark.skip(reason="not implemented yet")
def test_get_started_link(page: Page):

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()