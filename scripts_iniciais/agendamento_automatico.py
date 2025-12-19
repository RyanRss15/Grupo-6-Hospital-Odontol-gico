import pandas as pd
from openpyxl import load_workbook
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PADRAO = os.path.join(BASE_DIR, "lista_de_espera.xlsx")

def carregar_lista_espera(caminho_excel=CAMINHO_PADRAO):
    if not os.path.exists(caminho_excel):
        print(f"ERRO: O arquivo não foi encontrado: {caminho_excel}")
        sys.exit()
        
    df = pd.read_excel(caminho_excel, engine='openpyxl')
    return df

def agendar_pacientes(lista_espera, horarios, limite_pacientes, pular_pacientes=0):
    agendamentos = []

    qtd_disponivel_na_lista = len(lista_espera) - pular_pacientes
    qtd_agendar = min(len(horarios), limite_pacientes, qtd_disponivel_na_lista)

    if qtd_agendar <= 0:
        return []

    for i in range(qtd_agendar):
        idx_real = pular_pacientes + i
        paciente = lista_espera.iloc[idx_real]

        agendamentos.append({
            "Nome": paciente.get("Nome", "Desconhecido"),
            "CPF": str(paciente.get("CPF", "N/A")),
            "Horario": horarios[i]
        })

    return agendamentos

def salvar_agendamentos_append(agendamentos, nome_clinica):
    if not agendamentos:
        return

    df_novos = pd.DataFrame(agendamentos)
    nome_arquivo = f"agendamentos_{nome_clinica.replace(' ', '_')}.xlsx"
    
    if os.path.exists(nome_arquivo):
        print(f"Atualizando Excel de agendamentos: {nome_arquivo}")
        with pd.ExcelWriter(nome_arquivo, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            try:
                df_existente = pd.read_excel(nome_arquivo)
                start_row = len(df_existente) + 1 
                header = False 
            except ValueError: 
                start_row = 0
                header = True

            df_novos.to_excel(writer, index=False, header=header, startrow=start_row)
    else:
        print(f"Criando novo arquivo Excel: {nome_arquivo}")
        df_novos.to_excel(nome_arquivo, index=False)

def remover_agendados_cirurgico(qtd_a_remover, caminho_arquivo=CAMINHO_PADRAO):
    if qtd_a_remover == 0:
        return

    print(f"Removendo {qtd_a_remover} pacientes do topo da lista de espera...")
    
    wb = load_workbook(caminho_arquivo)
    ws = wb.active 
    ws.delete_rows(2, amount=qtd_a_remover)
    wb.save(caminho_arquivo)
    
    print("Lista de espera atualizada com sucesso!")