#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from rotor import *
from plugboard import *
from tooltip import *
import tkMessageBox

class Enigma(Frame):
    """ Symulator Enigmy M3 (Wermacht, Luftwaffe, Kriegsmarine) wraz z GUI """
    
    def __init__(self):
        """ Bezparametrowy konstruktor """
        Frame.__init__(self)
        self.master.title("Enigma")
        self.grid()

        # Rotory
        rI = ("I", Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'))
        rII = ("II", Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'))
        rIII = ("III", Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'))
        rIV = ("IV", Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'))
        rV = ("V", Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'))

        # Reflektory
        rb = ("B", Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT"))
        rc = ("C", Rotor("FVPJIAOYEDRZXWGCTKUQSBNMHL"))

        # Dostepna konfiguracja
        self.rotor = [rI, rII, rIII, rIV, rV]
        self.refl = [rb, rc]

        # Wybor konfiguracji domyslnej
        self.r = [rIII, rII, rI, rb]
        self.r[2][1].next = self.r[3][1]
        self.r[1][1].next = self.r[2][1]
        self.r[0][1].next = self.r[1][1]

        self.CreateWidgets()
        self.Update()

    def CreateWidgets(self):
        """ Tworzy guzikowy interfejs """

        # Wejscie
        self.entry = Text(self, width = 80, height = 12, font='Helvetica')
        sbar = Scrollbar(self)
        sbar.config(command = self.entry.yview)
        self.entry.config(yscrollcommand=sbar.set)
        self.entry.grid(columnspan = 4)
        sbar.grid(row = 0, column = 4, sticky = N+S)

        # Stan maszyny
        
        self.label = Label(self, font='Helvetica', relief = GROOVE)
        self.label.grid(row = 1, column = 0, sticky = N+S+W+E)
        self.label1 = Label(self, font='Helvetica', relief = GROOVE)
        self.label1.grid(row = 1, column = 1, sticky = E +W+S+N)
        self.label2 = Label(self, font='Helvetica', relief = GROOVE)
        self.label2.grid(row = 1, column = 2, sticky = N+S+W+E)
        self.label3 = Label(self, font='Helvetica', relief = GROOVE)
        self.label3.grid(row = 1, column = 3, sticky = W +E+S+N)

        self.label1w = Label(self, relief = GROOVE)
        self.label1w.grid(row = 2, column = 1, sticky = W+E)
        self.label2w = Label(self, relief = GROOVE)
        self.label2w.grid(row = 2, column = 2, sticky = W+E)
        self.label3w = Label(self, relief = GROOVE)
        self.label3w.grid(row = 2, column = 3, sticky = W+E)

        self.label1n = Label(self, relief = RIDGE)
        self.label1n.grid(row = 3, column = 1, sticky = E + W+S+N)
        self.label2n = Label(self, relief = RIDGE)
        self.label2n.grid(row = 3, column = 2, sticky = E+W+S+N)
        self.label3n = Label(self, relief = RIDGE)
        self.label3n.grid(row = 3, column = 3, sticky = W +E+S+N)

        ToolTip(self.label, msgFunc = lambda: self.GetRotorDesc(self.r[3]), delay = 0)
        ToolTip(self.label1n, msgFunc = lambda: self.GetRotorDesc(self.r[2]), delay = 0)
        ToolTip(self.label2n, msgFunc = lambda: self.GetRotorDesc(self.r[1]), delay = 0)
        ToolTip(self.label3n, msgFunc = lambda: self.GetRotorDesc(self.r[0]), delay = 0)

        # Lacznica kablowa
        self.label4 = Label(self, text="Lacznica kablowa:")
        self.label4.grid(row = 4)

        self.entry4 = Entry(self)
        self.entry4.grid(row = 4, column = 1, columnspan = 3, sticky = W+E)

        self.btn = Button(self, text = "Szyfruj", command = self.Encode)
        self.btn.grid(column = 0, columnspan = 4)

        # Wyjscie
        self.entry2 = Text(self, width = 80, height = 12, font='Helvetica')
        self.entry2.grid(columnspan = 4)
        sbar = Scrollbar(self)
        sbar.config(command = self.entry2.yview)
        self.entry2.config(yscrollcommand=sbar.set)
        self.entry2.grid(columnspan = 4)
        sbar.grid(row = 6, column = 4, sticky = N+S)

        # Dolaczenie eventow

        self.label1.bind("<Button-1>", (lambda e: self.r[2][1].incoffset() or self.Update()))
        self.label1.bind("<Button-3>", (lambda e: self.r[2][1].decoffset() or self.Update()))
        self.label2.bind("<Button-1>", (lambda e: self.r[1][1].incoffset() or self.Update()))
        self.label2.bind("<Button-3>", (lambda e: self.r[1][1].decoffset() or self.Update()))
        self.label3.bind("<Button-1>", (lambda e: self.r[0][1].incoffset() or self.Update()))
        self.label3.bind("<Button-3>", (lambda e: self.r[0][1].decoffset() or self.Update()))

        self.label.bind("<Button-1>", lambda e: self.ChangeReflector())
        self.label1n.bind("<Button-1>", lambda e: self.ChangeRotor(2))
        self.label2n.bind("<Button-1>", lambda e: self.ChangeRotor(1))
        self.label3n.bind("<Button-1>", lambda e: self.ChangeRotor(0))

        self.label1w.bind("<Button-1>", lambda e: self.r[2][1].incringsetting() or self.Update())
        self.label1w.bind("<Button-3>", lambda e: self.r[2][1].decringsetting() or self.Update())
        self.label2w.bind("<Button-1>", lambda e: self.r[1][1].incringsetting() or self.Update())
        self.label2w.bind("<Button-3>", lambda e: self.r[1][1].decringsetting() or self.Update())
        self.label3w.bind("<Button-1>", lambda e: self.r[0][1].incringsetting() or self.Update())
        self.label3w.bind("<Button-3>", lambda e: self.r[0][1].decringsetting() or self.Update())


    def GetRotorDesc(self, r):
        """ Zwraca opis (string) wybranego rotora """

        if r[1].next:
            s = "Rotor:       " + r[0] + "\n"
        else:
            s = "Reflektor:       " + r[0] + "\n"
            
        s += "Permutacja: " + r[1].getlayout()

        if r[1].next:
            s += "\nZapadka:    " + r[1].getnotch()
            
        return s

    def ChangeRotor(self, n):
        """ Zmienia rotor na kolejny z dostepnych """
        m = len(self.rotor)

        k = self.rotor.index(self.r[n])

        for l in range(1, m):
            l = (l + k) % m
            if self.rotor[l][1].next == None:
                # Male prze(sz)czepienie referencji rotorow
                self.r[n][1].next = None
                self.r[n] = self.rotor[l]
                self.r[n][1].next = self.r[n+1][1]

                if n - 1 > 0:
                    self.r[n-1][1].next = self.r[n][1]
                break

        self.Update()

    def ChangeReflector(self):
        """ Zmienia reflektor na kolejny z dostepnych """
        m = len(self.refl)
        k = (self.refl.index(self.r[3]) + 1) % m
        self.r[3] = self.refl[k]
        self.r[2][1].next = self.r[3][1]

        self.Update()

    def Update(self):
        """ Odswieza stan maszyny w GUI """        
        self.label.config(text = self.r[3][0])
        self.label1.config(text = self.r[2][1].getoffset())
        self.label2.config(text = self.r[1][1].getoffset())
        self.label3.config(text = self.r[0][1].getoffset())

        self.label1n.config(text = self.r[2][0])
        self.label2n.config(text = self.r[1][0])
        self.label3n.config(text = self.r[0][0])

        self.label1w.config(text = self.r[2][1].getringsetting())
        self.label2w.config(text = self.r[1][1].getringsetting())
        self.label3w.config(text = self.r[0][1].getringsetting())

    def Encode(self):
        """ Szyfruje wiadomosc i wyswietla zaszyfrowana """

        try:
            plgbrd = PlugBoard(self.entry4.get())
        except:
            tkMessageBox.showwarning("Enigma", "Niepoprawne dane lacznicy wejsciowej\n")
            
        sin = self.entry.get(1.0, END)
        sout = ""

        n = 0

        for c in sin:
            if c.isalpha():
                if n % 5 == 0 and n > 0:
                    sout += " " # wstawia ladne odstepy
                    
                self.r[0][1].advance()
                sout += plgbrd.put(self.r[0][1].put(plgbrd.put(c.upper())))
                n += 1;

        self.entry2.delete(1.0, END)
        self.entry2.insert(END, sout)
        
        self.Update()

app = Enigma()
app.mainloop()
