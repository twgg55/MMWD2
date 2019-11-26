from typing import List
from copy import deepcopy
import random  # Testowanie
import time

inf = -1  # TODO Rozwiazac ewentualne problemy z tym!


def print_matrix(matrix: List[List]):
    string = ""
    for i in range(0, len(matrix)):
        string = string + '|'
        for j in range(0, len(matrix[i])):
            string = string + '\t' + str(matrix[i][j])
        string = string + '|' + '\n'
    print(string)
    del string
    pass


def cost(matrix: List[List]) -> int:
    # Tak ogolnie to jest to suma wyrazow nad przekatna
    _sum = 0  # suma odleglosci miedzy punktami
    for i in range(0, len(matrix)-1):
        _sum = _sum + matrix[i][i+1]
    return _sum


def sort_matrix_by_distance(matrix: List[List], start_index: int = None):
    if start_index is None:
        _from = len(matrix) - 1
        _to = 0
        _visited = []
        # Znalezienie najkrotszego polaczenia w calej macierzy
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                if i != j and matrix[i][j] < matrix[_from][_to]:
                    _from, _to = i, j

        _visited.append(_from)  # Dolaczenie tych punktow do listy odwiedzonych
        _visited.append(_to)
        _from = _to
    else:
        _from = start_index  # Zaczynamy od zera, czyli bazy
        _to = 1
        _visited = [_from] # Dolaczenie tych punktow do listy odwiedzonych

    while len(_visited) < len(matrix):
        helper = deepcopy(matrix[_from])  # Usuniecie inf z tablicy pomocniczej (funkcje min/max maja z tym problem, gdy stoi na poczatku)
        for i in range(helper.count(inf)):
            helper.pop(helper.index(inf))
        _min_cost = max(helper)  # Znalezienie najwiekszej wartosci w tej liscie
        del helper
        _to = (matrix[_from]).index(_min_cost)  #Dla jakiego indeksu istnieje najwieksza wartosc
        for i in range(0, len(matrix[_from])):
            if i != _from and matrix[_from][i] is not inf and i not in _visited:
                if matrix[_from][i] < _min_cost:
                    _min_cost = matrix[_from][i]
                    _to = i  # Znaleziono punkt o mniejszym koszcie

        _visited.append(_to)  # Dodaj punkt do odwiedzonych
        _from = _to
        # Koniec while, szukaj nastpenego polaczenia

    # Gdy otrzymalismy juz kolejnosc zapisu, nalezy zmienic te macierz
    # Zamiana kolumn, wierszy wedlug wyznaczonej kolejnosci
    new_matrix = []
    for i in range(0, len(matrix)):
        helperek = []
        for j in range(0, len(matrix[i])):
            helperek.append(matrix[_visited[i]][_visited[j]])
            pass
        new_matrix.append(deepcopy(helperek))
        helperek.clear()
        pass

    zmiana = cost(matrix) - cost(new_matrix)
    if zmiana > 0:  # Jesli macierz kosztow ulegla poprawie
        matrix = new_matrix
        del new_matrix
    else:  # Jesli wyzmaczona macierz nie jest lepsza
        del new_matrix
    return matrix, _visited


# Generowanie losowych punktow na plaszczyznie (2 wymiary)
def random_2dim_points(quantity: int, max_value: int = 100, min_value: int = 0) -> List:
    _2D_points_list = [(0, 0)] # BAZA ma zawsze wspolrzedne 0,0. CZEMU? Bo wysypisko jest zawsze POZA miastem, a nie w centrum xD
    while len(_2D_points_list) < quantity:
        point = (random.randint(min_value, max_value), random.randint(min_value, max_value))
        if point in _2D_points_list:  # Sprawdzenie, czy nie wylosowalismy juz takiego samego punktu
            continue
        else:
            _2D_points_list.append(deepcopy(point))
        pass
    return _2D_points_list


def create_cost_matrix(points_list: List):
    cost_matrix = []
    for row in range(len(points_list)):
        list_helper = [0 for i in range(len(points_list))]
        for col in range(len(points_list)):
            if row == col:
                list_helper[col] = inf
            if row < col:
                delta_x = abs(points_list[row][0]-points_list[col][0])
                delta_y = abs(points_list[row][1]-points_list[col][1])
                list_helper[col] = int((delta_x**2 + delta_y**2)**(1/2))  # Odleglosc w lini prostej
            pass
        cost_matrix.append(deepcopy(list_helper))
        del list_helper
        pass
    for row in range(len(points_list)):
        for col in range(row):
            cost_matrix[row][col] = cost_matrix[col][row]
            pass
        pass
    return cost_matrix


