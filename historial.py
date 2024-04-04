from tkinter import *

class Historial():

    # Inicializa los componentes de la ventana de historial.
    # La declaración está compuesta por...
    #   wH: ventana de historial
    #   hi: lista del historial seleccionado - recordar que éste es un diccionario cuyos valores son listas
    def __init__(self, wH, hi):
        self.historial = hi
        self.keys = list(self.historial)

        self.windowHistorial = wH

        self.listBox = Listbox(self.windowHistorial,
                               bg = "light grey",
                               font = ("Arial", 15))
        self.listBox.config(width = 0)
        self.listBox.bind("<<ListboxSelect>>", self.mostrar_detalles)
        self.listBox.pack()

        self.llenar_listbox()
        self.windowHistorial.mainloop()

    # Ingresa los items de la lista historial en la Listbox.
    def llenar_listbox(self):
        for item in self.historial:
            self.listBox.insert(END, item)

    # Muestra los detalles de la operación seleccionada.
    # Estos detalles varían según el tipo de operación
    def mostrar_detalles(self, event):
        self.listBox.config(state = DISABLED)

        posicion = self.listBox.curselection()[0] # item seleccionado
        data = self.keys[posicion] # key del item
        info = self.historial[data] # valor del item

        self.windowDetalles = Toplevel(self.windowHistorial)

        x = self.windowHistorial.winfo_x()
        y = self.windowHistorial.winfo_y()
        self.windowDetalles.geometry("+%d+%d" % (x, y)) # centra la ventana

        labelInfo = Label(self.windowDetalles,
                          bg = "light grey",
                          font = ("Arial", 15))
        self.mostrar_informacion(info, labelInfo)
        labelInfo.pack()

        self.windowDetalles.protocol("WM_DELETE_WINDOW", self.cerrar_detalles)
        self.windowDetalles.mainloop()

    # Vuelca la información de la operación al label.
    # El formato varía según el código de operación,
    # ya que la información que guarda cada operación varía en cantidad y tipo de dato
    def mostrar_informacion(self, info, labelI):
        codigoOperacion = info[0]

        if codigoOperacion == 'c':
            labelI.config(text = "Prestado: ${}\nA pagar: ${}\n{}".format(info[1], info[2], info[3]))

        elif codigoOperacion == 'p':
            infoKey = list(info[1].keys())[0]
            labelI.config(text = "Deuda pagada: {}\nImporte: ${}".format(infoKey, info[1][infoKey]))

        elif codigoOperacion == 'tR':
            labelI.config(text = "Alias del emisor: {}".format(info[1]))

        elif codigoOperacion == 'tE':
            labelI.config(text = "Alias del receptor: {}".format(info[1]))

    def cerrar_detalles(self):
        self.windowDetalles.destroy()
        self.listBox.config(state = NORMAL)

if __name__ == "__main__":
    from homebanking import HomeBanking
    hb = HomeBanking(1)