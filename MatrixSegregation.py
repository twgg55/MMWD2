from typing import List
from copy import deepcopy
import random
import math

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
    for i in range(0, len(matrix) - 1):
        _sum = _sum + matrix[i][i + 1]
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
        _visited = [_from]  # Dolaczenie tych punktow do listy odwiedzonych

    while len(_visited) < len(matrix):
        helper = deepcopy(matrix[
                              _from])  # Usuniecie inf z tablicy pomocniczej (funkcje min/max maja z tym problem, gdy stoi na poczatku)
        for i in range(helper.count(inf)):
            helper.pop(helper.index(inf))
        _min_cost = max(helper)  # Znalezienie najwiekszej wartosci w tej liscie
        del helper
        _to = (matrix[_from]).index(_min_cost)  # Dla jakiego indeksu istnieje najwieksza wartosc
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

    if cost(matrix) - cost(new_matrix) > 0:  # Jesli macierz kosztow ulegla poprawie
        matrix = deepcopy(new_matrix)
        del new_matrix
    else:  # Jesli wyzmaczona macierz nie jest lepsza
        del new_matrix
    return matrix, _visited


# Generowanie losowych punktow na plaszczyznie (2 wymiary)
def random_2dim_points(quantity: int, max_value: int = 100, min_value: int = 0) -> List:
    _2D_points_list = [
        (0, 0)]  # BAZA ma zawsze wspolrzedne 0,0. CZEMU? Bo wysypisko jest zawsze POZA miastem, a nie w centrum xD
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
                delta_x = abs(points_list[row][0] - points_list[col][0])
                delta_y = abs(points_list[row][1] - points_list[col][1])
                # list_helper[col] = int((delta_x**2 + delta_y**2)**(1/2))  # Odleglosc w lini prostej
                list_helper[col] = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)
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


def sort_cost_matrix_only_for_indexes(cost_matrix: List, index_list_to_visit: List, start_point_index: int) -> List:
    _visited = [start_point_index]
    wyrownanie = 0 if start_point_index in index_list_to_visit else 1
    # len(index_list_to_visit) + wyrownanie  --> Sprawdzenie, czy nalezy wydluzyc poszukiwania w zaleznosci od tego,
    # czy punkt startowy jest w liscie punktow do odwiedzenia
    # start_point_index - index bazy!
    _from = start_point_index
    while len(_visited) < len(index_list_to_visit) + wyrownanie:
        helper = deepcopy(cost_matrix[
                              _from])  # Usuniecie inf z tablicy pomocniczej (funkcje min/max maja z tym problem, gdy stoi na poczatku)
        for i in range(helper.count(inf)):
            helper.pop(helper.index(inf))
        _min_cost = max(helper)  # Znalezienie najwiekszej wartosci w tej liscie
        del helper
        _to = (cost_matrix[_from]).index(_min_cost)  # Dla jakiego indeksu istnieje najwieksza wartosc
        for i in range(0, len(cost_matrix[_from])):
            """
            i != _from  -> wykluczenie przejscia w ten sam punkt
            cost_matrix[_from][i] is not inf  --> zabronione przejscia odrzucamy
            i not in _visited  -> odwiedzone przejscia rowniez
            i in index_list_to_visit  --> punkt musi znajdowac sie na liscie tych, ktore mamy odwiedzic
            """
            if i != _from and cost_matrix[_from][i] is not inf and i not in _visited and i in index_list_to_visit:
                if cost_matrix[_from][i] < _min_cost:
                    _min_cost = cost_matrix[_from][i]
                    _to = i  # Znaleziono punkt o mniejszym koszcie

        _visited.append(_to)  # Dodaj punkt do odwiedzonych
        _from = _to
        # Koniec while, szukaj nastpenego polaczenia
    return _visited[
           1:]  # Ucinam pierwszy punkt, poniewaz on bedzie tylko raz na poczatku calej listy (a nie w kazdym takim kawalku)


