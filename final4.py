# ### ----------------- ### ----------------- ###
#  |  \                  |                  /  |
#  |    \                |                /    |
#  |      \              |              /      |
#  |      ### --------- ### --------- ###      |
#  |       |  \          |          /  |       |
#  |       |    \        |        /    |       |
#  |       |      ### - ### - ###      |       |
#  |       |       |           |       |       |
# ### --- ### --- ###         ### --- ### --- ###
#  |       |       |           |       |       |
#  |       |      ### - ### - ###      |       |
#  |       |    /        |        \    |       |
#  |       |  /          |          \  |       |
#  |      ### --------- ### --------- ###      |
#  |      /              |              \      |
#  |    /                |                \    |
#  |  /                  |                  \  |
# ### ----------------- ### ----------------- ###

import copy
import statistics
import pygame
import sys
import time
culoare_jmin = None
culoare_jmax = None
blocat = False
winner = None
rem = False
nr_euristica = None

dific = {'u': "USOR", 'm': "MEDIU", 'g': "GREU"}
culs = {'r': "ROSU", 'n': "NEGRU"}


poz = {
    1: (100, 100), 2: (400, 100), 3: (700, 100), 4: (700, 400),
    5: (700, 700), 6: (400, 700), 7: (100, 700), 8: (100, 400),
    9: (200, 200), 10: (400, 200), 11: (600, 200), 12: (600, 400),
    13: (600, 600), 14: (400, 600), 15: (200, 600), 16: (200, 400),
    17: (300, 300), 18: (400, 300), 19: (500, 300), 20: (500, 400),
    21: (500, 500), 22: (400, 500), 23: (300, 500), 24: (300, 400)
}

mori = { 1: [[1, 2, 3], [1, 8, 7], [1, 9, 17]],
        2: [[1, 2, 3], [2, 10, 18]],
        3: [[1, 2, 3], [3, 4, 5], [3, 11, 19]],
        4: [[4, 12, 20], [3, 4, 5]],
        5: [[3, 4, 5], [5, 6, 7], [5, 13, 21]],
        6: [[5, 6, 7], [6, 14, 22]],
        7: [[7, 6, 5], [7, 8, 1], [7, 15, 23]],
        8: [[1, 8, 7], [8, 16, 24]],
        9: [[1, 9, 17], [9, 10, 11], [9, 16, 15]],
        10: [[9, 10, 11], [2, 10, 18]],
        11: [[11, 9, 10], [11, 12, 13], [3, 11, 19]],
        12: [[11, 12, 13], [20, 12, 4]],
        13: [[21, 13, 5], [15, 14, 13], [11, 12, 13]],
        14: [[22, 14, 6], [15, 14, 13]],
        15: [[15, 16, 9], [15, 14, 13], [7, 15, 23]],
        16: [[8, 16, 24], [9, 16, 15]],
        17: [[1, 9, 17], [17, 18, 19], [17, 24, 23]],
        18: [[17, 18, 19], [2, 10, 18]],
        19: [[17, 18, 19], [19, 11, 3], [19, 20, 21]],
        20: [[19, 20, 21], [20, 12, 4]],
        21: [[21, 22,  23], [21, 13, 5], [21, 20, 19]],
        22: [[22, 14, 6], [23, 22, 21]],
        23: [[23, 15, 7], [23, 24, 17], [23, 22, 21]],
        24: [[8, 16, 24], [17, 24, 23]] }

coord_piesa = {}
nr_noduri_gen = 0

class Nod:

    id = 1
    vecini = { 1: [2, 9, 8], # vecinii pe tabla pentru fiecare nod
            2: [1, 3, 10],
            3: [2, 11, 4],
            4: [3, 12, 5],
            5: [4, 13, 6],
            6: [5, 7, 14],
            7: [6, 15, 8],
            8: [1, 16, 7],
            9: [1, 10, 17, 16],
            10: [2, 11, 18, 9],
            11: [10, 3, 12, 19],
            12: [11, 20, 4, 13],
            13: [12, 14, 21, 5],
            14: [22, 15, 13, 6],
            15: [16, 14, 7, 23],
            16: [9, 8, 24, 15],
            17: [9, 18, 24],
            18: [10, 17, 19],
            19: [18, 11, 20],
            20: [19, 12, 21],
            21: [20, 22, 13],
            22: [23, 21, 14],
            23: [24, 22, 15],
            24: [16, 17, 23]}
    
    def __init__(self, id_nod = None, culoare = '', loc_anterior = None): # constructor pentru clasa Nod
        self.id_nod = Nod.id if id_nod == None else id_nod
        self.culoare = culoare
        if Nod.id < 25:
            self.vecini = Nod.vecini[self.id_nod]
        else:
            self.vecini = []
        self.loc_anterior = loc_anterior
        Nod.id += 1

    def __str__(self): # functia str pentru afisarea nodului in consola
        if self.culoare == '':
            if self.id_nod < 10:
                return ' ' + str(self.id_nod) + ' '
            else:
                return str(self.id_nod) + ' '
        else:
            if self.id_nod < 10:
                return self.culoare + str(self.id_nod) + ' '
            else:
                return self.culoare + str(self.id_nod)


