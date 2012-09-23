# -*- coding: utf-8 -*-

class Rotor:
    """ Klasa Symulujaca rotory Enigmy """
    def __init__(self, layout, notch = 'Z', ringsetting = 1, offset = 'A'):
        """ layout = permutacja alfabetu, ringsetting = obrot okablowania, offset = pozycja rotora, notch = zapdka """
        n = len(layout)
        if(n != 26): # tylko 26 znakow na rotorze
            raise ValueError("len(layout) != 26)")

        if not layout.isalpha():
            raise ValueError("invalid layout")

        if not notch.isalpha():
            raise ValueError("invalid notch")

        # Symulacja polaczenia kilku rotorow, wskazuje na nastepny (przypadek szczegolny Refelektor)
        self.next = None 
        
        self.__layout = layout

        # Tablica odwrotna, przydatna przy wracajacym sygnale
        self.__layout2 = zip(layout, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.__layout2.sort()
        self.__layout2 = reduce(lambda a, b: a + b[1], self.__layout2, "")
        #print self.__layout2

        # Zapadka    
        self.__notch = ord(notch) - ord('A')

        # Obrot wew. okablowania
        self.setringsetting(ringsetting)

        # Aktualna pozycja rotora
        self.setoffset(offset)

    def getlayout(self):
        """ Zwraca permutacje rotora

        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.getlayout()
        'BDFHJLCPRTXVZNYEIWGAKMUSQO'
        """
        return self.__layout

    def getnotch(self):
        """ Zwraca miejsce zapadki


        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.getnotch()
        'V'
        """
        return chr(self.__notch + ord('A'))

    def getringsetting(self):
        """ Zwraca obrot okablowania rotora

        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.getringsetting()
        1
        """
        return (26 - self.__ringstg) % 26 + 1

    def getoffset(self):
        """ Zwraca aktualna pozycje rotora

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.getoffset()
        'A'"""
        return chr(self.__offset + ord('A'))

    def setoffset(self, offset):
        """ Ustawia aktualna pozycje rotora

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.setoffset('G')
        >>> r3.getoffset()
        'G'
        """
        ofs = ord(offset) - ord('A')
        if ofs < 0 or ofs > 25:
            raise ValueError("invalid offset")

        self.__offset = ofs

    def incoffset(self):
        """ Zwieksza pozycje rotora o 1

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.incoffset()
        >>> r3.getoffset()
        'B'
        """
        self.setoffset(chr((ord(self.getoffset()) - ord('A') + 1) % 26 + ord('A')))

    def decoffset(self):
        """ Zmniejsza pozycje rotora o 1

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.decoffset()
        >>> r3.getoffset()
        'Z'
        """
        self.setoffset(chr((ord(self.getoffset()) - ord('A') - 1 + 26) % 26 + ord('A')))

    def setringsetting(self, ringsetting):
        """ Ustawia okablowanie

        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.setringsetting(12)
        >>> r3.getringsetting()
        12
        """
        if ringsetting < 1 or ringsetting > 26:
            raise ValueError("invalid ringsetting")
        
        self.__ringstg = (26 - ringsetting + 1) % 26

    def incringsetting(self):
        """ Przesuwa kabelki o jeden 'do przodu'

        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.incringsetting()
        >>> r3.getringsetting()
        2
        """
        self.setringsetting((self.getringsetting() % 26) + 1)

    def decringsetting(self):
        """ 'Cofa' kabelki o jeden

        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r3.decringsetting()
        >>> r3.getringsetting()
        26
        """
        self.setringsetting((self.getringsetting() - 1 - 1 + 26) % 26 + 1)

    def __checknotch(self):
        """ Sprawdza czy ma nastapic obrot tego rotora i sasiedniego (aktywana zapadka)

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.advance()
        >>> r1.setoffset('Z')
        >>> r2.setoffset('D')
        >>> r3.setoffset('V')
        >>> r3.advance()
        >>> r3.getoffset()
        'W'
        >>> r2.getoffset()
        'E'
        >>> r1.getoffset()
        'Z'
        >>> r.getoffset()
        'A'
        >>> r3.advance()
        >>> r3.getoffset()
        'X'
        >>> r2.getoffset()
        'F'
        >>> r1.getoffset()
        'A'
        >>> r.getoffset()
        'A'
        >>> r3.advance()
        >>> r3.getoffset()
        'Y'
        >>> r2.getoffset()
        'F'
        >>> r1.getoffset()
        'A'
        >>> r.getoffset()
        'A'
        """
        
        if not self.next:
            return # w takim razie jest to reflektor
        
        if self.__offset == self.__notch:
            self.next.advance()
            self.__offset = (self.__offset + 1) % 26
        else:
            self.next.__checknotch()

    def advance(self):
        """ Zmienia stan wszystkich rotorow (o ile trzeba) o nastepna pozycje

        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.advance()
        >>> r1.setoffset('Z')
        >>> r2.setoffset('D')
        >>> r3.setoffset('V')
        >>> r3.advance()
        >>> r3.getoffset()
        'W'
        >>> r2.getoffset()
        'E'
        >>> r1.getoffset()
        'Z'
        >>> r.getoffset()
        'A'
        >>> r3.advance()
        >>> r3.getoffset()
        'X'
        >>> r2.getoffset()
        'F'
        >>> r1.getoffset()
        'A'
        >>> r.getoffset()
        'A'
        >>> r3.advance()
        >>> r3.getoffset()
        'Y'
        >>> r2.getoffset()
        'F'
        >>> r1.getoffset()
        'A'
        >>> r.getoffset()
        'A'
        """
        
        if not self.next:
            return # w takim razie jest to reflektor
        
        if self.__offset == self.__notch:
            self.next.advance()
        else:
            self.next.__checknotch()
        
        self.__offset = (self.__offset + 1) % 26

    def __encode(self, ch):
        """ Koduje znak """
        c = ord(ch) - ord('A')
        aa = ord(self.__layout[(self.__ringstg + self.__offset + c) % 26]) - ord('A')
        #print "encode", ch, aa
        aa = chr(((52 + aa - self.__offset - self.__ringstg) % 26) + ord('A'))
        return aa

    def __decode(self, ch):
        """ Koduje wracajacy sygnal """
        c = (ord(ch) - ord('A') + self.__ringstg + self.__offset) % 26
        c = ord(self.__layout2[c]) - ord('A')
        c = chr(ord('A') + ((52 + c - self.__offset - self.__ringstg) % 26))
        #print "decode", ch, c
        return c
    
    def put(self, ch):
        """ Koduje znak puszczacjac przez pozostale rotory

        Test Reflektora:
        >>> r = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r.put('A')
        'E'
        >>> r.put('S')
        'S'
        >>> r.put('AS')
        Traceback (most recent call last):
        TypeError: ord() expected a character, but string of length 2 found
        >>>
        >>> r.put('-')
        Traceback (most recent call last):
        ValueError: ch is not alphabetic!

        Test calosciowy:
        >>> r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
        >>> r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
        >>> r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
        >>> r  = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> r3.next = r2
        >>> r2.next = r1
        >>> r1.next = r
        >>> r3.advance()
        >>> r1.setoffset('Z')
        >>> r2.setoffset('D')
        >>> r3.setoffset('V')
        >>> r3.advance()
        >>> r3.put('A')
        'P'
        >>> r3.advance()
        >>> r3.put('A')
        'Q'
        """

        if not ch.isalpha():
            raise ValueError("ch is not alphabetic!")
                             
        if not self.next:
            self.__offset = 0
            self.__ringstg = 0

        # Zakoduj znak wejsciowy
        c = self.__encode(ch)

        if not self.next:
            #print "Ref", c
            return c # gdyz jest to reflektor

        # Przekaz dalej...
        c = self.next.put(c)

        # ... zakoduj powrotny sygnal i zwroc
        return self.__decode(c)
        
