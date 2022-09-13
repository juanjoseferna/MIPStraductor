import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re


etiquetas = {}

registros = {"$zero": "00000", 
             "$at":   "00001", 
             "$v0":   "00010", 
             "$v1":   "00011", 
             "$a0":   "00100", 
             "$a1":   "00101", 
             "$a2":   "00110", 
             "$a3":   "00111", 
             "$t0":   "01000", 
             "$t1":   "01001", 
             "$t2":   "01010", 
             "$t3":   "01011", 
             "$t4":   "01100", 
             "$t5":   "01101", 
             "$t6":   "01110", 
             "$t7":   "01111", 
             "$s0":   "10000", 
             "$s1":   "10001", 
             "$s2":   "10010", 
             "$s3":   "10011", 
             "$s4":   "10100", 
             "$s5":   "10101", 
             "$s6":   "10110", 
             "$s7":   "10111", 
             "$t8":   "11000", 
             "$t9":   "11001", 
             "$k0":   "11010", 
             "$k1":   "11011", 
             "$gp":   "11100", 
             "$sp":   "11101", 
             "$fp":   "11110", 
             "$ra":   "11111"} 

instrucciones = {"add": ["R", "rd", "rs", "rt"], 
                 "addi": ["I", "rt", "rs", "imm"], 
                 "addiu": ["I", "rt", "rs", "imm"], 
                 "addu": ["R", "rd", "rs", "rt"],
                 "and": ["R", "rd", "rs", "rt"], 
                 "andi": ["I", "rt", "rs", "imm"],
                 "beq": ["I", "rs", "rt", "imm"],
                 "bne": ["I", "rs", "rt", "imm"],
                 "j": ["J", "imm"], 
                 "jal": ["J", "imm"], 
                 "jr": ["R", "rs"],
                 "lbu": ["I", "rt", "rs", "imm"], 
                 "lhu": ["I", "rt", "rs", "imm"], 
                 "ll": ["I", "rt", "rs", "imm"], 
                 "lui": ["I", "rt", "imm"], 
                 "lw": ["I", "rt", "rs", "imm"], 
                 "nor": ["R", "rd", "rs", "rt"],
                 "or": ["R", "rd", "rs", "rt"], 
                 "ori": ["I", "rt", "rs", "imm"], 
                 "slt": ["R", "rd", "rs", "rt"], 
                 "slti": ["I", "rt", "rs", "imm"], 
                 "sltiu": ["I", "rt", "rs", "imm"], 
                 "sltu": ["R", "rd", "rs", "rt"],
                 "sll": ["R", "rd", "rt", "shamt"], 
                 "srl": ["R", "rd", "rt", "shamt"], 
                 "sb": ["I", "rt", "rs", "imm"], 
                 "sc": ["I", "rt", "rs", "imm"],
                 "sh": ["I", "rt", "rs", "imm"], 
                 "sw": ["I", "rt", "rs", "imm"],
                 "sub": ["R", "rd", "rs", "rt"],
                 "subu": ["R", "rd", "rs", "rt"],
                 "mfhi": ["R", "rd"], 
                 "mflo": ["R", "rd"], 
                 "mult": ["R", "rs", "rt"], 
                 "multu": ["R", "rs", "rt"], 
                 "div": ["R", "rs", "rt"], 
                 "divu": ["R", "rs", "rt"]}

opcodes = { "add": [0, 32], 
            "addi": [8], 
            "addiu": [9], 
            "addu": [0, 33], 
            "and": [0, 36], 
            "andi": [12], 
            "beq": [4], 
            "bne": [5],
            "j": [2], 
            "jal": [3], 
            "jr": [0, 8], 
            "lbu": [36], 
            "lhu": [37],  
            "ll": [48], 
            "lui": [15], 
            "lw": [35], 
            "nor": [0, 39],
            "or": [0, 37], 
            "ori": [13], 
            "slt": [0, 42], 
            "slti": [10], 
            "sltiu": [11], 
            "sltu": [0, 43], 
            "sll": [0, 0], 
            "srl": [0, 2],
            "sb": [40], 
            "sc": [56], 
            "sh": [41], 
            "sw": [43], 
            "sub": [0, 34], 
            "subu": [0, 35], 
            "mfhi": [0, 16], 
            "mflo": [0, 18], 
            "mult": [0, 24], 
            "multu": [0, 25], 
            "div": [0, 26], 
            "divu": [0, 27]}

