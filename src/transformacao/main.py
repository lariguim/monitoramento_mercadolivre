import os
import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminho para o arquivo JSON
json_path = os.path.join(os.path.dirname(__file__), '../../data/data.json')

# Verificar se o arquivo existe
if not os.path.isfile(json_path):
    raise FileNotFoundError(f"O arquivo {json_path} não foi encontrado.")

# Verificar se o arquivo não está vazio
if os.path.getsize(json_path) == 0:
    raise ValueError(f"O arquivo {json_path} está vazio.")

# Ler o arquivo JSON como um todo
try:
    df = pd.read_json(json_path)
except ValueError as e:
    raise ValueError(f"Erro ao ler o arquivo JSON: {e}")

# Exibir o DataFrame resultante
print(df.head())

# Adicionar a coluna _source com um valor fixo
df['source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Adicionar a coluna _data_coleta com a data e hora atuais
df['data_coleta'] = datetime.now()

# Tratar os valores nulos para colunas numéricas e de texto
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parênteses das colunas `reviews_amount`
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços como floats e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover as colunas antigas de preços
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conectar ao banco de dados SQLite (ou criar um novo)
db_path = os.path.join(os.path.dirname(__file__), '../../data/quotes.db')
conn = sqlite3.connect(db_path)

# Salvar o DataFrame no banco de dados SQLite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

# Configurar pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Exibir o DataFrame resultante
print(df.head())
