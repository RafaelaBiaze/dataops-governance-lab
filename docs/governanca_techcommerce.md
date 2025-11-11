# Governança de Dados TechCommerce

## Organograma de Dados

- **Domínio Clientes**
  - Data Owner: Gerente de CRM
  - Data Steward: Analista de Dados de Clientes
  - Data Custodian: Engenheiro de Dados

- **Domínio Produtos**
  - Data Owner: Gerente de Produtos
  - Data Steward: Analista de Dados de Produtos
  - Data Custodian: Engenheiro de Dados

- **Domínio Vendas**
  - Data Owner: Diretor Comercial
  - Data Steward: Analista de Dados de Vendas
  - Data Custodian: Engenheiro de Dados

- **Domínio Logística**
  - Data Owner: Gerente de Operações
  - Data Steward: Analista de Dados de Logística
  - Data Custodian: Engenheiro de Dados

---

## Políticas de Qualidade

- **Completude:** Campos obrigatórios devem estar preenchidos. Limite máximo de 2% de registros incompletos.
- **Unicidade:** Chaves primárias e e-mails devem ser únicos. Duplicidade máxima permitida: 0,5%.
- **Validade:** Formatos de dados (e-mail, telefone, datas) devem seguir padrões definidos. Erros máximos: 2%.
- **Consistência:** Dados devem ser coerentes entre sistemas e dentro do próprio dataset.
- **Integridade Referencial:** Chaves estrangeiras devem existir nos datasets de referência.
- **Rastreabilidade:** Todas operações devem ser logadas e auditáveis, com histórico disponível por 2 anos.

**Ações corretivas:** 
- Notificação automática ao Data Steward.
- Correção automática via pipeline.
- Auditoria manual em casos críticos.

---

## Glossário de Negócios

- **Cliente Ativo:** Cliente com pelo menos uma compra nos últimos 12 meses.
- **Venda Válida:** Venda com status "Concluída" e valor total positivo.
- **Produto Ativo:** Produto com estoque > 0 e campo "ativo" igual a true.
- **Formato de Data:** AAAA-MM-DD
- **Formato de Telefone:** 11 dígitos numéricos
- **Formato de E-mail:** regex `^[\w\.-]+@[\w\.-]+\.\w+$`
- **Relacionamento:** Cada venda deve referenciar um cliente e um produto existentes.

---

## Padrões e Convenções

- Nomes de colunas em minúsculo e sem espaços.
- Datas no padrão ISO 8601.
- Auditoria centralizada em arquivo de log.
- Versionamento de Expectation Suites.

---

## Observações

- Todos os papéis e responsabilidades devem ser revisados semestralmente.
- Políticas de qualidade podem ser ajustadas conforme evolução do negócio.