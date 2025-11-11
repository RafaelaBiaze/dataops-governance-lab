import os
import logging
from great_expectations.data_context import DataContext

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def criar_checkpoint(context, checkpoint_name, suite_name, batch_request):
    """
    Cria e salva um checkpoint para automação das validações.
    """
    checkpoint_config = {
        "name": checkpoint_name,
        "config_version": 1.0,
        "class_name": "SimpleCheckpoint",
        "run_name_template": "%Y%m%d-%H%M%S",
        "validations": [
            {
                "batch_request": batch_request,
                "expectation_suite_name": suite_name,
            }
        ],
    }
    context.add_checkpoint(**checkpoint_config)
    logging.info(f"Checkpoint '{checkpoint_name}' criado para suite '{suite_name}'.")

if __name__ == "__main__":
    ge_root = os.path.join(os.getcwd(), "great_expectations")
    context = DataContext(ge_root)

    # Exemplo de batch_request para clientes
    import pandas as pd
    df_clientes = pd.read_csv("../data/datasets/clientes.csv")
    batch_request_clientes = {
        "datasource_name": "pandas_datasource",
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "clientes_runtime",
        "runtime_parameters": {"batch_data": df_clientes},
        "batch_identifiers": {"default_identifier_name": "clientes_1"},
    }

    criar_checkpoint(context, "checkpoint_clientes", "clientes_suite", batch_request_clientes)

    # Repita para produtos e vendas conforme necessário

    logging.info("Configuração de checkpoints concluída.")