"# WetherShopperAppTesting" 
# Weather Shopper App Testing

This project contains an automated test script using **Selenium** for the [Weather Shopper](https://weathershopper.pythonanywhere.com/) demo site.  
The script selects a product (sunscreen or moisturizer) based on the current temperature and completes a mock payment via Stripe.

## What It Does

- Reads the current temperature from the homepage
- Chooses to buy **sunscreens** if temp > 30°C, else **moisturizers**
- Adds the **lowest priced** item to cart
- Proceeds to checkout and fills in dummy payment details
- Prints confirmation message after mock payment

## Technologies Used

- Python 3.13
- Selenium WebDriver
- ChromeDriver

## Requirements

Install the required Python packages using:

```bash
pip install -r requirements.txt
