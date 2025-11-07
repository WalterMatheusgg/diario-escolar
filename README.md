```markdown
# 🏫 Sistema de Gestão Escolar

Sistema de gestão acadêmica desenvolvido em **Python 3** com **Tkinter** e **SQLite**, projetado para oferecer uma interface intuitiva e eficiente na administração de alunos, disciplinas, matrículas e notas.  
A aplicação foi desenvolvida com foco em **usabilidade, integridade de dados e escalabilidade**, podendo ser adaptada para instituições de diferentes portes.

---

## 📌 Sumário
1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Instalação e Execução](#instalação-e-execução)
6. [Banco de Dados](#banco-de-dados)
7. [Exportação e Backup](#exportação-e-backup)
8. [Destaques Técnicos](#destaques-técnicos)
9. [Autor](#autor)
10. [Licença](#licença)

---

## 📖 Visão Geral

O **Sistema de Gestão Escolar** tem como objetivo centralizar e automatizar processos administrativos de instituições de ensino, permitindo o gerenciamento completo de alunos, disciplinas, matrículas e notas em um ambiente integrado.

O sistema adota uma arquitetura modular, separando a interface gráfica, regras de negócio e persistência de dados em arquivos distintos, seguindo boas práticas de desenvolvimento e manutenção.

---

## ⚙️ Funcionalidades

### 👩‍🎓 Módulo de Alunos
- Cadastro de alunos com informações completas:
  - Nome completo  
  - Data de nascimento (com cálculo automático da idade)  
  - CPF, e-mail, telefone  
  - Endereço, série/turma, responsável e observações  
- Validação automática de dados e verificação de duplicidades.
- Matrícula gerada automaticamente.

### 📚 Módulo de Disciplinas
- Cadastro de disciplinas com:
  - Nome  
  - Professor responsável  
  - Turno (manhã, tarde, noite)  
  - Sala de aula  
  - Série vinculada  
- Integração direta com o módulo de matrículas e notas.

### 🧾 Módulo de Matrículas
- Associação de alunos às disciplinas compatíveis com sua série.
- Exibição automática das informações do aluno selecionado.
- Listagem das disciplinas nas quais o aluno está matriculado.

### 🧮 Módulo de Notas
- Lançamento de avaliações com:
  - Seleção de aluno e disciplina (apenas as disciplinas em que está matriculado)  
  - Tipo de avaliação (prova, trabalho, projeto, etc.)  
  - Validação de notas de 0 a 10  
- Prevenção de lançamentos duplicados e atualização automática da média.

### 👁️ Módulo de Visualização
- Consulta completa de informações:
  - Dados cadastrais do aluno  
  - Disciplinas matriculadas  
  - Notas e médias por disciplina  
- Visualização global ou individual.
- Exportação de relatórios em CSV com um clique.

---

## 🧩 Tecnologias Utilizadas

| Componente | Tecnologia |
|-------------|-------------|
| Linguagem | Python 3.x |
| Interface gráfica | Tkinter / ttk |
| Banco de dados | SQLite3 |
| Formato de exportação | CSV |
| Padrões de código | PEP 8 |

---

## 📁 Estrutura do Projeto

```

sistema_gestao_escolar_realista/
│
├── main.py                  # Interface principal (GUI)
├── banco.py                 # Conexão e operações no banco de dados SQLite
├── validacao.py             # Funções de validação de campos e regras de negócio
├── arquivo.py               # Módulo de exportação de dados em CSV
│
├── database/
│   └── escola_realista.db   # Banco de dados gerado automaticamente
│
├── arquivos/
│   ├── alunos.csv
│   ├── disciplinas.csv
│   ├── matriculas.csv
│   └── notas.csv
│
└── README.md

````

---

## 💻 Instalação e Execução

### Pré-requisitos
- **Python 3.6+**
- Sistema operacional compatível: Windows, Linux ou macOS
- Nenhum pacote externo é necessário (somente bibliotecas padrão do Python)

