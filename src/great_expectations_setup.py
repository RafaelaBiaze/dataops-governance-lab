"""
Configuração inicial do Great Expectations e criação de Expectation Suites
"""

import os
import subprocess
import logging
import pandas as pd
import great_expectations as ge

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_ge_project(project_root="great_expectations"):
    """
    Inicializa um projeto great_expectations no diretório especificado se não existir.
    Usa a CLI 'great_expectations' quando disponível como fallback simples.
    """
    if os.path.isdir(project_root) and os.path.isfile(os.path.join(project_root, "great_expectations.yml")):
        logging.info(f"Great Expectations já inicializado em: {project_root}")
        return

    # Tenta inicialização via CLI
    import shutil
    ge_cli = shutil.which("great_expectations")
    if ge_cli:
        logging.info("Inicializando Great Expectations via CLI...")
        subprocess.run([ge_cli, "init", "--yes"], check=False)
    else:
        logging.warning("CLI do Great Expectations não encontrada. Crie manualmente com `great_expectations init`.")

def ensure_pandas_datasource(context, datasource_name="pandas_datasource"):
    """
    Garante que exista uma datasource com PandasExecutionEngine e um RuntimeDataConnector.
    Retorna True se datasource estiver presente ou criado.
    """
    try:
        if datasource_name in context.list_datasources():
            logging.info(f"Datasource '{datasource_name}' já existe.")
            return True
    except Exception:
        pass

    datasource_config = {
        "name": datasource_name,
        "class_name": "Datasource",
        "execution_engine": {"class_name": "PandasExecutionEngine"},
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"],
            }
        },
    }

    try:
        context.add_datasource(**datasource_config)
        logging.info(f"Datasource '{datasource_name}' criada com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Falha ao criar datasource '{datasource_name}': {e}")
        return False

def create_expectation_suite_for_clientes(context, path_to_csv, suite_name="clientes_suite"):
    df = pd.read_csv(path_to_csv)
    context.create_expectation_suite(expectation_suite_name=suite_name, overwrite_existing=True)
    batch_request = {
        "datasource_name": "pandas_datasource",
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "clientes_runtime",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "clientes_1"},
    }
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)
    validator.expect_column_values_to_not_be_null("id_cliente")
    validator.expect_column_values_to_be_unique("id_cliente")
    validator.expect_column_values_to_not_be_null("nome")
    validator.expect_column_values_to_match_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")
    validator.expect_column_values_to_match_regex("telefone", r"^\d{10,11}$", mostly=0.95)
    validator.expect_column_values_to_match_regex("estado", r"^[A-Z]{2}$", mostly=0.95)
    validator.save_expectation_suite()
    logging.info(f"Expectation suite '{suite_name}' criada para clientes.")

def create_expectation_suite_for_produtos(context, path_to_csv, suite_name="produtos_suite"):
    df = pd.read_csv(path_to_csv)
    context.create_expectation_suite(expectation_suite_name=suite_name, overwrite_existing=True)
    batch_request = {
        "datasource_name": "pandas_datasource",
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "produtos_runtime",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "produtos_1"},
    }
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)
    validator.expect_column_values_to_not_be_null("id_produto")
    validator.expect_column_values_to_be_unique("id_produto")
    validator.expect_column_values_to_not_be_null("nome_produto")
    validator.expect_column_values_to_not_be_null("categoria", mostly=0.95)
    validator.expect_column_values_to_be_between("preco", min_value=0, strict_min=False)
    validator.expect_column_values_to_be_between("estoque", min_value=0, strict_min=False)
    validator.save_expectation_suite()
    logging.info(f"Expectation suite '{suite_name}' criada para produtos.")

def create_expectation_suite_for_vendas(context, path_to_csv, path_clientes_csv=None, path_produtos_csv=None, suite_name="vendas_suite"):
    df = pd.read_csv(path_to_csv)
    context.create_expectation_suite(expectation_suite_name=suite_name, overwrite_existing=True)
    batch_request = {
        "datasource_name": "pandas_datasource",
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "vendas_runtime",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "vendas_1"},
    }
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=suite_name)
    validator.expect_column_values_to_not_be_null("id_venda")
    validator.expect_column_values_to_be_unique("id_venda")
    validator.expect_column_values_to_be_between("quantidade", min_value=1)
    validator.expect_column_values_to_be_between("valor_unitario", min_value=0)
    df["_calc_total"] = df["quantidade"] * df["valor_unitario"]
    validator.expect_column_values_to_be_close("valor_total", df["_calc_total"], mostly=0.98, atol=1e-2)
    validator.expect_column_values_to_be_between("data_venda", min_value="1900-01-01", max_value=pd.Timestamp("today").strftime("%Y-%m-%d"))
    validator.expect_column_values_to_be_in_set("status", ["Concluída", "Pendente", "Cancelada", "Processando"], mostly=0.99)
    if path_clientes_csv:
        clientes_df = pd.read_csv(path_clientes_csv)
        clientes_set = set(clientes_df["id_cliente"].astype(str).tolist())
        validator.expect_column_values_to_be_in_set("id_cliente", list(clientes_set), mostly=0.99)
    if path_produtos_csv:
        produtos_df = pd.read_csv(path_produtos_csv)
        produtos_set = set(produtos_df["id_produto"].astype(str).tolist())
        validator.expect_column_values_to_be_in_set("id_produto", list(produtos_set), mostly=0.99)
    validator.save_expectation_suite()
    logging.info(f"Expectation suite '{suite_name}' criada para vendas.")

if __name__ == "__main__":
    ge_root = os.path.join(os.getcwd(), "great_expectations")
    context = ge.DataContext(ge_root)
    ensure_pandas_datasource(context, datasource_name="pandas_datasource")
    path_clientes = os.path.join("..", "data", "datasets", "clientes.csv")
    path_produtos = os.path.join("..", "data", "datasets", "produtos.csv")
    path_vendas = os.path.join("..", "data", "datasets", "vendas.csv")
    create_expectation_suite_for_clientes(context, path_clientes, suite_name="clientes_suite")
    create_expectation_suite_for_produtos(context, path_produtos, suite_name="produtos_suite")
    create_expectation_suite_for_vendas(context, path_vendas, path_clientes_csv=path_clientes, path_produtos_csv=path_produtos, suite_name="vendas_suite")
    logging.info("Configuração inicial de Great Expectations e Expectation Suites concluída.")