class Joc:

    jmin = None
    jmax = None
    timpi_rulare_jmin = []
    timpi_rulare_jmax = []
    lista_nr_noduri_generate = []

    def __init__(self, tabla = None, nr_piese_jmin = 0, nr_piese_jmax = 0): # constructor pentru clasa Joc
        
        # tabla tinuta sub forma de vector cu 24 de noduri(elemente de tip Nod)
        if tabla == None:
            self.tabla = [Nod() for _ in range(0,24)]
        else:
            self.tabla = tabla

        self.numar_piese_plasate_jmin = nr_piese_jmin # numarul de piese deja plasate de jucatorul jmin
        self.numar_piese_plasate_jmax = nr_piese_jmax # numarul de piese deja plasate de jucatorul jmax


    def afisare(self): # functia de afisare a tablei de joc
        print(str(self.tabla[0]) + ' ----------------- ' + str(self.tabla[1]) + ' ----------------- ' + str(self.tabla[2]))
        print(' |  \                  |                  /  |')
        print(' |    \                |                /    |')
        print(' |      \              |              /      |')
        print(' |      ' + str(self.tabla[8]) + ' --------- ' + str(self.tabla[9]) + ' --------- ' + str(self.tabla[10]) + '      |')    
        print(' |       |  \          |          /  |       |')
        print(' |       |    \        |        /    |       |')
        print(' |       |      ' + str(self.tabla[16]) + ' - ' + str(self.tabla[17]) + ' - ' + str(self.tabla[18]) + '      |       |')
        print(' |       |       |           |       |       |')
        print(str(self.tabla[7]) + ' --- ' + str(self.tabla[15]) + ' --- ' + str(self.tabla[23]) + '         ' + str(self.tabla[19]) + ' --- ' + str(self.tabla[11]) + ' --- ' + str(self.tabla[3]))
        print(' |       |       |           |       |       |')
        print(' |       |      ' + str(self.tabla[22]) + ' - ' + str(self.tabla[21]) + ' - ' + str(self.tabla[20]) + '      |       |')
        print(' |       |    /        |        \    |       |')
        print(' |       |  /          |          \  |       |')
        print(' |      ' + str(self.tabla[14]) + ' --------- ' + str(self.tabla[13]) + ' --------- ' + str(self.tabla[12]) + '      |')  
        print(' |      /              |              \      |')
        print(' |    /                |                \    |')
        print(' |  /                  |                  \  |')
        print(str(self.tabla[6]) + ' ----------------- ' + str(self.tabla[5]) + ' ----------------- ' + str(self.tabla[4]))

    # functia de desenare a tablei in interfata grafica
    def deseneaza_tabla(self, id_loc_liber = None, id_piesa_moara = None, piesa_aleasa = None, win = None, remiza = False):
        
        global culoare_jmax, culoare_jmin

        Joc.display.fill((28,81,112))

        pygame.draw.rect(Joc.display, (255,255,255), (100,100,600,600), 2)
        pygame.draw.rect(Joc.display, (255,255,255), (200,200,400,400), 2)
        pygame.draw.rect(Joc.display, (255,255,255), (300,300,200,200), 2)
        
        pygame.draw.line(Joc.display, (255,255,255), poz[1], poz[17])
        pygame.draw.line(Joc.display, (255,255,255), poz[8], poz[24])
        pygame.draw.line(Joc.display, (255,255,255), poz[7], poz[23])
        pygame.draw.line(Joc.display, (255,255,255), poz[6], poz[22])
        pygame.draw.line(Joc.display, (255,255,255), poz[5], poz[21])
        pygame.draw.line(Joc.display, (255,255,255), poz[4], poz[20])
        pygame.draw.line(Joc.display, (255,255,255), poz[3], poz[19])
        pygame.draw.line(Joc.display, (255,255,255), poz[2], poz[18])

        # daca id_piesa_moara != None, desenam moara formata pe tabla        
        if id_piesa_moara != None:

            # extragem configuratiile de mori din care face parte nodul cu id-ul id_piesa_moara
            lista_mori = mori[id_piesa_moara]
            if self.tabla[id_piesa_moara - 1].culoare == Joc.jmax:
                piese_jmin = self.piese_jucator_jmin_care_pot_fi_scoase()

                for moara in lista_mori:
                    for piesa in moara:
                        if self.tabla[piesa - 1].culoare != Joc.jmax: 
                            break
                    else:
                        for nod in self.tabla:
                            if nod.culoare == Joc.jmax:
                                if nod.id_nod in moara:
                                    pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                    pygame.draw.circle(Joc.display, (255,255,0), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 20, 0)
                                else:
                                    pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            elif nod.culoare == Joc.jmin:
                                if (Joc.jmin + str(nod.id_nod)) in piese_jmin:
                                    pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                    pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                                else:
                                    pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            else:
                                pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        break
            else:
                piese_jmax = self.piese_jucator_jmax_care_pot_fi_scoase()

                for moara in lista_mori:
                    for piesa in moara:
                        if self.tabla[piesa - 1].culoare != Joc.jmin: 
                            break
                    else:
                        for nod in self.tabla:
                            if nod.culoare == Joc.jmin:
                                if nod.id_nod in moara:
                                    pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                    pygame.draw.circle(Joc.display, (255,255,0), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 20, 0)
                                else:
                                    pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            elif nod.culoare == Joc.jmax:
                                if (Joc.jmax + str(nod.id_nod)) in piese_jmax:
                                    pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                    pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                                else:
                                    pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            else:
                                pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        break

        else:
            if remiza == False:
                for nod in self.tabla:
                    if nod.culoare == Joc.jmin:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                    elif nod.culoare == Joc.jmax:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        pygame.draw.circle(Joc.display, (153, 51, 255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 15, 0)
                    else:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                
                if win == None:
                    
                    if piesa_aleasa != None and self.tabla[piesa_aleasa - 1].culoare == Joc.jmin:    
                        if piesa_aleasa != None and self.numar_piese_plasate_jmin < 12:
                            vecini = self.tabla[piesa_aleasa - 1].vecini
                        elif piesa_aleasa != None and self.numara_piese_jmin() > 3 and self.numar_piese_plasate_jmin == 12:
                            vecini = self.tabla[piesa_aleasa - 1].vecini
                        elif piesa_aleasa != None and self.numara_piese_jmin() <= 3 and self.numar_piese_plasate_jmin == 12:
                            locuri_libere = self.locuri_libere()
                            vecini = []
                            for loc in locuri_libere:
                                vecini.append(int(loc))
                        else:
                            vecini = []
                    elif piesa_aleasa != None and self.tabla[piesa_aleasa - 1].culoare == Joc.jmax:
                        if piesa_aleasa != None and self.numar_piese_plasate_jmax < 12:
                            vecini = self.tabla[piesa_aleasa - 1].vecini
                        elif piesa_aleasa != None and self.numara_piese_jmax() > 3 and self.numar_piese_plasate_jmax == 12:
                            vecini = self.tabla[piesa_aleasa - 1].vecini
                        elif piesa_aleasa != None and self.numara_piese_jmax() <= 3 and self.numar_piese_plasate_jmax == 12:
                            locuri_libere = self.locuri_libere()
                            vecini = []
                            for loc in locuri_libere:
                                vecini.append(int(loc))
                        else:
                            vecini = []
                    else:
                        vecini = []

                    for nod in self.tabla:
                        if nod.culoare == Joc.jmin:
                            if piesa_aleasa == nod.id_nod:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                pygame.draw.circle(Joc.display, (255,255,0), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 15, 0)
                            else:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        elif nod.culoare == Joc.jmax:
                            if piesa_aleasa == nod.id_nod:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                pygame.draw.circle(Joc.display, (255,255,0), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 15, 0)
                            else:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        else:
                            if id_loc_liber != nod.id_nod:
                                if nod.id_nod in vecini and self.tabla[piesa_aleasa - 1].loc_anterior != nod.id_nod:
                                    coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (124,252,0), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                else:
                                    coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            else:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (123,123,123), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                    
                elif win != None:
                    pygame.display.set_caption("WINNER - " + culs[win])
                    for nod in self.tabla:  # (34,139,34)
                        if win != Joc.jmin:
                            if nod.culoare == Joc.jmin:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                            elif nod.culoare == Joc.jmax:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            else:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)

                        else:
                            if nod.culoare == Joc.jmin:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                            elif nod.culoare == Joc.jmax:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                                pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                            else:
                                coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)

            elif remiza == True:
                pygame.display.set_caption("REMIZA")
                for nod in self.tabla:
                    if nod.culoare == Joc.jmin:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        pygame.draw.circle(Joc.display, culoare_jmin, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                    elif nod.culoare == Joc.jmax:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)
                        pygame.draw.circle(Joc.display, culoare_jmax, [poz[nod.id_nod][0], poz[nod.id_nod][1]], 10, 0)
                    else:
                        coord_piesa[nod.id_nod] = pygame.draw.circle(Joc.display, (255,255,255), [poz[nod.id_nod][0], poz[nod.id_nod][1]], 30, 0)

        pygame.display.update()

    # functie care returrneaza o lista cu locurile libere de pe tabla de joc [str(loc.id_nod), ..] ex: ['1', '5', '23']
    def locuri_libere(self):
        l_libere = []
        for loc in self.tabla:
            if loc.culoare == '':
                l_libere.append(str(loc.id_nod))

        return l_libere

    # functie care returneaza o lista cu piesele jmin de pe tabla de joc [nod.culoare + str(nod.id_nod), ..] ex: ['r1', 'r5', 'r7']
    def piese_jmin(self):
        l_ocupate = []
        for loc in self.tabla:
            if loc.culoare == Joc.jmin:
                l_ocupate.append(loc.culoare + str(loc.id_nod))

        return l_ocupate 
    
    # functie care returneaza o lista cu piesele jmax de pe tabla de joc [nod.culoare + str(nod.id_nod), ..] ex: ['n2', 'n4', 'n22']
    def piese_jmax(self):
        l_ocupate = []
        for loc in self.tabla:
            if loc.culoare == Joc.jmax:
                l_ocupate.append(loc.culoare + str(loc.id_nod))

        return l_ocupate

    # functie care reseteaza locurile anterioare pt fiecare piesa a lui jmin
    def reseteaza_piese_jmin(self):
        for loc in self.tabla:
            if loc.culoare == Joc.jmin:
                loc.loc_anterior = None

    # functie care reseteaza locurile anterioare pt fiecare piesa a lui jmax
    def reseteaza_piese_jmax(self):
        for loc in self.tabla:
            if loc.culoare == Joc.jmax:
                loc.loc_anterior = None

    @classmethod
    def initializeaza(cls, display):
        cls.display = display

    # functie care returneaza jucatorul opus al jucatorului curent
    @classmethod
    def jucator_opus(cls, jucator):
        return cls.jmax if jucator == cls.jmin else cls.jmin

    @classmethod
    def afiseaza_info_final(cls):
        print("Timp minim de gandire al calculatorului: " + str(min(Joc.timpi_rulare_jmax)) + " ms.")
        print("Timp maxim de gandire al calculatorului: " + str(max(Joc.timpi_rulare_jmax)) + " ms.")
        print("Timp mediu de gandire al calculatorului: " + str(round(statistics.mean(cls.timpi_rulare_jmax))) + " ms.")
        print("Timp median de gandire al calculatorului: " + str(statistics.median(cls.timpi_rulare_jmax)) + " ms.")
        print()
        print("Numarul total de noduri generate: " + str(sum(cls.lista_nr_noduri_generate)))
        print("Numarul minim de noduri generate: " + str(min(cls.lista_nr_noduri_generate)))
        print("Numarul maxim de noduri generate: " + str(max(cls.lista_nr_noduri_generate)))
        print("Numarul mediu de noduri generate: " + str(statistics.mean(cls.lista_nr_noduri_generate)))
        print("Numarul median de noduri generate: " + str(statistics.median(cls.lista_nr_noduri_generate)))
        print()
        print("Durata joc: " + str(sum(cls.timpi_rulare_jmax) + sum(cls.timpi_rulare_jmin)) + " ms.")
        print("Numar de mutari ale jucatorului: " + str(len(cls.timpi_rulare_jmin)))
        print("Numar de mutari ale calculatorului: " + str(len(cls.timpi_rulare_jmax)))

    # functie care returneaza numarul de piese al lui jmin deja plasate pe tabla
    def numara_piese_jmin(self):
        nr = 0
        for loc in self.tabla:
            if loc.culoare == Joc.jmin:
                nr += 1
        
        return nr

    # functie care returneaza numarul de piese al lui jmax deja plasate pe tabla
    def numara_piese_jmax(self):
        nr = 0
        for loc in self.tabla:
            if loc.culoare == Joc.jmax:
                nr += 1
        
        return nr

    # functie care returneaza numarul total de mori de pe tabla actuala
    def numar_mori_pe_tabla(self):

        nr = 0
        for nod in self.tabla:
            if nod.culoare != '':
                if self.moara(self.tabla, nod.id_nod, nod.culoare):
                    nr += 1
            
        return nr

    # functia de final care testeaza daca tabla e una finala
    def final(self):
        
        l_libere = self.locuri_libere()

        
        if len(l_libere) == 0 and self.numar_mori_pe_tabla() == 0:
            return "remiza"
        elif self.numara_piese_jmin() < 3 and self.numar_piese_plasate_jmin >= 12:
            return Joc.jmax
        elif self.numara_piese_jmax() < 3 and self.numar_piese_plasate_jmax >= 12:
            return Joc.jmin
        else:
            if self.numar_piese_plasate_jmin == 12 and self.blocare_jmin() == True:
                return Joc.jmax
            elif self.numar_piese_plasate_jmax == 12 and self.blocare_jmax() == True:
                return Joc.jmin

        return False

    # functie care returneaza numarul de piese al unui jucator trimis ca parametru
    def get_numar_piese_plasate(self, jucator):
        if jucator == Joc.jmax:
            return self.numar_piese_plasate_jmax
        else:
            return self.numar_piese_plasate_jmin

    # functie care returneaza True daca jucatorul a format o moara dupa o plasare sau mutare pe locul cu id_nod
    # returneaza False altfel
    def moara(self, tabla_noua, id_nod, jucator):

        global mori
        lista_mori = mori[id_nod]

        for lista in lista_mori:
            for loc in lista:
                if tabla_noua[loc - 1].culoare != jucator:
                    break
            else:
                return True
            
        return False

    # functie care returneaza o lista a pieselor jmax care nu fac parte dintr-o moara
    def piese_jucator_jmax_care_pot_fi_scoase(self):

        l_piese_in_moara = []
        l_piese_not_in_moara = []

        for loc in self.tabla:
            if loc.culoare == Joc.jmax:
                if self.moara(self.tabla, loc.id_nod, Joc.jmax) == True:
                    l_piese_in_moara.append(Joc.jmax + str(loc.id_nod))
                else:
                    l_piese_not_in_moara.append(Joc.jmax + str(loc.id_nod))

        if len(l_piese_not_in_moara) != 0:
            return l_piese_not_in_moara
        else:
            return l_piese_in_moara

    # functie care returneaza o lista a pieselor jmin care nu fac parte dintr-o moara
    def  piese_jucator_jmin_care_pot_fi_scoase(self):
        l_piese_in_moara = []
        l_piese_not_in_moara = []

        for loc in self.tabla:
            if loc.culoare == Joc.jmin:
                if self.moara(self.tabla, loc.id_nod, Joc.jmin) == True:
                    l_piese_in_moara.append(Joc.jmin + str(loc.id_nod))
                else:
                    l_piese_not_in_moara.append(Joc.jmin + str(loc.id_nod))

        if len(l_piese_not_in_moara) != 0:
            return l_piese_not_in_moara
        else:
            return l_piese_in_moara

    # functie care returneaza o lista a pieselor jucatorului trimis ca parametru
    def piese_jucator_care_pot_fi_scoase(self, jucator):
        l_piese_in_moara = []
        l_piese_not_in_moara = []

        for loc in self.tabla:
            if loc.culoare == jucator:
                if self.moara(self.tabla, loc.id_nod, jucator) == True:
                    l_piese_in_moara.append(jucator + str(loc.id_nod))
                else:
                    l_piese_not_in_moara.append(jucator + str(loc.id_nod))

        if len(l_piese_not_in_moara) != 0:
            return l_piese_not_in_moara
        else:
            return l_piese_in_moara

    # functie care returneaza numarul de piese al unui jucator trimis ca parametru
    def numara_piese_jucator(self, jucator):
        nr = 0
        for loc in self.tabla:
            if loc.culoare == jucator:
                nr += 1

        return nr


    def reseteaza_piese_jucator(self, jucator, tabla_noua):
        for loc in tabla_noua:
            if loc.culoare == jucator:
                loc.loc_anterior = None

        return tabla_noua

    def reseteaza_piese_jucator_fara_piesa_mutata(self, jucator, tabla_noua, id_nod):
        for loc in tabla_noua:
            if loc.culoare == jucator and loc.id_nod != id_nod:
                loc.loc_anterior = None

        return tabla_noua

    def blocare_jmin(self):

        if self.numara_piese_jmin() > 3:
            piese_jmin = self.piese_jmin()
            for piesa in piese_jmin:
                vecini = self.tabla[int(piesa[1:]) - 1].vecini

                for vecin in vecini:
                    if self.tabla[vecin - 1].culoare == '' and self.tabla[int(piesa[1:]) - 1].loc_anterior != vecin:
                        return False
            
            else:
                return True
        else:
            return False

    def blocare_jmax(self):

        if self.numara_piese_jmax() > 3:
            piese_jmax = self.piese_jmax()
            for piesa in piese_jmax:
                vecini = self.tabla[int(piesa[1:]) - 1].vecini

                for vecin in vecini:
                    if self.tabla[vecin - 1].culoare == '' and self.tabla[int(piesa[1:]) - 1].loc_anterior != vecin:
                        return False
            
            else:
                return True
        else:
            return False



