# RealEstatePortal

## Descrição
O **RealEstatePortal** é um sistema completo para gerenciamento de um portal imobiliário, permitindo a gestão de imóveis, agentes, clientes, visitas, análises de mercado, financiamentos e avaliações.

## Funcionalidades Principais
O sistema oferece as seguintes funcionalidades, organizadas em um menu principal:

### Gerenciamento de Usuários
- Cadastro e autenticação de usuários
- Perfis de acesso diferenciados

### Gestão de Imóveis
- Cadastro, edição e remoção de imóveis
- Busca e filtragem de propriedades
- Detalhes completos de cada imóvel

### Agentes Imobiliários
- Criação e gerenciamento de perfis
- Atribuição de imóveis

### Clientes
- Cadastro de clientes 
- Preferências e histórico de visitas

### Visitas
- Agendamento de visitas
- Confirmação e cancelamento
- Acompanhamento de visitas realizadas

### Análise de Mercado
- Relatórios de tendências
- Preços médios por região

### Financiamento Imobiliário
- Simulação de financiamentos
- Cálculo de parcelas

### Avaliações
- Feedback de clientes
- Classificação de propriedades

## Estrutura do Projeto

### Models (Classes)
As classes representam as entidades do sistema na pasta `models/`:

- **`user.py`** - Usuários do sistema (agentes e clientes (por ora sem administradores))
- **`property.py`** - Imóveis cadastrados no sistema
- **`agent.py`** - Agentes imobiliários
- **`client.py`** - Clientes interessados em imóveis
- **`visit.py`** - Agendamentos de visitas
- **`market_analysis.py`** - Análises e relatórios de mercado
- **`mortgage.py`** - Simulações de financiamento
- **`review.py`** - Avaliações e feedbacks

### Controllers
Os controllers na pasta `controllers/` gerenciam a lógica de negócio:

- **`user_controller.py`** - Autenticação e gerenciamento de usuários
- **`property_controller.py`** - Operações com imóveis
- **`agent_controller.py`** - Gestão de agentes
- **`client_controller.py`** - Gestão de clientes
- **`visit_controller.py`** - Agendamento de visitas
- **`market_analysis_controller.py`** - Geração de relatórios de mercado
- **`mortgage_controller.py`** - Simulações de financiamento
- **`review_controller.py`** - Gestão de avaliações

## Outros Arquivos Importantes
- **`database.py`** - Simulação de banco de dados (repository)
- **`main.py`** - Ponto de entrada da aplicação

## Como Executar

1. Certifique-se de ter **Python 3.12** instalado.
4. Execute o arquivo principal:
   ```sh
   python main.py
   ```

## Tecnologias Utilizadas
- **Python**
- **Programação Orientada a Objetos (POO)**
