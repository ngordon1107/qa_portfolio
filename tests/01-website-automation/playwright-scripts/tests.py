# import subprocess
import pytest
from random import randint
from playwright.sync_api import Page, expect

# Data  -------------------------------------------------------
random_num = str(randint(1200, 99999))
random_char = chr(randint(65, 90))
password = f"<PASSWORD{randint(1200, 99999)}>"
test_data = {
    "login": {
        "first_name": f"Test_Kelly",
        "last_name": "Test_King",
        "password": password,
        "address": "123 Main St",
        "city": "Anytown",
        "state": "NY",
        "zip": "12345",
        "phone": "1234567890",
        "ssn": "123-45-6789",
        "username": f"user_{random_num}" # making random to avoid flakiness -- server doesn't allow to delete registrations and back-to-back testing causes "user already exists" errors
    }
}
# Setup Fixtures  -------------------------------------------------------
# @pytest.fixture(scope="session", autouse=True)
# def restart_parabank_container():
#     print("Restarting ParaBank container before tests...")
#     subprocess.run(["docker", "restart", "parabank"], check=True)
#     yield
#     print("Restarting ParaBank container after tests...")
#     subprocess.run(["docker", "restart", "parabank"], check=True)

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("http://localhost:8080/parabank/index.htm")
    print("successfully loaded page")
    yield

    print("after the test runs")

@pytest.fixture
def login(page: Page):
    # Arrange
    username_input_box = page.locator("input[name='username']")
    password_input_box = page.locator("input[name='password']")
    login_button = page.get_by_role("button", name="Log in")
    # forgot_login_link = page.get_by_role("link", name="Forgot login info?")

    # Act
    username_input_box.fill(test_data["login"]["username"])
    print(f"username during login: {test_data['login']['username']}")
    password_input_box.fill(test_data["login"]["password"])
    login_button.click()

@pytest.fixture
def logout(page: Page):
    def __logout():
        # Arrange
        logout_link = page.get_by_role("link", name="Log Out")

        # Act
        logout_link.click()
        print("successfully logged out")
    return __logout

# Test Suite -------------------------------------------------------
def test_registration(page: Page):
    # Arrange
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
    print(f"username during registration: {test_data['login']['username']}")
    expect(header).to_contain_text(f"Welcome {test_data["login"]["username"]}")

def test_login(page: Page, login):
    # Arrange
    header = page.locator("p.smallText")

    # Act (login fixture in params)

    # Assert
    expect(header).to_contain_text(f"Welcome {test_data['login']['first_name']} {test_data['login']['last_name']}")

def test_logout(page: Page, login, logout):
    # Arrange
    original_side_panel_header = (page.locator("p.smallText")).text_content()
    # page.pause()

    # Act
    # login using fixture
    logout() # using fixture
    new_side_panel_header = page.locator("h2")

    # Assert
    assert original_side_panel_header == f"Welcome {test_data['login']['first_name']} {test_data['login']['last_name']}"
    expect(new_side_panel_header).to_contain_text("Customer Login")

def test_bill_pay(page: Page, login):
    # Arrange
    bill_pay_link = page.get_by_role("link", name="Bill Pay")
    # pulling account number from account overview page
    verified_account_num = page.locator("table td:nth-child(1) a").text_content()
    payee_name_input = "PSEG"
    payee_address_input = "123 Presidents St"
    payee_city_input = "Edison"
    payee_state_input = "NJ"
    payee_zip_input = "54321"
    payee_phone_input = "0987654321"
    payee_account_num_input = "29010"
    amount_input = "500"

    # Act
    bill_pay_link.click()
    page_header_element = page.wait_for_selector("div#billpayForm h1", state="visible")
    page_header = page_header_element.inner_text()
    # bill pay fields
    payee_name = page.locator("input[name='payee.name']")
    payee_address = page.locator("input[name='payee.address.street']")
    payee_city = page.locator("input[name='payee.address.city']")
    payee_state = page.locator("input[name='payee.address.state']")
    payee_zip = page.locator("input[name='payee.address.zipCode']")
    payee_phone = page.locator("input[name='payee.phoneNumber']")
    payee_account_num = page.locator("input[name='payee.accountNumber']")
    payee_verify_account_num = page.locator("input[name='verifyAccount']")
    amount = page.locator("input[name='amount']")

    account_num_displayed_to_user = (page.locator("option")).text_content()
    account_num_actual_value = (page.locator("option")).get_attribute("value")
    submit_button = page.get_by_role("button", name="Send Payment")

    # filling fields
    payee_name.fill(payee_name_input)
    payee_address.fill(payee_address_input)
    payee_city.fill(payee_city_input)
    payee_state.fill(payee_state_input)
    payee_zip.fill(payee_zip_input)
    payee_phone.fill(payee_phone_input)
    payee_account_num.fill(payee_account_num_input)
    payee_verify_account_num.fill(payee_account_num_input)
    amount.fill(amount_input)

    # submitting form
    submit_button.click()

    status_header = page.locator("div#billpayResult h1")
    status_message_element = page.wait_for_selector("div#billpayResult p", state="visible")
    status_message = status_message_element.inner_text()

    # Assert
    # validating that the account number on the bill pay form is correct
    assert account_num_actual_value == account_num_displayed_to_user
    assert verified_account_num == account_num_displayed_to_user
    # validating the header of the bill pay page
    assert page_header == "Bill Payment Service"

    # validating header and status message indicate a successful submission
    expect(status_header).to_contain_text("Bill Payment Complete")
    assert f"Bill Payment to {payee_name_input} in the amount of ${float(amount_input):.2f} from account {verified_account_num} was successful" in status_message


@pytest.mark.skip(reason="not implemented yet")
def test_transfer_funds(page: Page, login):
    pass

@pytest.mark.skip(reason="not implemented yet")
def test_check_account_overview(page: Page, login):
    # Arrange
    account_number_label = page.locator("table td:nth-child(1) a")

    #Act
    account_number_label.click()
    account_details_header = page.locator("div[id='accountDetails']: h1")
    account_activity_header = page.locator("div[id='accountActivity']: h1")


    #