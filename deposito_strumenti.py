from operator import attrgetter

class Prestito:
    def __init__(self, data, id_prestito,  id_strumento, cognome_allievo):
        self.data = {}
        self.id_prestito = id_prestito
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return (f"{self.id_prestito} - strumento {self.id_strumento} "
                f"a {self.cognome_allievo} il {self.data}")





class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (f"{self.id_strumento} - {self.tipo} {self.marca} "
                f"(anno {self.anno_acquisto}, {self.valore:.2f} euro)")




class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self.contatore_prestiti = 0


    def carica_file_strumenti(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()
                if riga == "":
                    continue
                campi = riga.split(",")
                id_strumento = campi[0]
                tipo = campi[1]
                marca = campi[2]
                anno_acquisto = int(campi[3])
                valore = float(campi[4])
                self.strumenti[id_strumento] = Strumento(
                    id_strumento, tipo, marca, anno_acquisto, valore)

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        massimo = 0
        for id_strumento in self.strumenti:
            numero = int(id_strumento[1:])
            if numero > massimo:
                massimo = numero

        nuovo_id = 'S' + str(massimo + 1)
        self.strumenti[nuovo_id] = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)
        return self.strumenti[nuovo_id]

    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti.values(), key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):

        if id_strumento not in self.strumenti:
            raise Exception("Strumento non presente nel sistema.")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception("Strumento già in prestito.")

        self.contatore_prestiti += 1
        id_prestito = "P" + str(self.contatore_prestiti)
        prestito = Prestito(data, id_prestito, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = prestito
        return prestito

    def termina_prestito(self, id_prestito):

        if id_prestito not in self.prestiti:
            raise Exception("Prestito non trovato.")

        del self.prestiti[id_prestito]
