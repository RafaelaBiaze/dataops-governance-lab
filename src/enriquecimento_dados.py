import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def geocodificar_cidade(cidade):
    # Simulação: retorna latitude/longitude fictícia por cidade
    cidades_fake = {
        "São Paulo": (-23.5505, -46.6333),
        "Rio de Janeiro": (-22.9068, -43.1729),
        "Belo Horizonte": (-19.9167, -43.9345)
    }
    return cidades_fake.get(cidade, (0.0, 0.0))

def categorizar_produto(nome):
    # Simulação: categorização simples por palavra-chave
    if "Smartphone" in nome:
        return "Eletrônicos"
    elif "Notebook" in nome:
        return "Informática"
    elif "Mouse" in nome or "Teclado" in nome:
        return "Acessórios"
    else:
        return "Outros"

def calcular_idade(data_nascimento):
    try:
        nascimento = pd.to_datetime(data_nascimento, errors='coerce')
        hoje = datetime.now()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade if idade > 0 else 0
    except Exception:
        return 0

def calcular_tempo_entrega(data_envio, data_entrega_real):
    try:
        envio = pd.to_datetime(data_envio, errors='coerce')
        entrega = pd.to_datetime(data_entrega_real, errors='coerce')
        if pd.isnull(envio) or pd.isnull(entrega):
            return None
        return (entrega - envio).days
    except Exception:
        return None

def flag_qualidade_clientes(df):
    # Exemplo: flag para email válido e nome preenchido
    df['flag_email_valido'] = df['email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)
    df['flag_nome_preenchido'] = df['nome'].notnull() & (df['nome'] != "")
    return df

def enriquecer_clientes(path_in, path_out):
    df = pd.read_csv(path_in)
    df[['latitude', 'longitude']] = df['cidade'].apply(lambda x: pd.Series(geocodificar_cidade(x)))
    df['idade'] = df['data_nascimento'].apply(calcular_idade)
    df = flag_qualidade_clientes(df)
    df.to_csv(path_out, index=False)
    logging.info("Enriquecimento de clientes concluído.")

def enriquecer_produtos(path_in, path_out):
    df = pd.read_csv(path_in)
    df['categoria_auto'] = df['nome_produto'].apply(categorizar_produto)
    df.to_csv(path_out, index=False)
    logging.info("Enriquecimento de produtos concluído.")

def enriquecer_logistica(path_in, path_out):
    df = pd.read_csv(path_in)
    df['tempo_entrega'] = df.apply(lambda x: calcular_tempo_entrega(x['data_envio'], x['data_entrega_real']), axis=1)
    df.to_csv(path_out, index=False)
    logging.info("Enriquecimento de logística concluído.")

if __name__ == "__main__":
    enriquecer_clientes("../data/processed/clientes_corrigido.csv", "../data/processed/clientes_enriquecido.csv")
    enriquecer_produtos("../data/processed/produtos_corrigido.csv", "../data/processed/produtos_enriquecido.csv")
    enriquecer_logistica("../data/processed/logistica_corrigido.csv", "../data/processed/logistica_enriquecido.csv")
    logging.info("Enriquecimento de dados finalizado.")