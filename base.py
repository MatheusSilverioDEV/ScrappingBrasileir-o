from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from bs4 import BeautifulSoup

def extrairtabela(navegador):
    navegador.get('https://www.google.com/search?q=tabela+brasileirao&rlz=1C1GCEA_enBR1024BR1024&oq=ta&aqs=chrome.0.69i59j69i64j69i57j69i59l2j69i60l3.783j0j7&sourceid=chrome&ie=UTF-8#sie=lg;/g/11jspy1hvm;2;/m/0fnk7q;st;fp;1;;;')
    sleep(3)

    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')  ## armazena o HTML
    tabela = site.find_all('table',
                           attrs={'class': 'Jzru1c'})  ## procura tags 'a' com a classe especificada no dicionário
    tabela_html = tabela[0].prettify()  ## guarda somente a tabela do html
    tabelaP = pd.read_html(tabela_html, skiprows=0)[0]  # Cria o dataframe
    df = tabelaP  ## renomeia a variavel
    return df

def formatar_tabelas(df):
    nomes_colunas = ['excluir', 'excluir2', 'Clubes', 'PTS', 'PJ', 'VIT', 'E', 'DER', 'GM', 'GC', 'SG', 'Últimas 5',
                     'excluir3']  ## define nome das colunas (excluir são colunas vazias ou com dados desnecessarios que vieram pelo html)
    df.columns = nomes_colunas  ## Nomeia as colunas

    colunas_excluidas = ['excluir', 'excluir2', 'excluir3']  ## guarda as colunas que desejo excluir
    df = df.drop(colunas_excluidas, axis=1)  ## exclui as colunas

    for i, celula in enumerate(df['Últimas 5']):
        df.at[i, 'Últimas 5'] = celula.replace('Partida mais recente',
                                               '')  ## itera em cada celula retirando a palavra 'partida mais recente' colocado devido erros de html

    for i, celula in enumerate(df['Últimas 5']):  ## substitui as palavras por siglas
        celula = celula.replace('Vitórias', 'V')
        celula = celula.replace('Derrota', 'D')
        celula = celula.replace('Empates', 'E')
        df.at[i, 'Últimas 5'] = celula

    return df

dados = pd.read_excel('tabela.xlsx')

def radargraphic(dados):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Ordenando os clubes em ordem alfabética
    clubes = sorted(dados['Clubes'])

    # Ordenando os dados de acordo com a ordem alfabética dos clubes
    dados = dados.set_index('Clubes').loc[clubes].reset_index()

    # Dados das colunas
    PTS = dados['PTS']
    VIT = dados['VIT'].replace({'V': 1, 'E': 0, 'D': -1})
    E = dados['E'].replace({'V': 1, 'E': 0, 'D': -1})
    DER = dados['DER'].replace({'V': 1, 'E': 0, 'D': -1})
    GM = dados['GM']
    GC = dados['GC']
    SG = dados['SG']

    # Ângulos para os raios
    num_categorias = len(clubes)
    angulos = np.linspace(0, 2 * np.pi, num_categorias, endpoint=False).tolist()

    # Plotando os dados
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.fill(angulos + [angulos[0]], PTS.tolist() + [PTS.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], VIT.tolist() + [VIT.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], E.tolist() + [E.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], DER.tolist() + [DER.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], GM.tolist() + [GM.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], GC.tolist() + [GC.tolist()[0]], alpha=0.25)
    ax.fill(angulos + [angulos[0]], SG.tolist() + [SG.tolist()[0]], alpha=0.25)

    # Personalização do gráfico
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angulos)
    ax.set_xticklabels(clubes)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.grid(True)

    # Legenda
    ax.legend(['PTS', 'VIT', 'E', 'DER', 'GM', 'GC', 'SG'], loc='upper right')

    # Exibição do gráfico
    plt.show()

def radargraphicS(dados, nome_time):
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # Filtrando os dados apenas para o time desejado
        time = dados[dados['Clubes'] == nome_time]

        # Ordenando as colunas de acordo com o nome
        colunas = ['PTS', 'VIT', 'E', 'DER', 'GM', 'GC', 'SG']
        time = time[colunas]

        # Ajustando os valores para distribuir entre os raios
        num_categorias = len(colunas)
        valores = time.values.flatten()  # Flatten para ter apenas uma dimensão

        # Ângulos para os raios
        angulos = np.linspace(0, 2 * np.pi, num_categorias, endpoint=False).tolist()

        # Plotando o gráfico
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
        ax.fill(angulos, valores, alpha=0.25)
        ax.set_xticks(angulos)
        ax.set_xticklabels(colunas)
        ax.yaxis.set_tick_params(labelsize=8)
        ax.grid(True)

        # Título do gráfico
        ax.set_title(nome_time)

        # Exibição do gráfico
        plt.show()
