#Funckja sortujaca macierz w taki sposob, aby odloglosci miedzy sasiednimi indeksami byly jak najmniejsze.
#
#
# Funkcja jest najprostsza jak się da;
#
#
#
#
#
from typing import List
from copy import deepcopy
import random  # Testowanie
import time



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


def sort_matrix_by_distance(matrix: List[List]):
    _from = len(matrix)-1
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
    return matrix


def random_cost_matrix(size: int, max_value: int, min_value: int = 0) -> List[List]:
    matrix = [[random.randint(min_value, max_value) for i in range(size)] for j in range(size)]
    for i in range(0, len(matrix)):
        matrix[i][i] = inf
        for j in range(0, len(matrix[i])):
            if i < j:
                matrix[i][j] = matrix[j][i]
    return matrix


inf = float('nan')
wyniki = []
suma = 0
for i in range(5, 10):
    M = random_cost_matrix(i, 20, 1)
    koszt_przed = cost((M))
    M = sort_matrix_by_distance(M)
    wyniki.append( (i, koszt_przed, cost(M), 0-cost(M) + koszt_przed))
    suma = suma + 0-cost(M) + koszt_przed
    pass

#for i in range(len(wyniki)):
#    print(wyniki[i])

#print(suma)
#print(suma / (50-5))

print_matrix(M)