def sort_points_list(list_to_sort: List, given_order: List) -> List:
    if len(list_to_sort) != len(given_order):
        print("Kierowniku, listy maja rozne rozmiary. -> sort_points_list")
        Exception("Kierowniku, listy maja rozne rozmiary. -> sort_points_list")
    new_list = []
    return [list_to_sort[elem] for elem in given_order]


#Parametry symulacji
czy_pokazac_wykresy = True
czy_pokazac_macierze_w_konsoli = True
min_value = 0
max_value = 100
ilosc_punktow = 5


# Stworzenie macierzy
print("Parametry symulacji:")
print("Ilosc_punktow: " + str(ilosc_punktow))
print("Najmniejsza wartość wspolrzednych dla punktow: " + str(min_value))
print("Najwieksza wartość wspolrzednych dla punktow: " + str(max_value))

print("\nRozpoczecie symulacji:")
start = time.time()
punkty = random_2dim_points(ilosc_punktow, max_value, min_value)
czas_losowania = time.time() - start
print("Losowanie punktow zajelo: " + str(czas_losowania) + " sekund")
macierz_przed = create_cost_matrix(punkty)
print("Stworzenie macierzy kosztow zajelo: " + str(time.time() - start - czas_losowania) + " sekund")
koszt_przed = cost(macierz_przed)

# Sposob nr 1
czas_sortowania_f1 = time.time()
macierz_po, odwiedzone = sort_matrix_by_distance(macierz_przed)
czas_sortowania_f1 = time.time() - czas_sortowania_f1
print("\nCzas sortowania dla F1: " + str(czas_sortowania_f1) + " sekund")
koszt_po = cost(macierz_po)
roznica = koszt_przed - koszt_po
print("Poprawa o: " + str(roznica) + ", czyli o " + str(round(roznica*100/koszt_przed)) + "%.")

#Sposob nr 2
czas_sortowania_f2 = time.time()
macierz_po_od_0_0, odwiedzone_0_0 = sort_matrix_by_distance(macierz_przed, 0)
czas_sortowania_f2 = time.time() - czas_sortowania_f2
print("\nCzas sortowania dla F2: " + str(czas_sortowania_f2) + " sekund")
koszt_po = cost(macierz_po_od_0_0)
roznica = koszt_przed - koszt_po
print("Poprawa o: " + str(roznica) + ", czyli o " + str(round(roznica*100/koszt_przed)) + "%.")

if czy_pokazac_wykresy:
    #print("Lista punktow (x,y), ktore sa docelowymi lokalizacjami")
    print(punkty)
    print(sort_points_list(punkty, odwiedzone_0_0))
    if czy_pokazac_macierze_w_konsoli:
        print("Macierz wylosowana: ")
        print_matrix(macierz_przed)
        print("\n\n")
        print("Macierz posortowana F1 (od najkrotszego polaczenia): ")
        print_matrix(macierz_po)
        print("\n\n")
        print("Macierz posortowana F2 (od bazy): ")
        print_matrix(macierz_po_od_0_0)
        print("\n\n")

    import matplotlib.pyplot as plt

    # Parametry wyswietlania wykresow
    y_min = -1
    y_max = max_value+1
    x_min = -1
    x_max = max_value+1

    plt.subplot(2, 2, 1)
    plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r', marker='.')
    plt.xlabel('Wylosowane punkty')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
    plt.plot([i[0] for i in punkty], [i[1] for i in punkty])
    plt.plot([i[0] for i in punkty[0:2]], [i[1] for i in punkty[0:2]], c='r')
    plt.xlabel('Losowa kolejnosc')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()

    plt.subplot(2, 2, 3)
    plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
    plt.plot([punkty[i][0] for i in odwiedzone], [punkty[i][1] for i in odwiedzone])
    plt.plot([punkty[i][0] for i in odwiedzone[0:2]], [punkty[i][1] for i in odwiedzone[0:2]], c='r')
    plt.xlabel('F1: Start od najkrotszego polaczenia w calej macierzy')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()

    plt.subplot(2, 2, 4)
    plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
    plt.plot([punkty[i][0] for i in odwiedzone_0_0], [punkty[i][1] for i in odwiedzone_0_0])
    plt.plot([punkty[i][0] for i in odwiedzone_0_0[0:2]], [punkty[i][1] for i in odwiedzone_0_0[0:2]], c='r')
    plt.xlabel('F2: Start od bazy do najblizszego punktu')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()
    plt.show()



