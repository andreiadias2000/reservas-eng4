import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from tabulate import tabulate
from abc import ABC, abstractmethod

# Dados pré-cadastrados
salas = {
    'A': 'Salão de Festas',
    'B': 'Churrasqueira 1',
    'C': 'Churrasqueira 2',
    'D': 'Churrasqueira 3',
    'E': 'Churrasqueira 4'
}

# Apartamentos válidos e blocos
apartamentos_validos = [101, 102, 103, 104, 201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404, 501, 502, 503, 504]
bloco_apartamentos = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Reservas armazenadas
reservas = []

# Interface para as estratégias de notificação
class NotificacaoStrategy(ABC):
    @abstractmethod
    def enviar(self, destinatario, mensagem):
        pass

class NotificacaoEmail(NotificacaoStrategy):
    def enviar(self, destinatario, mensagem):
        print(f"Enviando email para {destinatario} com a mensagem: {mensagem}")
        # Aqui você pode adicionar a lógica real de envio de email usando smtplib

class NotificacaoWhatsApp(NotificacaoStrategy):
    def enviar(self, destinatario, mensagem):
        print(f"Enviando WhatsApp para {destinatario} com a mensagem: {mensagem}")
        # Aqui você pode adicionar a lógica real de envio de WhatsApp usando uma API específica

# Função para validar email
def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email)

# Função para validar telefone
def validar_telefone(telefone):
    return re.match(r'^\d{11}$', telefone)

# Função para verificar data válida
def validar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%d%m%Y')
        if data < datetime.now():
            print("Data retroativa! Tente novamente.")
            return False
        return data
    except ValueError:
        print("Data inválida! Use o formato DDMMYYYY.")
        return False

# Função para verificar horário
def validar_horario(horario):
    try:
        if len(horario) != 4 or not horario.isdigit():
            print("Horário inválido! Use o formato HHMM.")
            return False
        datetime.strptime(horario, '%H%M')
        return True
    except ValueError:
        print("Horário inválido! Use o formato HHMM.")
        return False

# Função para verificar se o apartamento já tem reserva no mês
def verificar_reserva_mes(apartamento, bloco, data):
    for reserva in reservas:
        if reserva['apartamento'] == apartamento and reserva['bloco'] == bloco:
            if reserva['data'].month == data.month and reserva['data'].year == data.year:
                print("Já existe uma reserva dentro deste mês/ano para este apartamento.")
                return True
    return False

