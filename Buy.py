



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import re


# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.implicitly_wait(10)  # Global wait for all element actions

# try:
#     #  Open website and get temperature
#     driver.get("https://weathershopper.pythonanywhere.com/")
#     temp_text = driver.find_element(By.ID, "temperature").text
#     temperature = int(re.sub(r'\D', '', temp_text))
#     print(f" Current Temperature: {temperature}°C")

#     #  Click on appropriate product button
#     if temperature > 30:
#         driver.find_element(By.XPATH, "//button[text()='Buy sunscreens']").click()
#         expected_title = "Sunscreens"
#     else:
#         driver.find_element(By.XPATH, "//button[text()='Buy moisturizers']").click()
#         expected_title = "Moisturizers"

#     #  Validate correct page opened
#     heading = driver.find_element(By.TAG_NAME, "h2").text
#     assert expected_title in heading, f"Expected '{expected_title}', but got '{heading}'"
#     print(f" Navigated to {heading} page")
   
#     #  Add lowest priced item to cart using a for loop
#     items = driver.find_elements(By.XPATH, "//p[contains(text(),'Price')]/..")
#     lowest_price = float('inf')
#     lowest_button = None

#     for item in items:
#         price_text = item.find_element(By.XPATH, "./p[contains(text(),'Price')]").text
#         price = int(price_text.split()[-1])  
#         if price < lowest_price:
#             lowest_price = price
#             lowest_button = item.find_element(By.TAG_NAME, "button")

#     if lowest_button:
#         lowest_button.click()
#         print(f" Added lowest priced product to cart: Rs. {lowest_price}")
#     else:
#         print(" No product button found.")

#     #  Proceed to cart and click Pay
#     driver.find_element(By.XPATH, "//button[contains(text(),'Cart')]").click()
#     # Pay button
#     driver.find_element(By.CSS_SELECTOR, "button.stripe-button-el").click()

#     #  Switch to Stripe iframe
#     stripe_frame = driver.find_element(By.CSS_SELECTOR, "iframe[name^='stripe_checkout_app']")
#     driver.switch_to.frame(stripe_frame)

#     #  Enter dummy payment details
#     driver.find_element(By.ID, "email").send_keys("testuser@example.com")
#     driver.execute_script("""
#         document.querySelector("input#card_number").value = "4242 4242 4242 4242";
#         document.querySelector("input#cc-exp").value = "12/25";
#         document.querySelector("input#cc-csc").value = "123";
#     """)
#     print("Dummy card details filled")

#     # Submit payment
#     driver.find_element(By.XPATH, "//span[contains(text(),'Pay INR')]").click()
#     driver.switch_to.default_content()

#     #  Wait for redirect using implicit wait + repeated check
#     while "confirmation" not in driver.current_url:
#         pass  

#     #  Print confirmation message
#     success_msg = driver.find_element(By.XPATH, "//*[contains(text(),'success') or contains(text(),'Success')]").text
#     print(f" Confirmation: {success_msg.strip()}")
#     print(f" Final URL: {driver.current_url}")

# except Exception as e:
#     print(" Error occurred:", e)

# finally:
#     input(" Press Enter to exit and close browser...")
#     driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
import re


driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)  # Global wait for all element actions

try:
    #  Open website and get temperature
    driver.get("https://weathershopper.pythonanywhere.com/")
    temp_text = driver.find_element(By.ID, "temperature").text
    temperature = int(re.sub(r'\D', '', temp_text))
    print(f" Current Temperature: {temperature}°C")

    #  Click on appropriate product button
    if temperature > 30:
        driver.find_element(By.XPATH, "//button[text()='Buy sunscreens']").click()
        expected_title = "Sunscreens"
    else:
        driver.find_element(By.XPATH, "//button[text()='Buy moisturizers']").click()
        expected_title = "Moisturizers"

    #  Validate correct page opened
    heading = driver.find_element(By.TAG_NAME, "h2").text
    assert expected_title in heading, f"Expected '{expected_title}', but got '{heading}'"
    print(f" Navigated to {heading} page")

    #  Add lowest priced item to cart using a for loop
    items = driver.find_elements(By.XPATH, "//p[contains(text(),'Price')]/..")
    lowest_price = float('inf')
    lowest_button = None

    for item in items:
        price_text = item.find_element(By.XPATH, "./p[contains(text(),'Price')]").text
        price = int(price_text.split()[-1])
        if price < lowest_price:
            lowest_price = price
            lowest_button = item.find_element(By.TAG_NAME, "button")

    if lowest_button:
        lowest_button.click()
        print(f" Added lowest priced product to cart: Rs. {lowest_price}")
    else:
        print(" No product button found.")

    #  Proceed to cart and click Pay
    driver.find_element(By.XPATH, "//button[contains(text(),'Cart')]").click()
    driver.find_element(By.CSS_SELECTOR, "button.stripe-button-el").click()

    #  Switch to Stripe iframe (exact match, no ^=)
    stripe_frame = driver.find_element(By.CSS_SELECTOR, "iframe[name='stripe_checkout_app']")
    driver.switch_to.frame(stripe_frame)

    #  Enter dummy payment details
    driver.find_element(By.ID, "email").send_keys("testuser@example.com")
    driver.execute_script("""
        document.querySelector("input#card_number").value = "4242 4242 4242 4242";
        document.querySelector("input#cc-exp").value = "12/25";
        document.querySelector("input#cc-csc").value = "123";
    """)
    print(" Dummy card details filled")

    # Submit payment
    driver.find_element(By.XPATH, "//span[contains(text(),'Pay INR')]").click()
    driver.switch_to.default_content()

    #  Find confirmation message directly using implicit wait
    success_msg = driver.find_element(By.XPATH, "//*[contains(text(),'success') or contains(text(),'Success')]").text
    print(f" Payment Confirmation: {success_msg.strip()}")
    print(f" Final URL: {driver.current_url}")

except Exception as e:
    print("  Error occurred:", e)

finally:
    input(" Press Enter to exit and close browser...")
    driver.quit()