###################
    def mutari(self, jucator):

        mutari = []

        if self.get_numar_piese_plasate(jucator) < 12:

            for nod in self.tabla:

                if nod.culoare == '': # loc pe tabla liber si mai avem piese de plasat 
                    tabla_noua = copy.deepcopy(self.tabla)
                    tabla_noua[nod.id_nod - 1].culoare = jucator

                    if self.moara(tabla_noua, nod.id_nod, jucator) == True:
                        piese_adversar_care_pot_fi_scoase = self.piese_jucator_care_pot_fi_scoase(Joc.jucator_opus(jucator))

                        for piesa in piese_adversar_care_pot_fi_scoase:
                            alta_tabla = copy.deepcopy(tabla_noua)
                            alta_tabla[int(piesa[1:]) - 1].culoare = ''
                            alta_tabla[int(piesa[1:]) - 1].loc_anterior = None

                            if jucator == Joc.jmin:
                                alta_tabla = self.reseteaza_piese_jucator(jucator, alta_tabla)
                                mutari.append(Joc(alta_tabla, self.numar_piese_plasate_jmin + 1, self.numar_piese_plasate_jmax))
                            else:
                                alta_tabla = self.reseteaza_piese_jucator(jucator,alta_tabla)
                                mutari.append(Joc(alta_tabla, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax + 1))

                    else:
                        if jucator == Joc.jmin:
                            tabla_noua = self.reseteaza_piese_jucator(jucator, tabla_noua)
                            mutari.append(Joc(tabla_noua, self.numar_piese_plasate_jmin + 1, self.numar_piese_plasate_jmax))
                        else:
                            tabla_noua = self.reseteaza_piese_jucator(jucator, tabla_noua)
                            mutari.append(Joc(tabla_noua, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax + 1))

                elif nod.culoare == jucator:
                    # putem muta o piesa
                    l_vecini = nod.vecini
                    for vecin in l_vecini:
                        if self.tabla[vecin - 1].culoare == '':
                            if nod.loc_anterior != vecin:
                                tabla_noua = copy.deepcopy(self.tabla)
                                tabla_noua[nod.id_nod - 1].culoare = ''
                                tabla_noua[nod.id_nod - 1].loc_anterior = None
                                tabla_noua[vecin - 1].culoare = jucator
                                tabla_noua[vecin - 1].loc_anterior = nod.id_nod

                                if self.moara(tabla_noua, vecin, jucator) == True:
                                    
                                    print(jucator)
                                    piese_adversar_care_pot_fi_scoase = self.piese_jucator_care_pot_fi_scoase(Joc.jucator_opus(jucator))

                                    for piesa in piese_adversar_care_pot_fi_scoase:
                                        alta_tabla = copy.deepcopy(tabla_noua)
                                        alta_tabla[int(piesa[1:]) - 1].culoare = ''
                                        alta_tabla[int(piesa[1:]) - 1].loc_anterior = None

                                        alta_tabla = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, alta_tabla, vecin)
                                        print(alta_tabla[vecin - 1].loc_anterior)
                                        mutari.append(Joc(alta_tabla, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax))

                                else:
                                    tabla_noua = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, tabla_noua, vecin)
                                    mutari.append(Joc(tabla_noua, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax))
        
        elif self.get_numar_piese_plasate(jucator) == 12 and self.numara_piese_jucator(jucator) == 3:

            l_libere = self.locuri_libere()
            for nod in self.tabla:
                if nod.culoare == jucator:
                    for loc_liber in l_libere:
                        if nod.loc_anterior != int(loc_liber):
                            tabla_noua = copy.deepcopy(self.tabla)
                            tabla_noua[int(loc_liber) - 1].culoare = jucator
                            tabla_noua[int(loc_liber) - 1].loc_anterior = nod.id_nod
                            tabla_noua[nod.id_nod - 1].culoare = ''
                            tabla_noua[nod.id_nod - 1].loc_anterior = None

                            if self.moara(tabla_noua, int(loc_liber), jucator) == True:
                                piese_adversar_care_pot_fi_scoase = self.piese_jucator_care_pot_fi_scoase(Joc.jucator_opus(jucator))

                                for piesa in piese_adversar_care_pot_fi_scoase:
                                    alta_tabla = copy.deepcopy(tabla_noua)
                                    alta_tabla[int(piesa[1:]) - 1].culoare = ''
                                    alta_tabla[int(piesa[1:]) - 1].loc_anterior = None

                                    alta_tabla = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, alta_tabla, int(loc_liber))
                                    mutari.append(Joc(alta_tabla, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax))
                            else:
                                tabla_noua = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, tabla_noua, int(loc_liber))
                                mutari.append(Joc(tabla_noua, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax))
    
        elif self.get_numar_piese_plasate(jucator) == 12 and self.numara_piese_jucator(jucator) > 3:

            for nod in self.tabla:
                if nod.culoare == jucator:
                    # putem muta o piesa
                    l_vecini = nod.vecini
                    for vecin in l_vecini:
                        if self.tabla[vecin - 1].culoare == '':
                            if nod.loc_anterior != vecin:
                                tabla_noua = copy.deepcopy(self.tabla)
                                tabla_noua[nod.id_nod - 1].culoare = ''
                                tabla_noua[nod.id_nod - 1].loc_anterior = None
                                tabla_noua[vecin - 1].culoare = jucator
                                tabla_noua[vecin - 1].loc_anterior = nod.id_nod

                                if self.moara(tabla_noua, vecin, jucator) == True:
                                    piese_adversar_care_pot_fi_scoase = self.piese_jucator_care_pot_fi_scoase(Joc.jucator_opus(jucator))

                                    for piesa in piese_adversar_care_pot_fi_scoase:
                                        alta_tabla = copy.deepcopy(tabla_noua)
                                        alta_tabla[int(piesa[1:]) - 1].culoare = ''
                                        alta_tabla[int(piesa[1:]) - 1].loc_anterior = None

                                        alta_tabla = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, alta_tabla, vecin)
                                        mutari.append(Joc(alta_tabla, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax))

                                else:
                                    tabla_noua = self.reseteaza_piese_jucator_fara_piesa_mutata(jucator, tabla_noua, vecin)
                                    mutari.append(Joc(tabla_noua, self.numar_piese_plasate_jmin, self.numar_piese_plasate_jmax)) 

        return mutari

