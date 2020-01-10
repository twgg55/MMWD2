from typing import List
from copy import deepcopy
import matplotlib.pyplot as plt


def show_routes(routes_lists: List, xy_points: List, colours: List[str] = None, arrow: bool = True,
                point_marker: str = None, point_color: str = None, separate_plots: bool = False) -> None:
    ###
    # routes_lists - rozwiązanie zadania. Lista list (tras śmieciarek) -> to powinny być indeksy punktow w liscie :)
    # xy_points - wylosowane punkty (Wspolrzedne XY) jako krotki w liscie
    # colours - lista kolejnych kolorow (jezeli chcemy, żeby była narzucona)
    # arrow - Czy rysowac strzalki? Jesli nie zostana zwykle linie
    # point_marker - jakim symbolem maja byc zaznaczane punkty
    # point_color - kolor punktu
    # separate_plots - Czy chcemy mieć osobne wykresy dla każdej śmieciarki?
    #
    ###
    if colours is None:
        colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'maroon', 'orangered', 'orange', 'lime']
    if point_marker is None:
        point_marker = 'o'
    if point_color is None:
        point_color = 'r'

    # _x = [xy[0] for xy in xy_points]  # Wyciągnięte argumenty
    # _y = [xy[1] for xy in xy_points]  # Wyciągnięte wartości

    lista_legendy = []
    for i in range(len(routes_lists)):  # Petla po kazdej smieciarce
        lista_legendy.append("ID pojazdu: " + str(i))  # TODO Dodac ewentualne ID pojazdu, jak beda rozrozniane
        _x_route = [xy_points[xyID][0] for xyID in routes_lists[i]]  # Punkty, ktore odwiedza dana smieciarka
        _y_route = [xy_points[xyID][1] for xyID in routes_lists[i]]

        # Ta czesc odpowiada za to, zeby wybierano po kolei kolory.
        # Gdy smieciarek bedzie wiecej niz dostepnych opcji kolorystycznych to kolory sie zapetla
        helper = deepcopy(i)  # TODO Tu mozna by dodac zmienna, zamiast co petle liczyc od nowa, ale EGAR
        while helper >= len(colours):
            helper = helper - len(colours)
        color_helper = colours[helper]
        del helper

        if arrow:
            for a in range(len(routes_lists[i])-1):
                _dx = _x_route[a+1] - _x_route[a]
                _dy = _y_route[a + 1] - _y_route[a]
                plt.arrow(_x_route[a], _y_route[a], _dx, _dy, head_width=1.2, head_length=2.5,
                          fc=color_helper, ec=color_helper, color=color_helper, length_includes_head=True)
        else:
            """plt.plot(_x_route[:2], _y_route[:2], c=color_helper, linestyle=':')  # Wyjazd z bazy do pierwszego punktu
            plt.plot(_x_route[1:len(_x_route) - 1], _y_route[1:len(_y_route) - 1], c=color_helper,  # Trasa
                     linestyle='-', label=('ID pojazdu: ' + str(i)))
            plt.plot(_x_route[len(_x_route) - 2:], _y_route[len(_y_route) - 2:], c=color_helper,
                     linestyle='-.')  # Powrot"""
            plt.plot([0, _x_route[0]], [0, _y_route[0]], c=color_helper, linestyle=':')  # Wyjazd z bazy do pierwszego punktu
            plt.plot(_x_route, _y_route, c=color_helper,  # Trasa
                     linestyle='-', label=('ID pojazdu: ' + str(i)))
            plt.plot([0, _x_route[len(_x_route) - 1]], [0, _y_route[len(_y_route) - 1]], c=color_helper,
                     linestyle='-.')  # Powrot

        if separate_plots or i == len(routes_lists)-1:
            plt.grid()
            if separate_plots:
                plt.title('Trasa śmieciarki nr ' + str(i))
            else:
                if arrow:
                    # plt.legend(lista_legendy)
                    pass
                else:
                    plt.legend()
                plt.title("Trasy smieciarek")
            plt.scatter([xy[0] for xy in xy_points], [xy[1] for xy in xy_points], c=point_color, marker=point_marker)
            # Na koncu, aby punkty byly na wierzchu

            plt.show()
        pass
    pass


"""def show_routes_all_details(routes_lists_full_detail: List, xy_points: List, separate_plots: bool = False,
                            show_not_visited_points: bool = False) -> None:
    # Funkcja rysuje pelna trase smieciarki (kazdy powrot jest zaznaczony)
    # routes_lists_full_detail - lista tras (powroty musza byc tam zaznaczone!)
    # xy_points - lista wspolrzednych (x, y) punktow - indeksy musza sie zgadzac z tymi w trasie!
    # separate_plots - czy wyswietlac osobne wykresy
    # show_not_visited_points - jezeli wyswietlamy osobne wykresy,
    #       czy wyswietlac punkty, ktore nie zostana owiedzone przez te smieciarke?
    #
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'maroon', 'orangered', 'orange', 'lime']
    point_colour = 'r'  # Kolor zaznaczonych punktow na wykresie

    # Przykladowa trasa [2, 5, 6, 3, 7, 8, 10, 11]
    # Musi zostac wprowadzona tutaj jako [0, 2, 5, 6, 3, 0, 7, 8, 10, 11, 0] - (zero w srodku to powrot)

    # Style 
    linestyle_normal_work = '-'
    linestyle_from_base = ':'
    linestyle_to_base = '-.'


    lista_legendy = []
    for i in range(len(routes_lists_full_detail)):  # Petla po kazdej smieciarce
        lista_legendy.append("ID pojazdu: " + str(i))  # TODO Dodac ewentualne ID pojazdu, jak beda rozrozniane
        _x_route = [xy_points[xyID][0] for xyID in routes_lists_full_detail[i]]  # Punkty, ktore odwiedza dana smieciarka
        _y_route = [xy_points[xyID][1] for xyID in routes_lists_full_detail[i]]

        # Ta czesc odpowiada za to, zeby wybierano po kolei kolory.
        # Gdy smieciarek bedzie wiecej niz dostepnych opcji kolorystycznych to kolory sie zapetla
        helper = deepcopy(i)  # TODO Tu mozna by dodac zmienna, zamiast co petle liczyc od nowa, ale EGAR
        while helper >= len(colours):
            helper = helper - len(colours)
        color_helper = colours[helper]
        del helper






        plt.plot([0, _x_route[0]], [0, _y_route[0]], c=color_helper,
                     linestyle=':')  # Wyjazd z bazy do pierwszego punktu
        plt.plot(_x_route, _y_route, c=color_helper,  # Trasa
                     linestyle='-', label=('ID pojazdu: ' + str(i)))
        plt.plot([0, _x_route[len(_x_route) - 1]], [0, _y_route[len(_y_route) - 1]], c=color_helper,
                     linestyle='-.')  # Powrot

        if separate_plots or i == len(routes_lists_full_detail) - 1:
            plt.grid()
            if separate_plots:
                plt.title('Trasa śmieciarki nr ' + str(i))
            else:

                plt.legend()
            plt.title("Trasy smieciarek")
            plt.scatter([xy[0] for xy in xy_points], [xy[1] for xy in xy_points], c=point_colour)  # Na koncu, aby punkty byly na wierzchu
            plt.show()


    pass
"""
