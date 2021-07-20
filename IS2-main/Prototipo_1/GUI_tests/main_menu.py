import tkinter as tk

TITLE_FONT= ("Verdana", 12)


class main_app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args , **kwargs)
        tk.Tk.title(self, "IS2")
        tk.Tk.geometry(self, "400x300")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, Horario, Materias):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)
        
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Aprende en tu tiempo libre", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Ver mi horario",
                            command=lambda: controller.show_frame(Horario))
        button1.pack()
        
        button2 = tk.Button(self, text="Ver mis materias",
                            command=lambda: controller.show_frame(Materias))
        button2.pack()
        
        button3 = tk.Button(self, text="Añadir materias a horas",
                            command=lambda: controller.show_frame(Materias))
        button3.pack()
        
        button4 = tk.Button(self, text="Recibir recomendaciones",
                            command=lambda: controller.show_frame(Materias))
        button4.pack()


class Horario(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack(side = tk.TOP, anchor = "nw")
        
        label = tk.Label(self, text="Horario", font=TITLE_FONT)
        label.pack(pady=10,padx=10)
        
class Materias(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack(side = tk.TOP, anchor = "nw")
        
        label = tk.Label(self, text="Materias", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        matFrame = tk.Frame(self)
        mat1 = tk.Button(matFrame, text = "mat1")
        mat1.grid(column = 0, row = 0)
        mat2 = tk.Button(matFrame, text = "mat2")
        mat2.grid(column = 1, row = 0)
        mat3 = tk.Button(matFrame, text = "mat3")
        mat3.grid(column = 0, row = 1)
        mat4 = tk.Button(matFrame, text = "mat4")
        mat4.grid(column = 1, row = 1)
        
        matFrame.pack()
    
app = main_app()
app.mainloop()