def esEtiqueta(param):
    try:
        eval(param)
        return False
    except:
        return True

def regToBin(registro):
    return registros[registro]

def shamtToBin(shamt):
    binario = list(str(bin(eval(shamt))))
    binario.pop(0)
    binario.pop(0)
    if len(binario) < 5:
        for i in range(5 - len(binario)):
            binario.insert(0,'0')
    return "".join(binario)

def opcodeToBin (opcode):
    binario = list(str(bin(opcode)))
    binario.pop(0)
    binario.pop(0)
    if len(binario) < 6:
        for i in range(6 - len(binario)):
            binario.insert(0,'0')
    return "".join(binario)

def tipoR(frase):
    traduccion = {"opcode":"000000", "rs":"00000","rt":"00000","rd":"00000","shamt":"00000","func":"000000"}
    parametros = frase.split()
    for i in range(len(parametros)): 
        if "rd" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("rd"):
                traduccion["rd"] = str(regToBin(parametros[i]))
        if "rt" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("rt"):
                traduccion["rt"] = str(regToBin(parametros[i]))
        if "rs" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("rs"):
                traduccion["rs"] = str(regToBin(parametros[i]))
        if "shamt" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("shamt"):
                traduccion["shamt"] = str(shamtToBin(parametros[i]))
    traduccion["func"] = str(opcodeToBin(opcodes[parametros[0]][1]))
    return (traduccion["opcode"] + traduccion["rs"] + traduccion["rt"] + traduccion["rd"] + traduccion["shamt"] + traduccion["func"])

def immToBin (imm):
    try:
        scale = 16
        numOfBits = 16
        res = bin(int(imm, scale))[2:].zfill(numOfBits)
    except:
        res = imm
    return str(res)

def indexSup (lista, elemento):
    try:
        res = lista.index(elemento)
        return res
    except:
        return False

def tipoI(frase):
    global PCactual
    traduccion = {"opcode":"000000", "rs":"00000","rt":"00000", "imm":"0000000000000000"}
    parametros = frase.split()
    for i in range(len(parametros)):
        if i == 0:
            traduccion["opcode"] = str(opcodeToBin(opcodes[parametros[i]][0]))
        if "rt" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("rt"):
                traduccion["rt"] = str(regToBin(parametros[i]))
        if "rs" in instrucciones[parametros[0]]:
            if i == instrucciones[parametros[0]].index("rs"):
                traduccion["rs"] = str(regToBin(parametros[i]))
        if i == instrucciones[parametros[0]].index("imm"):
            if esEtiqueta(parametros[i]):
                ope = int((etiquetas[parametros[i]] - PCactual - 4)/4)
                traduccion["imm"] = str(immToBin(hex(ope)))
            else:
                traduccion["imm"] = str(immToBin(parametros[i]))
    return (traduccion["opcode"] + traduccion["rs"] + traduccion["rt"] + traduccion["imm"])

def immToBinEsp(imm):
    try:
        scale = 16
        numOfBits = 26
        res = bin(int(imm, scale))[2:].zfill(numOfBits)
    except:
        res = imm
    return str(res)


def tipoJ(frase):
    traduccion = {"opcode":"000000","imm":"00000000000000000000000000"}
    parametros = frase.split()
    for i in range(len(parametros)): 
        if i == 0:
            traduccion["opcode"] = str(opcodeToBin(opcodes[parametros[i]][0]))
        if i == 1 and "imm" in instrucciones[parametros[0]]:
            if esEtiqueta(parametros[i]):
                traduccion["imm"] = str(immToBinEsp(hex(etiquetas[parametros[i]])))
            else:
                traduccion["imm"] = str(immToBinEsp(parametros[i]))
    #print(traduccion["opcode"]+traduccion["imm"])
    return (traduccion["opcode"]+traduccion["imm"])

def filtro(parame):
    global PCactual, etiquetas
    frase = parame.split()
    if instrucciones.get(frase[0],[0])[0] == "R":
        PCactual = PCactual + 4
        return tipoR(parame)
    elif instrucciones.get(frase[0],[0])[0] == "I":
        PCactual = PCactual + 4
        return tipoI(parame)
    elif instrucciones.get(frase[0],[0])[0] == "J":
        PCactual = PCactual + 4
        return tipoJ(parame)
    else:
        return parame

