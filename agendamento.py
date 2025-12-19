from datetime import datetime, timedelta
from scripts_iniciais import agendamento_automatico as planilhas
import api
import sys

def agendamento(login, senha, n_pacientes, n_dias, id_agenda = 280):

    data_hoje = datetime.now()
    local = 1 # 1 = Geral/CONSULTÓRIO

    print("Carregando lista de espera...")
    df_lista_espera = planilhas.carregar_lista_espera()
    
    if df_lista_espera.empty:
        print("A lista de espera está vazia! Encerrando.")
        return

    pacientes_agendados_count = 0
    dict_agendamentos_previa = {}
    ti_saude_api = api.TISaudeAPI(login, senha)
    
    print("Buscando horários e montando prévia...")

    for dia in range(n_dias):
        if pacientes_agendados_count >= n_pacientes:
            break

        data_agendamento = (data_hoje + timedelta(days=dia)).strftime("%Y-%m-%d")
        data_agendamento_f = (data_hoje + timedelta(days=dia)).strftime("%d/%m/%Y")

        try:
            horarios_response = ti_saude_api.get_horarios(id_agenda, data_agendamento, local)
        except Exception as e:
            print(f"Erro ao buscar horários para {data_agendamento_f}: {e}")
            continue

        if len(horarios_response) > 0:
            horarios_disponiveis = [item["hour"][:5] for item in horarios_response]

            novos_agendados = planilhas.agendar_pacientes(
                lista_espera=df_lista_espera, 
                horarios=horarios_disponiveis, 
                limite_pacientes=n_pacientes - pacientes_agendados_count,
                pular_pacientes=pacientes_agendados_count
            )
            
            if novos_agendados:
                dict_agendamentos_previa[data_agendamento_f] = novos_agendados
                pacientes_agendados_count += len(novos_agendados)

    if not dict_agendamentos_previa:
        print("Não foi possível agendar ninguém (sem horários ou lista vazia).")
        return

    print("\n=== PRÉVIA DOS AGENDAMENTOS ===")
    for data, lista_pct in dict_agendamentos_previa.items():
        print(f"\nData: {data}")
        for ag in lista_pct:
            print(f" - {ag['Horario']} | {ag['Nome']} | CPF: {ag['CPF']}")

    confirmar = input(f"\nConfirma o agendamento de {pacientes_agendados_count} pacientes? (S/N): ")
    
    if confirmar.upper() == "S":
        todos_agendamentos_sucesso = []

        for data_str, lista_pct in dict_agendamentos_previa.items():
            dt_obj = datetime.strptime(data_str, "%d/%m/%Y")
            data_api = dt_obj.strftime("%d-%m-%Y")

            for pct in lista_pct:
                try:
                    paciente = ti_saude_api.get_pacientes(pct["Nome"])
                    
                    if paciente == None:
                        print("Criando paciente...")
                        paciente = ti_saude_api.post_paciente(pct["CPF"], pct["Nome"]);
                    
                    id_paciente, nome_paciente = paciente
                    print(f"Agendando {nome_paciente} em {data_str} às {pct['Horario']}...", end="")
                    
                    resposta_agendamento = ti_saude_api.post_agendamento(
                        id_paciente,
                        nome_paciente,
                        data_api,
                        local,
                        id_agenda,
                        pct["Horario"]
                    )

                    if resposta_agendamento.status_code == 200:
                        print(" SUCESSO")
                        pct['Data'] = data_str
                        todos_agendamentos_sucesso.append(pct)
                        
                        # try:
                        #     ti_saude_api.put_paciente(nome_paciente, id_paciente, pct["CPF"])
                        # except:
                        #     print("Cpf do paciente perdido no meio do processo.")
                    else:
                        print(f" FALHA: {resposta_agendamento.text}")
                
                except Exception as e:
                    print(f" ERRO TÉCNICO: {e}")

        if todos_agendamentos_sucesso:
            print("\nAtualizando planilhas locais...")

            planilhas.salvar_agendamentos_append(todos_agendamentos_sucesso, "Clinica_Geral")

            planilhas.remover_agendados_cirurgico(len(todos_agendamentos_sucesso))
            
        else:
            print("Nenhum agendamento foi efetivado na API.")

    else:
        print("Operação cancelada pelo usuário.")