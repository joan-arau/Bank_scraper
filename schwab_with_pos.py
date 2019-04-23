import config
from   selenium import webdriver
from   selenium.webdriver.common.by import By
import time
import datetime
now = datetime.date.today().strftime(" %B %d %Y")
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import glob
import shutil
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



    time.sleep(5)

    element = browser.find_element(By.XPATH,'/html/body/div[3]/div[1]/span[2]/a').click()
    element = browser.find_element(By.XPATH,'//*[@id="accounts_summary"]/div[3]/div[1]/div/ul/li/div/div/div[2]/div[1]')
    print(element.text)
    value = element.text
    element = browser.find_element(By.XPATH, '// *[ @ id = "btn-menu"]').click()
    time.sleep(0.5)
    element = browser.find_element(By.XPATH, '// *[ @ id = "lnkFullSite"]').click()
    time.sleep(1)
    browser.get("https://client.schwab.com/secure/cc/accounts/positions")
    time.sleep(1)
    window_before = browser.window_handles[0]
    element = browser.find_element(By.XPATH, '//*[@id="exportLink"]').click()
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)
    time.sleep(1)
    element = browser.find_element(By.XPATH, '// *[ @ id = "ctl00_WebPartManager1_wpExportDisclaimer_ExportDisclaimer_btnOk"]').click()
    time.sleep(5)
    print("done")

    browser.quit()
    return value
value = get_balance()
fields=[now,value]

PATH=os.path.join(path,'portfolio_value.csv')

def line_prepender(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(fields[0])+','+str(fields[1]).replace(',','').strip('$') + '\n' + content)


def file_mover(download_folder,destination):

    list_of_files = glob.glob(os.path.join(download_folder,'*.CSV'))  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    name = latest_file.split('/')[-1]
    shutil.move(latest_file, os.path.join(destination,name))
# line_prepender(PATH,fields)
file_mover('/Users/joanarau-schweizer/Downloads',path)





