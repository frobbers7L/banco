import json
import os
from tkinter import *

class HomeBanking():

    # Inicializa la ventana de HomeBanking
    def __init__(self, d):
        self.dni = d

        self.windowHomeBanking = Tk()
        self.windowHomeBanking.title("")
        self.windowHomeBanking.config(bg = "light grey")
        self.windowHomeBanking.eval("tk::PlaceWindow . center")

        frameButtons = Frame(self.windowHomeBanking,
                                  bg = "light grey")
        buttonTransferencia = Button(frameButtons,
                                          font = ("Arial", 20, "bold"),
                                          text = "Transferir",
                                          command = self.transferencia)
        buttonTransferencia.grid(row = 0, column = 1)
        buttonPagar = Button(frameButtons,
                                  font = ("Arial", 20, "bold"),
                                  text = "Pagar cuentas",
                                  command = self.pagar_cuentas)
        buttonPagar.grid(row = 1, column = 1)
        buttonCredito = Button(frameButtons,
                                    font = ("Arial", 20, "bold"),
                                    text = "Créditos",
                                    command = self.sacar_credito)
        buttonCredito.grid(row = 2, column = 1)
        buttonHistorial = Button(frameButtons,
                                      font = ("Arial", 20, "bold"),
                                      text = "Mi historial",
                                      command = self.mostrar_historial)
        buttonHistorial.grid(row = 3, column = 1)
        frameButtons.pack(side = RIGHT, padx = 15, pady = 10)

        frameInfo = Frame(self.windowHomeBanking,
                               bg = "light grey")
        self.labelNombre = Label(frameInfo,
                                 font = ("Arial", 20),
                                 bg = "light grey")
        self.labelNombre.grid(row = 1, column = 0)
        self.labelDinero = Label(frameInfo,
                                 font = ("Arial", 15),
                                 bg = "light grey")
        self.labelDinero.grid(row = 2, column = 0)
        self.labelDeuda = Label(frameInfo,
                                font = ("Arial", 15),
                                 bg = "light grey")
        self.labelDeuda.grid(row = 3, column = 0)
        frameInfo.pack(side = LEFT, padx = 10)

        # Inicializo las variables que contienen a la dirección del archivo de usuarios,
        # a su contenido y a la lista ["users"] (esto es puramente estético, para abreviar el código)
        self.archivoUsuarios = os.path.dirname(os.path.realpath(__file__)) + "\\usuarios\\users.txt"
        with open(self.archivoUsuarios, 'r') as fr:
            self.data = json.load(fr)
            self.listaUsuarios = self.data["users"]

        # Guardo la posición del usuario operador
        self.posicionUsuario = self.posicion_dni()

        self.labelNombre.config(text="Bienvenido, {}".format(self.atributos(3)))
        self.labelDinero.config(text="Dinero en cuenta: ${}".format(self.atributos(5)))
        self.labelDeuda.config(text="Adeudas: ${}".format(self.atributos(6)))

        self.windowHomeBanking.mainloop()

    # Inicializa la ventana de transferencias.
    # Deshabilita la ventana de HomeBanking hasta el proceso sea terminado
    def transferencia(self):
        self.deshabilitar()

        windowTransferencias = Toplevel(self.windowHomeBanking)
        self.windowHomeBanking.eval(f"tk::PlaceWindow {str(windowTransferencias)} center")
        windowTransferencias.title("")
        windowTransferencias.config(bg="light grey")
        windowTransferencias.bind("<Destroy>", self.ventana_cerrada)

        from transferencias import Transferencias
        tf = Transferencias(windowTransferencias, self.posicionUsuario,
                            self.data, self.archivoUsuarios)

    # Inicializa la ventana de pago de cuentas.
    # Deshabilita la ventana de HomeBanking hasta que el proceso sea terminado
    def pagar_cuentas(self):
        self.deshabilitar()

        windowCuentas = Toplevel(self.windowHomeBanking)
        self.windowHomeBanking.eval(f"tk::PlaceWindow {str(windowCuentas)} center")
        windowCuentas.config(bg = "light grey")
        windowCuentas.bind("<Destroy>", self.ventana_cerrada)

        from cuentas import Cuentas
        pc = Cuentas(windowCuentas, self.posicionUsuario,
                     self.data, self.archivoUsuarios)

    def sacar_credito(self):
        self.deshabilitar()

        windowPrestamos = Toplevel(self.windowHomeBanking)
        self.windowHomeBanking.eval(f"tk::PlaceWindow {str(windowPrestamos)} center")
        windowPrestamos.config(bg = "light grey")
        windowPrestamos.bind("<Destroy>", self.ventana_cerrada)

        from prestamos import Prestamos
        pr = Prestamos(windowPrestamos, self.posicionUsuario,
                      self.data, self.archivoUsuarios)

    def mostrar_historial(self):
        self.deshabilitar()

        windowHistorial = Toplevel(self.windowHomeBanking)
        self.windowHomeBanking.eval(f"tk::PlaceWindow {str(windowHistorial)} center")
        windowHistorial.config(bg = "light grey")
        windowHistorial.bind("<Destroy>", self.ventana_cerrada)

        listaHistorial = self.atributos(7)

        from historial import Historial
        hi = Historial(windowHistorial, listaHistorial)

    # Devuelve información en base a la opción ingresada
    def atributos(self, opcion):

        if opcion == 1:
            return self.listaUsuarios["dni"][self.posicionUsuario]
        elif opcion == 2:
            return self.listaUsuarios["contrasena"][self.posicionUsuario]
        elif opcion == 3:
            return self.listaUsuarios["nombre"][self.posicionUsuario]
        elif opcion == 4:
            return self.listaUsuarios["alias"][self.posicionUsuario]
        elif opcion == 5:
            return self.listaUsuarios["dinero"][self.posicionUsuario]
        elif opcion == 6:
            deudaTotal = sum(self.listaUsuarios["deudas"][self.posicionUsuario].values())
            return deudaTotal # devuelve el monto total de las deudas del usuario
        elif opcion == 7:
            return self.listaUsuarios["historial"][self.posicionUsuario]

    # Devuelve la posición del usuario en la lista.
    # Realiza una búsqueda binaria sobre la lista de DNIs y devuelve su posición o error en caso de no haberla obtenido
    def posicion_dni(self):
        extremoIzquierdo = 0
        extremoDerecho = len(self.listaUsuarios["dni"]) - 1

        while extremoIzquierdo <= extremoDerecho:
            posicionDNI = (extremoIzquierdo + extremoDerecho) // 2

            if self.listaUsuarios["dni"][posicionDNI] < self.dni:
                extremoIzquierdo = posicionDNI + 1

            elif self.listaUsuarios["dni"][posicionDNI] > self.dni:
                extremoDerecho = posicionDNI - 1

            else:
                return posicionDNI

        return -6

    # Rehabilita los componentes de la ventana maestra y actualiza la lista de usuarios.
    # Primero comprueba que el elemento que accede a la función no sea un widget
    # para no ejecutarla una cantidad innecesaria de veces
    def ventana_cerrada(self, event):
        if event.widget != event.widget.winfo_toplevel():
            return

        for frame in self.windowHomeBanking.winfo_children():
            if frame != event.widget.winfo_toplevel():
                for widget in frame.winfo_children():
                    widget.configure(state = NORMAL)

        if str(event) == "<Destroy event>":
            self.actualizar_datos()

    # Actualiza los datos en pantalla, así como la lista de usuarios
    # Primero se accede al archivo para actualizar las variables "data" y "listaUsuarios"
    def actualizar_datos(self):
        with open(self.archivoUsuarios, 'r') as fr:
            self.data = json.load(fr)
            self.listaUsuarios = self.data["users"]

        self.labelDinero.config(text="Dinero en cuenta: ${}".format(self.atributos(5)))
        self.labelDeuda.config(text="Adeudas: ${}".format(self.atributos(6)))

    def deshabilitar(self):
        for frame in self.windowHomeBanking.winfo_children():
            for widget in frame.winfo_children():
                widget.configure(state = DISABLED)

if __name__ == '__main__':
    hb = HomeBanking(1)