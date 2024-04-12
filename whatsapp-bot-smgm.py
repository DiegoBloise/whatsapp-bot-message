import pyautogui
from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# Elements XPATH
initial_startup = "wa_web_initial_startup"
qr_code_xpath = "/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas"
search_box_xpath = "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]"
group_members_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div[2]/span"
contact_info_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div/div/div/span"
contact_phone_xpath = "/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[2]/div/span/span"
business_phone_xpath = "/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[3]/div/div/span/span"
send_button_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"

def find_subject(browser, subject_name):
    try:
        print("\x1b[1m[*]\x1b[m \x1b[33mSearching subject...\x1b[m")

        """ search_box = browser.find_element(By.XPATH, search_box_xpath)

        search_box.send_keys(Keys.CONTROL + "a" + Keys.DELETE)

        for key in subject_name:
            search_box.send_keys(key)
            sleep(0.1)

        sleep(1)
        search_box.send_keys(Keys.ARROW_DOWN)
        sleep(1) """

        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/header").click()

        sleep(10)

        pyautogui.press('tab', presses=7)

        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('delete')

        sleep(3)

        for key in subject_name:
            pyautogui.press(key)
            sleep(0.1)

        sleep(1)
        pyautogui.press('down')
        sleep(1)

        return

    except NoSuchElementException as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mSubject element not found: {e}\x1b[m")
        input()
        browser.quit()
        exit()


def get_phones(browser):
    try:
        print("\x1b[1m[*]\x1b[m \x1b[33mGetting phone list...\x1b[m")

        wait = WebDriverWait(browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, group_members_xpath), ", "))

        subjects = browser.find_element(By.XPATH, group_members_xpath).text.split(", ")
        for index, subject in enumerate(subjects):
            if not subject.replace("+", "").replace(" ", "").replace("-", "").isnumeric():
                print(f"\x1b[1m[*]\x1b[m \x1b[33mSaved contact found:\x1b[m \x1b[1m{subject}\x1b[m")
                print("\x1b[1m[*]\x1b[m \x1b[33mExtracting phone number...\x1b[m")

                find_subject(browser, subject)
                phone_number = get_phone_number(browser)
                print(f"\x1b[1m[+]\x1b[m \x1b[1;32mSuccess... | Phone: {phone_number}\x1b[m")

                subjects[index] = phone_number

        return subjects

    except NoSuchElementException as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mPhones list element not found: {e}\x1b[m")
        browser.quit()
        exit()


def get_phone_number(browser):
    try:
        browser.find_element(By.XPATH, contact_info_xpath).click()
        sleep(2)

    except NoSuchElementException as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mContact info element not found: {e}\x1b[m")
        browser.quit()
        exit()

    try:
        phone = browser.find_element(By.XPATH, contact_phone_xpath).text

    except:
        print(f"\x1b[1m[*]\x1b[m \x1b[33mNumber not found: It's a business account\x1b[m")

        try:
            phone = browser.find_element(By.XPATH, business_phone_xpath).text

        except NoSuchElementException as e:
            print(f"\x1b[1m[!]\x1b[m \x1b[1;31mNumber not found: {e}\x1b[m")
            browser.quit()
            exit()

    return phone


def send_text(browser, phone, text):
    try:
        try:
            text = text.replace("\\n", "%0A")
            browser.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")

        except Exception as e:
            print(f"\x1b[1m[!]\x1b[m \x1b[1;31mCould not send message: {e}\x1b[m")
            browser.quit()
            exit()
        print("\x1b[1m[*]\x1b[m \x1b[33mWaiting to send the message...\x1b[m")

        wait = WebDriverWait(browser, 30)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
        send_button = browser.find_element(By.XPATH, send_button_xpath)

        sleep(3)
        send_button.click()

        print(f"\x1b[1m[+]\x1b[m \x1b[1;32mMessage sent to phone: {phone}\x1b[m")
        sleep(2)
    except Exception as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mError: {e}\x1b[m")
        browser.quit()
        exit()


def banner():
    system("cls")
    print("\n{:.^75}".format("\x1b[37;4mhttps://github.com/DiegoBloise\x1b[0m"))
    print("\x1b[1;32m")
    print("-="*32)
    print()
    print(f"{'WhatsApp-Bot - Send Message to Group Members':^64}")
    print()
    print("-="*32)
    print("\x1b[m")


def main():
    banner()

    group_name = str(input("\nEnter the group name to search \x1b[1;32m~>>\x1b[m ")).lower()
    phones_to_exclude = str(input("\nEnter the 4 final numbers of all phones\nyou want to exclude separated by spaces\nEx: XXXX XXXX XXXX\n\x1b[1;32m~>>\x1b[m ")).split(" ")
    text = str(input("\nEnter text message (use \"\\n\" to write in another line)\nEx: First Line\\nSecond Line\n\x1b[1;32m~>>\x1b[m "))

    options = Options()
    options.add_argument("window-size=800,600")
    options.add_argument("--headless")

    print("\x1b[1;32m")
    print("-="*32)
    print("\x1b[m")

    print("\x1b[1m[*]\x1b[m \x1b[33mStarting WebDriver...\x1b[m")
    try:
        browser = webdriver.Firefox(options=options)
    except Exception as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mCould not start the WebDriver: {e}\x1b[m")
        exit()

    print("\x1b[1m[*]\x1b[m \x1b[33mAcessing WhatsAppWeb...\x1b[m")
    try:
        browser.get("https://web.whatsapp.com/")
    except Exception as e:
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31mCould not access WhatsAppWeb: {e}\x1b[m")
        browser.quit()
        exit()

    wait = WebDriverWait(browser, 120)
    wait.until(EC.visibility_of_element_located((By.ID, initial_startup)))

    print("\x1b[1m[*]\x1b[m \x1b[33mLoading QR Code...\x1b[m")
    wait.until(EC.visibility_of_element_located((By.XPATH, qr_code_xpath)))

    print("\x1b[1m[+]\x1b[m \x1b[1;32mScan the QR code to continue...\x1b[m")
    browser.find_element(By.CLASS_NAME, "landing-main").screenshot("qrcode.png")
    system("qrcode.png")

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "landing-main")))
    system("del qrcode.png")
    window = pyautogui.getWindowsWithTitle("qrcode.png")[0]
    window.activate()
    pyautogui.hotkey('alt', 'f4')

    print("\x1b[1m[*]\x1b[m \x1b[33mLoading...\x1b[m")
    wait.until(EC.visibility_of_element_located((By.ID, "pane-side")))

    print("\x1b[1m[+]\x1b[m \x1b[1;32mSuccess...\x1b[m")
    sleep(2)

    find_subject(browser, group_name)
    phones = get_phones(browser)

    print(f"\x1b[1m[*]\x1b[m \x1b[33mTotal of members: {len(phones)}\x1b[m")

    print("\x1b[1;33m")
    print("-="*32)
    print("\x1b[m")
    print("\x1b[1m[!]\x1b[m \x1b[1;31mAre you sure you want to send\n    the following message?:\n\x1b[m")
    print(text.replace("\\n", "\n"))
    print("\x1b[1;33m")
    print("-="*32)
    print("\x1b[m")

    if input("\x1b[1m[Y/N] \x1b[1;32m~>> \x1b[m").lower() in 'y':
        print("\n\n")

        for i, phone in enumerate(phones):
            if phone[-4:] not in phones_to_exclude:
                print(f"\x1b[1m[+]\x1b[m \x1b[1;33mSending Message to {i+1}º : {phone}\x1b[m")
                send_text(browser, phone, text)
    else:
        print("\x1b[1m[!]\x1b[m \x1b[1;31mAborted by user.\n\x1b[m")

    browser.quit()

    print("\x1b[1m[+]\x1b[m \x1b[1;32mAll done!\x1b[m")
    system("pause")


main()
