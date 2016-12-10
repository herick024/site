import json

class Data_file:

    data_temp = []

    def __init__(self):
        pass

    def data_read(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for row in data['results']:
                self.data_temp.append(row)

    def data_print(self):
        for row in self.data_temp:
            print row

    def data_campo(self,camponame):
        list_temp = []
        for row in self.data_temp:
            campo = row[camponame]
            if campo not in list_temp:
                list_temp.append(campo)
        return list_temp

    def data_result(self,state,grupo):
        list_temp = []
        for row in self.data_temp:
           if row['Nom_Ent'] == state and row['GpoEdad'] == grupo:
               list_temp.append(row['Planeado'],row['Noplaneado'])
        return list_temp

    def data_get(self):
        return self.data_temp
