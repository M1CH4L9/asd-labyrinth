import random

#brak szukania literek i więcej niż jednego algorytmu generowania (-3pkt, pls 17pkt still) :(


#węzel listy żeby zbudować stos i kolejke
class Wezel:
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.nastepny = None

#własny stos
class MojStos:
    def __init__(self):
        self.gora = None

    def push(self, wartosc):
        #kładziemy na góre
        nowy = Wezel(wartosc)
        nowy.nastepny = self.gora
        self.gora = nowy

    def pop(self):
        #zdejmujemy z góry
        if self.is_empty():
            return None
        wartosc = self.gora.wartosc
        self.gora = self.gora.nastepny
        return wartosc

    def is_empty(self):
        return self.gora is None

#własna kolejka
class MojaKolejka:
    def __init__(self):
        self.przod = None
        self.tyl = None

    def enqueue(self, wartosc):
        #dodajemy na koniec
        nowy = Wezel(wartosc)
        if self.tyl:
            self.tyl.nastepny = nowy
        self.tyl = nowy
        if not self.przod:
            self.przod = nowy

    def dequeue(self):
        #bierzemy z przodu
        if self.is_empty():
            return None
        wartosc = self.przod.wartosc
        self.przod = self.przod.nastepny
        if not self.przod:
            self.tyl = None
        return wartosc

    def is_empty(self):
        return self.przod is None

#pojedyncza kratka w labiryncie
class Komorka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #ściany: góra[0], prawo[1], dól[2], lewo[3]
        self.sciany = [True, True, True, True] 
        self.odwiedzona = False

