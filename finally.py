import re
import time
import asyncio
import threading
import nest_asyncio
from selenium import webdriver
from telethon import TelegramClient, events
from telethon.sessions import MemorySession
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome as UndetectedChrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Replace these with your own values
api_id = '28859355'
api_hash = '27773de1f4411601c645e4156ca07687'
phone_number = '+918869040360'
channel_username = '@amiteshhsingh'

# Create a new MemorySession to avoid database locking issues
session = MemorySession()
client = TelegramClient(session, api_id, api_hash)

current_pair = ''
trade_direction = ''
duration = ''

# Global variable to store the browser instance
driver = None
is_logged_in = False
is_crypto_idx_selected = False

async def setup_browser():
    global driver, is_logged_in, is_crypto_idx_selected

    try:
        if driver is None:
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            driver = UndetectedChrome(options=options)
            print("Browser initialized successfully.")

        if not is_logged_in:
            driver.get("https://binomo.com/in-en/")
            print("Navigated to Binomo website.")

            # Click the login button on the homepage
            login_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div[2]/div[1]/a[1]"))
            )
            login_button.click()
            print("Clicked login button.")

            # Wait for binomo launch msg
            launch_msg = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/vui-button[2]"))
            )
            launch_msg.click()
            print("Pop up declined successfully.")

            # Wait for the login form to appear
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/aside[2]/vui-sidebar/div/div/div/div/vui-scroll/div[1]/div/auth-form/div/vui-tabs/div/div[1]/div/vui-tab-button[2]"))
            )
            print("Login form appeared.")

            # Locate the username and password fields and sign-in button
            username_field = driver.find_element(By.XPATH,
                                                 "/html/body/aside[2]/vui-sidebar/div/div/div/div/vui-scroll/div[1]/div/auth-form/div/div/sa-auth-form/div/div/app-sign-in/div/form/div[1]/app-input/way-input/div/div[1]/way-input-text/input")
            password_field = driver.find_element(By.XPATH,
                                                 "/html/body/aside[2]/vui-sidebar/div/div/div/div/vui-scroll/div[1]/div/auth-form/div/div/sa-auth-form/div/div/app-sign-in/div/form/div[2]/app-input/way-input/div/div/way-input-password/input")
            signin_button = driver.find_element(By.XPATH,
                                                "/html/body/aside[2]/vui-sidebar/div/div/div/div/vui-scroll/div[1]/div/auth-form/div/div/sa-auth-form/div/div/app-sign-in/div/form/vui-button/button")

            # Enter the username and password
            username_field.send_keys("gejero9084@stikezz.com")
            password_field.send_keys("Amitesh@0403")
            print("Entered login credentials.")

            # Click the sign-in button
            signin_button.click()
            print("Clicked sign-in button.")

            # Wait for the login to process and the next page to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/binomo-root/platform-ui-scroll/div/div/platform-layout-header/header/div[2]/ng-component/div"))
            )

            is_logged_in = True
            print("Logged in successfully.")

        if not is_crypto_idx_selected:
            # Locate and click on the search bar
            search_bar = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/binomo-root/platform-ui-scroll/div/div/platform-layout-header/header/div[2]/ng-component/div/vui-button"))
            )
            search_bar.click()
            print("Clicked the search bar successfully.")

            # Locate the search input field and enter "Crypto IDX"
            search_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/vui-popover/div[2]/assets-block/asset-search/way-input/div/div/way-input-search/input"))
            )
            search_input.send_keys("Crypto IDX")
            print("Entered 'Crypto IDX' in search field.")

            # Now, initiate the search by clicking Crypto IDX
            search_idx = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/vui-popover/div[2]/assets-block/div/asset-list/div/platform-ui-scroll/div/div/section/div[2]/div"))
            )
            search_idx.click()
            print("Clicked on Crypto IDX in search results.")

            # Wait for the Crypto IDX to be selected and the trading interface to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/binary-info/div[2]/div/trading-buttons/vui-button[1]"))
            )
            print("Crypto IDX selected and trading interface loaded.")

            # Increase bet price 
            search_plusbet = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/div/vui-input/div[1]/div/div[1]/vui-input-number/div/div[1]"))
            )
            search_plusbet.click()
            print("Bet price increased.")

        is_crypto_idx_selected = True

    except TimeoutException as e:
        print(f"Timeout error: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")

