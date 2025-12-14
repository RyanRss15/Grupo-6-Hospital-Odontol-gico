import agendamento

def cli():
    cmd = ""
    print("Bem-vindo ao sistema de agendamento automático.")

    print("Insira o Login e a Senha para continuar.")
    login = input("Login: ")
    senha = input("Senha: ")

    id_agenda = input("Insira o ID da agenda (calendário): ") # 280
    n_pacientes = input("Insira quantos pacientes deseja agendar: ")
    n_dias = input("Insira quantos dias a partir de hoje deseja preencher: ")
    print("Lendo planilha e exibindo prévia dos agendamentos...")
    agendamento.agendamento(login, senha, int(n_pacientes), int(n_dias) + 1, int(id_agenda))
    while cmd.upper() != "X":
        cmd = input("Insira 'X' para sair: ")