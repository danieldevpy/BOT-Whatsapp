import pandas
nameFile = 'bancodedados.xlsx'
bd = pandas.read_excel(nameFile)
searchNumber = bd["numero"].values

lista = []
for num in searchNumber:
    lista.append(num)


print(lista)