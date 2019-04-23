import config
from   selenium import webdriver
from   selenium.webdriver.common.by import By
import time
import datetime
now = datetime.date.today().strftime(" %B %d %Y")
from selenium.webdriver.chrome.options import Options
import os

path = os.path.join(config.db_path,'consors')
LOGIN = config.consors_cred['login']
PASSWORD = config.consors_cred['password']

def get_balance():
    options = Options()


    # options.add_argument("headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=600,800")

    browser = webdriver.Chrome(executable_path=r'/Users/joanarau-schweizer/PycharmProjects/stockbot/chromedriver 10.15.44 pm',options=options)


    ### Login
    LOGIN_URL = 'https://www.consorsbank.de/home'
    browser.get(LOGIN_URL)
    # browser.switch_to.frame('mobile-login')
    element = browser.find_element(By.XPATH, '//*[@id="header-login-button"]').click()
    time.sleep(1)
    username = browser.find_element(By.XPATH,'//*[@id="user-id"]')
    password = browser.find_element(By.XPATH,'//*[@id="password"]')
    username.send_keys(LOGIN)
    password.send_keys(PASSWORD)
    browser.find_element_by_id('login').click()

    # Wait until login is done... (is AJAX login)
    while  browser.current_url == LOGIN_URL:
      print('waiting...')
      time.sleep(0.1)



    time.sleep(5)

    dict={}


    element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber1"]/table/tbody/tr[2]/td[6]/div/span/span[1]')

    dict['portfolio_firma'] = element.text

    element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber1"]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['cash_firma'] = element.text

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[2]/table/tbody/tr[2]/td[6]/div')
    dict['portfolio_a'] = element.text

    element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber2"]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['portfolio_a_cash'] = element.text

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[3]/table/tbody/tr[2]/td[6]/div')
    dict['portfolio_b'] = element.text

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[3]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['portfolio_b_cash'] = element.text



    browser.quit()
    print(dict)
    portfolios = {'firma':[dict['portfolio_firma'],dict['cash_firma']],'personal_a':[dict['portfolio_a'],dict['portfolio_a_cash']],'personal_b':[dict['portfolio_b'],dict['portfolio_b_cash']]}
    return portfolios
value = get_balance()
print(value)
fields=[now,value]



def line_prepender(filename,fields):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        field = str(fields[1])
        f.write(str(fields[0])+','+field.replace('.','').replace(',','.').replace(' EUR', '') + '\n' + content)

fields=[now,[value['firma'][0],value['firma'][1]]]
PATH=os.path.join(path,'portfolio_firma.csv')
print(PATH)
line_prepender(PATH,fields)

fields=[now,[value['personal_a'][0],value['personal_a'][1],value['personal_b'][0],value['personal_b'][1]]]
PATH=os.path.join(path,'portfolio_personal.csv')
print(PATH)
line_prepender(PATH,fields)



