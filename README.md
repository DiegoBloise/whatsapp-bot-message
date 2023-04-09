# Whatsapp Bot - Send Messages to Group Members

This script uses the Selenium webdriver to extract phone numbers of members from a WhatsApp group. It opens a WhatsApp Web instance in your default browser, asks you to log in, and then takes a group name as input to extract the phone numbers of all the members in that group.

## Installation

  1. Install Python ( https://www.python.org/downloads/ )
  2. Install Selenium using pip: `pip install selenium`

## Usage
  1. Run the script `whatsapp-bot-smgm.py`
  2. Enter the name of the group from which you want to extract members' phone numbers.
  3. Enter the phone numbers you want to exclude to avoid sending them messages.
  4. Enter the message you want to send.
  5. Log in to your WhatsApp Web account when prompted.
  6. Wait for the script to extract all phone numbers.
  7. When the extraction is complete, the script will print all the phone numbers in the console.
  8. The message will be sent to all members of the group except those you have excluded.

Note: Please make sure that you have the latest version of Firefox installed on your system. You can download it from https://www.mozilla.org/en-US/firefox/new/

## Caution

This script is meant for educational purposes only. Misuse of this script can lead to legal issues. Use it at your own risk.
