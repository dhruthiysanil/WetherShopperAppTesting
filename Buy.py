# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import config  # Load temperature threshold and XPath values

# Function to fetch the current temperature from the homepage
def get_temperature(driver):
    driver.get("https://weathershopper.pythonanywhere.com/")
    temp_text = driver.find_element(By.ID, "temperature").text
    temperature = int(re.sub(r'\D', '', temp_text))
    print(f" Current Temperature: {temperature}°C")
    return temperature

# Select the correct product category based on the temperature
def select_product(driver, temperature):
    if temperature >= config.TEMP:
        driver.find_element(By.XPATH, config.BUY_SUNSCREENS_BTN).click()
        expected_title = "Sunscreens"
    else:
        driver.find_element(By.XPATH, config.BUY_MOISTURIZERS_BTN).click()
        expected_title = "Moisturizers"

    heading = driver.find_element(By.TAG_NAME, config.HEADING_TAG).text
    assert expected_title in heading, f"Expected '{expected_title}', but got '{heading}'"
    print(f" Navigated to {heading} page")

# Add the lowest priced product on the page to the cart
def add_lowest_priced_item_to_cart(driver):
    items = driver.find_elements(By.XPATH, "//p[contains(text(),'Price')]/..")
    lowest_price = float('inf')
    lowest_button = None
    product_name = ""

    for item in items:
        price_text = item.find_element(By.XPATH, "./p[contains(text(),'Price')]").text
        price = int(price_text.split()[-1])
        
        if price < lowest_price:
            lowest_price = price
            lowest_button = item.find_element(By.TAG_NAME, "button")
            product_name = item.find_element(By.XPATH, "./p[1]").text

    if lowest_button:
        lowest_button.click()
        print(f" Added lowest priced product to cart: '{product_name}' for Rs. {lowest_price}")
    else:
        print("No product button found.")

    return lowest_price, product_name

# Handle payment with dummy Stripe details
def complete_payment(driver):
    driver.find_element(By.XPATH, "//button[contains(text(),'Cart')]").click()
    driver.find_element(By.CSS_SELECTOR, "button.stripe-button-el").click()

    stripe_frame = driver.find_element(By.CSS_SELECTOR, "iframe[name='stripe_checkout_app']")
    driver.switch_to.frame(stripe_frame)

    driver.find_element(By.ID, "email").send_keys("dhruthir@gmail.com")
    driver.execute_script("""
        document.querySelector("input#card_number").value = "4242 4242 4242 4242";
        document.querySelector("input#cc-exp").value = "12/25";
        document.querySelector("input#cc-csc").value = "123";
    """)
    print(" Dummy card details filled")    
    driver.find_element(By.XPATH, "//span[contains(text(),'Pay INR')]").click()
    driver.switch_to.default_content()

    success_msg = driver.find_element(By.XPATH, "//*[contains(text(),'success')]").text
    print(f" Payment Confirmation: {success_msg.strip()}")
    print(f" Final URL: {driver.current_url}")

# ---------- Main Automation Flow ----------
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

try:
    temperature = get_temperature(driver)
    select_product(driver, temperature)
    add_lowest_priced_item_to_cart(driver)
    complete_payment(driver)

except Exception as e:
    print(" Error occurred:", e)

finally:
    input(" Press Enter to exit and close browser...")
    driver.quit()