class Labirynt:
    def __init__(self, szerokosc, wysokosc):
        self.szer = szerokosc
        self.wys = wysokosc
        #budujemy plansze
        self.siatka = []
        for y in range(wysokosc):
            wiersz = []
            for x in range(szerokosc):
                wiersz.append(Komorka(x, y))
            self.siatka.append(wiersz)
        
        #start i koniec ustawi funkcja generuj
        self.start = (0, 0)
        self.koniec = (0, 0)
        
    def sprawdz_sasiadow(self, k):
        #szukamy gdzie mozna iść (tylko nieodwiedzone)
        sasiadzi = []
        if k.y > 0 and not self.siatka[k.y - 1][k.x].odwiedzona:
            sasiadzi.append(('Gora', self.siatka[k.y - 1][k.x]))
        if k.x < self.szer - 1 and not self.siatka[k.y][k.x + 1].odwiedzona:
            sasiadzi.append(('Prawo', self.siatka[k.y][k.x + 1]))
        if k.y < self.wys - 1 and not self.siatka[k.y + 1][k.x].odwiedzona:
            sasiadzi.append(('Dol', self.siatka[k.y + 1][k.x]))
        if k.x > 0 and not self.siatka[k.y][k.x - 1].odwiedzona:
            sasiadzi.append(('Lewo', self.siatka[k.y][k.x - 1]))
        return sasiadzi

    def losuj_punkt_na_scianie(self):
        #losowanie punktu na krawędzi
        strona = random.choice(['Gora', 'Dol', 'Lewo', 'Prawo'])
        if strona == 'Gora':
            return (random.randint(0, self.szer - 1), 0)
        elif strona == 'Dol':
            return (random.randint(0, self.szer - 1), self.wys - 1)
        elif strona == 'Lewo':
            return (0, random.randint(0, self.wys - 1))
        else: # Prawo
            return (self.szer - 1, random.randint(0, self.wys - 1))

    def generuj(self):
        stos = MojStos()
        #zaczynamy od środka
        start_gen = self.siatka[self.wys // 2][self.szer // 2]
        start_gen.odwiedzona = True
        stos.push(start_gen)
        
        #algorytm z nawracaniem (recursive backtracker)
        while not stos.is_empty():
            obecna = stos.pop()
            sasiadzi = self.sprawdz_sasiadow(obecna)
            
            if sasiadzi:
                stos.push(obecna)
                #losujemy gdzie idziemy
                kierunek, nastepna = random.choice(sasiadzi)
                
                #burzymy sciany
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

        #robimy dodatkowe przejścia (pętle) śeby były różne drogi
        ile_dziur = int(self.szer * self.wys * 0.15)
        for _ in range(ile_dziur):
            rx = random.randint(0, self.szer - 2)
            ry = random.randint(0, self.wys - 2)
            if random.choice([True, False]):
                self.siatka[ry][rx].sciany[1] = False
                self.siatka[ry][rx+1].sciany[3] = False
            else:
                self.siatka[ry][rx].sciany[2] = False
                self.siatka[ry+1][rx].sciany[0] = False
        
        #losujemy start i koniec
        self.start = self.losuj_punkt_na_scianie()
        while True:
            self.koniec = self.losuj_punkt_na_scianie()
            if self.koniec != self.start:
                break
    
    def rysuj(self, sciezka=None):
        print("+" + "---+" * self.szer)

        for y in range(self.wys):
            linia_srodek = "|"
            linia_dol = "+"

            for x in range(self.szer):
                k = self.siatka[y][x]
                
                #rysowanie symboli (start, koniec, ścieżka)
                symbol = "   "
                if (x, y) == self.start:
                    symbol = " S "
                elif (x, y) == self.koniec:
                    symbol = " K "
                elif sciezka and (x, y) in sciezka:
                    symbol = " * "

                #ściany
                if k.sciany[1]:
                    linia_srodek += symbol +"|"
                else:
                    linia_srodek += symbol + " "

                if k.sciany[2]:
                    linia_dol += "---+"
                else:
                    linia_dol += "   +"

            print(linia_srodek)
            print(linia_dol)

    #algorytm BFS - zawsze najkrotsza droga (na kolejce)
    def rozwiaz_bfs(self):
        kolejka = MojaKolejka()
        kolejka.enqueue(self.start)
        
        rodzice = {self.start: None} 
        odwiedzone = {self.start}
        
        while not kolejka.is_empty():
            ox, oy = kolejka.dequeue()
            
            if (ox, oy) == self.koniec:
                break

            k = self.siatka[oy][ox]
            #ruchy: góra, prawo, dól, lewo
            ruchy = [(0, 0, -1), (1, 1, 0), (2, 0, 1), (3, -1, 0)]
            
            for idx, dx, dy in ruchy:
                #gdy brak ściany
                if not k.sciany[idx]:
                    nx, ny = ox + dx, oy + dy
                    if 0 <= nx < self.szer and 0 <= ny < self.wys:
                        if (nx, ny) not in odwiedzone:
                            odwiedzone.add((nx, ny))
                            rodzice[(nx, ny)] = (ox, oy)
                            kolejka.enqueue((nx, ny))

        if self.koniec in rodzice:
            sciezka = []
            krok = self.koniec
            while krok is not None:
                sciezka.append(krok)
                krok = rodzice[krok]
            return sciezka
        return []

    #algorytm DFS - droga zazwyczaj jest dłuższa niż BFS (na stosie)
    def rozwiaz_dfs(self):
        stos = MojStos()
        stos.push(self.start)
        
        rodzice = {self.start: None} 
        odwiedzone = {self.start}
        
        while not stos.is_empty():
            ox, oy = stos.pop()
            
            if (ox, oy) == self.koniec:
                break

            k = self.siatka[oy][ox]
            ruchy = [(0, 0, -1), (1, 1, 0), (2, 0, 1), (3, -1, 0)]
            
            for idx, dx, dy in ruchy:
                if not k.sciany[idx]:
                    nx, ny = ox + dx, oy + dy
                    if 0 <= nx < self.szer and 0 <= ny < self.wys:
                        if (nx, ny) not in odwiedzone:
                            odwiedzone.add((nx, ny))
                            rodzice[(nx, ny)] = (ox, oy)
                            stos.push((nx, ny))

        if self.koniec in rodzice:
            sciezka = []
            krok = self.koniec
            while krok is not None:
                sciezka.append(krok)
                krok = rodzice[krok]
            return sciezka
        return []

if __name__ == "__main__":
    lab = Labirynt(10, 10)
    
    print("---Generujemy labirynt---")
    lab.generuj()
    
    print(f"\nLabirynt (S={lab.start}, K={lab.koniec}):")
    lab.rysuj() 


    #1. BFS
    print("---Algorytm BFS---")

    droga_bfs = lab.rozwiaz_bfs()

    if droga_bfs:
        dlugosc_bfs = len(droga_bfs)
        print(f"BFS (Kolejka) - Dlugosc drogi: {dlugosc_bfs} (Na 100% najkrotsza)")

        print("\nRysuje rozwiazanie BFS (najkrotsze):")
        lab.rysuj(droga_bfs)
    else:
        print("Brak przejscia")
        dlugosc_bfs = 0


    #2. DFS
    print("---Algorytm DFS---")

    droga_dfs = lab.rozwiaz_dfs()

    if droga_dfs:
        dlugosc_dfs = len(droga_dfs)
        print(f"DFS (Stos) - Dlugosc drogi: {dlugosc_dfs}")

        print("\nRysuje sciezke DFS (moze nie najkrotsze):")
        lab.rysuj(droga_dfs)
    else:
        print("Brak przejscia")
        dlugosc_dfs = 0

    
    print("\n---POROWNANIE ALGORYTMOW---")
    print(f"BFS (Kolejka) - Dlugosc drogi: {dlugosc_bfs} (Na 100% najkrotsza)")
    print(f"DFS (Stos) - Dlugosc drogi: {dlugosc_dfs}")

    if dlugosc_bfs != 0 and dlugosc_dfs != 0:
        if dlugosc_bfs == dlugosc_dfs:
            print("\nDlugosc drogi jest taka sama z obu algorytmow.")
        else:
            #BFS może być tylko szybszy lub ewentualnie taki sam
            print(f"\nBFS jest szybszy o {dlugosc_dfs - dlugosc_bfs} krok/kroki/krokow.")
    else:
        print("\nBrak jednej ze sciezek.")