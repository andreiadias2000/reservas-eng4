# Sistema de Reservas de Salas - Padrão Strategy

Este é um sistema de reservas de salas para um condomínio, desenvolvido em Python, que utiliza o **padrão de projeto Strategy** para implementar notificações via **e-mail** ou **WhatsApp**. O sistema permite o cadastro, listagem e cancelamento de reservas, com validações para garantir a integridade das informações.

## Funcionalidades

- **Cadastro de reservas**:
  - Validação de nome, e-mail, telefone, data e horário.
  - Verificação de disponibilidade da sala para o mesmo apartamento no mesmo mês.
  - Escolha de notificações por **e-mail** ou **WhatsApp**.

- **Listagem de reservas**:
  - Exibe todas as reservas em uma tabela formatada.

- **Cancelamento de reservas**:
  - Permite cancelar reservas existentes.

- **Notificações**:
  - Implementação com o padrão Strategy:
    - **E-mail**: Utiliza `smtplib` (simulado no momento).
    - **WhatsApp**: Requer integração com uma API (simulado no momento).

## Tecnologias Utilizadas

- Python 3
- Padrão de Projeto: **Strategy**
- Bibliotecas:
  - `tabulate` para exibição formatada de tabelas.
  - `datetime` para manipulação de datas e horários.
  - `re` para validação de e-mails e telefones.

## Como Usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/andreiadias2000/reservas-eng4.git