# Função para cadastrar reserva
def cadastrar_reserva():
    print("Cadastro de Reserva")

    while True:
        nome = input("Digite o seu NOME ou 'sair' para cancelar: ").strip()
        if nome.lower() == 'sair':  # Permite cancelar a operação
            print("Operação cancelada.")
        if nome.isalpha() and len(nome) > 1:  # Verifica se o nome contém apenas letras e não está vazio
            continue
        print("O nome deve conter apenas letras e não pode estar vazio. Tente novamente ou digite 'sair' para cancelar.")
    
        if not nome:  # Verifica se o nome está vazio
            continue
        print("O nome não pode estar vazio. Tente novamente ou digite 'sair' para cancelar.")

    while True:
        apartamento = input("Digite o número do apartamento: ").strip()
        if apartamento.lower() == 'sair':
            return
        try:
            apartamento = int(apartamento)
            if apartamento not in apartamentos_validos:
                print("Número de apartamento inválido! Tente novamente.")
                continue
            break
        except ValueError:
            print("Formato inválido! O número do apartamento deve ser numérico.")

    while True:
        bloco = input("Digite a letra do bloco: ").upper().strip()
        if bloco.lower() == 'sair':
            print("Operação cancelada.")
            return
        if not bloco:
            print("O bloco não pode estar vazio. Tente novamente.")
            continue
        if bloco not in bloco_apartamentos:
            print("Bloco inválido! Tente novamente.")
        else:
            break

    while True:
        email = input("Digite seu email ou 'sair' para cancelar: ").strip()
        if email.lower() == 'sair':
            print("Operação cancelada.")
            return
        if validar_email(email):
            break
        print("Email inválido! Por favor, digite novamente ou digite 'sair' para cancelar.")

    while True:
        telefone = input("Digite seu telefone (somente números): ").strip()
        if telefone.lower() == 'sair':
            return
        if not validar_telefone(telefone):
            print("Telefone inválido! Insira 11 dígitos.")
            continue
        break

    print("Escolha uma sala:")
    for key, value in salas.items():
        print(f"{key}: {value}")

    while True:
        sala_escolhida = input("Digite a letra da sala desejada: ").upper().strip()
        if sala_escolhida == 'SAIR':
            print("Operação cancelada.")
            return
        if sala_escolhida not in salas:
            print("Sala inválida! Tente novamente.")
        else:
            print(f"Sala {salas[sala_escolhida]} escolhida com sucesso!")
            break

    while True:
        data_str = input("Digite a data da reserva (DDMMYYYY) ou digite 'sair' para cancelar: ").strip()
        if data_str.lower() == 'sair':
            return
        data_reserva = validar_data(data_str)
        if data_reserva:
            break
        print("Data inválida! Por favor, insira no formato correto (DDMMYYYY).")

    if verificar_reserva_mes(apartamento, bloco, data_reserva):
        return

    while True:
        horario_inicio = input("Digite o horário de início (HHMM) ou digite 'sair' para cancelar: ").strip()
        if horario_inicio.lower() == 'sair':
            return
        if validar_horario(horario_inicio):
            break
        print("Horário inválido! Certifique-se de usar o formato correto (HHMM).")

    while True:
        horario_fim = input("Digite o horário de término (HHMM) ou digite 'sair' para cancelar: ").strip()
        if horario_fim.lower() == 'sair':
            return
        if validar_horario(horario_fim):
            break
        print("Horário inválido! Certifique-se de usar o formato correto (HHMM).")

    reservas.append({
        'nome': nome,
        'apartamento': apartamento,
        'bloco': bloco,
        'email': email,
        'telefone': telefone,
        'sala': salas[sala_escolhida],
        'data': data_reserva,
        'horario_inicio': horario_inicio,
        'horario_fim': horario_fim
    })

    print(f"Reserva confirmada para {salas[sala_escolhida]} no dia {data_reserva.strftime('%d/%m/%Y')}")
    print("Sala deve ser entregue limpa, caso contrário, multa será aplicada.")

    # Escolher tipo de notificação
    while True:
        tipo_notificacao = input("Escolha o tipo de notificação: A para Email, B para WhatsApp: ").strip().upper()
        if tipo_notificacao == 'A':
            notificacao = NotificacaoEmail()
            notificacao.enviar(email, "Sua reserva foi confirmada com sucesso!")
            break
        elif tipo_notificacao == 'B':
            notificacao = NotificacaoWhatsApp()
            notificacao.enviar(telefone, "Sua reserva foi confirmada com sucesso!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Função para listar todas as reservas
def listar_reservas():
    if not reservas:
        print("Não há reservas no momento.")
        return

    reservas_formatadas = []
    for reserva in reservas:
        reservas_formatadas.append([
            reserva['sala'],
            reserva['data'].strftime('%d/%m/%Y'),
            reserva['horario_inicio'],
            reserva['horario_fim'],
            reserva['nome'],
            reserva['apartamento'],
            reserva['bloco']
        ])
    print(tabulate(reservas_formatadas, headers=['Sala', 'Data', 'Início', 'Fim', 'Nome', 'Apartamento', 'Bloco'], tablefmt='pretty'))

# Função para cancelar reserva
def cancelar_reserva():
    listar_reservas()
    reserva_id = input("Digite o número da reserva que deseja cancelar ou 'sair' para cancelar a operação: ").strip()
    if reserva_id.lower() == 'sair':
        return
    try:
        reserva_id = int(reserva_id)
        if reserva_id < 0 or reserva_id >= len(reservas):
            print("Reserva não encontrada!")
        else:
            reservas.pop(reserva_id)
            print(f"Reserva {reserva_id} cancelada com sucesso!")
    except ValueError:
        print("Entrada inválida! Tente novamente.")

# Função para menu principal
def menu():
    while True:
        print("\n----Menu Reservas -----:")
        print("1. Cadastrar reserva")
        print("2. Listar reservas")
        print("3. Cancelar reserva")
        print("4. Sair")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == '1':
            cadastrar_reserva()
        elif escolha == '2':
            listar_reservas()
        elif escolha == '3':
            cancelar_reserva()
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu()
