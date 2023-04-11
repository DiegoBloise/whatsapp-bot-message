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
search_box_xpath = "/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]"
group_members_xpath = "/html/body/div[1]/div/div/div[5]/div/header/div[2]/div[2]/span"
send_button_xpath = "/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"
contact_info_xpath = "/html/body/div[1]/div/div/div[5]/div/header/div[2]"
contact_phone_xpath = "/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div/span/span"
business_phone_xpath = "/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[3]/div/div/span/span"


def find_subject(browser, subject_name):
    try:
        print("\033[1m[*]\033[m \033[33mSearching subject...\033[m")

        search_box = browser.find_element(By.XPATH, search_box_xpath)

        search_box.send_keys(Keys.CONTROL + "a" + Keys.DELETE)

        for key in subject_name:
            search_box.send_keys(key)
            sleep(0.1)

        sleep(3)

        search_box.send_keys(Keys.ARROW_DOWN)
        sleep(1)

        return

    except NoSuchElementException as e:
        print(f"\033[1m[!]\033[m \033[1;31mSubject element not found: {e}\033[m")
        input()
        browser.quit()
        exit()


def get_phones(browser):
    try:
        print("\033[1m[*]\033[m \033[33mGetting phone list...\033[m")

        wait = WebDriverWait(browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, group_members_xpath), ", "))

        subjects = browser.find_element(By.XPATH, group_members_xpath).text.split(", ")
        for index, subject in enumerate(subjects):
            if not subject.replace("+", "").replace(" ", "").replace("-", "").isnumeric():
                print(f"\033[1m[*]\033[m \033[33mSaved contact found: \033[1;30m{subject}\033[m")
                print("\033[1m[*]\033[m \033[33mExtracting phone number...\033[m")

                find_subject(browser, subject)
                phone_number = get_phone_number(browser)
                print(f"\033[1m[+]\033[m \033[1;32mSuccess... | Phone: {phone_number}\033[m")

                subjects[index] = phone_number

        return subjects

    except NoSuchElementException as e:
        print(f"\033[1m[!]\033[m \033[1;31mPhones list element not found: {e}\033[m")
        browser.quit()
        exit()


def get_phone_number(browser):
    try:
        browser.find_element(By.XPATH, contact_info_xpath).click()
        sleep(2)

    except NoSuchElementException as e:
        print(f"\033[1m[!]\033[m \033[1;31mContact info element not found: {e}\033[m")
        browser.quit()
        exit()

    try:
        phone = browser.find_element(By.XPATH, contact_phone_xpath).text

    except:
        print(f"\033[1m[*]\033[m \033[33mNumber not found: It's a business account\033[m")

        try:
            phone = browser.find_element(By.XPATH, business_phone_xpath).text

        except NoSuchElementException as e:
            print(f"\033[1m[!]\033[m \033[1;31mNumber not found: {e}\033[m")
            browser.quit()
            exit()

    return phone


def send_text(browser, phone, text):
    try:
        try:
            text = text.replace("\\n", "%0A")
            browser.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")

        except Exception as e:
            print(f"\033[1m[!]\033[m \033[1;31mCould not send message: {e}\033[m")
            browser.quit()
            exit()
        print("\033[1m[*]\033[m \033[33mWaiting to send the message...\033[m")

        wait = WebDriverWait(browser, 120)
        wait.until(EC.visibility_of_element_located((By.XPATH, send_button_xpath)))

        browser.find_element(By.XPATH, send_button_xpath).click()
        print(f"\033[1m[+]\033[m \033[1;32mMessage sent to phone: {phone}\033[m")
        #sleep(1)
    except Exception as e:
        print(f"\033[1m[!]\033[m \033[1;31mError: {e}\033[m")
        browser.quit()
        exit()


def banner():
    print("\033[1;32m")
    print("-="*25)
    print()
    print(f"{'WhatsApp-Bot - Send Message to Group Members':^50}")
    print()
    print("-="*25)
    print("\033[m")


def main():
    banner()

    group_name = str(input("\nEnter the group name to search \033[1;32m~>>\033[m ")).lower()
    phones_to_exclude = str(input("\nEnter the 4 final numbers of all phones to exclude separated by spaces\nEx: XXXX XXXX XXXX\n\033[1;32m~>>\033[m ")).split(" ")
    text = str(input("\nEnter text message (use \"\\n\" to write in another line)\nEx: First Line\\nSecond Line\n\033[1;32m~>>\033[m "))

    options = Options()
    options.add_argument("window-size=800,600")
    options.add_argument("--headless")

    print("\033[1;32m")
    print("-="*25)
    print("\033[m")

    print("\033[1m[*]\033[m \033[33mStarting WebDriver...\033[m")
    try:
        browser = webdriver.Firefox(options=options)
    except Exception as e:
        print(f"\033[1m[!]\033[m \033[1;31mCould not start the WebDriver: {e}\033[m")
        exit()

    print("\033[1m[*]\033[m \033[33mAcessing WhatsAppWeb...\033[m")
    try:
        browser.get("https://web.whatsapp.com/")
    except Exception as e:
        print(f"\033[1m[!]\033[m \033[1;31mCould not access WhatsAppWeb: {e}\033[m")
        browser.quit()
        exit()

    wait = WebDriverWait(browser, 120)
    wait.until(EC.visibility_of_element_located((By.ID, "initial_startup")))

    print("\033[1m[*]\033[m \033[33mLoading QR Code...\033[m")
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "canvas")))

    print("\033[1m[+]\033[m \033[1;32mScan the QR code to continue...\033[m")
    browser.find_element(By.CLASS_NAME, "landing-main").screenshot("qrcode.png")
    system("qrcode.png")

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "landing-main")))
    system("del qrcode.png")

    print("\033[1m[*]\033[m \033[33mLoading...\033[m")
    wait.until(EC.visibility_of_element_located((By.ID, "pane-side")))

    print("\033[1m[+]\033[m \033[1;32mSuccess...\033[m")
    sleep(3)

    find_subject(browser, group_name)
    phones = get_phones(browser)

    print(f"\033[1m[*]\033[m \033[33mTotal of members: {len(phones)}\033[m")

    print("\033[1;33m")
    print("-="*25)
    print("\033[m")
    print("\033[1m[!]\033[m \033[1;31mAre you sure you want to send the following message?:\n\033[m")
    print(text.replace("\\n", "\n"))
    print("\033[1;33m")
    print("-="*25)
    print("\033[m")

    q = input("\033[1;32m[Y/N] ~>> \033[m").lower()
    if q == 'y':
        for i, phone in enumerate(phones):
            if phone[-4:] not in phones_to_exclude:
                print(f"\033[1m[+]\033[m \033[1;32mSending Message to {i+1}º : {phone}\033[m")
                send_text(browser, phone, text)
    else:
        print("\033[1m[!]\033[m \033[1;31mAborted by user.\n\033[m")

    browser.quit()

    print("\033[1m[+]\033[m \033[1;32mAll done!\033[m")


main()
