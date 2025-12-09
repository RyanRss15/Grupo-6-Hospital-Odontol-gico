# Passo a passo da requisição (nesse momento falta só fazer o código, levando em consideração a iteração dos dias para verificação da data e vagas disponiveis, colocar para fazer o preenchimento de vagas a partir de uma determinada quantidade que for informada e buscar fazer o relatório de agendamentos marcados automaticamente em pdf, a partir da API, passando a info do calendário do perfil da clínica desejado, o tipo de situação que quer verificar, a de pacientes marcados, o periodo que é o mês em questão, a clínica qual o profissional(perfil da clínica) está localizado e o procedimento, que é consulta), a partir disso deve ser gerado um relatório dos pacientes marcados para aquela clínica para o procedimento de consulta

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
