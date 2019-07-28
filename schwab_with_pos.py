import config
from   selenium import webdriver
from   selenium.webdriver.common.by import By
import time
import datetime
import twilio_msgr as message

now = datetime.date.today().strftime('%Y-%m-%d')

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import glob
import shutil
import pandas as pd

downloads = config.downloads
chromedriver = config.chromedriver
path = os.path.join(config.db_path,'schwab')
LOGIN = config.schwab_cred['login']
PASSWORD = config.schwab_cred['password']
pd.set_option('display.max_columns', 500)
def get_balance():
    options = Options()

    browser = webdriver.Chrome(executable_path=chromedriver,options=options)


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

    # Wait until login is done...
    while  browser.current_url == LOGIN_URL:
      print('waiting...')
      time.sleep(0.1)



    time.sleep(5)

    # check if login was successful, else quit
    try:
        element = browser.find_element(By.XPATH,'/html/body/div[3]/div[1]/span[2]/a').click()
    except:
        browser.quit()
        message.send('Schwab Login Failed')
        exit()
    time.sleep(3)
    element = browser.find_element(By.XPATH,'//*[@id="accounts_summary"]/div[3]/div[1]/div/ul/li/div/div/div[2]/div[1]')
    value = element.text

    element = browser.find_element(By.XPATH,'//*[@id="accounts_summary"]/div[3]/div[1]/div/ul/li/div/div/div[1]/div[1]').click()
    time.sleep(5)
    element = browser.find_element(By.CSS_SELECTOR,'#collapseEquity_7 > li > div > div:nth-child(2) > div.h5.nowrap')
    cash = element.text


    value = float(value.replace("$","").replace(",",""))
    cash = float(cash.replace("$", "").replace(",",""))


    mkt_vl = value - cash
    print('total: ',value,'market_vl: ',mkt_vl,'cash: ',cash)

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
    time.sleep(2)
    element = browser.find_element(By.XPATH, '// *[ @ id = "ctl00_WebPartManager1_wpExportDisclaimer_ExportDisclaimer_btnOk"]').click()
    time.sleep(5)


    print("done")
    #browser.close()
    browser.quit()
    return value, mkt_vl,cash
value = get_balance()
print(value)
fields2=[now,value[0],1,int('54816757'),value[1],value[2],'USD',]

# fields=[now,float('10000.05'),int('1'),int('54816757'),float('10000.05'),float('5000.05'),'USD']
print(fields2)
PATH=os.path.join(path,'portfolio_value.csv')

def line_prepender(filename,fields):


    df = pd.DataFrame.from_csv(os.path.join(config.db_path, 'mysql_db_csv/portfolio_value/','54816757.csv'))
    print(df.tail())
    new_row=pd.DataFrame([[fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6]]],columns=['Date','total_value','broker_id','account_number','portfolio_value','cash','currency'])
    new_row=new_row.reset_index(drop=True)
    df=df.reset_index()
    print(new_row)
    df=df.append(new_row.reset_index(drop=True))

    df=df.reset_index(drop=True)
    df['entry']=0
    print(df.tail(10))
    df.to_csv(os.path.join(config.db_path, 'mysql_db_csv/portfolio_value/','54816757.csv'), index=False)



def file_mover(download_folder,destination):

    list_of_files = glob.glob(os.path.join(download_folder,'*.CSV'))  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    name = latest_file.split('/')[-1]
    shutil.move(latest_file, os.path.join(destination,name))


if __name__=="__main__":
    #test
    # line_prepender(PATH,fields)
    line_prepender(PATH,fields2)
    file_mover(downloads,path)





