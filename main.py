from tkinter import *
import json
import os

class Ingreso():

    # Inicializa la ventana de ingreso a la cuenta
    def __init__(self):

        FILE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.archivoUsuarios = FILE_PATH + "\\usuarios\\users.txt"
        with open(self.archivoUsuarios, 'r') as fr:
            self.data = json.load(fr)
            self.listaUsuarios = self.data["users"]

        self.crearCuenta = False

        self.windowIngreso = Tk()
        self.windowIngreso.title("")
        self.windowIngreso.config(bg = "light grey")
        self.windowIngreso.eval("tk::PlaceWindow . center")

        labelUsuario = Label(self.windowIngreso,
                                  font = ("Arial", 15, "bold"),
                                  text = "Usuario",
                                  bg = "light grey")
        labelUsuario.grid(row = 0, column = 0)
        self.entryUsuario = Entry(self.windowIngreso,
                                  font = ("Arial", 15))
        self.entryUsuario.grid(row = 0, column = 1)
        self.entryUsuario.focus_force()

        labelContraseña = Label(self.windowIngreso,
                                     font = ("Arial", 15, "bold"),
                                     text = "Contraseña",
                                     bg = "light grey")
        labelContraseña.grid(row = 1, column = 0)
        self.entryContraseña = Entry(self.windowIngreso,
                                     font = ("Arial", 15),
                                     show = "*")
        self.entryContraseña.grid(row = 1, column = 1)
        buttonMostrar = Button(self.windowIngreso,
                                    font = ("Arial", 10, "bold"),
                                    text = "M",
                                    command = self.mostrar_contraseña)
        buttonMostrar.grid(row = 1, column = 2)

        self.labelError = Label(self.windowIngreso,
                                font = ("Arial", 10, "italic"),
                                fg = "red",
                                bg = "light grey")
        self.labelError.grid(row=2, column=1)

        buttonIngresar = Button(self.windowIngreso,
                                     font = ("Arial", 20, "bold"),
                                     text = "Ingresar",
                                     command = self.ingresar_usuario)
        buttonIngresar.grid(row = 3, column = 1)
        buttonCrearUsuario = Button(self.windowIngreso,
                                         font = ("Arial", 20, "bold"),
                                         text = "Crear usuario",
                                         command = self.crear_usuario)
        buttonCrearUsuario.grid(row = 3, column = 0)

        self.windowIngreso.mainloop()

    # Verifica que el usuario y contraseña estén correctos. En caso de ser así, inicia sesión
    # e inicializa la ventana de HomeBanking
    def ingresar_usuario(self):
        posicion, dni = self.busqueda_binaria()
        if posicion > -1:
            self.windowIngreso.destroy()

            from homebanking import HomeBanking
            hb = HomeBanking(dni)

        else:
            self.labelError.config(text = "Algo salió mal. (código {})".format(posicion * (-1)))

    # Inicializa la ventana de creación de usuario
    def crear_usuario(self):
        self.crearCuenta = True # Variable que indica que el usuario está intentando crear una cuenta
                                # Es utilizada en la función busqueda_binaria

        for item in self.windowIngreso.winfo_children():
            item.config(state = DISABLED)

        windowCrearUsuario = Toplevel(self.windowIngreso)
        windowCrearUsuario.title("")
        windowCrearUsuario.config(bg = "light grey")
        self.windowIngreso.eval(f"tk::PlaceWindow {str(windowCrearUsuario)} center")
        windowCrearUsuario.bind("<Destroy>", self.ventana_cerrada)

        labelNombreNuevo = Label(windowCrearUsuario,
                                      font = ("Arial", 15, "bold"),
                                      text = "Nombre completo",
                                      bg = "light grey")
        labelNombreNuevo.grid(row = 0, column = 0)
        self.entryNombreNuevo = Entry(windowCrearUsuario,
                                      font=("Arial", 15))
        self.entryNombreNuevo.grid(row=0, column=1)
        self.entryNombreNuevo.focus_force()

        labelUsuarioNuevo = Label(windowCrearUsuario,
                                       font = ("Arial", 15, "bold"),
                                       text = "Usuario",
                                       bg = "light grey")
        labelUsuarioNuevo.grid(row=1, column=0)
        self.entryUsuarioNuevo = Entry(windowCrearUsuario,
                                       font=("Arial", 15))
        self.entryUsuarioNuevo.grid(row=1, column=1)

        labelAliasNuevo = Label(windowCrearUsuario,
                                     font = ("Arial", 15, "bold"),
                                     text = "Alias",
                                     bg = "light grey")
        labelAliasNuevo.grid(row = 2, column = 0)
        self.entryAliasNuevo = Entry(windowCrearUsuario,
                                     font=("Arial", 15))
        self.entryAliasNuevo.grid(row=2, column=1)

        labelContraseñaNueva = Label(windowCrearUsuario,
                                          font = ("Arial", 15, "bold"),
                                          text = "Contraseña",
                                          bg = "light grey")
        labelContraseñaNueva.grid(row = 3, column = 0)
        self.entryContraseñaNueva = Entry(windowCrearUsuario,
                                          font = ("Arial", 15),
                                          show = "*")
        self.entryContraseñaNueva.grid(row = 3, column = 1)

        self.labelErrorNuevo = Label(windowCrearUsuario,
                                     font = ("Arial", 10, "italic"),
                                     fg = "red",
                                     bg = "light grey")
        self.labelErrorNuevo.grid(row = 4, column = 1)

        buttonCrearNuevo = Button(windowCrearUsuario,
                                       font = ("Arial", 20, "bold"),
                                       text = "Ingresar",
                                       command = self.ingresar_en_lista)
        buttonCrearNuevo.grid(row = 5, column = 1)
        buttonMostrarNuevo = Button(windowCrearUsuario,
                                         font = ("Arial", 10, "bold"),
                                         text = "M",
                                         command = self.mostrar_contraseña)
        buttonMostrarNuevo.grid(row = 3, column = 2)

        windowCrearUsuario.mainloop()

    # Habilita la ventana principal y sus componentes si el usuario cierra la ventana de creación de usuario
    def ventana_cerrada(self, event):
        for item in self.windowIngreso.winfo_children():
            if item != event.widget.winfo_toplevel():
                item.config(state = NORMAL)

    # Ingresa al usuario en la lista.
    # Verifica que la información ingresada en los campos tenga el formato correcto.
    # En caso de ser válido, procede a insertar al usuario en la lista según la posición devuelta por busqueda_binaria
    # Sobreescribe el archivo users.txt y procede a inicializar la ventana de HomeBanking
    def ingresar_en_lista(self):
        posicion, dni = self.busqueda_binaria()

        if (self.entryNombreNuevo.get() == ""
            or self.entryAliasNuevo.get() == ""
            or self.entryUsuarioNuevo.get() == ""
            or self.entryContraseñaNueva.get() == ""):
                self.labelErrorNuevo.config(text = "Rellene todos los campos")

        elif posicion < 0:
            self.labelErrorNuevo.config(text = "Algo salió mal. (código {})".format(posicion * (-1)))

        elif self.entryNombreNuevo.get().isnumeric() or self.entryAliasNuevo.get().isnumeric():
            self.labelErrorNuevo.config(text = "Algo salió mal. (código 1)")

        elif self.listaUsuarios["alias"].count(self.entryAliasNuevo.get()) == 1:
            self.labelErrorNuevo.config(text = "Algo salió mal. (código 5)")

        else:
            self.labelErrorNuevo.config(text="")

            self.listaUsuarios["dni"].insert(posicion, int(self.entryUsuarioNuevo.get()))
            self.listaUsuarios["nombre"].insert(posicion, self.entryNombreNuevo.get())
            self.listaUsuarios["contrasena"].insert(posicion, self.entryContraseñaNueva.get())
            self.listaUsuarios["alias"].insert(posicion, self.entryAliasNuevo.get())
            self.listaUsuarios["dinero"].insert(posicion, 0)
            self.listaUsuarios["deudas"].insert(posicion, {})
            self.listaUsuarios["historial"].insert(posicion, {})

            with open(self.archivoUsuarios, 'w') as overwrite:
                json.dump(self.data, overwrite, indent = 3)

            self.windowIngreso.destroy()
            from homebanking import HomeBanking
            hb = HomeBanking(dni)

    # Busca al usuario en la lista.
    # Primero comprueba si el usuario está o no creando una cuenta, y si el formato de ésta es válido
    # Luego realiza una búsqueda binaria en la sublista de DNIs y devuelve error si:
    # (-4) El usuario asociado al DNI ya fue creado
    # (-2) El usuario existe pero la contraseña ingresada es inválida
    # (-3) El usuario no existe
    def busqueda_binaria(self):
    # ACLARACIÓN: la función devuelve "<posición>, <dni ingresado>"
    # En caso de existir un error, devuelve "<código de error>, None"
    # Es por esto que para devolver el error uso "format(posición * (-1))" (múltiplico por -1 por motivos estéticos),
    # ya que "posición" es la variable que contiene el código de error

        if self.crearCuenta: # se está creando un usuario nuevo
            dniIngresado = self.entryUsuarioNuevo.get()
            contraseñaIngresada = self.entryContraseñaNueva.get()

        else: # inicio de sesión
            dniIngresado = self.entryUsuario.get()
            contraseñaIngresada = self.entryContraseña.get()

        if self.formato_invalido(dniIngresado, contraseñaIngresada):
            return -1, None

        dniIngresado = int(dniIngresado) # transformo la variable en un entero para poder comparar entre números

        extremoIzquierdo = 0
        extremoDerecho = len(self.listaUsuarios["dni"]) - 1

        if self.listaUsuarios["dni"][extremoIzquierdo] > dniIngresado and self.crearCuenta:
            return extremoIzquierdo, dniIngresado
        elif self.listaUsuarios["dni"][extremoDerecho] < dniIngresado and self.crearCuenta:
            return extremoDerecho+1, dniIngresado

        else:
            while extremoIzquierdo <= extremoDerecho:
                posicionUsuario = (extremoIzquierdo + extremoDerecho) // 2

                if extremoIzquierdo == extremoDerecho and self.crearCuenta:
                    posicionUsuario = extremoIzquierdo # ubicación exacta donde debe ir el nuevo usuario

                    if self.listaUsuarios["dni"][posicionUsuario] == dniIngresado:
                        return -4, None
                    elif self.listaUsuarios["dni"][posicionUsuario] > dniIngresado:
                        return posicionUsuario, dniIngresado
                    elif self.listaUsuarios["dni"][posicionUsuario] < dniIngresado:
                        return posicionUsuario+1, dniIngresado

                elif self.listaUsuarios["dni"][posicionUsuario] < dniIngresado:
                    extremoIzquierdo = posicionUsuario + 1

                    if extremoIzquierdo > extremoDerecho: # caso excepcional para creación de usuario
                        extremoIzquierdo = extremoDerecho

                elif self.listaUsuarios["dni"][posicionUsuario] > dniIngresado:
                    extremoDerecho = posicionUsuario - 1

                    if extremoDerecho < extremoIzquierdo: # caso excepcional para creación de usuario
                        extremoDerecho = extremoIzquierdo

                else:
                    if self.listaUsuarios["contrasena"][posicionUsuario] == contraseñaIngresada:
                        return posicionUsuario, dniIngresado

                    else:
                        return -2, None
        return -3, None

    # Comprueba si los formatos ingresados en los campos son válidos (ya sea por longitud o carácteres)
    # CASO EXCEPCIONAL con el DNI "1" ya que es una cuenta de testeo
    def formato_invalido(self, dniIngresado, contraseñaIngresada):
        if self.crearCuenta and ((len(self.entryAliasNuevo.get()) == 0 or len(self.entryNombreNuevo.get()) == 0)): # alias y/o nombre inválidos
            return True
        elif ((len(dniIngresado) != 8 or not dniIngresado.isnumeric()) or len(contraseñaIngresada) == 0) and not dniIngresado == "1":
            return True
        return False

    def mostrar_contraseña(self):
        if self.crearCuenta:
            if self.entryContraseñaNueva.cget("show") == "*":
                self.entryContraseñaNueva.config(show = "")
            else:
                self.entryContraseñaNueva.config(show = "*")
        else:
            if self.entryContraseña.cget("show") == "*":
                self.entryContraseña.config(show = "")
            else:
                self.entryContraseña.config(show = "*")


ingreso = Ingreso()

#### CÓDIGOS DE ERROR ####
## 1: el formato del NOMBRE DE USUARIO y/o CONTRASEÑA es inválido, ya sea por longitud o tipos de caracteres
## 2: el usuario ingresado existe, pero su CONTRASEÑA es inválida
## 3: el usuario ingresado NO existe
## 4: se está intentando crear una cuenta con un DNI ya asociado a otra
## 5: se está intentando crear una cuenta con un ALIAS ya asociado a otra