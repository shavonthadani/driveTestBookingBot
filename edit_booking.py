from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import threading
import sys
import pyttsx3
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
city = 0
license_num = "edit this"

license_exp = "edit this"

def countdown():
    print("Countdown started")
    global timer
    timer = 2640
    for x in range(2640):
        timer = timer -1
        time.sleep(1)

def __main__():


    geckodriver_autoinstaller.install()

    profile = webdriver.FirefoxProfile(
        '/Users/shavonthadani/Library/Application Support/Firefox/Profiles/i4zlqd4a.Drivetest')

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0")
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    driver = webdriver.Firefox(firefox_profile=profile,
                               desired_capabilities=desired)
    driver.get("https://drivetest.ca/book-a-road-test/booking.html#/verify-driver")
    time.sleep(1)
    login(driver)
    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()
    rebook(driver)
    reschedule(driver)
    pickDate(driver,"August")
    #find_avail_days(driver)
    time.sleep(1000)
    return

def waitForPage(driver, delay,xpath):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
        driver.quit()

def login(driver):
    #driver.find_element_by_name("emailAddress").send_keys(email)
    #driver.find_element_by_name("confirmEmailAddress").send_keys(email)
    time.sleep(60)
    while True:
        try:
            driver.find_element_by_name("licenceNumber").send_keys(license_num)
            break
        except:
            time.sleep(5)
            print("still in queue")
            pass


    driver.find_element_by_name("licenceExpiryDate").send_keys(license_exp)
    time.sleep(1)
    driver.find_elements_by_id("regSubmitBtn")[0].click()

def rebook(driver):
    while True:
        if driver.current_url == "https://drivetest.ca/book-a-road-test/booking.html#/dashboard":
            break
        time.sleep(1)
    driver.execute_script("window.scrollTo(0, 500)")
    driver.implicitly_wait(5)
    driver.find_elements_by_class_name('btn-quaternary')[0].click()

def reschedule(driver):
    waitForPage(driver, 15,'//*[@title="reschedule"]')
    while True:
        if driver.current_url == "https://drivetest.ca/book-a-road-test/booking.html#/dashboard":
            try:
                element = driver.find_element_by_xpath('//*[@title="reschedule"]')
                webdriver.ActionChains(driver).move_to_element(element ).click(element ).perform()
            except:
                pass
        else:
            break


def pickDate(driver,month):
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(1)
    while True:
        try:
            driver.find_elements_by_class_name("btn-primary")[0].click()
            break
        except:
            pass
        #get months
    desired_month = int(datetime.datetime.strptime(month, "%B").month)
    current_month = int(datetime.datetime.now().strftime("%m"))

        #calculate month difference
    month_difference = month_diff(month)
    element = driver.find_element_by_xpath('//*[@title="next month"]')
    for month in range(month_difference +1):
        webdriver.ActionChains(driver).move_to_element(element ).click(element ).perform()
    find_avail_days(driver)

def find_avail_days(driver):
    waitForPage(driver, 30, '//*[@class="ap-resize0"]')
    while True:
        if timer <= 0:
            print("times up!")
            driver.quit()
            __main__()
        days = driver.find_elements_by_class_name("ap-resize0")
        for day in days:
            try:
                if day.value_of_css_property('color') == 'rgba(52, 152, 219, 1)':
                    print("found dates")
                    engine = pyttsx3.init()
                    engine.say("Found dates, found dates, found dates,found dates, found dates, found dates, found dates, found dates")
                    engine.runAndWait()
                    time.sleep(40)
                    break
            except:
                pass
        time.sleep(1)
        next_month = driver.find_element_by_xpath('//*[@title="next month"]')
        webdriver.ActionChains(driver).move_to_element(next_month ).click(next_month ).perform()
        time.sleep(1)
        previous_month = driver.find_element_by_xpath('//*[@title="previous month"]')
        webdriver.ActionChains(driver).move_to_element(previous_month ).click(previous_month ).perform()

def month_diff(month):
    #get months
    desired_month = int(datetime.datetime.strptime(month, "%B").month)
    current_month = int(datetime.datetime.now().strftime("%m"))
    #calculate month difference
    month_difference = desired_month - current_month
    if month_difference < 0:
        month_difference = 12 + month_difference
    return month_difference


__main__()
