import pandas
import requests
import threading

nameFile = 'bancodedados.xlsx'

# noinspection PyArgumentList
class Information:

    def __init__(self, number):
        self.nameFile = nameFile
        self.lista = []
        self.number = number
        self.bd = pandas.read_excel(nameFile)

        searchNumber = self.bd["numero"].values

        for num in searchNumber:
            self.lista.append(num)

        if self.number in self.lista:
            self.position = self.lista.index(self.number)
            self.name = str(list(self.bd.loc[self.position, ["nome"]]))[2:-2]
            self.unity = str(list(self.bd.loc[self.position, ["unidade"]]))[2:-2]
            self.sector = int((self.bd.loc[self.position, ["setor"]]))
            self.stage = str(list(self.bd.loc[self.position, ["etapa"]]))[1:-1]
            self.message = str(list(self.bd.loc[self.position, ["msg"]]))[2:-2]
            self.active = int((self.bd.loc[self.position, ["ativo"]]))

        else:
            value = len(self.lista)+1
            self.position = len(self.lista)
            self.number = self.bd.loc[value, ['numero']] = self.number
            self.name = self.bd.loc[value, ['nome']] = 'empty'
            self.unity = self.bd.loc[value, ['unidade']] = 'empty'
            self.sector = self.bd.loc[value, ['setor']] = 0
            self.stage = self.bd.loc[value, ['etapa']] = '0'
            self.message = self.bd.loc[value, ['msg']] = 'empty'
            self.active = self.bd.loc[value, ['ativo']] = 0
            self.bd.to_excel(self.nameFile, index=False)

    def get(self):
        return self.bd, self.position, self.nameFile, self.name, \
               self.unity, self.sector, self.stage, self.message, self.active


class Update(Information):

    def updateName(self, value):
        try:
            self.bd.loc[self.position, ['nome']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

    def updateUnity(self, value):
        try:
            self.bd.loc[self.position, ['unidade']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

    def updateSector(self, value):
        try:
            self.bd.loc[self.position, ['setor']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

    def updateStage(self, value):
        try:
            self.bd.loc[self.position, ['etapa']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

    def updateMessage(self, value):
        try:
            self.bd.loc[self.position, ['msg']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

    def updateActive(self, value):
        try:
            self.bd.loc[self.position, ['ativo']] = value
            self.bd.to_excel(self.nameFile, index=False)
        except RuntimeError:
            print('Error changing data')

def req(title, message):
    url = f'http://localhost:2000/{title}/{message}'
    requests.get(url)


def Finish(name, unity, message, bd, position):
    title = f'Chamado feito por {name} da unidade {unity}'
    try:
        threading.Thread(target=req, args=(title, message)).start()
    except RuntimeError:
        print('SERVIDOR DESLIGADO')

    with open('group.txt', 'a') as file:
        file.close()
    with open('group.txt', 'w') as file:
        file.write(f'{title} foi aberto no GLPI!')

    file.close()
    resetValues(bd, position, nameFile, 2)


def resetValues(bd, position, file, active=1):
    bd.loc[position, ['setor']] = 0
    bd.loc[position, ['etapa']] = '0'
    bd.loc[position, ['msg']] = 'empty'
    bd.loc[position, ['ativo']] = active
    bd.to_excel(file, index=False)
