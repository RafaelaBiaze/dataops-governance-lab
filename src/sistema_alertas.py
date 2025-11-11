import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def verificar_alertas_clientes(path):
    df = pd.read_csv(path)
    alertas = []
    if df['email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False).mean() < 0.98:
        alertas.append("Alerta: Mais de 2% dos emails de clientes são inválidos!")
    if df['nome'].isnull().mean() > 0.02:
        alertas.append("Alerta: Mais de 2% dos clientes sem nome informado!")
    return alertas

def verificar_alertas_produtos(path):
    df = pd.read_csv(path)
    alertas = []
    if (df['preco'] < 0).mean() > 0.01:
        alertas.append("Alerta: Existem produtos com preço negativo!")
    if df['categoria'].isnull().mean() > 0.02:
        alertas.append("Alerta: Mais de 2% dos produtos sem categoria!")
    return alertas

def verificar_alertas_vendas(path):
    df = pd.read_csv(path)
    alertas = []
    if (df['quantidade'] < 1).mean() > 0.01:
        alertas.append("Alerta: Existem vendas com quantidade negativa ou zero!")
    if (df['valor_total'] < 0).mean() > 0.01:
        alertas.append("Alerta: Existem vendas com valor total negativo!")
    return alertas

def dashboard_alertas(alertas):
    print("\n--- Dashboard de Alertas Ativos ---")
    if not alertas:
        print("Nenhum alerta crítico ativo.")
    else:
        for alerta in alertas:
            print(alerta)

if __name__ == "__main__":
    alertas = []
    alertas += verificar_alertas_clientes("../data/processed/clientes_corrigido.csv")
    alertas += verificar_alertas_produtos("../data/processed/produtos_corrigido.csv")
    alertas += verificar_alertas_vendas("../data/processed/vendas_corrigido.csv")
    dashboard_alertas(alertas)
    logging.info("Sistema de alertas executado.")