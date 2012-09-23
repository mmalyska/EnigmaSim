# -*- coding: utf-8 -*-

class PlugBoard:
    def __init__(self, inverttbl):
        """ Konstruktor przyjmuje argument polaczen w postaci: "AZ BC"
            (zamienione znaki parami A i Z oraz B i C
        """
        invert = inverttbl.split(" ")

        self.__tbl = {}

        for pair in invert:
            if pair == '':
                continue

            if len(pair) != 2 or not pair.isalpha() or not pair.isupper():
                raise ValueError("invalid inverttbl")
            
            a = pair[0]
            b = pair[1]

            self.__tbl[a] = b
            self.__tbl[b] = a

        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if not ch in self.__tbl:
                self.__tbl[ch] = ch

    def put(self, char):
        """ Zamienia znak zgodnie ze wczesniej podanymi polaczeniami """
        if not char.isalpha():
            raise ValueError("invalid char")
        
        return self.__tbl[char]