###################

    def numara_mori(self, jucator):
        nr_mori = 0
        for loc in self.tabla:
            if loc.culoare == jucator and self.moara(self.tabla, loc.id_nod, jucator):
                nr_mori += 1

        return nr_mori

    def egal(self, alta_tabla):
        for nod in self.tabla:
            if nod.culoare != alta_tabla[nod.id_nod - 1].culoare:
                return False

        return True 

    def numara_mori_oprite(self, jucator):
        nr = 0
        jucator_opus = Joc.jucator_opus(jucator)

        for id_nod in mori:
            set_mori = mori[id_nod]
            for moara in set_mori:
                if self.tabla[moara[0] - 1].culoare == jucator and self.tabla[moara[1] - 1].culoare == jucator_opus and self.tabla[moara[2] - 1].culoare == jucator_opus:
                    nr += 1
                if self.tabla[moara[1] - 1].culoare == jucator and self.tabla[moara[0] - 1].culoare == jucator_opus and self.tabla[moara[2] - 1].culoare == jucator_opus:
                    nr += 1
                if self.tabla[moara[2] - 1].culoare == jucator and self.tabla[moara[1] - 1].culoare == jucator_opus and self.tabla[moara[0] - 1].culoare == jucator_opus:
                    nr += 1

        return nr

    def numara_mori_aproape_formate(self, jucator):
        nr = 0

        for id_nod in mori:
            set_mori = mori[id_nod]
            for moara in set_mori:
                if self.tabla[moara[0] - 1].culoare == '' and self.tabla[moara[1] - 1].culoare == jucator and self.tabla[moara[2] - 1].culoare == jucator:
                    nr += 1
                if self.tabla[moara[1] - 1].culoare == '' and self.tabla[moara[0] - 1].culoare == jucator and self.tabla[moara[2] - 1].culoare == jucator:
                    nr += 1
                if self.tabla[moara[2] - 1].culoare == '' and self.tabla[moara[1] - 1].culoare == jucator and self.tabla[moara[0] - 1].culoare == jucator:
                    nr += 1

        return nr

    def numara_mori_existente(self, jucator):
        nr = 0

        for id_nod in mori:
            set_mori = mori[id_nod]
            for moara in set_mori:
                if self.tabla[moara[0] - 1].culoare == jucator and self.tabla[moara[1] - 1].culoare == jucator and self.tabla[moara[2] - 1].culoare == jucator:
                    nr += 1

        return nr  

    def nr_mutari(self, jucator):
        nr = 0

        if self.numara_piese_jucator(jucator) > 3:
            for nod in self.tabla:
                if nod.culoare == jucator:
                    for vecin in nod.vecini:
                        if vecin == '' and nod.loc_anterior != vecin:
                            nr += 1

            return nr
        else:
            return len(self.locuri_libere()) - 1

    def nr_miscari(self, jucator):
        
        if self.get_numar_piese_plasate(jucator) < 12:
            return len(self.locuri_libere()) + self.nr_mutari(jucator)
        else:
            return self.nr_mutari(jucator)

    def estimeaza_scor(self, adancime, jucator):
        global nr_euristica
        fin = self.final()
    
        if nr_euristica == 1:
            if fin == Joc.jmax and jucator == Joc.jmax:
                return 999 + adancime
            elif fin == Joc.jmin and jucator == Joc.jmin:
                return -999 - adancime
            elif fin == "remiza":
                return 0
            else:
                if Joc.jmax == jucator:
                    piese_jucator = 3 * self.numara_piese_jucator(jucator) - 3 * self.numara_piese_jucator(Joc.jucator_opus(jucator))
                    mori_oprite = 1.5 * self.numara_mori_oprite(jucator) - 1.5 * self.numara_mori_oprite(Joc.jucator_opus(jucator))
                    numar_mori_aproape_formate = 6 * self.numara_mori_aproape_formate(jucator) - 6 * self.numara_mori_aproape_formate(Joc.jucator_opus(jucator))
                    
                    return piese_jucator + mori_oprite + numar_mori_aproape_formate
                else:
                    piese_jucator = -3 * self.numara_piese_jucator(jucator) + 3 * self.numara_piese_jucator(Joc.jucator_opus(jucator))
                    mori_oprite = -1.5 * self.numara_mori_oprite(jucator) + 1.5 * self.numara_mori_oprite(Joc.jucator_opus(jucator))
                    numar_mori_aproape_formate = -6 * self.numara_mori_aproape_formate(jucator) + 6 * self.numara_mori_aproape_formate(Joc.jucator_opus(jucator))
                
                    return piese_jucator + mori_oprite + numar_mori_aproape_formate
        else:
            if fin == Joc.jmax and jucator == Joc.jmax:
                return 999 + adancime
            elif fin == Joc.jmin and jucator == Joc.jmin:
                return -999 - adancime
            elif fin == "remiza":
                return 0
            else:
                if Joc.jmax == jucator:
                    piese_jucator = 3 * self.numara_piese_jucator(jucator) - 3 * self.numara_piese_jucator(Joc.jucator_opus(jucator))
                    mori_ex = self.numara_mori_existente(jucator) - self.numara_mori_existente(Joc.jucator_opus(jucator))
                    nr_miscari = 0.1 * self.nr_miscari(jucator) - 0.1 * self.nr_miscari(Joc.jucator_opus(jucator))

                    return piese_jucator + mori_ex + nr_miscari
                else:
                    piese_jucator = -3 * self.numara_piese_jucator(jucator) + 3 * self.numara_piese_jucator(Joc.jucator_opus(jucator))
                    mori_ex = -1 * self.numara_mori_existente(jucator) + self.numara_mori_existente(Joc.jucator_opus(jucator))
                    nr_miscari = -0.1 * self.nr_miscari(jucator) + 0.1 * self.nr_miscari(Joc.jucator_opus(jucator))

                    return piese_jucator + mori_ex + nr_miscari


