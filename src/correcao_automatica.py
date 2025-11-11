import pandas as pd
import re
import logging
import os

os.makedirs('../data/processed', exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def padronizar_email(email):
    if pd.isnull(email):
        return ""
    return email.strip().lower()

def padronizar_telefone(telefone):
    if pd.isnull(telefone):
        return ""
    telefone = re.sub(r'\D', '', str(telefone))
    return telefone.zfill(11) if len(telefone) <= 11 else telefone[:11]

def padronizar_data(data):
    try:
        return pd.to_datetime(data, errors='coerce').strftime('%Y-%m-%d')
    except Exception:
        return ""

def remover_duplicatas(df, subset):
    antes = len(df)
    df = df.drop_duplicates(subset=subset)
    depois = len(df)
    logging.info(f"Removidas {antes - depois} duplicatas.")
    return df

def preencher_campos_vazios_clientes(df):
    df['nome'] = df['nome'].fillna('Cliente Não Informado')
    df['email'] = df['email'].fillna('email@naoinformado.com')
    return df

def corrigir_clientes(path_in, path_out):
    df = pd.read_csv(path_in)
    df['email'] = df['email'].apply(padronizar_email)
    df['telefone'] = df['telefone'].apply(padronizar_telefone)
    df['data_nascimento'] = df['data_nascimento'].apply(padronizar_data)
    df['data_cadastro'] = df['data_cadastro'].apply(padronizar_data)
    df = remover_duplicatas(df, ['id_cliente', 'email'])
    df = preencher_campos_vazios_clientes(df)
    df.to_csv(path_out, index=False)
    logging.info("Correção de clientes concluída.")

def corrigir_produtos(path_in, path_out):
    df = pd.read_csv(path_in)
    df['nome_produto'] = df['nome_produto'].fillna('Produto Não Informado')
    df['categoria'] = df['categoria'].fillna('Sem Categoria')
    df['preco'] = df['preco'].apply(lambda x: max(float(x), 0))
    df['estoque'] = df['estoque'].apply(lambda x: max(int(x), 0))
    df['data_criacao'] = df['data_criacao'].apply(padronizar_data)
    df = remover_duplicatas(df, ['id_produto', 'nome_produto'])
    df.to_csv(path_out, index=False)
    logging.info("Correção de produtos concluída.")

def corrigir_vendas(path_in, path_out, clientes_path, produtos_path):
    df = pd.read_csv(path_in)
    clientes = pd.read_csv(clientes_path)
    produtos = pd.read_csv(produtos_path)
    df['quantidade'] = df['quantidade'].apply(lambda x: max(int(x), 1))
    df['valor_unitario'] = df['valor_unitario'].apply(lambda x: max(float(x), 0))
    df['valor_total'] = df['quantidade'] * df['valor_unitario']
    df['data_venda'] = df['data_venda'].apply(padronizar_data)
    # Validação de chaves estrangeiras
    df = df[df['id_cliente'].isin(clientes['id_cliente'])]
    df = df[df['id_produto'].isin(produtos['id_produto'])]
    df.to_csv(path_out, index=False)
    logging.info("Correção de vendas concluída.")

def corrigir_logistica(path_in, path_out, vendas_path):
    df = pd.read_csv(path_in)
    vendas = pd.read_csv(vendas_path)
    df['data_envio'] = df['data_envio'].apply(padronizar_data)
    df['data_entrega_prevista'] = df['data_entrega_prevista'].apply(padronizar_data)
    df['data_entrega_real'] = df['data_entrega_real'].apply(padronizar_data)
    # Validação de chaves estrangeiras
    df = df[df['id_venda'].isin(vendas['id_venda'])]
    df.to_csv(path_out, index=False)
    logging.info("Correção de logística concluída.")

if __name__ == "__main__":
    corrigir_clientes("./notebooks/datasets/clientes.csv", "../data/processed/clientes_corrigido.csv")
    corrigir_produtos("./notebooks/datasets/produtos.csv", "../data/processed/produtos_corrigido.csv")
    corrigir_vendas("./notebooks/datasets/vendas.csv", "../data/processed/vendas_corrigido.csv", "../data/processed/clientes_corrigido.csv", "../data/processed/produtos_corrigido.csv")
    corrigir_logistica("./notebooks/datasets/logistica.csv", "../data/processed/logistica_corrigido.csv", "../data/processed/vendas_corrigido.csv")
    logging.info("Sistema de correção automática finalizado.")