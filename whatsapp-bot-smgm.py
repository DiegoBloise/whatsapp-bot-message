from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Elements XPATH
search_box_xpath = '/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]'
group_members_xpath = '/html/body/div[1]/div/div/div[5]/div/header/div[2]/div[2]/span'
pane_side_xpath = '//*[@id="pane-side"]'
send_button_xpath = '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'


def find_group(browser, group_name):
    elements = []
    try:
        print("Finding group...")
        for key in group_name:
            browser.find_element(By.XPATH, search_box_xpath).send_keys(key)
        sleep(1)
        elements = browser.find_element(By.XPATH, pane_side_xpath).find_elements(By.TAG_NAME, 'span')
        for element in elements:
            if element.text == group_name:
                print(f"Group found: {element.text}")
                return element
    except NoSuchElementException as e:
        print(f"Group element not found: {e}")
        browser.quit()
        exit()


def get_phones(browser, group):
    phones = []
    try:
        print("Getting phone list...")
        group.click()
        wait = WebDriverWait(browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, group_members_xpath), ", "))
        phones = browser.find_element(By.XPATH, group_members_xpath).text.split(', ')
        return phones
    except NoSuchElementException as e:
        print(f"Phones list element not found: {e}")
        browser.quit()
        exit()


def send_text(browser, phone, text):
    try:
        try:
            text = text.replace("\\n", "%0A")
            browser.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")
        except Exception as e:
            print(f"Could not send message: {e}")
            browser.quit()
            exit()
        print("Waiting to send the message...")
        wait = WebDriverWait(browser, 120)
        wait.until(EC.visibility_of_element_located((By.XPATH, send_button_xpath)))
        browser.find_element(By.XPATH, send_button_xpath).click()
        print(f"Message sent to phone: {phone}")
        #sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        browser.quit()
        exit()


def main():

    group_name = str(input("Enter the group name to search ~>> "))
    phones_to_exclude = str(input("\nEnter the 4 final numbers of all phones to exclude separated by spaces\nEx: XXXX XXXX XXXX\n~>> ")).split(" ")
    text = str(input("\nEnter text message (use \"\\n\" to write in another line)\nEx: First Line\\nSecond Line\n~>> "))

    print("Opening browser...")

    # initialize the browser
    try:
        browser = webdriver.Firefox()
    except Exception as e:
        print(f"Could not start the browser: {e}")
        exit()

    # navigate to WhatsApp Web
    try:
        browser.get("https://web.whatsapp.com/")
    except Exception as e:
        print(f"Could not open WhatsAppWeb: {e}")
        browser.quit()
        exit()

    # wait for QR code get scanned
    print("Scan the QR code to log in...")
    wait = WebDriverWait(browser, 120)
    wait.until(EC.visibility_of_element_located((By.ID, 'pane-side')))

    print("Success...")

    group = find_group(browser, group_name)
    phones = get_phones(browser, group)

    print(f"Total of members: {len(phones)}")

    # send the text message to all contacts extracted from the group
    for i, phone in enumerate(phones):
        print(f"{i+1}º - {phone}")
        if phone not in phones_to_exclude:
            send_text(browser, phone, text)

    # close the browser
    browser.quit()

    print("All done!")

main()
