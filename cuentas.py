from tkinter import *

class Cuentas():

    # Inicializa los componentes de la ventana de pago de cuentas.
    # La clase está compuesta por...
    #   windowC: ventana de pago de cuentas
    #   pU: posición del usuario (información necesaria para modificar la lista)
    #   da: archivo de usuarios
    #   archivoU: dirección del archivo de usuarios
    def __init__(self, windowC, pU, da, archivoU):

        self.windowCuentas = windowC
        self.posicionUsuario = pU
        self.data = da
        self.archivoUsuarios = archivoU

        self.dinero = self.data["users"]["dinero"][self.posicionUsuario]
        self.deuda = self.data["users"]["deudas"][self.posicionUsuario]

        self.montoTotal = 0

        self.listBox = Listbox(self.windowCuentas,
                               font = ("Arial", 20),
                               bg = "light grey",
                               selectmode = MULTIPLE)
        self.listBox.pack()
        self.listBox.config(height = 0, width = 0)
        self.listBox.bind("<<ListboxSelect>>", self.actualizar_total)

        self.labelTotal = Label(self.windowCuentas,
                                font = ("Arial", 20),
                                bg = "light grey",
                                text = "TOTAL: $0")
        self.labelTotal.pack()


        self.labelError = Label(self.windowCuentas,
                                font = ("Arial", 10, "italic"),
                                bg = "light grey",
                                fg = "red")
        self.labelError.pack()

        buttonPagar = Button(self.windowCuentas,
                                  font = ("Arial", 20, "bold"),
                                  text = "PAGAR",
                                  command = self.pagar)
        buttonPagar.pack()

        self.llenar_listbox()
        self.windowCuentas.mainloop()

    # Inserta las deudas del usuario en las Listbox.
    # Primero la vacía para empezar la Listbox de cero
    def llenar_listbox(self):
        self.listBox.delete(0, len(self.deuda))

        i = 0
        for key in self.deuda:
            value = self.deuda[key]

            self.listBox.insert(i, "{}: ${}".format(key, value))
            i += 1

    # Actualiza el monto acumulado de las deudas seleccionadas según la selección del usuario
    def actualizar_total(self, event):
        self.keys = list(self.deuda)
        self.listaSeleccionados = self.listBox.curselection()

        self.montoTotal = 0
        for i in self.listaSeleccionados:
            self.montoTotal += self.deuda[self.keys[i]]
        print(self.listaSeleccionados)

        self.labelTotal.config(text = "TOTAL: ${}".format(self.montoTotal))

    # Paga las deudas seleccionadas.
    # Primero verifica que el usuario haya seleccionado algo y que su selección no le deje el saldo
    # en negativo. Luego actualiza su dinero, deudas e historial en base a lo seleccionado y actualiza el archivo
    def pagar(self):
        if self.montoTotal == 0:
            self.labelError.config(text = "No ha seleccionado ninguna cuenta a pagar.")
        elif self.dinero - self.montoTotal < 0:
            self.labelError.config(text = "Saldo insuficiente.")

        else:
            self.labelError.config(text = "")

            deudasPagadas = {}
            for i in self.listaSeleccionados:
                if self.keys[i] in self.deuda:
                    deudasPagadas[self.keys[i]] = self.deuda[self.keys[i]]
                    self.deuda.pop(self.keys[i])

            self.data["users"]["dinero"][self.posicionUsuario] = self.dinero - self.montoTotal
            self.data["users"]["deudas"][self.posicionUsuario] = self.deuda

            import time
            fecha = time.ctime(time.time())

            self.data["users"]["historial"][self.posicionUsuario]\
                ["{}: Pagaste deudas por un total de ${}".format(fecha, self.montoTotal)] = \
                ["p", deudasPagadas]
                # código de operación, deudas pagadas

            import json
            with open(self.archivoUsuarios, 'w') as overwrite:
                json.dump(self.data, overwrite, indent = 3)

            from tkinter import messagebox
            messagebox.showinfo(title = "Operación exitosa",
                                message = "Pagaste un total de ${}".format(self.montoTotal))

            self.windowCuentas.destroy()

if __name__ == "__main__":
    from homebanking import HomeBanking
    hb = HomeBanking(1)