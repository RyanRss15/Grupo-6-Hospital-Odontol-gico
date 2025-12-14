from datetime import datetime, timedelta
from scripts_iniciais import agendamento_automatico as planilhas
import api

def agendamento(login, senha, n_pacientes, n_dias, id_agenda = 280):

    data_hoje = datetime.now()                      # (YYYY-MM-DD) Data atual do sistema
    local = 1                                       # 1 = Geral/CONSULTÓRIO; 2 = CIn; 3 = CCM
    pacientes_agendados = 0
    agendamentos = {}
    ti_saude_api = api.TISaudeAPI(login, senha)
    confirmar = 0
    
    for dia in range(n_dias):

        if( pacientes_agendados >= n_pacientes):
            break

        data_agendamento = (data_hoje + timedelta(days=dia)).strftime("%Y-%m-%d")
        data_agendamento_f = (data_hoje + timedelta(days=dia)).strftime("%d/%m/%Y")
        horarios_response = ti_saude_api.get_horarios(id_agenda, data_agendamento, local)
        if len(horarios_response) > 0:
            horarios_disponveis = [item["hour"][:5] for item in horarios_response]
            agendamentos[data_agendamento_f] = planilhas.agendar_pacientes(planilhas.carregar_lista_espera(), horarios_disponveis, n_pacientes - pacientes_agendados, pacientes_agendados)
            pacientes_agendados += len(agendamentos[data_agendamento_f])

    print("Prévia dos agendamentos:")
    for data in agendamentos.keys():
        print(data)

        for agendamento in agendamentos[data]:
            print(f" - {agendamento['Nome']} \t| {agendamento['CPF']} \t| {agendamento['Horario']}")

    confirmar = input(f"\nConfirma os agendamentos acima? (S/N): ")
    if confirmar.upper() == "S":
        
        for data in agendamentos.keys():
            for i in range(len(agendamentos[data])):
                id_paciente, nome_paciente = ti_saude_api.get_pacientes(agendamentos[data][i]["CPF"])
                print(f"Agendando paciente {nome_paciente}...")
                resposta_agendamento = ti_saude_api.post_agendamento(
                    id_paciente,
                    nome_paciente,
                    data,
                    local,
                    id_agenda,
                    agendamentos[data][i]["Horario"]
                )
                if(resposta_agendamento.status_code == 200):
                    print(f"SUCESSO")
                else:
                    print(f"FALHA: {resposta_agendamento.text}")