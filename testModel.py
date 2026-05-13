from model.model import Model

modello = Model()
modello.creaGrafo(2014, 2016)
titolo, testo1, testo2 = modello.outputGrafo()
print(titolo)
print(testo1)
print(testo2)
titolo0, testo0, titolo, titolo2, testo = modello.dettagli()
print(titolo0)
print(testo0)
print(titolo)
print(titolo2)
print(testo)
titolo, testo = modello.ricorsione(5)
print(titolo)
print(testo)


