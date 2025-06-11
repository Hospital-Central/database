# Hospital Central - Sistema de Banco de Dados

Este repositório contém a implementação de um sistema de banco de dados para um hospital central utilizando Python e SQLAlchemy. O sistema gerencia pacientes, funcionários, consultas, internações, leitos, exames, agendamentos, faturas, prescrições e medicamentos.

---
## Estrutura do Projeto

- `app/`
  - `database/`
    - `models.py` - Define as tabelas e relacionamentos do banco (Pacientes, Funcionários, Consultas, etc).
    - `procedures.py` - Funções para criar e manipular os dados.
    - `triggers.py` - Funções que simulam triggers (ex: marcar leito indisponível, gerar fatura automática).
    - `setup.py` - Configuração da conexão com o banco e criação da base declarativa.
    - `__init__.py` - Torna a pasta um pacote Python.
  - `create_db.py` - Script para criar as tabelas no banco.
  - `main.py` - Exemplo de uso das funções para inserir e consultar dados.
- `.gitignore` - Arquivos e pastas ignorados pelo Git.
- `requirements.txt` - Dependências Python para rodar o projeto.

---

## Tecnologias Utilizadas

- Python 3.8+
- SQLAlchemy
- PyMySQL
- MySQL (servidor local)

---
## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/Hospital-Central/database.git](https://github.com/Hospital-Central/database.git)
    cd database
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure seu banco de dados MySQL** e atualize a string de conexão no arquivo `app/database/setup.py`:

    ```python
    engine = create_engine(
        'mysql+pymysql://root:senha@localhost:3306/Hospital',
        echo=True,
    )
    ```

---
## Como Usar

1.  **Crie o banco e tabelas:**
    Execute o script para criar o banco e as tabelas:

    ```bash
    python app/create_db.py
    ```

2.  **Testar as operações básicas:**
    Execute o script principal que cria alguns registros e demonstra o funcionamento básico:

    ```bash
    python app/main.py
    ```
    Este script irá:
    * Criar um paciente
    * Criar um funcionário
    * Criar um leito
    * Criar uma internação e atualizar a disponibilidade do leito
    * Criar um agendamento e gerar uma fatura automaticamente
    * Listar pacientes cadastrados

---
## Funcionalidades Principais

* **Models:** Definem as tabelas do banco e seus relacionamentos (Paciente, Funcionário, Consulta, Internação, Leito, Exame, Agendamento, Fatura, Prescrição e Medicamento).
* **Procedures:** Funções para criação e manipulação dos dados.
* **Triggers:** Funções que implementam regras de negócio, como marcar leitos como indisponíveis ao internar um paciente e gerar faturas automaticamente ao criar um agendamento.
* **Setup:** Configuração do engine e sessão do SQLAlchemy.

---
## Estrutura das Tabelas Principais

* **Paciente:** Dados do paciente, relaciona consultas, internações, exames, agendamentos, prescrições e faturas.
* **Funcionario:** Dados do funcionário, com cargo e especialidade.
* **Consulta:** Registro das consultas entre paciente e funcionário.
* **Internacao:** Internações de pacientes, com referência a leitos.
* **Leito:** Leitos disponíveis e suas características.
* **Exame:** Exames realizados.
* **Agendamento:** Agendamentos de consultas.
* **Fatura:** Faturas geradas para pacientes.
* **Prescricao:** Prescrições médicas com associação a medicamentos.
* **Medicamento:** Medicamentos disponíveis.

---
## Próximos Passos / Melhorias

* Adicionar autenticação e controle de acesso.
* Criar uma API REST para integrar com front-end.
* Implementar testes unitários.
* Tratar melhor exceções e validar dados.

---
## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Equipe de Desenvolvimento

- [Samara Araújo] (https://github.com/s4mnara)
- [Eveline Síntia] (https://github.com/EvelineSintia)
- [Ana Clara] (https://github.com/anacfmonte)
- [Adriel Gomes] (https://github.com/Adriel-grs)

---

Obrigado por usar o sistema Hospital Central!