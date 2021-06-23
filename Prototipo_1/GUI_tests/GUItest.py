# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 20:54:56 2021

@author: caleu
"""

import tkinter as tk

window = tk.Tk()
window.geometry("400x300")
window.title("IS2")


label = tk.Label(window, text="this is a label", bg='cyan')
label.pack(side = tk.BOTTOM)

dato = ''

def foo():
    print('button clicked!!')
    
def panda(string):
    print('button 3 clicked!! ' + string)
    

    
# orden de definicion parece importar para las inputbox
txtbx = tk.Entry(window)
txtbx.pack()

def inputBox():
    dato = txtbx.get()
    print(dato)
    

btn = tk.Button(window, text = 'click me!!', command = foo)
btn.pack(side=tk.LEFT)

btn2 = tk.Button(window, text = 'click me too!!', command = inputBox)
btn2.pack(after=txtbx)

# para llamar funciones con parametros, utilizar 'lambda: func()'
btn3 = tk.Button(window, text = 'click me three!!', command = lambda: panda(dato))
btn3.pack(side=tk.RIGHT)

window.mainloop()