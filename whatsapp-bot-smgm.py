from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# Elements XPATH
group_info_xpath = '/html/body/div[1]/div/div/div[5]/div/header/div[2]/div[1]'
contacts_list_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[1]/div/div/div[1]'
contacts_box_xpath = '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div/div[2]'
contacts_header_xpath = '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div/header'
contact_chat_xpath = '/html/body/div[1]/div/span[4]/div/ul/div/li[4]'
contact_info_xpath = '/html/body/div[1]/div/div/div[5]/div/header/div[2]'
contact_phone_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div/span/span'
business_phone_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[3]/div/div/span/span'
number_of_members_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[1]/div/div/div[1]/span'
group_admin_marker_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[6]/div[2]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[2]/div'
close_info_button_xpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/header/div/div[1]/div'
send_button_xpath = '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'


def find_group(browser, group_name):
    elements = []
    try:
        print("Finding group...")
        elements = browser.find_elements(By.TAG_NAME, 'span')
        for element in elements:
            if element.get_attribute("title") == group_name:
                print(f"Group found: {element.text}")
                return element
    except NoSuchElementException as e:
        print(f"Group element not found: {e}")
        browser.quit()
        exit()


def create_phone_list(browser, group, number_of_members):
    phones = []
    get_contacts(browser, group)
    for index in range(number_of_members):
        next_contact(browser, index)
        if (show_contact_chat(browser)):
            show_contact_info(browser)
            phones.append(get_phone_number(browser))
            get_contacts(browser, group)
    return phones


def get_contacts(browser, group):
    group.click()
    sleep(1)
    show_group_info(browser)
    show_contacts_list(browser)


def show_group_info(browser):
    try:
        browser.find_element(By.XPATH, group_info_xpath).click()
        sleep(1)
    except NoSuchElementException as e:
        print(f"Group info element not found: {e}")
        browser.quit()
        exit()


def show_contacts_list(browser):
    try:
        browser.find_element(By.XPATH, contacts_list_xpath).click()
        sleep(1)
    except NoSuchElementException as e:
        print(f"Contacts list element not found: {e}")
        browser.quit()
        exit()


def get_number_of_members(browser, group):
    group.click()
    show_group_info(browser)
    try:
        number_of_members = int(group.find_element(By.XPATH, number_of_members_xpath).text[0])
        print(f"Number of members: {number_of_members}")
    except NoSuchElementException as e:
        print(f"Number of members element not found: {e}")
        browser.quit()
        exit()
    try:
        browser.find_element(By.XPATH, close_info_button_xpath).click()
    except NoSuchElementException as e:
        print(f"Close button element not found: {e}")
        browser.quit()
        exit()
    return number_of_members


def next_contact(browser, index):
    elements = []
    try:
        print("Finding contacts...")
        elements = browser.find_element(By.XPATH, contacts_box_xpath).find_elements(By.TAG_NAME, 'div')
        for element in elements:
            if element.get_attribute('data-testid') and element.get_attribute('data-testid') == f"list-item-{index}":
                print(f"Contact: {element.find_element(By.TAG_NAME, 'span').text}")
                element.click()
                sleep(1)
    except NoSuchElementException as e:
        print(f"Contacts not found: {e}")
        browser.quit()
        exit()


def show_contact_chat(browser):
    try:
        browser.find_element(By.XPATH, contact_chat_xpath).click()
        sleep(1)
        return True
    except NoSuchElementException as e:
        print(f"Trying to message yourself, skipping...")
        try:
            browser.find_element(By.XPATH, contacts_header_xpath).click()
            sleep(1)
            return False
        except NoSuchElementException as e:
            print(f"Contact chat element not found: {e}")
            browser.quit()
            exit()


def show_contact_info(browser):
    try:
        browser.find_element(By.XPATH, contact_info_xpath).click()
        sleep(1)
    except NoSuchElementException as e:
        print(f"Contact info element not found: {e}")
        browser.quit()
        exit()


def get_phone_number(browser):
    try:
        phone = browser.find_element(By.XPATH, contact_phone_xpath).text
    except:
        print(f"Number not found, may be is a business account")
        try:
            phone = browser.find_element(By.XPATH, business_phone_xpath).text
        except NoSuchElementException as e:
            print(f"Number not found: {e}")
            browser.quit()
            exit()
    print(f"Phone: {phone}")
    return phone


def send_text(browser, phone, text):
    try:
        try:
            browser.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")
        except Exception as e:
            print(f"Could not send message: {e}")
            browser.quit()
            exit()
        while len(browser.find_elements(By.XPATH, send_button_xpath)) < 1:
            print("Waiting to send the message...")
            sleep(3)
        browser.find_element(By.XPATH, send_button_xpath).click()
        print("Message sent.")
        sleep(3)
    except Exception as e:
        print(f"Error: {e}")
        browser.quit()
        exit()


def main():

    group_name = str(input("Enter group name: "))
    text = str(input("Enter message: "))
    phones = []

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
    while len(browser.find_elements(By.ID, 'pane-side')) < 1:
        print("Scan the QR code to log in...")
        sleep(3)

    print("Success...")

    sleep(3)

    group = find_group(browser, group_name)
    phones = create_phone_list(browser, group, get_number_of_members(browser, group))

    print(phones)

    # send the text message to all contacts extracted from the group
    for phone in phones:
        send_text(browser, phone, text)

    print("All done!")

    # close the browser
    browser.quit()


main()
