import requests
import re
from modules import login
from constants import patient_create_payload, patient_update_payload

class TISaudeAPI:

    def __init__(self, LOGIN, PASSWORD):
        self.base_url = "https://api.tisaude.com/api"
        self.token = login.login(LOGIN, PASSWORD)
    

    # Retorna lista com horários disponíveis
    def get_horarios(self, id_calendar, date, local):
        url = f"{self.base_url}/schedule/filter/calendar/hours?idCalendar={id_calendar}&date={date}&local={local}"

        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        
        r = requests.get(url, headers=headers)
        return r.json().get('schedules')
    

    # Retorna 2upla com o ID e o nome do paciente
    def get_pacientes(self, name):
        url = f"{self.base_url}/patients?search={name}"

        headers = {
            'Authorization': 'Bearer ' + self.token
        }

        data = requests.get(url, headers=headers).json().get("data")
        
        if(len(data) <= 0):
            print("Paciente nao encontrado.")
            return None
        
        return data[0]["id"], data[0]["name"]
    
    def post_paciente(self, cpf, name):
        
        url = f"{self.base_url}/patients/create"

        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        
        patient_create_payload["name"] = name
        patient_create_payload["cpf"] = re.sub(r'\D', '', cpf)
        
        r = requests.post(url, headers=headers, json=patient_create_payload)
        if(r.status_code != 200):
            raise Exception("Fail in create patient", r.text)
        
        patient = r.json().get("patient")
        
        print(patient)
        return patient["id"], patient["name"]
    
    def put_paciente(self, name, id, cpf):
        
        url = f"{self.base_url}/patients/edit"

        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        
        patient_update_payload["name"] = name
        patient_update_payload["id"] = id
        patient_update_payload["cpf"] = re.sub(r'\D', '', cpf)
        
        r = requests.put(url, headers=headers, json=patient_update_payload)
        
        if(r.status_code != 200):
            raise Exception("Fail in update patient", r.text)
        
        print("cpf do paciente resgatado com sucesso.")
        print(r.json())
        
    

    # Retorna a resposta completa do agendamento
    def post_agendamento(self, id, nome, data, local, id_calendario, hora, procedimentos = 1):
        url = f"{self.base_url}/schedule/new"

        headers = {
                    'Authorization': 'Bearer ' + self.token,
                    'Content-Type': 'application/json'
                }
        
        payload = {
            "idPatient": id,
            "name": nome,
            "schedule": [
                {
                    "id": "",
                    "idScheduleReturn": None,
                    "dateSchudule": data,
                    "local": local,
                    "idCalendar": id_calendario,
                    "procedures": [
                        procedimentos
                    ],
                    "hour": hora
                }
            ]
        }

        r = requests.post(url, json=payload, headers=headers)
        return r