class Stare:

    def __init__(self, tabla_joc, jucator_curent, adancime, parinte = None, estimare = None):
        self.tabla_joc = tabla_joc
        self.jucator_curent = jucator_curent
        self.adancime = adancime
        self.estimare = estimare
        self.mutari_posibile = []
        self.parinte = parinte
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.jucator_curent)
        j_opus = Joc.jucator_opus(self.jucator_curent)

        if len(l_mutari) == 0:
            l_stari_mutari = [Stare(copy.deepcopy(self.tabla_joc), j_opus, self.adancime - 1, parinte = self)]
        else:
            l_stari_mutari = [Stare(mutare, j_opus, self.adancime - 1, parinte = self) for mutare in l_mutari]

        return l_stari_mutari

    def mutare_jmin(self, id_nod_de_mutat, id_nod_liber):

        self.tabla_joc.reseteaza_piese_jmin()
        self.tabla_joc.tabla[id_nod_de_mutat - 1].culoare = ''
        self.tabla_joc.tabla[id_nod_de_mutat - 1].loc_anterior = None
        self.tabla_joc.tabla[id_nod_liber - 1].culoare = Joc.jmin
        self.tabla_joc.tabla[id_nod_liber - 1].loc_anterior = id_nod_de_mutat

    def mutare_jmax(self, id_nod_de_mutat, id_nod_liber):
        self.tabla_joc.reseteaza_piese_jmax()
        self.tabla_joc.tabla[id_nod_de_mutat - 1].culoare = ''
        self.tabla_joc.tabla[id_nod_de_mutat - 1].loc_anterior = None
        self.tabla_joc.tabla[id_nod_liber - 1].culoare = Joc.jmax
        self.tabla_joc.tabla[id_nod_liber - 1].loc_anterior = id_nod_de_mutat

    def plasare_jmin(self, id_nod):

        self.tabla_joc.reseteaza_piese_jmin()
        self.tabla_joc.tabla[id_nod - 1].culoare = Joc.jmin
        self.tabla_joc.numar_piese_plasate_jmin += 1

    def plasare_jmax(self, id_nod):
        self.tabla_joc.reseteaza_piese_jmax()
        self.tabla_joc.tabla[id_nod - 1].culoare = Joc.jmax
        self.tabla_joc.numar_piese_plasate_jmax += 1

