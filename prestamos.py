from tkinter import *

class Prestamos():

    # Inicializa los componentes de la ventana de préstamos
    # La declaración está compuesta por...
    #   windowP: ventana de préstamos
    #   pU: posición del usuario en la lista
    #   data: archivo de usuarios
    #   archivoU: dirección del archivo de usuarios
    def __init__(self, windowP, pU, data, archivoU):

        self.windowPrestamos = windowP
        self.posicionUsuario = pU
        self.data = data
        self.archivoUsuarios = archivoU

        self.listBox = Listbox(self.windowPrestamos,
                               bg = "light grey",
                               font = ("Arial", 15))
        self.listBox.pack()
        self.listBox.config(height = 0, width = 0)

        self.labelError = Label(self.windowPrestamos,
                                bg = "light grey",
                                fg = "red",
                                font = (("Arial", 10, "italic")))
        self.labelError.pack()

        botonConfirmar = Button(self.windowPrestamos,
                                     text = "Confirmar",
                                     command = self.confirmar)
        botonConfirmar.pack()

        self.llenar_listBox()
        self.windowPrestamos.mainloop()

    # Completa la listbox con las 3 opciones de préstamo.
    def llenar_listBox(self):
        from datetime import datetime, date
        añoActual = datetime.now().timetuple().tm_year
        diaActual = datetime.now().timetuple().tm_yday

        diaVencimiento1 = diaActual + 31
        fechaVencimiento1 = date.fromordinal(date(añoActual, 1, 1).toordinal() + diaVencimiento1 - 1)

        diaVencimiento2 = diaActual + 93
        fechaVencimiento2 = date.fromordinal(date(añoActual, 1, 1).toordinal() + diaVencimiento2 - 1)

        diaVencimiento3 = diaActual + 365
        fechaVencimiento3 = date.fromordinal(date(añoActual, 1, 1).toordinal() + diaVencimiento3 - 1)

        self.dictOpciones = {fechaVencimiento1: 10000,
                             fechaVencimiento2: 100000,
                             fechaVencimiento3: 10000000}
        self.listBox.insert(1, "Prestamo $10.000 | Vencimiento {}".format(fechaVencimiento1))
        self.listBox.insert(2, "Prestamo $100.000 | Vencimiento {}".format(fechaVencimiento2))
        self.listBox.insert(3, "Prestamo $1.000.000 | Vencimiento {}".format(fechaVencimiento3))

    # Realiza la operación del préstamo.
    # Primero verifica que se haya seleccionado alguna opción,
    # luego le transfiere el dinero al usuario y por último inserta la operación en su historial
    def confirmar(self):
        if len(self.listBox.curselection()) == 0:
            self.labelError.config(text = "Por favor, seleccione una opción")

        else:
            opcion = self.listBox.curselection()[0]


            # Le agrego el dinero del prestamo contraído al dinero en cuenta del usuario
            dineroDeuda =  list(self.dictOpciones.values())[opcion]
            self.data["users"]["dinero"][self.posicionUsuario] += dineroDeuda

            # Le agrego la deuda contraída a la lista de deudas del usuario
            dineroInteres = int(dineroDeuda * 1.1) # 10% de interés
            fechaVencimiento = "Vencimiento {}".format(list(self.dictOpciones.keys())[opcion])
            self.data["users"]["deudas"][self.posicionUsuario][fechaVencimiento] = dineroInteres

            import time
            fecha = time.ctime(time.time())

            self.data["users"]["historial"][self.posicionUsuario]\
                ["{}: Adquiriste un credito por un total de ${}".format(fecha, dineroDeuda)] = \
                ["c", dineroDeuda, dineroInteres, fechaVencimiento]
                # código de operación, dinero prestado, dinero a pagar, fecha de vencimiento

            import json
            with open(self.archivoUsuarios, 'w') as overwrite:
                json.dump(self.data, overwrite, indent = 3)

            from tkinter import messagebox
            messagebox.showinfo(title = "Operación exitosa",
                                message = "El monto a pagar es de ${}".format(dineroInteres))

            self.windowPrestamos.destroy()

if __name__ == "__main__":
    from homebanking import HomeBanking
    hb = HomeBanking(1)