# Passo a passo da requisição

Get login com o acesso do atendente do Napa(pessoa responsavel pelo processo de agendamento dos pacientes) 
pegaria o token automaticamente e faria a autenticação para as requisições

~~Get calendars puxa todos os calendários dos profissionais, a partir disso puxamos o nome da clínica e pegamos o id do calendário da clínica específica;~~

~~Get médico puxa todos os perfis de profissionais cadastrados, a partir disso procuramos o nome da clínica do perfil e pega o id do médico~~

Get Horarios passando como parâmetro o id ca clínica e uma data específica retorna os horários disponivéis(os que ainda não há marcação) nos dias que possuem horarios, e retorna nada nos dias que não possuem;
Itera os dias para verificação a partir do dia da requisição, e vai verificando 1 a 1, até preencher a quantidade de vagas pedidas;

quando acha um horario disponivel, a api vai acessar a planilha com mesmo nome do perfil que estará no mesmo diretório do programa.
da planilha específica, ele resgata os dados do primeiro paciente(considerando que a planilha estivesse já devidamente ordenada)

get paciente pesquisando pelo cpf retornando id do paciente, pega o nome do paciente no ti saúde

post agendamento, para o dia e horario encontrado no id do calendário da clínica específica, no get post coloca nome do paciente, id do paciente, data e hora que estava disponivel, id do calendário e id do local da clínica(do geral)
