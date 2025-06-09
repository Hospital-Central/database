import datetime
import pymysql  # ou use outro conector que você usa

# Conexão com o banco
conn = pymysql.connect(
    host='localhost',
    user='seu_usuario',
    password='sua_senha',
    db='seu_banco',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def atualiza_disponibilidade_leito(id_leito):
    with conn.cursor() as cursor:
        sql = "UPDATE Leito SET Disponivel = FALSE WHERE ID_Leito = %s"
        cursor.execute(sql, (id_leito,))
    conn.commit()

def libera_leito_apos_alta(id_leito, data_saida_old, data_saida_new):
    if data_saida_old is None and data_saida_new is not None:
        with conn.cursor() as cursor:
            sql = "UPDATE Leito SET Disponivel = TRUE WHERE ID_Leito = %s"
            cursor.execute(sql, (id_leito,))
        conn.commit()

def gera_fatura_apos_agendamento(id_paciente):
    with conn.cursor() as cursor:
        sql = """
        INSERT INTO Fatura (Data_Emissao, Valor, Status_Pagamento, ID_Paciente)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (datetime.datetime.now(), 100.00, 'Pendente', id_paciente))
    conn.commit()


# Quando inserir uma nova internação:
def inserir_internacao(id_leito, outros_campos):
    with conn.cursor() as cursor:
        # Inserção
        sql = "INSERT INTO Internacao (ID_Leito, ...) VALUES (%s, ...)"
        cursor.execute(sql, (id_leito, ...))
    conn.commit()
    atualiza_disponibilidade_leito(id_leito)

# Quando atualizar uma internação (para alta):
def atualizar_internacao(id_internacao, data_saida_old, data_saida_new, id_leito):
    with conn.cursor() as cursor:
        sql = "UPDATE Internacao SET Data_Saida=%s WHERE ID_Internacao=%s"
        cursor.execute(sql, (data_saida_new, id_internacao))
    conn.commit()
    libera_leito_apos_alta(id_leito, data_saida_old, data_saida_new)

# Quando inserir um agendamento:
def inserir_agendamento(id_paciente, outros_campos):
    with conn.cursor() as cursor:
        sql = "INSERT INTO Agendamento (ID_Paciente, ...) VALUES (%s, ...)"
        cursor.execute(sql, (id_paciente, ...))
    conn.commit()
    gera_fatura_apos_agendamento(id_paciente)