def informacion():
    messagebox.showinfo(message= "Creado por: \n Juan José Fernández \n Esteban Llanos \n Jesus Valencia", title= "Información")

def calcularEtiqueta(parame):
    global PCactual, etiquetas
    parame = parame.replace(':','')
    #print("Se agrego", parame, "a etiquetas ")
    etiquetas[parame] = PCactual

def filtrarEtiquetas(parame):
    global PCactual, etiquetas
    #print(hex(PCactual), '.', parame)
    frase = parame.split()
    if instrucciones.get(frase[0],[0])[0] == "R":
        PCactual = PCactual + 4
    elif instrucciones.get(frase[0],[0])[0] == "I":
        PCactual = PCactual + 4
    elif instrucciones.get(frase[0],[0])[0] == "J":
        PCactual = PCactual + 4
    elif parame.endswith(':'):
        return calcularEtiqueta(parame)

def botonTraducir():
    global PCactual,etiquetas
    salida.delete("1.0", "end")
    entrr = str(entrada.get("1.0", "end"))
    PCactual = 0x400000
    lista = re.split(r'\n',entrr)
    final = ''
    for i in lista:
        if i != '':
            filtrarEtiquetas(i)
    PCactual = 0x400000
    #print(etiquetas)
    for i in lista: 
        if i != '':
            final += filtro(i)
            final += "\n"
    salida.insert(INSERT,final)

def cargarArchivo():
    nombreArchivo = filedialog.askopenfilename(initialdir = "/", title = "Seleccione Archivo", filetypes = (("txt files", "*.txt"), ("Todos los archivos", "*.*")))
    if(nombreArchivo != ""):
        archivo = open(nombreArchivo, "r", encoding="utf-8")
        contArchivo = archivo.read()
        archivo.close()
        entrada.delete("1.0", END)
        entrada.insert("1.0", contArchivo)

def salir():
    sys.exit()

PCactual = 0

ventana = Tk() #Se crea la interfaz grafica con TKinter
ventana.geometry("1280x720+130+50") #Se definen las dimensiones de la ventana
ventana.configure(bg="gray") #Se define el color de la ventana
ventana.title("Traductor MIPS") #Se define el titulo de la ventana
nombreApp = Label(ventana, text="Traductor MIPS", font=("Comic Sans MS", 40), bg="gray") #Se define el label que referencia al titulo
nombreApp.place(x=440, y=10) #Se ubica el primer label
entrada = Text(ventana, height=25, width=50, font=("Comic Sans MS", 11)) #Se define el primer cuadro de texto
entrada.place(x=20, y=150) #Se ubica el primer cuadro de texto
salida = Text(ventana, height=25, width=50, font=("Comic Sans MS", 11)) #Se define el segundo cuadro de texto el cual es de salida
salida.place(x=775, y=150) #Se ubica el cuadro de texto de salida
boton = Button(ventana, text="Convertir", bg="red", fg="black", font=("Comic Sans MS", 25), command=botonTraducir) #se define el boton de conversion
boton.place(x=550, y=300) #se ubica el boton
info = Button(ventana, text="Info", bg="red", fg="black", font=("Comic Sans MS", 15), command=informacion) #se define el boton de conversion
info.place(x=600, y=500) #se ubica el boton
intructivo = Label(ventana, text="Ejemplo: \nsw t1 t0 0x000", font=("Comic Sans MS", 15), bg="gray") #Se crea el label intructivo
intructivo.place(x=560, y=235) #Se ubica el label
botonArchivo = Button(ventana, text="Cargar Archivo", bg="red", fg="black", font=("Comic Sans MS", 15), command=cargarArchivo) #Se define el boton para cargar archivo
botonArchivo.place(x=100, y=50) #Se ubica el boton de archivo
botonSalida = Button(ventana, text="Salir", bg="red", fg="black", font=("Comic Sans MS", 15), command=salir) #Se define el boton para salir
botonSalida.place(x=1100, y=50) #Se ubica el boton para salir

ventana.mainloop()