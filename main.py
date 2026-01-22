import random

#węzęł listy żeby zbudowqać stos i kolejke
class Wezel:
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.nastepny = None

#własny stos do generowania labiryntu
class MojStos:
    def __init__(self):
        self.gora = None

    def push(self, wartosc):
        #tworzymy nowy element i dajemy go na górę
        nowy = Wezel(wartosc)
        nowy.nastepny = self.gora
        self.gora = nowy

    def pop(self):
        #ściągamy element z góry
        if self.is_empty():
            return None
        wartosc = self.gora.wartosc
        self.gora = self.gora.nastepny
        return wartosc

    def is_empty(self):
        return self.gora is None

#własna kolejka do szukania najkrótszej drogi
class MojaKolejka:
    def __init__(self):
        self.przod = None
        self.tyl = None

    def enqueue(self, wartosc):
        #dodaje na koniec kolejki
        nowy = Wezel(wartosc)
        if self.tyl:
            self.tyl.nastepny = nowy
        self.tyl = nowy
        if not self.przod:
            self.przod = nowy

    def dequeue(self):
        #zabieramy z przodu kolejki
        if self.is_empty():
            return None
        wartosc = self.przod.wartosc
        self.przod = self.przod.nastepny
        if not self.przod:
            self.tyl = None
        return wartosc

    def is_empty(self):
        return self.przod is None

#klasa pojedynczej kratki w labiryncie (cienkie ściany)
class Komorka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #ściany (góra, prawo, dół, lewo)
        self.sciany = [True, True, True, True] 
        self.odwiedzona = False


class Labirynt:
    def __init__(self, szerokosc, wysokosc):
        self.szer = szerokosc
        self.wys = wysokosc
        #tworzenie siatki komórek (macierz obiektów)
        self.siatka = []
        for y in range(wysokosc):
            wiersz = []
            for x in range(szerokosc):
                wiersz.append(Komorka(x, y))
            self.siatka.append(wiersz)
        
    def sprawdz_sasiadow(self, k):
        #szukamy nieodwiedzonych sąsiadów
        sasiadzi = []
        
        #gora (y-1)
        if k.y > 0 and not self.siatka[k.y - 1][k.x].odwiedzona:
            sasiadzi.append(('Gora', self.siatka[k.y - 1][k.x]))
        #prawo (x+1)
        if k.x < self.szer - 1 and not self.siatka[k.y][k.x + 1].odwiedzona:
            sasiadzi.append(('Prawo', self.siatka[k.y][k.x + 1]))
        #dol (y+1)
        if k.y < self.wys - 1 and not self.siatka[k.y + 1][k.x].odwiedzona:
            sasiadzi.append(('Dol', self.siatka[k.y + 1][k.x]))
        #lewo (x-1)
        if k.x > 0 and not self.siatka[k.y][k.x - 1].odwiedzona:
            sasiadzi.append(('Lewo', self.siatka[k.y][k.x - 1]))
            
        return sasiadzi

    def generuj(self):
        stos = MojStos()
        #zaczynamy w rogui [0][0]
        start = self.siatka[0][0]
        start.odwiedzona = True
        stos.push(start)
        
        while not stos.is_empty():
            #bierzemy komórkę
            obecna = stos.pop()
            
            sasiadzi = self.sprawdz_sasiadow(obecna)
            
            if sasiadzi:
                #wrzucamy z powrotem, żeby tu wrócić jak utknie
                stos.push(obecna)
                
                #losuje sąsiada gdzie pójdę
                kierunek, nastepna = random.choice(sasiadzi)
                
                #burzymy ścianę między nami
                if kierunek == 'Gora':
                    obecna.sciany[0] = False
                    nastepna.sciany[2] = False
                elif kierunek == 'Prawo':
                    obecna.sciany[1] = False
                    nastepna.sciany[3] = False
                elif kierunek == 'Dol':
                    obecna.sciany[2] = False
                    nastepna.sciany[0] = False
                elif kierunek == 'Lewo':
                    obecna.sciany[3] = False
                    nastepna.sciany[1] = False
                
                nastepna.odwiedzona = True
                stos.push(nastepna)
    
    def rysuj(self):
        #rysowanie górnej krawędzi całego labiryntu
        print("+" + "---+" * self.szer)

        for y in range(self.wys):
            #zaczynamu od lewej ściany
            linia_srodek = "|"
            #zaczynamy od rogu
            linia_dol = "+"

            for x in range(self.szer):
                k = self.siatka[y][x]
                
                #sprawdzamy ścianę z prawej [1]
                if k.sciany[1]:
                    linia_srodek += "   |"
                else:
                    linia_srodek += "    "

                #sprawdzamy ścianę na dole [2]
                if k.sciany[2]:
                    linia_dol += "---+"
                else:
                    linia_dol += "   +"

            print(linia_srodek)
            print(linia_dol)


#TEST
if __name__ == "__main__":
    lab = Labirynt(10, 10)
    lab.generuj()
    lab.rysuj()