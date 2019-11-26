from typing import List
from copy import deepcopy
import matplotlib.pyplot as plt


def show_routes(routes_lists: List, xy_points: List, colours: List[str] = None,
                point_marker: str = None, point_color: str = None, separate_plots: bool = False) -> None:
    ###
    # routes_lists - rozwiązanie zadania. Lista list (tras śmieciarek) -> to powinny być indeksy punktow w liscie :)
    # xy_points - wylosowane punkty (Wspolrzedne XY) jako krotki w liscie
    # colours - lista kolejnych kolorow (jezeli chcemy, żeby była narzucona)
    # point_marker - jakim symbolem maja byc zaznaczane punkty
    # point_color - kolor punktu
    # separate_plots - Czy chcemy mieć osobne wykresy dla każdej śmieciarki?
    #
    ###
    if colours is None:
        colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'maroon', 'orangered', 'orange', 'lime']
    if point_marker is None:
        point_marker = '.'
    if point_color is None:
        point_color = 'r'

    # _x = [xy[0] for xy in xy_points]  # Wyciągnięte argumenty
    # _y = [xy[1] for xy in xy_points]  # Wyciągnięte wartości

    lista_legendy = []

    for i in range(len(routes_lists)):  # Petla po kazdej smieciarce
        # lista_legendy.append("ID pojazdu: " + str(i))  # TODO Dodac ewentualne ID pojazdu, jak beda rozrozniane
        _x_route = [xy_points[xyID][0] for xyID in routes_lists[i]]  # Punkty, ktore odwiedza dana smieciarka
        _y_route = [xy_points[xyID][1] for xyID in routes_lists[i]]

        # Ta czesc odpowiada za to, zeby wybierano po kolei kolory.
        # Gdy smieciarek bedzie wiecej niz dostepnych opcji kolorystycznych to kolory sie zapetla
        helper = deepcopy(i)  # TODO Tu mozna by dodac zmienna, zamiast co petle liczyc od nowa, ale EGAR
        while helper >= len(colours):
            helper = helper - len(colours)
        color_helper = colours[helper]
        del helper

        plt.plot(_x_route[:2], _y_route[:2], c=color_helper, linestyle=':')  # Wyjazd z bazy do pierwszego punktu
        plt.plot(_x_route[1:len(_x_route)-1], _y_route[1:len(_y_route)-1], c=color_helper,  # Trasa
                 linestyle='-', label=('ID pojazdu: '+str(i)))
        plt.plot(_x_route[len(_x_route)-2:], _y_route[len(_y_route)-2:], c=color_helper, linestyle='-.')  # Powrot

        if separate_plots or i == len(routes_lists)-1:
            plt.grid()
            if separate_plots:
                plt.title('Trasa śmieciarki nr ' + str(i))
            else:
                # plt.legend(lista_legendy)
                plt.legend()
                plt.title("Trasy smieciarek")
            plt.scatter([xy[0] for xy in xy_points], [xy[1] for xy in xy_points], c=point_color, marker=point_marker)  # Na koncu, aby punkty byly na wierzchu
            plt.show()
        pass
    pass


Punkty = [(0, 0), (44, 8), (56, 66), (43, 99), (11, 40), (15, 42), (1, 10)]
Trasy = [[0, 1, 2, 5, 6, 0],
         [0, 3, 4, 0]]


show_routes(Trasy, Punkty, separate_plots=False)

