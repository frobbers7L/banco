from tkinter import *

class Transferencias():

    # Inicializa los componentes de la ventana de transferencias.
    # La declaración está compuesta por...
    #   windowT: ventana maestra del módulo de transferencias
    #   pU: posición del usuario operador (emisor)
    #   data: archivo de usuarios
    #   archivoU: dirección del archivo de usuarios
    def __init__(self, windowT, pU, data, archivoU):

        self.posicionEmisor = pU
        self.data = data
        self.archivoUsuarios = archivoU
        self.windowTransferencias = windowT

        labelAliasT = Label(self.windowTransferencias,
                                 font = ("Arial", 20, "bold"),
                                 text = "Alias",
                                 bg = "light grey")
        labelAliasT.grid(row = 0, column = 0)
        self.entryAliasT = Entry(self.windowTransferencias,
                                 font=("Arial", 15))
        self.entryAliasT.grid(row=0, column=1)

        labelMontoT = Label(self.windowTransferencias,
                                 font = ("Arial", 20, "bold"),
                                 text = "Monto",
                                 bg = "light grey")
        labelMontoT.grid(row = 1, column = 0)
        self.entryMontoT = Entry(self.windowTransferencias,
                                 font = ("Arial", 15))
        self.entryMontoT.grid(row = 1, column = 1)

        self.labelErrorT = Label(self.windowTransferencias,
                                 font = ("Arial", 10, "italic"),
                                 fg = "red",
                                 bg = "light grey")
        self.labelErrorT.grid(row = 2, column = 1)

        buttonTransferirT = Button(self.windowTransferencias,
                                        font = ("Arial", 20, "bold"),
                                        text = "Transferir",
                                        command = self.transferir)
        buttonTransferirT.grid(row = 3, column = 1)

        self.windowTransferencias.mainloop()

    # Transfiere dinero entre usuarios.
    # Comprueba que el alias ingresado y el dinero a transferir sean válidos.
    # Si no hay inconvenientes, realiza la transferencia y sobreescribe el archivo de usuarios
    def transferir(self):
        aliasReceptor = self.entryAliasT.get()
        montoTransferir = self.entryMontoT.get()

        posicionReceptor = self.posicion_alias(aliasReceptor)

        if aliasReceptor == "" or montoTransferir == "":
            self.labelErrorT.config(text = "Rellene todos los campos")

        elif posicionReceptor < 0:
            self.labelErrorT.config(text = "Algo salió mal (código {})".format(posicionReceptor * (-1)))

        else:
            montoTransferir = int(montoTransferir)

            if self.verificar_monto(montoTransferir) < 0:
                self.labelErrorT.config(text = "Algo salió mal (código {})".format(montoVerificado * (-1)))

            else:
                self.data["users"]["dinero"][self.posicionEmisor] -= montoTransferir
                self.data["users"]["dinero"][posicionReceptor] += montoTransferir

                import time
                fecha = time.ctime(time.time())

                self.data["users"]["historial"][self.posicionEmisor]["{}: Transferiste ${}"\
                    .format(fecha, montoTransferir)] = \
                    ["tE", aliasReceptor]
                    # código de operación, alias receptor

                aliasEmisor = self.data["users"]["alias"][self.posicionEmisor]
                self.data["users"]["historial"][posicionReceptor]["{}: Te transfirieron ${}"\
                    .format(fecha, montoTransferir)] = \
                    ["tR", aliasEmisor]
                    # código de operación, alias emisor


                import json
                with open(self.archivoUsuarios, 'w') as overwrite:
                    json.dump(self.data, overwrite, indent = 3)

                from tkinter import messagebox
                messagebox.showinfo(title = "Transferencia exitosa",
                                    message = "Se han transferido ${} a la cuenta {}".format(montoTransferir, aliasReceptor))

                self.windowTransferencias.destroy()

    # Verifica que el usuario tenga en cuenta el dinero que desea transferir.
    def verificar_monto(self, montoTransferir):
        dineroEnCuenta = self.data["users"]["dinero"][self.posicionEmisor]

        if dineroEnCuenta < montoTransferir:
            return -6

        else:
            return 1

    # Verifica que el usuario asociado al alias exista y que éste no sea el del usuario emisor
    # (es decir, que no se quiera transferir dinero a sí mismo)
    def posicion_alias(self, alias):
        if alias == (aliasEmisor := self.data["users"]["alias"][self.posicionEmisor]):
            pass

        else:
            for posicionReceptor in range(len(self.data["users"]["alias"])):
                if self.data["users"]["alias"][posicionReceptor] == alias:
                    return posicionReceptor

        return -7

#### CÓDIGOS DE ERROR ####
## 6: el DINERO en cuenta es menor al monto a transferir ingresado
## 7: no existe usuario asociado al ALIAS ingresado, o éste es el del usuario operador

if __name__ == "__main__":
    from homebanking import HomeBanking
    hb = HomeBanking(1)