def afis_daca_final(stare):
    global winner, rem

    final = stare.tabla_joc.final()
    
    if final:
        if final == "remiza":
            rem = True
            print("\nRezultat: REMIZA\n")
            Joc.afiseaza_info_final()
        else:
            if final == 'r':
                print("\nCastigator: ROSU\n")
                Joc.afiseaza_info_final()
            else:
                print("\nCastigator: NEGRU\n")
                Joc.afiseaza_info_final()
            winner = final

        return True
    
    return False

###
def minimax(stare):
    global nr_noduri_gen
    nr_noduri_gen += 1

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.jucator_curent)
        return stare

    stare.mutari_posibile = stare.mutari()

    mutari_cu_estimare = [minimax(x) for x in stare.mutari_posibile]

    if stare.jucator_curent == Joc.jmax:
        stare.stare_aleasa = max(mutari_cu_estimare, key = lambda x: x.estimare)
    else:
        stare.stare_aleasa = min(mutari_cu_estimare, key = lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare
###

def alpha_beta(alpha, beta, stare):
    global nr_noduri_gen
    nr_noduri_gen += 1

    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.jucator_curent)
        return stare

    if alpha > beta:
        return stare

    stare.mutari_posibile = stare.mutari()

    if stare.jucator_curent == Joc.jmax:

        estimare_curenta = float('-inf')

        stare.mutari_posibile.sort(key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime, Joc.jmax), reverse=True)

        for mutare in stare.mutari_posibile:
            
            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.jucator_curent == Joc.jmin:
        estimare_curenta = float('inf')

        stare.mutari_posibile.sort(key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime, Joc.jmin), reverse=True)
  
        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            
            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    
    stare.estimare = stare.stare_aleasa.estimare
    
    return stare

class Buton:
    def __init__(self, display = None, left = 0, top = 0,  w = 0, h = 0, culoareFundal = (53,80,115), culoareFundalSel = (89, 134, 194), text = "", font = "arial", fontDimensiune = 16, culoareText = (255,255,255), valoare = ""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.dreptunghiText = self.textRandat.get_rect(center = self.dreptunghi.center)
        self.valoare = valoare

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center = self.dreptunghi.center)

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, lista_butoane = [], indice_selectat = 0, spatiu_butoane = 10, left = 10, top = 0):
        self.listaButoane = lista_butoane
        self.indiceSelectat = indice_selectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiu_butoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare

def deseneaza_alegeri(display, tabla_curenta):

    btn_alg = GrupButoane(
        top = 30,
        left = 100,
        lista_butoane = [
            Buton(display = display, w = 80, h = 30, text = "minimax", valoare = "minimax"),
            Buton(display = display, w = 80, h = 30, text = "alphabeta", valoare = "alphabeta")
        ],
        indice_selectat = 0
    )

    btn_juc = GrupButoane(
        top = 100,
        left = 100,
        lista_butoane = [
            Buton(display=display, w = 80, h = 30, text = "rosu", valoare = "r"),
            Buton(display=display, w = 80, h = 30, text = "negru", valoare = "n")
        ],
        indice_selectat = 0 
    )

    btn_dif = GrupButoane(
        top = 200,
        left = 100,
        lista_butoane = [
            Buton(display=display, w = 80, h = 30, text = "usor", valoare = "u"),
            Buton(display=display, w = 80, h = 30, text = "mediu", valoare = "m"),
            Buton(display=display, w = 80, h = 30, text = "greu", valoare = "g")
        ],
        indice_selectat = 0 
    )

    btn_eur = GrupButoane(
        top = 300,
        left = 100,
        lista_butoane = [
            Buton(display=display, w = 80, h = 30, text = "erst 1", valoare = "1"),
            Buton(display=display, w = 80, h = 30, text = "erst 2", valoare = "2")
        ],
        indice_selectat = 0 
    )

    btn_mod = GrupButoane(
        top = 400,
        left = 100,
        lista_butoane = [
            Buton(display=display, w = 80, h = 30, text = "juc vs calc", valoare = "jvc"),
            Buton(display=display, w = 80, h = 30, text = "juc vs juc", valoare = "jvj"),
        ],
        indice_selectat = 0 
    )

    ok = Buton(display = display, top = 500, left = 100, w = 40, h = 30, text = "ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    btn_eur.deseneaza()
    btn_mod.deseneaza()
    ok.deseneaza()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if not btn_mod.selecteazaDupacoord(pos):
                                if not btn_eur.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0,0,0))
                                        tabla_curenta.deseneaza_tabla()
                                        return btn_juc.getValoare(), btn_alg.getValoare(), btn_dif.getValoare(), btn_mod.getValoare(), btn_eur.getValoare()
        pygame.display.update()


pygame.init()
ecran = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Cirlan Daniel 232 - Twelve Men's Morris")