### Passos para execução
```bash
# 1. Clonar ou extrair o projeto
cd sistema_gestao_escolar_realista

# 2. Executar a aplicação
python main.py
````

---

## 🗄️ Banco de Dados

O sistema utiliza **SQLite3**, um banco de dados leve e local, armazenado em `database/escola_realista.db`.

### Estrutura das Tabelas

**Tabela `alunos`**

| Campo           | Tipo      | Descrição                    |
| --------------- | --------- | ---------------------------- |
| matricula       | TEXT (PK) | Identificador único do aluno |
| nome            | TEXT      | Nome completo                |
| data_nascimento | TEXT      | Data de nascimento           |
| cpf             | TEXT      | CPF                          |
| email           | TEXT      | E-mail                       |
| telefone        | TEXT      | Telefone                     |
| endereco        | TEXT      | Endereço completo            |
| serie           | TEXT      | Série/Turma                  |
| idade           | INTEGER   | Idade calculada              |

**Tabela `disciplinas`**

| Campo     | Tipo         | Descrição                   |
| --------- | ------------ | --------------------------- |
| id        | INTEGER (PK) | Identificador da disciplina |
| nome      | TEXT         | Nome da disciplina          |
| professor | TEXT         | Professor responsável       |
| turno     | TEXT         | Turno                       |
| sala      | TEXT         | Sala de aula                |
| serie     | TEXT         | Série vinculada             |

**Tabela `matriculas`**

| Campo           | Tipo         | Descrição                  |
| --------------- | ------------ | -------------------------- |
| id              | INTEGER (PK) | Identificador da matrícula |
| matricula_aluno | TEXT         | Matrícula do aluno         |
| id_disciplina   | INTEGER      | ID da disciplina vinculada |

**Tabela `notas`**

| Campo           | Tipo         | Descrição             |
| --------------- | ------------ | --------------------- |
| id              | INTEGER (PK) | Identificador da nota |
| matricula_aluno | TEXT         | Matrícula do aluno    |
| id_disciplina   | INTEGER      | ID da disciplina      |
| avaliacao       | TEXT         | Tipo de avaliação     |
| valor           | REAL         | Nota (0 a 10)         |

---

## 📤 Exportação e Backup

O sistema gera automaticamente arquivos CSV contendo:

* **alunos.csv**
* **disciplinas.csv**
* **matriculas.csv**
* **notas.csv**

Os arquivos são salvos na pasta `/arquivos/` e podem ser utilizados para análise externa ou importação em outros sistemas.

---

## 🧠 Destaques Técnicos

* Interface gráfica desenvolvida em **Tkinter com ttk**, organizada em abas.
* Arquitetura modular com separação clara entre interface, lógica e persistência.
* Combobox dinâmicas com **filtro por série e aluno**.
* Controle de duplicidade em matrículas e notas.
* Exportação rápida de dados em formato CSV.
* Código estruturado conforme padrões **PEP 8**.

---

## 👨‍💻 Autor

**Walter Matheus**  
Desenvolvedor Júnior Python especializado em automação, análise de dados e desenvolvimento de sistemas administrativos.  

📧 **E-mail:** [waltermatheus688@gmail.com](mailto:waltermatheus688@gmail.com)  
💼 **LinkedIn:** [linkedin.com/in/walter504](https://www.linkedin.com/in/walter504/)

---
## 🧾 Licença

Este projeto está licenciado sob a **MIT License**.
Você pode utilizá-lo, modificá-lo e distribuí-lo livremente, desde que mantenha os créditos originais.

---

<p align="center">
  © 2025 — Sistema de Gestão Escolar Realista<br>
  Desenvolvido com 💻 e ☕ por <b>Walter Matheus</b><br>
  <a href="https://www.linkedin.com/in/walter504/">LinkedIn</a> |
  <a href="https://github.com/WalterMatheus">GitHub</a>
</p>