def sort_matrix_areas(cost_matrix: List, points_list: List, amount_trucks: int, _x_base: int = 0, _y_base: int = 0,
                      list_of_lists: bool = False):
    ###
    # list_of_lists - zwracana lista ma byc lista list (dla kazdej smieciarki) czy lista pojedynczych elementow (ciag punktow)
    ###

    if amount_trucks < 4:
        Exception()
    # Krotki: (x, y, r, sin, cos, index_w_liscie_i_macierzy)
    base_index = points_list.index((_x_base, _y_base))
    point_info = [(points_list[i][0], points_list[i][1], cost_matrix[base_index][i],
                   ((points_list[i][1] - _x_base) / cost_matrix[base_index][i] if i != base_index else inf),
                   ((points_list[i][0] - _y_base) / cost_matrix[base_index][i] if i != base_index else inf),
                   i) for i in range(len(points_list))]
    # ((_x_base-points_list[i][1])/cost_matrix[base_index][i] if cost_matrix[base_index][i] != inf else inf)
    # (odleglosc danego punktu od punktu bazy)/odleglosc miedzy nimi
    """
    O co tu kaman? Wyliczajac sinusy i cosinusy musze wykluczyc opcje dzielenia przez zero. Czemu? 
    Wiem co jest baza (podawane wspolrzedne w argumentach funckji), 
    tworzac base_index policze rowniez odleglosc bazy od bazy, a nastpenie sinusy i cosinusy.
    Nie moge tego ominac, poniewaz musze miec zgodne indeksy w point info jak i w cost_matrix oraz points_list
    ALE
    bede pamietal o tym, aby zawsze pomijac punkt bazy w point_info (Bo jaki jest kat miedzy punktem, a soba)

    Punktem odniesienia do wyliczania katow nie jest punkt (0, 0), a jest nim punkt BAZY, nie wazne gdzie jest

    """
    # Lista list:
    # Kazda strefa (smieciarka) ma przypisane do siebie punkty
    points_per_area = []

    def porownanie(value, _min, _max) -> bool:
        if _min > _max:
            return True if _max < value <= _min else False
        return True if _min < value <= _max else False

    for i in range(amount_trucks):
        # angle_min = i * 2*math.pi/amount_trucks
        # angle_max = (i+1) * 2*math.pi/amount_trucks
        sin_min = math.sin(i * 2 * math.pi / amount_trucks)
        sin_max = math.sin((i + 1) * 2 * math.pi / amount_trucks)
        cos_min = math.cos(i * 2 * math.pi / amount_trucks)
        cos_max = math.cos((i + 1) * 2 * math.pi / amount_trucks)

        helper_sin = sin_max
        helper_cos = cos_max
        if cos_min * cos_max < 0:
            # Rozne znaki cosinusow -> sinus osiaga maksimum w srodku przedzialu
            # sin zaczal juz malec
            helper_sin = 1 if sin_min > 0 else -1
            sin_min = helper_sin * min([abs(sin_min), abs(sin_max)])
        if sin_min * sin_max < 0:
            helper_cos = 1 if cos_min > 0 else -1
            cos_min = helper_cos * min([abs(cos_min), abs(cos_max)])
            pass
        sin_max = helper_sin
        cos_max = helper_cos
        del helper_sin, helper_cos
        helper_list = []

        for elem in point_info:
            #  0, 1, 2, 3,   4,   5
            # (x, y, r, sin, cos, index_w_liscie_i_macierzy)
            if elem[0] != _x_base or elem[1] != _y_base:

                if porownanie(elem[3], sin_min, sin_max) and porownanie(elem[4], cos_min, cos_max):
                    helper_list.append(elem[5])
                    # print(str(elem) + " OK")
                    pass
                else:
                    # print(str(elem) + "NOK")
                    pass

        points_per_area.append(deepcopy(helper_list))
        del helper_list, sin_max, sin_min, cos_max, cos_min
    # Po tym forze, mamy podzial na strefy (rowny podzial kątowy)

    # Czas na sortowanie xD
    route = [base_index]
    route_lists_in_list = [base_index]
    for i in range(len(points_per_area)):
        if list_of_lists:
            route_lists_in_list.append(sort_cost_matrix_only_for_indexes(cost_matrix, points_per_area[i], base_index))
        else:
            route = route + sort_cost_matrix_only_for_indexes(cost_matrix, points_per_area[i], base_index)
        pass

    # Gdy otrzymalismy juz kolejnosc zapisu, nalezy zmienic te macierz
    # Zamiana kolumn, wierszy wedlug wyznaczonej kolejnosci
    new_matrix = []
    for i in range(0, len(cost_matrix)):
        helperek = []
        for j in range(0, len(cost_matrix[i])):
            helperek.append(cost_matrix[route[i]][route[j]])
            pass
        new_matrix.append(deepcopy(helperek))
        helperek.clear()
        pass

    if list_of_lists:
        return new_matrix, route_lists_in_list
    return new_matrix, route


def make_cost_matrix(amount_of_points: int, amount_trucks: int, function_id: int = 1, max_val: int = 100,
                     min_val: int = -100):
    points = random_2dim_points(amount_of_points, max_val, min_val)  # Losowanko punktow
    cost_matrix = create_cost_matrix(points)  # stworzenie macierzy kosztow
    if function_id == 1:
        cost_matrix, route = sort_matrix_by_distance(cost_matrix, 0)
    elif function_id == 2:
        cost_matrix, route = sort_matrix_areas(cost_matrix, points, amount_trucks)

    return cost_matrix, points