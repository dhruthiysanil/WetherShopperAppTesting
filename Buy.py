"""
Automated Selenium script to:
- Fetch temperature from the Weather Shopper homepage.
- Navigate to the Sunscreen or Moisturizer page based on temperature.
- Add the lowest priced item to the cart.
- Proceed to checkout using Stripe with dummy test data.
- Confirm the successful payment message after completion.
"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import config


# Fetch the current temperature from the homepage.
def get_temperature(driver):
    driver.get(config.BASE_URL)
    temp_text = driver.find_element(By.ID, config.TEMPERATURE_ID).text
    temperature = int(re.sub(r'\D', '', temp_text))
    print(f"Current Temperature: {temperature}°C")
    return temperature


# Select the product category (Sunscreen or Moisturizer) based on temperature.
def select_product(driver, temperature):
    if temperature >= config.TEMP:
        driver.find_element(By.XPATH, config.BUY_SUNSCREENS_BTN).click()
        expected_title = "Sunscreens"
    else:
        driver.find_element(By.XPATH, config.BUY_MOISTURIZERS_BTN).click()
        expected_title = "Moisturizers"

    heading = driver.find_element(By.TAG_NAME, config.HEADING_TAG).text
    assert expected_title in heading, f"Expected '{expected_title}', but got '{heading}'"
    print(f"Navigated to {heading} page")


# Find and add the lowest-priced product from the product list to the cart.
def add_lowest_priced_item_to_cart(driver):
    items = driver.find_elements(By.XPATH, config.PRODUCT_CONTAINER)
    lowest_price = float('inf')
    lowest_button = None
    product_name = ""

    for item in items:
        price_text = item.find_element(By.XPATH, config.PRODUCT_PRICE).text
        price = int(price_text.split()[-1])

        if price < lowest_price:
            lowest_price = price
            lowest_button = item.find_element(By.TAG_NAME, "button")
            product_name = item.find_element(By.XPATH, config.PRODUCT_NAME).text

    if lowest_button:
        lowest_button.click()
        print(f"Added lowest priced product to cart: '{product_name}' for Rs. {lowest_price}")
    else:
        print("No product button found.")

    return lowest_price, product_name


# Proceed to payment and simulate Stripe payment using dummy test data.
def complete_payment(driver):
    driver.find_element(By.XPATH, config.CART_BTN).click()
    driver.find_element(By.CSS_SELECTOR, config.STRIPE_BTN).click()

    stripe_frame = driver.find_element(By.CSS_SELECTOR, config.STRIPE_IFRAME)
    driver.switch_to.frame(stripe_frame)

    driver.find_element(By.ID, "email").send_keys(config.EMAIL)

    driver.execute_script(f"""
        document.querySelector("input#card_number").value = "{config.CARD_NUMBER}";
        document.querySelector("input#cc-exp").value = "{config.EXPIRY}";
        document.querySelector("input#cc-csc").value = "{config.CVC}";
    """)
    print("Dummy card details filled")

    driver.find_element(By.XPATH, config.STRIPE_PAY_BTN).click()
    driver.switch_to.default_content()

    success_msg = driver.find_element(By.XPATH, config.SUCCESS_MSG).text
    print(f"Payment Confirmation: {success_msg.strip()}")
    print(f"Final URL: {driver.current_url}")


# Main function to execute the end-to-end automation flow:
# - Temperature fetch
# - Product selection
# - Cart addition
# - Payment simulation
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress most Chrome logs

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    try:
        temperature = get_temperature(driver)
        select_product(driver, temperature)
        add_lowest_priced_item_to_cart(driver)
        complete_payment(driver)

    except Exception as error:
        print("Error occurred:", error)

    finally:
        input("Press Enter to exit and close browser...")
        driver.quit()


if __name__ == "__main__":
    main()
