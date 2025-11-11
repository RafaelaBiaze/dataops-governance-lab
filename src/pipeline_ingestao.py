import pandas as pd
import logging
from datetime import datetime
import os

os.makedirs('../data/quality', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)

# Configuração do logger de auditoria
logging.basicConfig(
    filename='../data/quality/auditoria.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def carregar_dados(caminho, nome):
    try:
        df = pd.read_csv(caminho)
        logging.info(f'Dataset {nome} carregado com sucesso. Registros: {len(df)}')
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar {nome}: {e}')
        return pd.DataFrame()

def validar_schema(df, schema, nome):
    erros = []
    for coluna, tipo in schema.items():
        if coluna not in df.columns:
            erros.append(f'Coluna ausente: {coluna}')
        elif not df[coluna].map(lambda x: isinstance(x, tipo) or pd.isnull(x)).all():
            erros.append(f'Tipo incorreto na coluna: {coluna}')
    if erros:
        logging.warning(f'Erros de schema em {nome}: {erros}')
    else:
        logging.info(f'Schema validado para {nome}')
    return erros

# Schemas esperados (exemplo simplificado)
schema_clientes = {
    'id_cliente': int,
    'nome': str,
    'email': str,
    'telefone': str,
    'data_nascimento': str,
    'cidade': str,
    'estado': str,
    'data_cadastro': str
}

schema_produtos = {
    'id_produto': int,
    'nome_produto': str,
    'categoria': str,
    'preco': float,
    'estoque': int,
    'data_criacao': str,
    'ativo': str
}

# Carregar datasets
clientes = carregar_dados('../notebooks/datasets/clientes.csv', 'clientes')
produtos = carregar_dados('../notebooks/datasets/produtos.csv', 'produtos')
vendas = carregar_dados('../notebooks/datasets/vendas.csv', 'vendas')
logistica = carregar_dados('../notebooks/datasets/logistica.csv', 'logistica')

# Validar schemas
validar_schema(clientes, schema_clientes, 'clientes')
validar_schema(produtos, schema_produtos, 'produtos')
# Adicione validação para vendas e logística conforme necessário

# Tratamento de erros de formato (exemplo para datas)
def padronizar_data(df, coluna, formato='%Y-%m-%d'):
    try:
        df[coluna] = pd.to_datetime(df[coluna], format=formato, errors='coerce')
        logging.info(f'Datas padronizadas na coluna {coluna}')
    except Exception as e:
        logging.error(f'Erro ao padronizar datas em {coluna}: {e}')
    return df

clientes = padronizar_data(clientes, 'data_nascimento')
clientes = padronizar_data(clientes, 'data_cadastro')
produtos = padronizar_data(produtos, 'data_criacao')

# Salvar dados processados
clientes.to_csv('../data/processed/clientes.csv', index=False)
produtos.to_csv('../data/processed/produtos.csv', index=False)
vendas.to_csv('../data/processed/vendas.csv', index=False)
logistica.to_csv('../data/processed/logistica.csv', index=False)

logging.info('Pipeline de ingestão finalizado com sucesso.')