def main():

    global culoare_jmax, culoare_jmin, blocat, winner, rem, nr_euristica, nr_noduri_gen

    Joc.initializeaza(ecran)

    adancime_maxima = None    
    tabla_curenta = Joc()
    
    Joc.jmin, tip_algoritm, dificultate, mod_joc, nr_eur = deseneaza_alegeri(ecran, tabla_curenta)

    Joc.jmax = 'r' if Joc.jmin == 'n' else 'n'
    nr_euristica = 1 if nr_eur == '1' else 2

    if Joc.jmin == 'r':
        culoare_jmin = (255,0,0)
    else:
        culoare_jmin = (0,0,0)
        
    culoare_jmax = (255,0,0) if Joc.jmin == 'n' else (0,0,0)

    if dificultate == 'u':
        adancime_maxima = 1
    elif dificultate == 'm':
        adancime_maxima = 2
    else:
        adancime_maxima = 3
           
    stare_curenta = Stare(tabla_curenta, Joc.jmin, adancime_maxima) 

    if mod_joc == "jvc":

        timp_rulare = time.time()
        print("\nCuloare jucator: " + culs[Joc.jmin] + "\nTip algoritm: " + tip_algoritm.upper() + "\nDificultate: " + dific[dificultate] + "\nNumar euristica: " + nr_eur + '\n')  

        print("\nTabla initiala:\n")
        stare_curenta.tabla_joc.afisare()

        while True:
            if stare_curenta.jucator_curent == Joc.jmin:
                
                timp_start_jmin = time.time()
                print("\nTabla dupa mutarea jucatorului:\n")
                run = True

                ok = False

                while run:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == '' and stare_curenta.tabla_joc.numar_piese_plasate_jmin < 12:
                                    stare_curenta.tabla_joc.deseneaza_tabla( id_loc_liber = nod.id_nod)
                                    break
                                elif coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == Joc.jmin:
                                    stare_curenta.tabla_joc.deseneaza_tabla( piesa_aleasa= nod.id_nod)
                                    break
                            else:
                                stare_curenta.tabla_joc.deseneaza_tabla()
                                break
                            
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos):

                                    if nod.culoare == '': # loc liber
                                        
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:
                                            # putem plasa o piesa
                                            stare_curenta.plasare_jmin(nod.id_nod)
                                            
                                            
                                            if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, nod.id_nod, stare_curenta.jucator_curent) == True:

                                                stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= nod.id_nod)

                                                piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                            
                                                run_1 = True
                                                while run_1:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()

                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                            pos1 = pygame.mouse.get_pos()

                                                            for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                if coord_piesa[nod_1.id_nod].collidepoint(pos1) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                    nod_1.culoare = ''
                                                                    nod_1.loc_anterior = None
                                                                    run_1 = False
                                                                    break
                                            ok = True
                                            run = False
                                            
                                        else:
                                            ok = False

                                    elif nod.culoare == stare_curenta.jucator_curent and stare_curenta.tabla_joc.blocare_jmin() == False:
                                        
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:

                                            for vecin in nod.vecini:
                                                if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                    break
                                            else:
                                                break

                                            run_3 = True
                                            while run_3:
                                                stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                for event in pygame.event.get():

                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        sys.exit()
                                                    
                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                        pos2 = pygame.mouse.get_pos()
                                                        vecini = nod.vecini

                                                        for vecin in vecini:
                                                            if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                if coord_piesa[vecin].collidepoint(pos2):
                                                                    # mutare
                                                                    stare_curenta.mutare_jmin(nod.id_nod, vecin)
                                                                    ok = True
                                                                    
                                                                    if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                        
                                                                        stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                        piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                            
                                                                        run_1 = True
                                                                        while run_1:
                                                                            for event in pygame.event.get():
                                                                                if event.type == pygame.QUIT:
                                                                                    pygame.quit()
                                                                                    sys.exit()

                                                                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                    pos3 = pygame.mouse.get_pos()

                                                                                    for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                                        if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                            nod_1.culoare = ''
                                                                                            nod_1.loc_anterior = None
                                                                                            run_1 = False
                                                                                            break

                                                                    run_3 = False
                                                                    break

                                        else:
                                            if stare_curenta.tabla_joc.numara_piese_jmin() > 3:

                                                for vecin in nod.vecini:
                                                    if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                        break
                                                else:
                                                    break

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            vecini = nod.vecini

                                                            for vecin in vecini:
                                                                if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                    if coord_piesa[vecin].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmin(nod.id_nod, vecin)
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                            piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                            else:

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            locuri_libere = stare_curenta.tabla_joc.locuri_libere()

                                                            for loc in locuri_libere:
                                                                if int(loc) != nod.loc_anterior and stare_curenta.tabla_joc.tabla[int(loc) - 1].culoare == '':
                                                                    if coord_piesa[int(loc)].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmin(nod.id_nod, int(loc))
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, int(loc), stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= int(loc))

                                                                            piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                                break

                                    # elif stare_curenta.tabla_joc.blocare_jmin() == True:
                                    #     ok = True
                                    #     break

                            if ok == True:
                                run = False
                                break

                        if stare_curenta.tabla_joc.blocare_jmin() == True and stare_curenta.tabla_joc.numar_piese_plasate_jmin == 12:
                            run = False
                            break       

                timp_total = time.time() - timp_start_jmin
                stare_curenta.tabla_joc.afisare()
                print("\nJucatorul a gandit timp de " + str(round(timp_total * 1000)) + " ms.")
                Joc.timpi_rulare_jmin.append(round(timp_total * 1000))
                stare_curenta.tabla_joc.deseneaza_tabla()

                if afis_daca_final(stare_curenta):
                    while True:
                        if rem == True:
                            stare_curenta.tabla_joc.deseneaza_tabla(remiza = True)
                        else:
                            stare_curenta.tabla_joc.deseneaza_tabla(win = winner)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                stare_curenta.jucator_curent = Joc.jmax

            else:

                nr_noduri_gen = 0

                timp_start_jmax = time.time()
                if tip_algoritm == 'minimax':
                    stare_actualizata = minimax(stare_curenta)
                else:
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)

                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

                timp_total = time.time() - timp_start_jmax
                Joc.timpi_rulare_jmax.append(round(timp_total * 1000))
                stare_curenta.tabla_joc.deseneaza_tabla()
                
                print("\nTabla dupa mutarea calculatorului:\n")

                Joc.lista_nr_noduri_generate.append(nr_noduri_gen)

                stare_curenta.tabla_joc.afisare()

                print("\nCalculatorul a gandit timp de " + str(round(timp_total * 1000)) + " ms.")
                print("Calculatorul a generat " + str(nr_noduri_gen)  + " noduri.")
                if afis_daca_final(stare_curenta):
                    while True:
                        if rem == True:
                            stare_curenta.tabla_joc.deseneaza_tabla(remiza = True)
                        else:
                            stare_curenta.tabla_joc.deseneaza_tabla(win = winner)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                stare_curenta.jucator_curent = Joc.jmin

    elif mod_joc == "jvj":

        while True:
            if stare_curenta.jucator_curent == Joc.jmin:
                
                print("\nTabla dupa mutarea jucatorului 1:\n")
                run = True

                ok = False

                while run:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == '' and stare_curenta.tabla_joc.numar_piese_plasate_jmin < 12:
                                    stare_curenta.tabla_joc.deseneaza_tabla( id_loc_liber = nod.id_nod)
                                    break
                                elif coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == Joc.jmin:
                                    stare_curenta.tabla_joc.deseneaza_tabla( piesa_aleasa= nod.id_nod)
                                    break
                            else:
                                stare_curenta.tabla_joc.deseneaza_tabla()
                                break
                            
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos):

                                    if nod.culoare == '': # loc liber
                                        
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:
                                            # putem plasa o piesa
                                            stare_curenta.plasare_jmin(nod.id_nod)
                                            
                                            
                                            if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, nod.id_nod, stare_curenta.jucator_curent) == True:

                                                stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= nod.id_nod)

                                                piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                            
                                                run_1 = True
                                                while run_1:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()

                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                            pos1 = pygame.mouse.get_pos()

                                                            for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                if coord_piesa[nod_1.id_nod].collidepoint(pos1) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                    nod_1.culoare = ''
                                                                    nod_1.loc_anterior = None
                                                                    run_1 = False
                                                                    break
                                            ok = True
                                            run = False
                                            
                                        else:
                                            ok = False

                                    elif nod.culoare == stare_curenta.jucator_curent:
                                        
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:

                                            for vecin in nod.vecini:
                                                if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                    break
                                            else:
                                                break

                                            run_3 = True
                                            while run_3:
                                                stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                for event in pygame.event.get():

                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        sys.exit()
                                                    
                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                        pos2 = pygame.mouse.get_pos()
                                                        vecini = nod.vecini

                                                        for vecin in vecini:
                                                            if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                if coord_piesa[vecin].collidepoint(pos2):
                                                                    # mutare
                                                                    stare_curenta.mutare_jmin(nod.id_nod, vecin)
                                                                    ok = True
                                                                    
                                                                    if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                        
                                                                        stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                        piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                            
                                                                        run_1 = True
                                                                        while run_1:
                                                                            for event in pygame.event.get():
                                                                                if event.type == pygame.QUIT:
                                                                                    pygame.quit()
                                                                                    sys.exit()

                                                                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                    pos3 = pygame.mouse.get_pos()

                                                                                    for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                                        if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                            nod_1.culoare = ''
                                                                                            nod_1.loc_anterior = None
                                                                                            run_1 = False
                                                                                            break

                                                                    run_3 = False
                                                                    break

                                        else:
                                            if stare_curenta.tabla_joc.numara_piese_jmin() > 3:

                                                for vecin in nod.vecini:
                                                    if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                        break
                                                else:
                                                    break

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            vecini = nod.vecini

                                                            for vecin in vecini:
                                                                if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                    if coord_piesa[vecin].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmin(nod.id_nod, vecin)
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                            piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                            else:

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            locuri_libere = stare_curenta.tabla_joc.locuri_libere()

                                                            for loc in locuri_libere:
                                                                if int(loc) != nod.loc_anterior and stare_curenta.tabla_joc.tabla[int(loc) - 1].culoare == '':
                                                                    if coord_piesa[int(loc)].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmin(nod.id_nod, int(loc))
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, int(loc), stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= int(loc))

                                                                            piese_jmax = stare_curenta.tabla_joc.piese_jucator_jmax_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmax and (Joc.jmax + str(nod_1.id_nod)) in piese_jmax:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                                break

                            if ok == True:
                                run = False
                                break

                        if stare_curenta.tabla_joc.blocare_jmin() == True and stare_curenta.tabla_joc.numar_piese_plasate_jmin == 12:
                            run = False
                            break       

                stare_curenta.tabla_joc.afisare()
                stare_curenta.tabla_joc.deseneaza_tabla()

                if afis_daca_final(stare_curenta):
                    while True:
                        if rem == True:
                            stare_curenta.tabla_joc.deseneaza_tabla(remiza = True)
                        else:
                            stare_curenta.tabla_joc.deseneaza_tabla(win = winner)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                stare_curenta.jucator_curent = Joc.jmax

            else:
                
                print("\nTabla dupa mutarea jucatorului 2:\n")
                run = True

                ok = False

                while run:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        elif event.type == pygame.MOUSEMOTION:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == '' and stare_curenta.tabla_joc.numar_piese_plasate_jmax < 12:
                                    stare_curenta.tabla_joc.deseneaza_tabla( id_loc_liber = nod.id_nod)
                                    break
                                elif coord_piesa[nod.id_nod].collidepoint(pos) and nod.culoare == Joc.jmax:
                                    stare_curenta.tabla_joc.deseneaza_tabla( piesa_aleasa= nod.id_nod)
                                    break
                            else:
                                stare_curenta.tabla_joc.deseneaza_tabla()
                                break
                            
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            for nod in stare_curenta.tabla_joc.tabla:

                                if coord_piesa[nod.id_nod].collidepoint(pos):

                                    if nod.culoare == '': # loc liber
                                        
                                        print("Am fost aici")
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:
                                            # putem plasa o piesa
                                            stare_curenta.plasare_jmax(nod.id_nod)
                                            print("Am fost aici 1")
                                            
                                            if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, nod.id_nod, stare_curenta.jucator_curent) == True:

                                                stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= nod.id_nod)

                                                piese_jmin = stare_curenta.tabla_joc.piese_jucator_jmin_care_pot_fi_scoase()
                                            
                                                run_1 = True
                                                while run_1:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()

                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                            pos1 = pygame.mouse.get_pos()

                                                            for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                if coord_piesa[nod_1.id_nod].collidepoint(pos1) and nod_1.culoare == Joc.jmin and (Joc.jmin + str(nod_1.id_nod)) in piese_jmin:
                                                                    nod_1.culoare = ''
                                                                    nod_1.loc_anterior = None
                                                                    run_1 = False
                                                                    break
                                            ok = True
                                            run = False
                                            
                                        else:
                                            ok = False

                                    elif nod.culoare == stare_curenta.jucator_curent:
                                        
                                        if stare_curenta.tabla_joc.get_numar_piese_plasate(stare_curenta.jucator_curent) < 12:

                                            for vecin in nod.vecini:
                                                if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                    break
                                            else:
                                                break

                                            run_3 = True
                                            while run_3:
                                                stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                for event in pygame.event.get():

                                                    if event.type == pygame.QUIT:
                                                        pygame.quit()
                                                        sys.exit()
                                                    
                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                        pos2 = pygame.mouse.get_pos()
                                                        vecini = nod.vecini

                                                        for vecin in vecini:
                                                            if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                if coord_piesa[vecin].collidepoint(pos2):
                                                                    # mutare
                                                                    stare_curenta.mutare_jmax(nod.id_nod, vecin)
                                                                    ok = True
                                                                    
                                                                    if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                        
                                                                        stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                        piese_jmin = stare_curenta.tabla_joc.piese_jucator_jmin_care_pot_fi_scoase()
                                            
                                                                        run_1 = True
                                                                        while run_1:
                                                                            for event in pygame.event.get():
                                                                                if event.type == pygame.QUIT:
                                                                                    pygame.quit()
                                                                                    sys.exit()

                                                                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                    pos3 = pygame.mouse.get_pos()

                                                                                    for nod_1 in stare_curenta.tabla_joc.tabla:
                                                            
                                                                                        if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmin and (Joc.jmin + str(nod_1.id_nod)) in piese_jmin:
                                                                                            nod_1.culoare = ''
                                                                                            nod_1.loc_anterior = None
                                                                                            run_1 = False
                                                                                            break

                                                                    run_3 = False
                                                                    break

                                        else:
                                            if stare_curenta.tabla_joc.numara_piese_jmax() > 3:

                                                for vecin in nod.vecini:
                                                    if stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '' and vecin != nod.loc_anterior:
                                                        break
                                                else:
                                                    break

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            vecini = nod.vecini

                                                            for vecin in vecini:
                                                                if vecin != nod.loc_anterior and stare_curenta.tabla_joc.tabla[vecin - 1].culoare == '':
                                                                    if coord_piesa[vecin].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmax(nod.id_nod, vecin)
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, vecin, stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= vecin)

                                                                            piese_jmin = stare_curenta.tabla_joc.piese_jucator_jmin_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmin and (Joc.jmin + str(nod_1.id_nod)) in piese_jmin:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                            else:

                                                run_3 = True
                                                while run_3:
                                                    stare_curenta.tabla_joc.deseneaza_tabla(piesa_aleasa = nod.id_nod)
                                            
                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            sys.exit()
                                                    
                                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                                        
                                                            pos2 = pygame.mouse.get_pos()
                                                            locuri_libere = stare_curenta.tabla_joc.locuri_libere()

                                                            for loc in locuri_libere:
                                                                if int(loc) != nod.loc_anterior and stare_curenta.tabla_joc.tabla[int(loc) - 1].culoare == '':
                                                                    if coord_piesa[int(loc)].collidepoint(pos2):
                                                                        # mutare
                                                                        stare_curenta.mutare_jmax(nod.id_nod, int(loc))
                                                                        ok = True

                                                                        if stare_curenta.tabla_joc.moara(stare_curenta.tabla_joc.tabla, int(loc), stare_curenta.jucator_curent) == True:
                                                                            
                                                                            stare_curenta.tabla_joc.deseneaza_tabla(id_loc_liber= None, id_piesa_moara= int(loc))

                                                                            piese_jmin = stare_curenta.tabla_joc.piese_jucator_jmin_care_pot_fi_scoase()
                                                
                                                                            run_1 = True
                                                                            while run_1:
                                                                                for event in pygame.event.get():
                                                                                    if event.type == pygame.QUIT:
                                                                                        pygame.quit()
                                                                                        sys.exit()

                                                                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                                                                        pos3 = pygame.mouse.get_pos()

                                                                                        for nod_1 in stare_curenta.tabla_joc.tabla:
                                                                
                                                                                            if coord_piesa[nod_1.id_nod].collidepoint(pos3) and nod_1.culoare == Joc.jmin and (Joc.jmin + str(nod_1.id_nod)) in piese_jmin:
                                                                                                nod_1.culoare = ''
                                                                                                nod_1.loc_anterior = None
                                                                                                run_1 = False
                                                                                                break

                                                                        run_3 = False
                                                        
                                                run = False
                                                break

                            if ok == True:
                                run = False
                                break

                        if stare_curenta.tabla_joc.blocare_jmax() == True and stare_curenta.tabla_joc.numar_piese_plasate_jmax == 12:
                            
                            run = False
                            break       

                stare_curenta.tabla_joc.afisare()
                stare_curenta.tabla_joc.deseneaza_tabla()

                if afis_daca_final(stare_curenta):
                    while True:
                        if rem == True:
                            stare_curenta.tabla_joc.deseneaza_tabla(remiza = True)
                        else:
                            stare_curenta.tabla_joc.deseneaza_tabla(win = winner)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                stare_curenta.jucator_curent = Joc.jmin


if __name__ == "__main__":
    main()