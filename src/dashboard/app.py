import os
import sqlite3
import pandas as pd
import streamlit as st

# Definir o caminho absoluto para o banco de dados SQLite baseado no diretório de trabalho atual
db_path = os.path.abspath(os.path.join(os.getcwd(), '../../data/quotes.db'))

# Imprimir o caminho do arquivo para depuração
st.write(f"Caminho do banco de dados: {db_path}")

# Verificar se o arquivo de banco de dados existe
if os.path.exists(db_path):
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(db_path)
        
        # Carregar os dados da tabela 'mercadolivre_items' em um DataFrame pandas
        df = pd.read_sql_query("SELECT * FROM mercadolivre_items", conn)
        
        # Fechar a conexão com o banco de dados
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        df = pd.DataFrame()  # Definir df como um DataFrame vazio em caso de erro
    except Exception as e:
        st.error(f"Um erro ocorreu: {e}")
        df = pd.DataFrame()  # Definir df como um DataFrame vazio em caso de erro
else:
    st.error("Arquivo de banco de dados não encontrado.")
    df = pd.DataFrame()  # Definir df como um DataFrame vazio

if not df.empty:
    # Título da aplicação
    st.title('Pesquisa de Mercado - Tênis Esportivos no Mercado Livre')

    # Melhorar o layout com colunas para KPIs
    st.subheader("KPIs Principais")
    col1, col2, col3 = st.columns(3)

    # KPI 1: Número total de itens
    total_items = df.shape[0]
    col1.metric(label="Número Total de Itens", value=total_items)

    # KPI 2: Número de marcas únicas
    unique_brands = df['brand'].nunique()
    col2.metric(label="Número de Marcas Únicas", value=unique_brands)

    # KPI 3: Preço médio novo (em reais)
    average_new_price = df['new_price'].mean()
    col3.metric(label="Preço Médio Novo (R$)", value=f"{average_new_price:.2f}")

    # Quais marcas são mais encontradas até a 10ª página
    st.subheader('Marcas mais encontradas até a 10ª página')
    col1, col2 = st.columns([4, 2])
    top_10_pages_brands = df.head(500)['brand'].value_counts().sort_values(ascending=False)
    col1.bar_chart(top_10_pages_brands)
    col2.write(top_10_pages_brands)

    # Qual o preço médio por marca
    st.subheader('Preço médio por marca')
    col1, col2 = st.columns([4, 2])
    average_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
    col1.bar_chart(average_price_by_brand)
    col2.write(average_price_by_brand)

    # Qual a satisfação por marca
    st.subheader('Satisfação por marca')
    col1, col2 = st.columns([4, 2])
    df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
    satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
    col1.bar_chart(satisfaction_by_brand)
    col2.write(satisfaction_by_brand)
else:
    st.error("Nenhum dado disponível para exibir.")
