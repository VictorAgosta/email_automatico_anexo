import pyautogui as pa
import clipboard
import time
import pandas as pd
from os import chdir, getcwd, listdir
from os.path import isfile

## Deixar o gmail aberto e logado no chrome ##

#################################################################################################################
# Caminho onde ficam as planilhas dos recibos de cada empresa cliente 
# extraidos com uma outra automação (repositório: VictorAgosta/Coleta_exporta_dados, arquivo: recibos.py) 

caminho = r'X:\e-Social\teste_envio_recibos'

#################################################################################################################
# função para criar uma lista com os nomes dos arquivos para serem enviados para as empresas

def criar_lista():
    chdir(caminho)
    print(getcwd())

    tabela = []

    for c in listdir():
        if isfile(c):
            tabela.append(c)

    dataframe = pd.DataFrame(tabela, columns=['arquivos'])
    dataframe.to_excel(rf'{caminho}\lista_recibos.xlsx', index=False)

#################################################################################################################
# função para abrir o navegador onde o gmail já deve estar aberto e logado

def abrir_navegador():
    pa.moveTo(220, 1006)
    pa.leftClick()

#################################################################################################################    
# função para clicar no botão "mensagem" do gmail

def clicar_mensagem():
    pa.moveTo(74, 211)
    pa.leftClick()
    
#################################################################################################################
# função para escrever o email

def escrever_email():
    assunto = f'Recibos eSocial - {nome_v}'

    corpo_email = f'''Boa tarde,

Sou da equipe de desenvolvimento do Inmestra, responsável pelos envios ao eSocial.

Estamos entrando em contato para o envio dos comprovantes dos eventos do eSocial da empresa {nome_v}.

Segue em anexo o arquivo com os números dos recibos.

Qualquer dúvida estamos à disposição através do email: email do nosso suporte.
Obrigado!
'''

#################################################################################################################    
    # colar o destinatário
    
    clipboard.copy(email_v)
    pa.hotkey('ctrl', 'v')
    pa.press('tab')
    time.sleep(1)

#################################################################################################################
    # colar o assunto
    
    clipboard.copy(assunto)
    pa.hotkey('ctrl', 'v')
    pa.press('tab')
    time.sleep(1)
    
#################################################################################################################
    # colar o corpo do email
    
    clipboard.copy(corpo_email)
    pa.hotkey('ctrl', 'v')
    time.sleep(1)
    
#################################################################################################################
    # clicar no botão de anexo
    
    pa.moveTo(777, 951)
    pa.leftClick()
    time.sleep(1)
    
#################################################################################################################
    # colar o caminho do arquivo e dar enter
    
    clipboard.copy(rf'{caminho}\{anexo_v}')
    pa.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pa.press('enter')
    time.sleep(5)

#################################################################################################################
    # enviar o email (ctrl + enter)
    pa.hotkey('ctrl', 'enter')

#################################################################################################################
# inicio da aplicação

#################################################################################################################
# chamada da criação da lista com os nomes dos arquivos
criar_lista()

#################################################################################################################
# leitura dos dados de emails das empresas clientes e das empresas que possuem recibos

lista_plan_recibos = pd.read_excel(rf'{caminho}\lista_recibos.xlsx')
lista_plan_email = pd.read_excel(rf'X:\e-Social\dados\codigo_email.xlsx')

#################################################################################################################
# Criação das listas que irão armazenar as informações para gerar os emails

nome = []
anexo = []
cod = []
email = []

#################################################################################################################
# definição das variaveis a partir da lista de arquivos para serem enviados

for arquivo in lista_plan_recibos['arquivos']:

#################################################################################################################
    # Desconsiderar o arquivo da lista de arquivos e do nome das empresas
    
    if arquivo == 'lista_recibos.xlsx':
        continue
    if arquivo == 'nomes_empresas.xlsx':
        continue
        
#################################################################################################################
    # Definição dos nomes das empresas baseado nos nomes dos arquivos
    
    nome_arquivo_l = arquivo.split('_')
    nome_empresa = nome_arquivo_l[3]
    cod_empresa = nome_arquivo_l[2]
    cod.append(cod_empresa)
    nome.append(nome_empresa)
    anexo.append(arquivo)

#################################################################################################################
# encontrando o email das empresas 
# utilizando como chave o código de cada empresa gerado no sistema SOC que utilizamos

for codigo in cod:
    indice_1 = lista_plan_email[lista_plan_email['cod'] == int(codigo)].index
    email_valores = lista_plan_email['email'].values[indice_1]
    email_string = str(email_valores)
    fim = (len(email_string) - 2)
    email_empresa = email_string[2:fim]
    email.append(email_empresa)

#################################################################################################################
# criação do dicionário com todas informações para o email

dit = {'cod': cod, 'nome': nome, 'anexo': anexo, 'email': email}

#################################################################################################################
# transformando o dicionário em uma planilha para conferência caso necessário

dit_df = pd.DataFrame(dit)
dit_df.to_excel(rf'{caminho}\nomes_empresas.xlsx', index=False)

#################################################################################################################
###### inicio da automação do email ######

#################################################################################################################
# Leitura da planilha com os dados para os emails

planilha = pd.read_excel(rf'{caminho}\nomes_empresas.xlsx')

#################################################################################################################
# chamada da função de abertura do navegador
abrir_navegador()

#################################################################################################################
# utilização de um loop para execução da automação baseado na planilha com os dados para envio do email

for empresa in planilha['cod']:
    indice_2 = planilha[planilha['cod'] == int(empresa)].index

    nome_array = planilha['nome'].values[indice_2]
    nome_string = str(nome_array)
    fim = (len(nome_string) - 2)
    nome_v = nome_string[2:fim]

    anexo_array = planilha['anexo'].values[indice_2]
    anexo_string = str(anexo_array)
    fim = (len(anexo_string) - 2)
    anexo_v = anexo_string[2:fim]

    email_array = planilha['email'].values[indice_2]
    email_string = str(email_array)
    fim = (len(email_string) - 2)
    email_v = email_string[2:fim]

#################################################################################################################
    # Execução das funções
    time.sleep(1)
    clicar_mensagem()
    time.sleep(1)
    escrever_email()
