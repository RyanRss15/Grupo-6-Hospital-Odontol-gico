import requests
from modules import login

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
    def get_pacientes(self, cpf):
        url = f"{self.base_url}/patients?search={cpf}"

        headers = {
            'Authorization': 'Bearer ' + self.token
        }

        r = requests.get(url, headers=headers)
        return r.json().get("data")[0]["id"], r.json().get("data")[0]["name"]
    

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