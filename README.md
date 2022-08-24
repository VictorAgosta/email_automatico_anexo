# email_automatico_anexo

Criei uma automação para verificar para quais empresas clientes foi gerado uma planilha de recibos de envios de documentos ao eSocial, e enviar um email para essas empresas com esses recibos em anexo.

Os arquivos de recibos são gerados com uma automação disponível no repositório VictorAgosta/Coleta_exporta_dados/recibos.py

Essa automação gera uma planilha com os nomes dos arquivos gerados (que possuem o código e o nome da empresa cliente) utilizando a biblioteca <b>pandas</b> e a partir disso gera um email, inclui o arquivo dos recibos como anexo e envia para as empresas clientes utilizando a biblioteca <b>pyautoGUI</b>
