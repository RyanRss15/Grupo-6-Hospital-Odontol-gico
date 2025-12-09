import pandas as pd
import sys
import os

def carregar_lista_espera(caminho_excel):
    print(f"Lendo arquivo em: {caminho_excel}")
    if not os.path.exists(caminho_excel):
        print("ERRO: O arquivo não foi encontrado neste caminho.")
        sys.exit()
        
    df = pd.read_excel(caminho_excel, engine='openpyxl')
    return df

def agendar_pacientes(lista_espera, horarios):
    agendamentos = []
    qtd_agendar = min(len(lista_espera), len(horarios))

    for i in range(qtd_agendar):
        paciente = lista_espera.iloc[i]

        data_bruta = paciente.get("Nascimento", "N/A")
        data_formatada = data_bruta
        
        if hasattr(data_bruta, 'strftime'):
            data_formatada = data_bruta.strftime('%d/%m/%Y')

        agendamentos.append({
            "Nome": paciente.get("Nome", "Desconhecido"),
            "CPF": paciente.get("CPF", "N/A"),
            "Telefone": paciente.get("Telefone", "N/A"),
            "Nascimento": data_formatada,
            "Horário": horarios[i]
        })

    return agendamentos

def salvar_agendamentos(agendamentos, nome_clinica):
    if not agendamentos:
        print("Nenhum agendamento foi criado.")
        return

    df = pd.DataFrame(agendamentos)
    nome_arquivo = f"agendamentos_{nome_clinica.replace(' ', '_')}.xlsx"
    
    df.to_excel(nome_arquivo, index=False)
    print(f"\n Arquivo de agenda gerado: {nome_arquivo}")


def remover_agendados_da_fila(lista_espera_df, qtd_agendada, caminho_arquivo_original):
    if qtd_agendada == 0:
        return

    nova_lista_espera = lista_espera_df.iloc[qtd_agendada:]

    nova_lista_espera.to_excel(caminho_arquivo_original, index=False)
    print(f"Lista de espera atualizada! {qtd_agendada} pessoas removidas da fila.")
    print(f"Restam {len(nova_lista_espera)} pessoas na espera.")


def main():
    url = r"" #colocar o caminho para o arquivo exel xlsx

    print("=== Sistema de Agendamento Automático ===")
    clinica = input("Nome da clínica: ")

    print("\nDigite os horários disponíveis separados por vírgulas.")
    print("Exemplo: 08:00, 08:30, 09:00")
    horarios_input = input("Horários: ")
    
    horarios = [h for h in horarios_input.split(",")]

    if not horarios:
        print("Nenhum horário informado. Encerrando.")
        return

    lista_espera = carregar_lista_espera(url)
    print(f"Lista de espera carregada com {len(lista_espera)} pacientes.")

    agendamentos = agendar_pacientes(lista_espera, horarios)

    if agendamentos:
        print("\n--- PACIENTES AGENDADOS AGORA ---")
        for p in agendamentos:
            print(f" {p['Horário']} - {p['Nome']} (Tel: {p['Telefone']})")
        print("---------------------------------")
    else:
        print("\nNinguém foi agendado (lista vazia ou sem horários).")

    salvar_agendamentos(agendamentos, clinica)

    if agendamentos:
        remover_agendados_da_fila(lista_espera, len(agendamentos), url)

if __name__ == "__main__":
    main()