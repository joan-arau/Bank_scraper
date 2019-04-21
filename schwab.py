import config
from   selenium import webdriver
from   selenium.webdriver.common.by import By
import time
import datetime
now = datetime.date.today().strftime(" %B %d %Y")
from selenium.webdriver.chrome.options import Options
import os

path = config.db_path
LOGIN = config.schwab_cred['login']
PASSWORD = config.schwab_cred['password']

def get_balance():
    options = Options()


    # options.add_argument("headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=600,800")

    browser = webdriver.Chrome(executable_path=r'/Users/joanarau-schweizer/PycharmProjects/stockbot/chromedriver 10.15.44 pm',options=options)


    ### Login
    LOGIN_URL = 'https://www.schwab.com/public/schwab/nn/login/mobile-login.html&lang=en'
    browser.get(LOGIN_URL)
    browser.switch_to.frame('mobile-login')
    username = browser.find_element_by_id('LoginId')
    password = browser.find_element_by_id('Password')
    username.send_keys(LOGIN)
    password.send_keys(PASSWORD)
    browser.find_element_by_id('RememberLoginId').click()
    browser.find_element_by_id('Submit').click()

    # Wait until login is done... (is AJAX login)
    while  browser.current_url == LOGIN_URL:
      print('waiting...')
      time.sleep(0.1)



    print(browser.current_url)

    time.sleep(5)

    element = browser.find_element(By.XPATH,'/html/body/div[3]/div[1]/span[2]/a').click()
    element = browser.find_element(By.XPATH,'//*[@id="accounts_summary"]/div[3]/div[1]/div/ul/li/div/div/div[2]/div[1]')
    print(element.text)

    value = element.text
    browser.quit()
    return value
value = get_balance()
fields=[now,value]

PATH=os.path.join(path,'portfolio_value.csv')
print(PATH)

def line_prepender(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(fields[0])+','+str(fields[1]).replace(',','').strip('$') + '\n' + content)

line_prepender(PATH,fields)





