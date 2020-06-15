import sys
import time
import os
import subprocess
import selenium
from selenium import  webdriver
from bs4 import BeautifulSoup
from datetime import  datetime

url_to_refresh = "https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1"
url_to_signin = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
url_to_cart = "https://www.amazon.com/cart/localmarket"

#ENTER AMAZON EMAIL AND PASSWORD HERE
login_email = ""
login_password = ""

unavailable_text = "No delivery windows available"
available_texts = ["Next available", "1-hour delivery windows", "2-hour delivery windows"]

#DEFAULT CREDIT CARD SELECTION
defaultCC = "/html/body/div[5]/div[1]/div[2]/div[2]/div[4]/div/form/div[2]/div/div/div[1]/div[3]"

browser = webdriver.Safari(executable_path = '/usr/bin/safaridriver')

def open_browser():
    browser.fullscreen_window()
    browser.get(url_to_signin)
    time.sleep(1.0)
    signin()

def signin():
    browser.find_element_by_id("ap_email").send_keys(login_email)
    browser.find_element_by_id("continue").click()
    time.sleep(2)
    browser.find_element_by_name("rememberMe").click()
    browser.find_element_by_id("ap_password").send_keys(login_password)
    browser.find_element_by_id("auth-signin-button").click()
    time.sleep(17)
    to_cart_until_slots()

def to_cart_until_slots():
    browser.get(url_to_cart)
    time.sleep(2.0)
    browser.find_element_by_class_name("a-button-input").click()
    time.sleep(5.0)
    browser.find_element_by_class_name("a-button-inner").click()
    time.sleep(4.0)
    check_for_slots()

def check_for_slots():
    slot_open = False
    while not slot_open:
        browser.get(url_to_refresh)
        time.sleep(5.0)
        html_page = browser.page_source
        soup = BeautifulSoup(html_page, 'html.parser')

        try:
            immediate_available = str([x.text for x in soup.findAll('h4', class_ ='ufss-slotgroup-heading-text a-text-normal')])
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            if "Next available" in immediate_available:
                print("available :)", current_time)
                slot_open = True
                autoCheckout()
            else:
                print("no luck :(", current_time)
        except AttributeError:
            print("no dice :(")

        time.sleep(15.0)


def autoCheckout():
   try:
      slot_select_button = browser.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button')
      slot_select_button.click()
      send_text_slot_opened_and_selected()

      print("Clicked open slot")
   except NoSuchElementException:
      try:
         slot_select_button = browser.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[4]/div/div/ul/li/span/span/div/div[2]/span/span/button')
         slot_select_button.click()
         send_text_slot_opened_and_selected()
      except NoSuchElementException:
         print("Found a slot but it got taken, run script again.")
         os.system('say "Found a slot but it got taken, run script again."')

   try:
      slot_continue_button = browser.find_element_by_xpath('//*[@id="shipoption-select"]/div/div/div/div/div[2]/div[3]/div/span/span/span/input')
      slot_continue_button.click()
      print("Selected slot and continued to next page")
   except NoSuchElementException:
      slot_continue_button = browser.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div[3]/div/span/span/span/input')
      slot_continue_button.click()
      print("Selected slot and continued to next page")

   try:
      time.sleep(6)
      is_out_of_stock = browser.find_element_by_xpath('//*[@id="changeQuantityFormId"]/div[3]/div/h4')
      outofstock_select_continue = browser.find_element_by_css_selector('[class="a-button-text"]')
      outofstock_select_continue.click()
      print("Passed out of stock")
   except NoSuchElementException:
      pass

   try:
      time.sleep(6)
      payment_select_continue = browser.find_element_by_xpath('//*[@id="continue-top"]')
      payment_select_continue.click()
      print("Payment method selected")

      time.sleep(6)
      try:
         review_select_continue = browser.find_element_by_xpath('//*[@id="placeYourOrder"]/span/input')
         review_select_continue.click()
         print("Order reviewed")
      except NoSuchElementException:
         review_select_continue = browser.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/form/div/div/div/div[2]/div/div[1]/div/div[1]/div/span/span/input')
         review_select_continue.click()
         print("Order reviewed")

      send_text_order_almost_placed()
      print("Order Placed!")
      os.system('say "Order Placed!"')
   except NoSuchElementException:
      print("Found a slot but it got taken, run script again.")
      os.system('say "Found a slot but it got taken, run script again."')
      time.sleep(1400)


def checkout():
    browser.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button').click()
    send_text_slot_opened_and_selected()
    time.sleep(1.5)
    browser.find_element_by_xpath('//*[@id="shipoption-select"]/div/div/div/div/div[2]/div[3]/div/span/span/span/input').click()
    time.sleep(1.5)
    browser.find_element_by_id("continue-top").click()
    placeorder()


def placeorder():
    send_text_order_almost_placed()
    time.sleep(3.0)
    browser.find_element_by_id("placeYourOrder")
    time.sleep(10.0)
    browser.quit()

def send_text_slot_opened_and_selected():
    #ENTER PHONE NUMBER HERE
    os.system("osascript sendmessage.scpt 1234567890 'SLOT OPENED & SELECTED'")

def send_text_order_almost_placed():
    #ENTER PHONE NUMBER HERE
    os.system("osascript sendmessage.scpt 1234567890 'ORDER ABOUT TO BE PLACED IN < 10seconds'")

def main():
    open_browser()

if __name__ == '__main__':
    main()



