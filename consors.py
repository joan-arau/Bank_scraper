import config
from   selenium import webdriver
from   selenium.webdriver.common.by import By
import time
import datetime
now = datetime.date.today().strftime('%Y-%m-%d')
import pandas as pd
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

    browser = webdriver.Chrome(config.chromedriver,options=options)


    ### Login
    LOGIN_URL = 'https://www.consorsbank.de/home'
    browser.get(LOGIN_URL)
    # browser.switch_to.frame('mobile-login')
    time.sleep(5)
    element = browser.find_element(By.XPATH, '//*[@id="header-login-button"]').click()

    time.sleep(5)
    username = browser.find_element(By.XPATH,'//*[@id="user-id"]')
    username.send_keys(LOGIN)

    time.sleep(5)
    password = browser.find_element(By.XPATH,'//*[@id="password"]')
    password.send_keys(PASSWORD)
    browser.find_element_by_id('login').click()

    # Wait until login is done... (is AJAX login)
    # while  browser.current_url == LOGIN_URL:
    #   print('waiting...')
    #   time.sleep(0.1)



    time.sleep(10)

    dict={}
    load =False
    x = 0
    while load == False:
        try:
            element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber1"]/table/tbody/tr[2]/td[6]/div/span/span[1]')
            load = True
        except:
            print('Loading page...')
            pass
        x+=1
        if x > 100:
            break



    dict['portfolio_firma'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))

    element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber1"]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['cash_firma'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[2]/table/tbody/tr[2]/td[6]/div')
    dict['portfolio_a'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))

    element = browser.find_element(By.XPATH,'//*[@id="Kontouebersicht.Inhaber2"]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['portfolio_a_cash'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[3]/table/tbody/tr[2]/td[6]/div')
    dict['portfolio_b'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))

    element = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/ul/li[1]/div[1]/div[3]/table/tbody/tr[3]/td[5]/div/span/span[1]')
    dict['portfolio_b_cash'] = float(element.text.replace('.','').replace(',','.').replace(' EUR',''))



    browser.quit()
    print(dict)
    portfolios = {'firma':[dict['portfolio_firma'],dict['cash_firma']],'personal_a':[dict['portfolio_a'],dict['portfolio_a_cash']],'personal_b':[dict['portfolio_b'],dict['portfolio_b_cash']]}
    return portfolios
value = get_balance()
print(value)
fields=[now,value]


fields1=[now,
         value['personal_a'][0]+value['personal_a'][1]+value['personal_b'][0]+value['personal_b'][1],
         2,
         int('8600629891'),
         value['personal_a'][0]+value['personal_b'][0],
         value['personal_a'][1]+value['personal_b'][1],
         'EUR',]

fields2=[now,
         value['firma'][0]+value['firma'][1],
         2,
         int('8600629892'),
         value['firma'][0],
         value['firma'][1],
         'EUR',]

# def line_prepender(filename,fields):
#     with open(filename, 'r+') as f:
#         content = f.read()
#         f.seek(0, 0)
#         field = str(fields[1])
#         f.write(str(fields[0])+','+field.replace('.','').replace(',','.').replace(' EUR', '') + '\n' + content)

def line_prepender(account,fields):


    df = pd.read_csv(os.path.join(config.db_path, 'mysql_db_csv/portfolio_value/',account+'.csv'))
    print(df.tail())
    new_row=pd.DataFrame([[fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6]]],columns=['Date','total_value','broker_id','account_number','portfolio_value','cash','currency'])
    new_row=new_row.reset_index(drop=True)
    df=df.reset_index(drop=True)
    print(new_row)
    df=df.append(new_row.reset_index(drop=True))

    df=df.reset_index(drop=True)
    df['entry']=0
    print(df.tail(10))
    df.to_csv(os.path.join(config.db_path, 'mysql_db_csv/portfolio_value/',account+'.csv'), index=False)


line_prepender('8600629891',fields1)
line_prepender('8600629892',fields2)

# fields=[now,[value['personal_a'][0],value['personal_a'][1],value['personal_b'][0],value['personal_b'][1]]]
# PATH=os.path.join(path,'portfolio_personal.csv')
# line_prepender(PATH,fields)



