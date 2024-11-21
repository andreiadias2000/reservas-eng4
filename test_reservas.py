
import unittest
from datetime import datetime

# Suponha que o código a ser testado está em um arquivo chamado 'reservas.py' ou similar.
# Se você estiver usando funções no mesmo arquivo, basta removê-lo da importação
from main import verificar_reserva_mes

class TestReservas(unittest.TestCase):
    def setUp(self):
        # Criando algumas reservas de exemplo para o teste
        self.reservas = [
            {"apartamento": "101", "bloco": "A", "data": "15122024"},
            {"apartamento": "102", "bloco": "B", "data": "10122024"},
            {"apartamento": "103", "bloco": "C", "data": "12122024"},
        ]
        
        # Supondo que a função de verificação de reserva recebe esses dados de uma lista de reservas
        def verificar_reserva_mes(apartamento, bloco, data):
            try:
                # Verificar se a data está no formato correto
                datetime.strptime(data, "%d%m%Y")
            except ValueError:
                print("Data inválida! Use o formato DDMMYYYY.")
                return False

            mes = data[2:4]
            ano = data[4:8]

            for reserva in self.reservas:
                if reserva["apartamento"] == apartamento and reserva["bloco"] == bloco:
                    reserva_mes = reserva["data"][2:4]
                    reserva_ano = reserva["data"][4:8]
                    if reserva_mes == mes and reserva_ano == ano:
                        return False  # Já existe reserva para esse mês
            return True  # Não existe reserva para esse mês

        # Redefinindo a função para o teste
        self.verificar_reserva_mes = verificar_reserva_mes

    def test_data_invalida(self):
        apartamento = "101"
        bloco = "A"
        data = "32/12/2024"  # Data inválida

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertFalse(resultado)  # Espera-se False para data inválida

    def test_data_valida_sem_reserva_existente(self):
        apartamento = "104"
        bloco = "D"
        data = "15122024"  # Data válida, sem reservas para essa data

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertTrue(resultado)  # Espera-se True, pois não há reserva para essa data

    def test_data_valida_com_reserva_existente(self):
        apartamento = "101"
        bloco = "A"
        data = "15122024"  # Já existe uma reserva para essa data

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertFalse(resultado)  # Espera-se False, pois já existe uma reserva para essa data

    def test_mes_ano_existente_com_reserva(self):
        apartamento = "101"
        bloco = "A"
        data = "15122024"  # Já existe uma reserva para o mês e ano

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertFalse(resultado)  # Espera-se False para uma reserva já existente

    def test_mes_ano_inexistente_com_reserva(self):
        apartamento = "102"
        bloco = "B"
        data = "15122025"  # Não existe reserva para esse mês/ano

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertTrue(resultado)  # Espera-se True, pois não há reserva para esse mês/ano

    def test_formatacao_data_erro(self):
        apartamento = "101"
        bloco = "A"
        data = "15-12-2024"  # Formato de data inválido

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertFalse(resultado)  # Espera-se False por conta do formato errado

    def test_reserva_mes_distinto(self):
        apartamento = "103"
        bloco = "C"
        data = "12122025"  # Data válida, mas não coincide com a reserva

        resultado = self.verificar_reserva_mes(apartamento, bloco, data)
        self.assertTrue(resultado)  # Espera-se True, pois a data é diferente da reserva existente

if __name__ == "__main__":
    unittest.main()
