from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_autoinstaller import install  # Auto installer
from telegram import Update
from telegram.ext import Application, CommandHandler
import asyncio
import time
import os

# Login credentials
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "7804928909")  # Use environment variables for security
PASSWORD = os.getenv("PASSWORD", "Game55555")
LOGIN_URL = "https://www.lottery7s.com/#/login"
CHART_URL = "https://www.lottery7s.com/#/home/AllLotteryGames/WinGo?typeId=1"

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "7214568559:AAG7pBO_5-f67AcAUrOrUfjnQrFNlIRTrCQ")

# Function to set up Selenium WebDriver
def setup_driver():
    install()  # Auto-install Chromedriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to login and fetch chart data
def login_and_fetch_chart():
    driver = setup_driver()
    driver.get(LOGIN_URL)
    time.sleep(5)  # Wait for page to load

    try:
        # Phone number input
        phone_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter phone number']")
        phone_input.send_keys(PHONE_NUMBER)

        # Password input
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter password']")
        password_input.send_keys(PASSWORD)

        # Login button
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        time.sleep(5)  # Wait for login to complete

        # Navigate to chart URL
        driver.get(CHART_URL)
        time.sleep(5)  # Wait for chart to load

        # Scrape chart data (Update these selectors based on actual page structure)
        period_element = driver.find_element(By.XPATH, "//div[@class='period-class']")  # Replace with actual XPath
        result_element = driver.find_element(By.XPATH, "//div[@class='result-class']")  # Replace with actual XPath

        period = period_element.text
        result = result_element.text

        driver.quit()
        return {"period": period, "result": result}

    except Exception as e:
        driver.quit()
        return f"Error: {e}"

# Prediction logic
def check_prediction(data):
    period = data["period"]
    result = data["result"]

    last_digit = int(str(period)[-1])  # Get last digit
    if last_digit == 9:
        prediction = "Small"
        if result.lower() == "small":
            return f"Period: {period}\nPrediction: {prediction}\nResult: Win"
        else:
            return f"Period: {period}\nPrediction: {prediction}\nResult: Loss"
    else:
        return f"Period: {period}\nNo prediction. Last digit is not 9."

# Telegram bot function
async def start(update: Update, context):
    await update.message.reply_text("Bot started. Monitoring chart...")
    while True:
        data = login_and_fetch_chart()  # Login and fetch chart data
        if isinstance(data, dict):  # If data is valid
            result = check_prediction(data)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text(data)  # Error message
        await asyncio.sleep(60)  # Check every 1 minute

# Main Telegram bot setup
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()


---