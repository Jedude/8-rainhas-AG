from tkinter import *
import tkinter as tk
from tkinter import Tk


resultado=[]

import back
class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1="white", color2="black"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


# image comes from the silk icon set which is under a Creative Commons
# license. For more information see http://www.famfamfam.com/lab/icons/silk/
imagedata =".\\rainha.png"



if __name__ == "__main__":
    root: Tk = tk.Tk()
    root.title("ALGORITMOS GENÉTICOS - 8 RAINHAS")
    root.geometry("600x700")
    root.minsize(549,659)
    root.maxsize(549,659)
    board = GameBoard(root)

    resultado=[0,0,0,0,0,0,0,0]

    top=Frame(root)
    top.pack(side=TOP)
    bot = Frame(root)
    bot.pack(side=BOTTOM)

    tamanho_var= tk.StringVar()
    tamanho_var.set(10)
    maximo_var = tk.StringVar()
    maximo_var.set(1000)
    mutacao_var = tk.StringVar()
    mutacao_var.set(0.05)
    cromo_var = tk.StringVar()
    cromo_var.set("Teste")
    gera_var = tk.StringVar()
    gera_var.set("Teste")
    pop_var = tk.StringVar()
    pop_var.set("Teste")
    vc=tk.IntVar()
    c1 = tk.Checkbutton(text='Dizimação', variable=vc, onvalue=1, offvalue=0)
    vc.set(1)

    #frame1 = tk.Frame()
    ltamanho = tk.Label(text="Tamanho(pop):")
    entrada = tk.Entry(textvariable=tamanho_var,width="8")

    lmaximo = tk.Label(text="Maximo(ger):")
    entradag = tk.Entry(textvariable=maximo_var,width="8")

    lmutacao = tk.Label(text="Taxa(mutação):")
    entradam = tk.Entry(textvariable=mutacao_var,width="8")

    lresultados = tk.Label(text="Resultados")
    lcr = tk.Label(text="Cromossomo")
    lge = tk.Label(text="Gerações")
    lpt = tk.Label(text="População Total")

    ltamanho.pack(in_=top,side=LEFT)
    entrada.pack(in_=top,side=LEFT)
    lmaximo.pack(in_=top,side=LEFT)
    entradag.pack(in_=top,side=LEFT)
    lmutacao.pack(in_=top, side=LEFT)
    entradam.pack(in_=top, side=LEFT)
    lresultados.pack(in_=bot)
    lcr.pack(in_=bot, side=LEFT)
    lge.pack(in_=bot, side=LEFT)
    lpt.pack(in_=bot, side=LEFT)


    def posicionaR():
        rainha1 = tk.PhotoImage(file=imagedata)
        rainha2 = tk.PhotoImage(file=imagedata)
        rainha3 = tk.PhotoImage(file=imagedata)
        rainha4 = tk.PhotoImage(file=imagedata)
        rainha5 = tk.PhotoImage(file=imagedata)
        rainha6 = tk.PhotoImage(file=imagedata)
        rainha7 = tk.PhotoImage(file=imagedata)
        rainha8 = tk.PhotoImage(file=imagedata)

        # adicionar peças
        board.addpiece("rainha1", rainha1, 0, resultado[0])
        board.addpiece("rainha2", rainha2, 1, resultado[1])
        board.addpiece("rainha3", rainha3, 2, resultado[2])
        board.addpiece("rainha4", rainha4, 3, resultado[3])
        board.addpiece("rainha5", rainha5, 4, resultado[4])
        board.addpiece("rainha6", rainha6, 5, resultado[5])
        board.addpiece("rainha7", rainha7, 6, resultado[6])
        board.addpiece("rainha8", rainha8, 7, resultado[7])

    def clique():
        global resultado
        resolver = True
        populacao = back.populacaoInicial(int(entrada.get()))
        geracoes = 1
        back.MAX_GERACAO=int(entradag.get())
        back.probabilidadeMutacao=float(entradam.get())
        if vc.get()==1:
            back.DIZIMACAO=True
            print("True")
        else:
            back.DIZIMACAO =False
            print("Falso")
        back.AG()
        resultado=back.resultado
        geracoes=back.geracoes
        posicionaR()
        lcr.config(text="Cromossomo: " + str(resultado))
        lge.config(text="Gerações: " + str(geracoes))
        lpt.config(text="População Total: " + str(geracoes * int(entrada.get())))
        back.geracoes=0
        """
        while (resolver):
            print(back.DIZIMACAO)
            for i in populacao:
                if i.aptidao == 28:
                    resultado = i.posicoes
                    posicionaR()
                    print("resultado:", resultado)
                    lcr.config(text="Cromossomo: "+str(resultado))
                    print("Quantidade de gerações: ", geracoes)
                    lge.config(text="Gerações: "+str(geracoes))
                    print("Quantidade de individuos: ", geracoes * back.POPULACAO)
                    lpt.config(text="População Total: "+str(geracoes*int(entrada.get())))
                    resolver = False
                    break
            populacao = back.gerarPopulacao(int(entrada.get()))
            geracoes += 1

            if geracoes >= back.MAX_GERACAO:
                resolver = False
        """

    #botão e checkbox
    b = Button(root, text="Achar solução", width=20, height=2,command= clique)
    c1.pack(in_=top, side=LEFT)
    b.pack(pady=1)

    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    #board.grid(row=2,column= 0, sticky="nsew",pady=10, padx=10)
    #board.grid_rowconfigure(0, weight=10)
    #board.grid_columnconfigure(0, weight=10)

    rainha1 = tk.PhotoImage(file=imagedata)
    rainha2 = tk.PhotoImage(file=imagedata)
    rainha3 = tk.PhotoImage(file=imagedata)
    rainha4 = tk.PhotoImage(file=imagedata)
    rainha5 = tk.PhotoImage(file=imagedata)
    rainha6 = tk.PhotoImage(file=imagedata)
    rainha7 = tk.PhotoImage(file=imagedata)
    rainha8 = tk.PhotoImage(file=imagedata)

    # adicionar peças
    board.addpiece("rainha1", rainha1, 0, resultado[0])
    board.addpiece("rainha2", rainha2, 1, resultado[1])
    board.addpiece("rainha3", rainha3, 2, resultado[2])
    board.addpiece("rainha4", rainha4, 3, resultado[3])
    board.addpiece("rainha5", rainha5, 4, resultado[4])
    board.addpiece("rainha6", rainha6, 5, resultado[5])
    board.addpiece("rainha7", rainha7, 6, resultado[6])
    board.addpiece("rainha8", rainha8, 7, resultado[7])

    root.mainloop()
