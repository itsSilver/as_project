# coding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def get_bet365_url(sports, ranks):
    urls0 = "https://www.bet365.com/en/"
    urls1 = "https://www.bet365.com/#/IP/"
    driver = webdriver.Chrome()
    driver.get(urls0)
    driver.get(urls1)    
    ranks1 = ranks.split(" - ")[0]
    time.sleep(5)
    xpath_str = "//div[text()='%s']"%sports
    ac = driver.find_element_by_xpath(xpath_str)
    ActionChains(driver).move_to_element(ac).click(ac).perform()
    ac1 = driver.find_element_by_xpath(u"//span[text()='%s']"%ranks1)
    ActionChains(driver).move_to_element(ac1).click(ac1).perform()

    cookies = driver.get_cookies()
    cookies_str = ""
    for co in cookies:
        for c in co.items():
            cookies_str += "%s=%s;"%(str(c[0]), str(c[1]))
    time.sleep(10);
    driver.quit()
    url_cookie = {}
    url_cookie['urls'] = urls1
    url_cookie['cookie'] = cookies_str
    return url_cookie 
