import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def popolaAnni(self):
        anni = self._model.popola()
        for element in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(f"{element}"))
            self._view._ddAnno2.options.append(ft.dropdown.Option(f"{element}"))
        self._view._btnCreaGrafo.disabled=False
        self._view.update_page()

    def handleCreaGrafo(self,e, data1, data2):
        self._view.txt_result.controls.clear()
        if data1>data2:
            self._view.txt_result.controls.append(ft.Text(f"Hai selezionato un range non valido", color = "red"))
            self._view.update_page()
            return
        self._model.creaGrafo(int(data1), int(data2))
        titolo, testo1, testo2 = self._model.outputGrafo()
        self._view.txt_result.controls.append(ft.Text(f"{titolo}"))
        self._view.txt_result.controls.append(ft.Text(f"{testo1}"))
        self._view.txt_result.controls.append(ft.Text(f"{testo2}"))
        self._view._btnstampa.disabled=False
        self._view._btnCerca.disabled = False
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()
        titolo0, testo0, titolo, titolo2, testo = self._model.dettagli()
        self._view.txt_result.controls.append(ft.Text(f"{titolo0}", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"{testo0}"))
        self._view.txt_result.controls.append(ft.Text(f"{titolo}", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"{titolo2}", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"{testo}"))
        self._view.update_page()


    def handleCerca(self, e, k):
        self._view.txt_result.controls.clear()
        try:
            int(k)
        except ValueError:
            stringa = ft.Text("Non hai inserito un numero")
            self._view.txt_result.controls.append(ft.Text(f"{stringa}"))
            self._view.update_page()
            return
        k = int(k)
        if k > self._model.numeroNodi():
            stringa = ft.Text("Hai scelto un numero di costruttori troppo alto")
            self._view.txt_result.controls.append(ft.Text(f"{stringa}"))
            self._view.update_page()
            return
        else:
            titolo, testo = self._model.ricorsione(int(k))
            self._view.txt_result.controls.append(ft.Text(f"{titolo}"))
            self._view.txt_result.controls.append(ft.Text(f"{testo}"))
            self._view.update_page()

