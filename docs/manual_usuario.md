# Manual do Usuário TechCommerce DataOps

## Passo a Passo

1. **Preparação do ambiente**
   - Instale Python 3.8+ e as dependências do projeto
   - Organize os arquivos conforme a estrutura indicada

2. **Execução dos scripts**
   - Pipeline de ingestão: `python src/pipeline_ingestao.py`
   - Correção automática: `python src/correcao_automatica.py`
   - Enriquecimento de dados: `python src/enriquecimento_dados.py`
   - Validação com Great Expectations: `python src/great_expectations_setup.py`
   - Geração de Data Docs: `python src/dashboard_qualidade.py`
   - Sistema de alertas: `python src/sistema_alertas.py`

3. **Acesso aos resultados**
   - Dados corrigidos: `data/processed/`
   - Relatórios de qualidade: `data/quality/`
   - Data Docs: `great_expectations/uncommitted/data_docs/`
   - Logs de auditoria: `data/quality/auditoria.log`

## Suporte

- Dúvidas técnicas: professor@techcommerce.com
- Office hours: Terças e Quintas, 14h-16h

## Observações

- Recomenda-se rodar os scripts na ordem sugerida para garantir integridade dos dados.
- Consulte o documento de governança para detalhes sobre políticas e papéis.