@client.on(events.NewMessage(chats=channel_username))
async def my_event_handler(event):
    global current_pair, trade_direction, duration
    message_text = event.message.text

    if '💱**Currency pair: ' in message_text:
        pair_start_index = message_text.find('💱**Currency pair: ') + len('💱**Currency pair: ')
        pair_end_index = message_text.find('**', pair_start_index)
        current_pair = message_text[pair_start_index:pair_end_index]
        print(f'New message received: Current Pair - {current_pair}')

    if '📊**Trade direction: ' in message_text:
        trade_direction = re.search(r'📊\*\*Trade direction: (.*?)\*\*', message_text).group(1)
        trade_direction = re.sub(r'[^a-zA-Z]', '', trade_direction)
        print(f'New message received: Trade Direction - {trade_direction}')

    if '⏳**Duration: ' in message_text:
        start_index = message_text.find('⏳**Duration: ') + len('⏳**Duration: ')
        end_index = message_text.find('**', start_index)
        duration = message_text[start_index:end_index].strip()
        numeric_part = duration.split()[0]  # Split on whitespace and take the first part
        print(f'New message received: Duration - {numeric_part}')

        # Call perform_trade function after receiving the required messages
        await perform_trade()

async def perform_trade():
    global driver, is_logged_in, is_crypto_idx_selected

    try:
        if not is_logged_in or not is_crypto_idx_selected:
            await setup_browser()

        print("Starting trade execution...")
        
        # Search for time bar
        search_idx = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/div/div/binary-time-input/vui-input"))
        )
        search_idx.click()
        print("Clicked on the time bar.")

        # Increase the time
        time_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/div/div/binary-time-input/vui-input/div[1]/vui-popover/div[2]/platform-ui-scroll/div/div/div/div[1]/vui-option[5]"))
        )
        time_option.click()
        print("Selected time duration.")

        # Locate and click the appropriate trade arrow
        if trade_direction == "UP":
            uptime_arrow = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/binary-info/div[2]/div/trading-buttons/vui-button[1]"))
            )
            uptime_arrow.click()
            print("Clicked the uptime arrow.")
        elif trade_direction == "DOWN":
            downtime_arrow = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/binomo-root/platform-ui-scroll/div/div/ng-component/main/div/app-panel/ng-component/section/binary-info/div[2]/div/trading-buttons/vui-button[2]"))
            )
            downtime_arrow.click()
            print("Clicked the downtime arrow.")

        print("Trade placed successfully. Waiting for next signal.")
        
        # Handle unexpected alerts or pop-ups
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert.accept()
            print("Alert accepted.")
        except TimeoutException:
            pass  # No alert present
        print("Trade placed successfully. Waiting for next signal.")
        
    except TimeoutException as e:
        print(f"Timeout error during trade execution: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")
        is_logged_in = False
        is_crypto_idx_selected = False
    except NoSuchElementException as e:
        print(f"Element not found during trade execution: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")
        is_logged_in = False
        is_crypto_idx_selected = False
    except Exception as e:
        print(f"An unexpected error occurred during trade execution: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source: {driver.page_source}")
        is_logged_in = False
        is_crypto_idx_selected = False

async def main():
    try:
        await client.start(phone=phone_number)
        print('Telegram Client Created')
        await setup_browser()
        await client.run_until_disconnected()
    except asyncio.exceptions.IncompleteReadError as e:
        print(f'Error: {e}')
    finally:
        if driver:
            driver.quit()

# Function to keep the script running
def keep_alive():
    while True:
        time.sleep(20)  # Adjust the interval as needed

# Create a thread to keep the script running
alive_thread = threading.Thread(target=keep_alive)
alive_thread.start()

# Run the Telegram client
asyncio.run(main())



