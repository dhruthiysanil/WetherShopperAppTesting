# config.py

# Temperature threshold
TEMP = 30

# Base URL
BASE_URL = "https://weathershopper.pythonanywhere.com/"

# XPath selectors
BUY_SUNSCREENS_BTN = "//button[text()='Buy sunscreens']"
BUY_MOISTURIZERS_BTN = "//button[text()='Buy moisturizers']"
CART_BTN = "//button[contains(text(),'Cart')]"
STRIPE_BTN = "button.stripe-button-el"
STRIPE_IFRAME = "iframe[name='stripe_checkout_app']"
STRIPE_PAY_BTN = "//span[contains(text(),'Pay INR')]"

# Stripe test data
EMAIL = "dhruthir@gmail.com"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/25"
CVC = "123"

# XPath for success message
SUCCESS_MSG = "//*[contains(text(),'success')]"

# Element locators
TEMPERATURE_ID = "temperature"
HEADING_TAG = "h2"
PRODUCT_CONTAINER = "//p[contains(text(),'Price')]/.."
PRODUCT_PRICE = "./p[contains(text(),'Price')]"
PRODUCT_NAME = "./p[1]"
