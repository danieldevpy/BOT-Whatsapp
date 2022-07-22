import funcoes
from selenium.webdriver.common.keys import Keys
import datetime

mesma_linha = [Keys.SHIFT, Keys.ENTER, Keys.SHIFT]


class Structure:

    def __init__(self, number, message, text_field):
        self.number = number
        self.message = message
        self.text_field = text_field
        ######
        people = funcoes.Information(self.number).get()

        if people:
            self.bd = people[0]
            self.position = people[1]
            self.nameFile = people[2]
            self.name = people[3]
            self.unity = people[4]
            self.sector = people[5]
            self.stage = people[6]
            self.bankMessage = people[7]
            self.active = people[8]


class Decision(Structure):
    # Classe responsavel por responder
    def reply(self):
        # Caso seja o primeiro contato com o bot
        if self.active == 0:
            data = int(str(datetime.datetime.now())[11:13])
            if data < 12:
                salute = 'Bom dia'
            elif data < 18:
                salute = 'Boa Tarde'
            elif data >= 18:
                salute = 'Boa Noite'
            else:
                salute = 'Tudo bem?'
            self.text_field.send_keys(
                f'Olá, {salute}! Sou *CisBoot*, o robô virtual do CISBAF, para começarmos digite o seu *nome*!',
                Keys.ENTER)
            funcoes.Update(self.number).updateActive(1)
        # Aqui o bot estará pegando a unidade
        elif self.name == 'empty' and self.active == 1:
            funcoes.Update(self.number).updateName(self.message)
            self.text_field.send_keys(f'*Obrigado {self.message}*, me diga qual é a sua *unidade.* ', Keys.ENTER)
        # Aqui o bot estará pegando o setor
        elif self.unity == 'empty' and self.active == 1:
            funcoes.Update(self.number).updateUnity(self.message)
            self.text_field.send_keys(
                f'Porfavor, digite o *número* correspondente ao *setor* com que você deseja falar. ', mesma_linha)
            self.text_field.send_keys(
                f'*1*. Falar com o TI. ', mesma_linha)
            self.text_field.send_keys(
                f'*2*. Falar com o RH. ', Keys.ENTER)
        # Aqui começa a verificação da escolha dos setores
        elif self.sector == 0 and self.active == 1:
            if self.message == '1':
                funcoes.Update(self.number).updateSector(self.message)
                self.text_field.send_keys(
                    f'*Você escolheu o setor de TI, agora digite o número correspondente ao motivo do contato*. ',
                    mesma_linha)
                self.text_field.send_keys(
                    f'Digite *1* : Suporte Sistema SSO.', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *2* : Problemas com tablet. ', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *3* : Suporte para Computador/Impressora/Outros', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *4* : Atualizar WhatsApp', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *5* : Para falar com um tecnico', mesma_linha)
                self.text_field.send_keys(
                    f'*OBS: Sempre que precisar voltar para o inicio das opções digite 0.*', Keys.ENTER)
            elif self.message == '2':
                #funcoes.Update(self.number).updateSector(self.message)
                self.text_field.send_keys(
                    f'*O setor do RH está inativo!*. ', Keys.ENTER)
                self.text_field.send_keys(
                    f'*Digite 1 para falar com o TI!*. ', Keys.ENTER)
            elif self.message != 1 or self.message != 2:
                self.text_field.send_keys(
                    f'Porfavor, digite o *número* correspondente ao *setor* com que você deseja falar. ', mesma_linha)
                self.text_field.send_keys(
                    f'*1*. Falar com o TI. ', mesma_linha)
                self.text_field.send_keys(
                    f'*2*. Falar com o RH. ', Keys.ENTER)

        # Aqui será chamando quando a pessoa já teve o seu primeiro contato com o bot
        elif self.active == 2:
            funcoes.Update(self.number).updateActive(1)
            self.text_field.send_keys(
                f'Olá {self.name}! Porfavor, digite o *número* correspondente ao *setor* '
                f'com que você deseja falar. ', mesma_linha)
            self.text_field.send_keys(
                f'*1*. Falar com o TI. ', mesma_linha)
            self.text_field.send_keys(
                f'*2*. Falar com o RH. ', Keys.ENTER)
        #  Após escolher o setor de TI
        if self.sector == 1:

            try:
                new_stage = self.stage[0]
            except RuntimeError:
                new_stage = '0'

            # Escolha do primeiro menu, no valor 1
            if self.stage == '0' and self.message == '1' or self.stage == '0.0' and self.message == '1' \
                    or new_stage == '1':
                if self.stage == '0' and self.message == '1' or self.stage == '0.0' and self.message == '1':
                    funcoes.Update(self.number).updateStage('1.0')
                    self.text_field.send_keys(
                        f'*Entendido, diga o que você precisa!*', mesma_linha)
                    self.text_field.send_keys(
                        f'*1*. Problema na hora do login', mesma_linha)
                    self.text_field.send_keys(
                        f'*2*. Criação de login', Keys.ENTER)

                elif self.stage == '1.0' and self.message == '1':
                    funcoes.Update(self.number).updateStage('1.1')
                    self.text_field.send_keys(f'Digite um *texto* explicando o problema que ele será passado'
                                              f' para o setor de TI!', Keys.ENTER)
                elif self.stage == '1.1' and self.message != '0':
                    # Finalizando o chamado
                    finality = f'Problema na hora do login: {self.message}'
                    funcoes.Finish(self.name, self.unity, finality, self.bd, self.position)
                    self.text_field.send_keys(
                        f'*Seu problema foi enviado para o suporte por favor aguarde o contato!*', Keys.ENTER)

                elif self.stage == '1.0' and self.message == '2':
                    funcoes.Update(self.number).updateStage('1.2')
                    self.text_field.send_keys(
                        'Entendido, para criar o login, digite o seu *nome completo*', Keys.ENTER)
                elif self.stage == '1.2':
                    funcoes.Update(self.number).updateStage('1.21')
                    funcoes.Update(self.number).updateMessage(self.message)
                    self.text_field.send_keys(
                        'Agora digite o seu *CPF*', Keys.ENTER)
                elif self.stage == '1.21':
                    funcoes.Update(self.number).updateStage('1.22')
                    funcoes.Update(self.number).updateMessage(f'nome: {self.bankMessage} cpf: {self.message}')
                    self.text_field.send_keys(
                        'Agora digite seu *CARGO*', Keys.ENTER)
                elif self.stage == '1.22' and self.message != '0':
                    # Finalizando o chamado
                    finality = f'Criar login: {self.bankMessage} cargo: {self.message}'
                    funcoes.Finish(self.name, self.unity, finality, self.bd, self.position)
                    self.text_field.send_keys('*O chamado para abertura de login foi criado, '
                                              'em breve você será contatado pela equipe de TI!!*', Keys.ENTER)
                else:
                    if self.message != '0':
                        self.text_field.send_keys(
                            f'*Entendido, diga o que você precisa!*', mesma_linha)
                        self.text_field.send_keys(
                            f'*1*. Problema na hora do login', mesma_linha)
                        self.text_field.send_keys(
                            f'*2*. Criação de login', Keys.ENTER)
            # Escolha do primeiro menu, no valor 2
            elif self.stage == '0' and self.message == '2' or self.stage == '0.0' and self.message == '1' \
                    or new_stage == '2':
                if self.stage == '0' and self.message == '2' or self.stage == '0.0' and self.message == '2':
                    funcoes.Update(self.number).updateStage('2')
                    self.text_field.send_keys(
                        f'*Qual tipo de problema?*', mesma_linha)
                    self.text_field.send_keys(
                        f'*1*. Ocorrencia não chega', mesma_linha)
                    self.text_field.send_keys(
                        f'*2*. Ocorrencia travada', mesma_linha)
                    self.text_field.send_keys(
                        f'*3*. Não consigo logar no sistema', mesma_linha)
                    self.text_field.send_keys(
                        f'*4*. Problemas físicos', mesma_linha)
                    self.text_field.send_keys(
                        f'*5*. Tablet não carrega', Keys.ENTER)
                elif self.stage == '2' and self.message == '1' or self.stage == '2' and self.message == '2' or\
                        self.stage == '2' and self.message == '3':
                    funcoes.Update(self.number).updateStage('2.1')
                    self.text_field.send_keys(
                        f'Verifique o sinal de internet (Dados Móveis), desligue o wifi e reinicie o equipamento.',
                        mesma_linha)
                    self.text_field.send_keys( f'O problema foi solucionado?',mesma_linha)
                    self.text_field.send_keys(f'*1*. SIM', mesma_linha)
                    self.text_field.send_keys(f'*2*. NÃO', Keys.ENTER)
                if self.message == "1":
                    funcoes.Update(self.number).updateMessage('Problema no tablet: Ocorrencia não chega')
                elif self.message == '2':
                    funcoes.Update(self.number).updateMessage('Problema no tablet: Ocorrencia travada')
                elif self.message == '3':
                    funcoes.Update(self.number).updateMessage('Problema no tablet: SSO não loga')
                elif self.message == '4':
                    funcoes.Update(self.number).updateStage('2.2')
                    self.text_field.send_keys(f'Digite um *texto* explicando o problema que ele será passado para '
                                              f'o setor de TI!', Keys.ENTER)
                elif self.message == '5':
                    finality = f'Problema no tablet: Tablet não carrega'
                    self.text_field.send_keys(f'*Seu problema foi enviado para o suporte por favor aguarde o contato!*',
                                              Keys.ENTER)
                    # Finalizando chamado
                    funcoes.Finish(self.name, self.unity, finality, self.bd, self.position)
                else:
                    if self.message != '0':
                        self.text_field.send_keys(
                            f'*Qual tipo de problema?*', mesma_linha)
                        self.text_field.send_keys(
                            f'*1*. Ocorrencia não chega', mesma_linha)
                        self.text_field.send_keys(
                            f'*2*. Ocorrencia travada', mesma_linha)
                        self.text_field.send_keys(
                            f'*3*. Não consigo logar no sistema', mesma_linha)
                        self.text_field.send_keys(
                            f'*4*. Problemas físicos', mesma_linha)
                        self.text_field.send_keys(
                            f'*5*. Tablet não carrega', Keys.ENTER)
                if self.stage == '2.1':
                    if self.message == '1':
                        funcoes.resetValues(self.bd, self.position, self.nameFile)
                        self.text_field.send_keys(
                            f'Que bom que você conseguiu resolver o problema, ficamos felizes '
                            f'que podemos te ajudar! Qualquer coisa entre em contato!', Keys.ENTER)
                    elif self.message == '2':
                        self.text_field.send_keys(
                            f'*Seu problema foi enviado para o suporte por favor aguarde o contato!*',
                            Keys.ENTER)
                        # Finalizando chamado
                        funcoes.Finish(self.name, self.unity, self.bankMessage, self.bd, self.position)
                if self.stage == '2.2' and self.message != '0':
                    funcoes.Finish(self.name, self.unity, self.message, self.bd, self.position)
                    self.text_field.send_keys(
                        f'*Seu problema foi enviado para o suporte por favor aguarde o contato!*',
                        Keys.ENTER)

            # Escolha do primeiro menu, no valor 3
            elif self.stage == '0' and self.message == '3' or self.stage == '0.0' and self.message == '3' \
                    or new_stage == '3':
                if self.stage == '0' and self.message == '3' or self.stage == '0.0' and self.message == '3':
                    funcoes.Update(self.number).updateStage('3')
                    self.text_field.send_keys(
                        f'Por favor digite um *texto* explicando o seu problema detalhadamente!', Keys.ENTER)
                elif self.stage == '3' and self.message != '0':
                    funcoes.Finish(self.name, self.unity, self.message, self.bd, self.position)
                    self.text_field.send_keys(
                        f'*Seu problema foi enviado para o suporte por favor aguarde o contato!*', Keys.ENTER)

            # Escolha do primeiro menu, no valor 4
            elif self.stage == '0' and self.message == '4' or self.stage == '0.0' and self.message == '4' \
                    or new_stage == '4':
                if self.stage == '0' and self.message == '4' or self.stage == '0.0' and self.message == '4':
                    finality = 'deseja atualizar o whatsapp'
                    funcoes.Finish(self.name, self.unity, finality, self.bd, self.position)
                    self.text_field.send_keys(
                        f'*Ok! Aguarde o suporte entrar em contato, para atualizar o seu Whatsapp!*', Keys.ENTER)

            # Escolha do primeiro menu, no valor 5
            elif self.stage == '0' and self.message == '5' or self.stage == '0.0' and self.message == '5' \
                    or new_stage == '5':
                if self.stage == '0' and self.message == '5' or self.stage == '0.0' and self.message == '5':
                    funcoes.Update(self.number).updateStage('5')
                    self.text_field.send_keys(
                        f'*{self.name}* me diga o motivo do contato, que abriremos uma solitação e o '
                        f'suporte logo entrará em contato!', Keys.ENTER)
                elif self.stage == '5' and self.message != '0':
                    finality = f'Suporte solicitado: {self.message}'
                    funcoes.Finish(self.name, self.unity, finality, self.bd, self.position)
                    self.text_field.send_keys(
                        f'*A solicitação foi aberta e o suporte entrará em contato!*', Keys.ENTER)
            else:
                self.text_field.send_keys(
                    f'*Você escolheu o setor de TI, agora digite o número correspondente ao motivo do contato*. ',
                    mesma_linha)
                self.text_field.send_keys(
                    f'Digite *1* : Suporte Sistema SSO.', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *2* : Problemas com tablet. ', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *3* : Suporte para Computador/Impressora/Outros', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *4* : Atualizar WhatsApp', mesma_linha)
                self.text_field.send_keys(
                    f'Digite *5* : Para falar com um tecnico', mesma_linha)
                self.text_field.send_keys(
                    f'*OBS: Sempre que precisar voltar para o inicio das opções digite 0.*', Keys.ENTER)
        # Após escolher o setor do RH
        elif self.sector == 2:
            pass

        # Se o usuario quiser voltar para o menu
        if self.message == '0':
            funcoes.resetValues(self.bd, self.position, self.nameFile)
            self.text_field.send_keys(
                f'Olá {self.name}! Porfavor, digite o *número* correspondente ao *setor* '
                f'com que você deseja falar. ', mesma_linha)
            self.text_field.send_keys(
                f'*1*. Falar com o TI. ', mesma_linha)
            self.text_field.send_keys(
                f'*2*. Falar com o RH. ', Keys.ENTER)
