from time import sleep
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def protocol(url):
    """
    returns communication protocol specified in the url
    e.g. : returns "https" if specified url is https://youtube.com
    """
    return url.split('://')[0]

def domain_name(url):
    """
    returns domain name specified in the url
    e.g. : returns "youtube.com" if specified url is https://youtube.com
    """
    try:
        domain_results = __sub_domain_name(url).split('.')
        return domain_results[-2] + '.' + domain_results[-1]
    except:
        return None

def __sub_domain_name(url):
    """
    returns network path specified in the url
    e.g. : returns "www.youtube.com" if specified url is https://www.youtube.com
    """
    try:
        return urlparse(url).netloc
    except:
        return None

def start(url, wait_seconds_after_launch=10):
    """
    1. Starts a browser session with specified url
    2. Launches the specified url page
    3. Waits in the state for seconds specified in "wait_seconds_after_launch"
    4. Returns the driver object of browser sesssion
    """
    # start a new browser session
    browser_driver = webdriver.Safari()

    # launch the url
    browser_driver.get(url)

    # maximize the browser window
    browser_driver.maximize_window()

    # keep the session open for x seconds
    sleep(wait_seconds_after_launch)

    # return the web driver
    return browser_driver

def stop(browser_driver):
    """
    Stops the specified browser session
    """
    # close the browser session
    browser_driver.close()

def get_hyper_links(url):
    """
    Returns a list of hyper links in specified url as dictionary
    Items in dictionary represent each hyper link with
    Key : Link text
    Value : Hyper Link
    """
    hyper_links = {}
    page_source = requests.get(url)
    page_source_text = page_source.text
    soup = BeautifulSoup(page_source_text, features="lxml")
    for link in soup.find_all('a'):
        text = link.text
        href_sub = link.get('href')
        if href_sub:
            if domain_name(url) != domain_name(href_sub):
                href = url + href_sub
            else:
                url = protocol(url) + '://' + href_sub
            if text:
                text = text.strip()
                hyper_links[text] = href
            else:
                hyper_links['No Link Text'] = href
        else:
            text = text.strip()
            hyper_links[text] = 'No link'
    return hyper_links

def screen_shot(browser_driver, output_file):
    """
    Saves screen shot of current browser state with specified output file name
    """
    browser_driver.save_screenshot(output_file)