import copy
from datetime import datetime
from math import inf

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._G = None
        self._nodi = []
        self._Dnodi = {}
        self._archi = []
        self._Darchi = {}
        self._soluzione = []
        self._top = inf

    def creaGrafo(self, anno1, anno2):
        self._Darchi = {}
        self._G = nx.Graph()
        self._nodi = DAO.getNodi(anno1, anno2)
        self._G.add_nodes_from(self._nodi)
        for element in self._nodi:
            self._Dnodi[element.constructorId] = element
        self._archi = DAO.getArchi(anno1, anno2)
        for arco in self._archi:
            stringa1 = str(arco.nodo1) + "_" + str(arco.nodo2)
            stringa = str(arco.nodo2) + "_" + str(arco.nodo1)
            self._Darchi[stringa] = "ego"
            self._Darchi[stringa1] = "sum"
            nodo1 = self._Dnodi[arco.nodo1]
            nodo2 = self._Dnodi[arco.nodo2]
            peso =arco.peso
            self._G.add_edge(nodo1, nodo2, weight= peso)

    def popola(self):
        return DAO.getAllYears()

    def piuAnziani(self):
        anni = DAO.getAnni()
        for element in anni:
            nodo = self._Dnodi.get(element[0])
            if nodo != None:
                nodo.oldest_driver_dob = element[1]

    def listaNodiVicini(self, lista, nodo2):
        for nodo1 in lista:
            stringa = str(nodo1) + "_" + str(nodo2)
            if self._Darchi.get(stringa) != None:
                return False
        return True

    def ricorsione(self, k):
        self._soluzione = []
        self._top = inf
        self.piuAnziani()
        for element in self._nodi:
            parziale = [element]
            self.itera(parziale, k)
        titolo = f"Percorso che minimizza età di {k} veterani, con costo {self.differenza(self._soluzione)}:"
        testo = ""
        for element in self._soluzione:
            if testo == "":
                testo = testo + element.__str__()
            else:
                testo = testo + "\n" + element.__str__()
        return titolo, testo

    def differenza(self, lista):
        lista.sort()
        d1 = lista[0].oldest_driver_dob
        d2 = lista[len(lista)-1].oldest_driver_dob
        return abs((d2 - d1).days)

    def numeroNodi(self):
        return nx.number_of_nodes(self._G)

    def itera(self, parziale, k):
        if len(parziale) == k:
            if self.differenza(parziale)<self._top:
                self._soluzione = copy.deepcopy(parziale)
                self._top = self.differenza(parziale)
        else:
            for element in self._nodi:
                if element not in parziale:
                    if self.listaNodiVicini(parziale, element) == True:
                        parziale.append(element)
                        self.itera(parziale, k)
                        parziale.pop()









    def grado(self, nodo):
        return str(self._G.degree(nodo))

    def outputGrafo(self):
        titolo = "Grafo correttamente creato"
        testo1 = f"Numero di nodi: {len(self._nodi)}"
        testo2 = f"Numero di archi: {len(self._archi)}"
        return titolo, testo1, testo2

    def dettagli(self):
        titolo0 = "Archi con peso maggiore"
        testo0 = ""
        self._archi.sort(reverse=True)
        for i in range(0, 3):
            elemento = self._archi[i]
            nodo1 = self._Dnodi[elemento.nodo1]
            nodo2 = self._Dnodi[elemento.nodo2]
            if testo0 == "":
                testo0 = testo0 + nodo1.name + "--->" +  nodo2.name + " " + str(elemento.peso)
            else:
                testo0 = testo0 + "\n" + nodo1.name + "--->" + nodo2.name + " " + str(elemento.peso)

        numeroComponenti = nx.number_connected_components(self._G)
        piuGrande = self._G.subgraph(max(nx.connected_components(self._G), key=len))
        titolo = f"Ci sono {numeroComponenti} componenti connesse"
        titolo2 = f"La componente connessa più grande ha {nx.number_of_nodes(piuGrande)} nodi"
        testo = ""
        nodi = sorted(piuGrande.nodes(), key= lambda n: piuGrande.degree(n), reverse = True)
        for element in nodi:
            if testo == "":
                testo = testo + element.__str__() + "(" + self.grado(element) + ")"
            else:
                testo = testo + "\n" + element.__str__() + "(" + self.grado(element) + ")"
        return titolo0, testo0, titolo, titolo2, testo
