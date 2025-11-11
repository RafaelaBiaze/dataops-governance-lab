import os
import logging
from great_expectations.data_context import DataContext

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def gerar_data_docs(context):
    """
    Gera os Data Docs (relatórios HTML) do Great Expectations.
    """
    context.build_data_docs()
    logging.info("Data Docs gerados com sucesso.")

def abrir_data_docs(context):
    """
    Abre o Data Docs no navegador padrão.
    """
    docs_sites = context.get_docs_sites_urls()
    for site in docs_sites:
        print(f"Data Docs disponível em: {site['site_url']}")

if __name__ == "__main__":
    ge_root = os.path.join(os.getcwd(), "great_expectations")
    context = DataContext(ge_root)
    gerar_data_docs(context)
    abrir_data_docs(context)
    logging.info("Dashboard de qualidade finalizado.")