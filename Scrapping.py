from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd

from time import sleep

from bs4 import BeautifulSoup

from base import extrairtabela, formatar_tabelas, radargraphic, radargraphicS

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome()

df = extrairtabela(navegador) ## usa função para armazenar tabela no dataframe

df = formatar_tabelas(df)

## exportar para excel
arquivo = 'tabela.xlsx'
df.to_excel(arquivo, index=False)


radargraphicS(df, 'São Paulo')

