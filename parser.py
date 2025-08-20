from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EDC
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
link="https://finance.yahoo.com/quote/BTC-USD/history/?period1=1410912000&period2=1724750859"
driver.get(link)
driver.implicitly_wait(10)

#find table and save it
table1=driver.find_element(By.CSS_SELECTOR, '.table.yf-ewueuo')
rows = table1.find_elements(By.TAG_NAME, 'tr')

column_names=[]
for k in table1.find_elements(By.TAG_NAME, 'th'):
    column_names.append(k.text)

data=pd.DataFrame(columns=column_names)

for row in rows[1:]:
    info=row.find_elements(By.TAG_NAME, 'td')
    info_text_row=[i.text for i in info]
    length=len(data)
    data.loc[length]=info_text_row

data.to_csv('Bitcoin_price.csv')

