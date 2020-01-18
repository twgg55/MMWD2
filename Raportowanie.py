import ShowSolutions
#
#
# {'nazwa_funkcji': [1, 10, 22, 55]}  # Numery iteracji, w ktorych zostala uzyta
#
#
from typing import Dict, List
dict_function_usage = dict()
counter = 0  # Licznik iteracji dla glownego programu
# 'koszt_rozwiazania' !!! klucz slowny
klucz_slowny_optymalnego_kosztu_rozwiazania = 'optymalny_koszt_rozwiazania'
klucz_slowny_lista_koszt_od_iteracji = 'koszt_rozw_od_iteracji_lista'
klucz_slowny_kosztu_rozwiazania = 'koszt_rozwiazania'
klucz_rozmiar_tabu_1 = 'tabu_1_rozmiar'
klucz_rozmiar_tabu_2 = 'tabu_2_rozmiar'
klucz_rozmiar_tabu_3 = 'tabu_3_rozmiar'

zakaz_zliczania = True


def used_function(f_name: str, number=counter):
    if zakaz_zliczania:
        # zliczaj tylko klucz_slowny_lista_koszt_od_iteracji
        if f_name == klucz_slowny_lista_koszt_od_iteracji:
            if f_name not in dict_function_usage.keys():
                # Stworz w slowniku odpowiednie pole
                dict_function_usage[f_name] = list()
            dict_function_usage[f_name].append(number)
        return

    # Pomijanie kluczy, gdy testowanie jest juz zbedne, ale zeby nie szukac tego po kodzie
    wykluczone_klucze = ['truck_ride_cost', klucz_rozmiar_tabu_1, klucz_rozmiar_tabu_2, klucz_rozmiar_tabu_3]
    if f_name in wykluczone_klucze:
        return

    if f_name not in dict_function_usage.keys():
        # Stworz w slowniku odpowiednie pole
        dict_function_usage[f_name] = list()
        dict_function_usage[f_name].append(number)
    else:
        # dodaj numer iteracji programu do pamieci wywolan
        dict_function_usage[f_name].append(number)
    pass


def show_raport(routes_data: Dict = None, title: str = None):
    if zakaz_zliczania:
        if routes_data is not None:
            show_info_trasy_smieciarek(routes_data, title)
            show_trasa_z_powrotami(routes_data, title, arrow=False)
            show_wypelnienie_od_trasy(routes_data, title)
            show_trasa_z_powrotami(routes_data, title, separate_plots=False)
        print('Zabroniono zliczania -> parametr "zakaz_zliczania" w pliku Raportowanie')
        return
    """

    :param routes_data:
    :param title:
    :return:
    """
    print('\nRaport uzycia funkcji: (funckja: show_raport)')
    max_length = 0
    for key in dict_function_usage.keys():
        # szukanie najdluzszego slowa (frazy klucza) ze wszystkich
        if max_length < len(key):
            max_length = len(key)

    # Wypisanie wszystkich uzytych funkcji
    for key in dict_function_usage.keys():
        tekst_wyrownawczy = '-'*(max_length-len(str(key)))
        procentowe_wykorzystanie = round(10000*len(dict_function_usage[key])/counter)/100
        print('- "' + str(key) + '"' + tekst_wyrownawczy + '\t->\t', len(dict_function_usage[key]),
              ' '*(10-len(str(len(dict_function_usage[key])))) + ' ~ ', procentowe_wykorzystanie, '%')
    print('\n')

    show_used_functions_by_keyname('_poprawa', 'Funkcje zmieniajace rozwiazanie, ktore poprawily rozwiazanie')
    show_used_functions_by_keyname('_True', 'Funkcje zabraniajace zmiany rozwiazania -> True')
    show_used_functions_by_keyname('_False', 'Funkcje zabraniajace zmiany rozwiazania -> False')

    # ---------------------------------------------------------------------------------------------------------------
    if routes_data is not None:
        show_trasa_z_powrotami(routes_data, title)
        show_wypelnienie_od_trasy(routes_data, title)
        show_info_trasy_smieciarek(routes_data, title)

        pass
    print('\nProgram wykonal ', counter, ' iteracji.\n')
    pass


def show_used_functions_by_keyname(key_name: str, description: str):
    if zakaz_zliczania:
        print('Zabroniono zliczania -> parametr "zakaz_zliczania" w pliku Raportowanie')
        return
    # Nazwa funkcji ma postac functionName_KeyName_Value
    # Usuwam to z konca i mam dostac nazwe funkcji!

    # szukanie kluczy z fraza
    ch_poprawa_keys = list()
    max_length = 0
    for key in dict_function_usage.keys():
        if key_name in key:
            ch_poprawa_keys.append(key)
            # szukanie najdluzszego slowa (frazy klucza) ze wszystkich
            if max_length < len(key):
                max_length = len(key)

    # Raport funkcji zawierajacych klucz
    print('\n', description)
    print('Znaleziono ', len(ch_poprawa_keys), ' funkcji zawierajacych szukana fraze: ', key_name)

    for key in ch_poprawa_keys:
        try:
            ch_f_key = key[:key.index(key_name)]
            tekst_wyrownawczy = '-' * (max_length - len(str(ch_f_key)))
            procentowe_wykorzystanie = round(
                10000 * len(dict_function_usage[key]) / len(dict_function_usage[ch_f_key])) / 100
            """
            - "ch_nazwa_f" --------- -> 124  /  240    ~  51 %
            """
            print('- "' + str(ch_f_key) + '"' + tekst_wyrownawczy + '\t->\t', len(dict_function_usage[key]),
                  ' ' * (4 - len(str(len(dict_function_usage[key])))), '/', len(dict_function_usage[ch_f_key]),
                  ' ' * (5 - len(str(len(dict_function_usage[key])))) + ' ~ ', procentowe_wykorzystanie, '%')
        except KeyError:
            print('\n\n---------\nERROR, Wyjatek w "show_used_functions_by_keyname"')
            print('KeyError')
            print('szukana fraza w nazwach funkcji to: "key_name"')
            print('Nazwa funkcji bez tej frazy to: "ch_f_key"')
            pass

    return


def show_solution_cost(name_key: str, plot_title: str = None, plot_x_label: str = None, plot_y_label: str = None):
    if zakaz_zliczania:
        print('Zabroniono zliczania -> parametr "zakaz_zliczania" w pliku Raportowanie')
        print('Wyswietlanie klucz_slowny_lista_koszt_od_iteracji: ', klucz_slowny_lista_koszt_od_iteracji)
        x = [elem[0] for elem in dict_function_usage[klucz_slowny_lista_koszt_od_iteracji]]
        y = [elem[1] for elem in dict_function_usage[klucz_slowny_lista_koszt_od_iteracji]]
        ShowSolutions.plt.plot(x, y)
        del x, y
        ShowSolutions.plt.grid()
        ShowSolutions.plt.title(plot_title)
        ShowSolutions.plt.xlabel(plot_x_label)
        ShowSolutions.plt.ylabel(plot_y_label)
        ShowSolutions.plt.show()
        return
    # ShowSolutions.plt.scatter(range(counter), dict_function_usage[klucz_slowny_kosztu_rozwiazania], marker='.', c='r')
    if name_key not in dict_function_usage.keys():
        print('Brak takiego klucza w slowniku. Szukana fraza: "'+str(name_key)+'", type->', type(name_key))
        return False
    ShowSolutions.plt.plot(dict_function_usage[name_key])
    ShowSolutions.plt.grid()
    ShowSolutions.plt.title(plot_title)
    ShowSolutions.plt.xlabel(plot_x_label)
    ShowSolutions.plt.ylabel(plot_y_label)
    ShowSolutions.plt.show()
    pass


def show_tabu_size(plot_title: str = 'Rozmiar list tabu', plot_x_label: str = 'Iteracje', plot_y_label: str = 'Rozmiar'):
    if zakaz_zliczania:
        print('Zabroniono zliczania -> parametr "zakaz_zliczania" w pliku Raportowanie')
        return
    for name_key in [klucz_rozmiar_tabu_1, klucz_rozmiar_tabu_2, klucz_rozmiar_tabu_3]:
        if name_key not in dict_function_usage.keys():
            print('\nERR\nBrak takiego klucza w slowniku. Szukana fraza: "' + str(name_key) + '", type->', type(name_key))
            return False
        ShowSolutions.plt.plot(dict_function_usage[name_key], label=name_key)
    ShowSolutions.plt.grid()
    ShowSolutions.plt.title(plot_title)
    ShowSolutions.plt.xlabel(plot_x_label)
    ShowSolutions.plt.ylabel(plot_y_label)
    ShowSolutions.plt.legend()
    ShowSolutions.plt.show()
    pass


def real_route_from_solution(_solution: List, cost_matrix: List, rubbish_in_location: List, trucks_max_volumes: List,
                             xy_points: List) -> Dict:
    """
    Dostajac solution, zwracam dokladny przejazd smieciarki, liczbe powrotow, liczbe odwiedzonych punktow
        dla kazdej smieciarki
    :param xy_points: lista wspolrzednych (x, y) kazdego punktu na plaszczyznie
    :param trucks_max_volumes: lista z pojemnosciami kazdej smieciarki
    :param rubbish_in_location: lista smieci w kazdym z punktow
    :param cost_matrix: macierz kosztow podrozy dla punktow
    :param _solution: rozwiazanie, ktore chcemy wyrysowac
    :return:
    """
    routes_data = dict()
    real_route_solution = [[0] for n_truck_route in _solution]  # Wszystkie startuja z 0
    truck_returns = [0]*len(_solution)  # Ilosc powrotow kazdej smieciarki, Policzyc zera w wyznaczonej trasie
    trucks_filled_volume = [[0] for n_truck_route in _solution]  # Historia zapelnienia smieciarki poczas trasy
    ride_cost = [[0] for n_truck_route in _solution]  # Historia kosztu trasy, ile do danego momentu juz przejechano

    for truck_route_index in range(len(_solution)):
        truck_route = _solution[truck_route_index]  # Trasa konkretnej smieciarki

        _from_index = 0  # index bazy
        for i in range(len(truck_route)):

            real_route_solution[truck_route_index].append(truck_route[i])
            ride_cost[truck_route_index].append(ride_cost[truck_route_index][-1] + cost_matrix[_from_index][truck_route[i]])
            # od bazy 0 do pierwszego na liscie
            trucks_filled_volume[truck_route_index].append(
                trucks_filled_volume[truck_route_index][-1] + rubbish_in_location[truck_route[i]]
            )  # Zaladunek smieci

            if i + 1 >= len(truck_route):  # To byl ostatni punkt trasy, Powrot do bazy
                ride_cost[truck_route_index].append(
                    ride_cost[truck_route_index][-1] + cost_matrix[truck_route[i]][0])
                _from_index = 0
                real_route_solution[truck_route_index].append(0)

            elif trucks_max_volumes[truck_route_index] < trucks_filled_volume[truck_route_index][-1] \
                    + rubbish_in_location[truck_route[i+1]]:
                # Smieciarka nie moze zaladowac nastepnego punktu, musi jechac sie rozladowac
                ride_cost[truck_route_index].append(
                    ride_cost[truck_route_index][-1] + cost_matrix[_from_index][0])
                _from_index = 0  # index bazy
                real_route_solution[truck_route_index].append(0)
                trucks_filled_volume[truck_route_index].append(0)  # Rozladowano
            else:
                _from_index = truck_route[i]  # W nastepnym kroku, wyruszamy z punktu, ktory teraz odwiedzono

        truck_returns[truck_route_index] = real_route_solution[truck_route_index].count(0) - 1

        # print('Raport trasy smieciarki:')
        # print('Smieciarka nr:\t', truck_route_index)
        # print('Pojemnosc: ', trucks_max_volumes[truck_route_index])
        # print('Ilosc punktow do odwiedzenia: ', len(real_route_solution[truck_route_index]))
        # print('Liczba powrotow: ', truck_returns[truck_route_index])
        # print('trucks_filled_volume[truck_route_index]', trucks_filled_volume[truck_route_index])
        # print('ride_cost[truck_route_index])', ride_cost[truck_route_index])
        pass

    routes_data['real_route_solution'] = real_route_solution
    routes_data['truck_returns'] = truck_returns
    routes_data['trucks_filled_volume'] = trucks_filled_volume
    routes_data['ride_cost'] = ride_cost
    routes_data['solution'] = _solution
    routes_data['trucks_max_volumes'] = trucks_max_volumes
    routes_data['xy_points'] = xy_points

    return routes_data


def show_trasa_z_powrotami(routes_data: Dict, title: str = None, separate_plots: bool = False,
                           arrow: bool = True):
    """

    :param arrow:
    :param separate_plots:
    :param title:
    :param routes_data:
    :return:
    """
    if title is None:
        title = ''
    ShowSolutions.show_routes(routes_lists=routes_data['real_route_solution'], xy_points=routes_data['xy_points'],
                              arrow=arrow, separate_plots=separate_plots,
                              title='Trasa z zaznaczonymi powrotami. ' + title)
    pass


def show_info_trasy_smieciarek(routes_data: Dict, title: str = None):
    """

    :param title:
    :param routes_data:
    :return:
    """
    if title is None:
        title = ''
    print('\nRaport tras smieciarek: (info: ' + title + ')')
    print('- Numer, Pojemnosc, Punktow, Powrotow')
    for truck_route_index in range(len(routes_data['solution'])):
        """
            - Numer, Pojemnosc, Punktow, Powrotow
        """
        print('- ' + str(truck_route_index) + ' ' * (len('Numer') - len(str(truck_route_index))),
              '  ' + str(routes_data['trucks_max_volumes'][truck_route_index]) + ' ' * (
                          len('Pojemnosc') - len(str(routes_data['trucks_max_volumes'][truck_route_index]))),
              '  ' + str(len(routes_data['real_route_solution'][truck_route_index])) + ' ' * (
                          len('Punktow') - len(str(len(routes_data['real_route_solution'][truck_route_index]))) - 1),
              '  ' + str(routes_data['truck_returns'][truck_route_index]) + ' ' * (
                          len('Powrotow') - len(str(routes_data['truck_returns'][truck_route_index])))
              )

        pass
    return


def show_wypelnienie_od_trasy(routes_data: Dict, title: str = None):
    """

    :param title:
    :param routes_data:
    :return:
    """
    from matplotlib import pyplot as plt2
    colours = ['b', 'g', 'c', 'm', 'y', 'k', 'maroon', 'orangered', 'orange', 'lime', 'r']

    if title is None:
        title = ''
    for truck_route_index in range(len(routes_data['solution'])):
        if len(routes_data['ride_cost'][truck_route_index]) <= 1 or len(routes_data['trucks_filled_volume'][truck_route_index]) <= 1:
            # Printuj blad
            print('\n\n---------------------------------')
            print('Wyswietlanie informacji o bledzie () -> real_route_from_solution')
            print('Trasa tej smieciarki jest pusta, stad nie mozna narysowac jej wykresu')
            print('Smieciarka nr:\t', truck_route_index)
            print('Pojemnosc: ', routes_data['trucks_max_volumes'][truck_route_index])
            print('Ilosc punktow do odwiedzenia: ', len(routes_data['real_route_solution'][truck_route_index]))
            print('Liczba powrotow: ', routes_data['truck_returns'][truck_route_index])
            print('len(tego nizej)', len(routes_data['trucks_filled_volume'][truck_route_index]))
            print('trucks_filled_volume[truck_route_index]', routes_data['trucks_filled_volume'][truck_route_index])
            print('Na wykresie: ')
            print('Wspolrzedna X -> ', "routes_data['ride_cost'][truck_route_index]",
                  routes_data['ride_cost'][truck_route_index])
            print('Wspolrzedna Y -> ', "routes_data['trucks_filled_volume'][truck_route_index]",
                  routes_data['trucks_filled_volume'][truck_route_index])
            print('---------------------------------\n')
            plt2.scatter([0], [0])
            plt2.plot([0], [0])
        else:
            helper = truck_route_index
            while helper >= len(colours):
                helper = helper - len(colours)
            color_helper = colours[helper]
            del helper
            plt2.scatter(
                routes_data['ride_cost'][truck_route_index],
                routes_data['trucks_filled_volume'][truck_route_index] + [0], c=color_helper)

            plt2.step(
                routes_data['ride_cost'][truck_route_index],
                routes_data['trucks_filled_volume'][truck_route_index] + [0], c=color_helper, where='post')

        pass

    plt2.title('Zapelnienie smieciarek od przejechanego dystansu. ' + title)
    plt2.grid()
    plt2.legend(
        ['ID=' + str(truck_route_index) + '; V=' + str(routes_data['trucks_max_volumes'][truck_route_index]) + '; Pkt=' + str(len(routes_data['solution'][truck_route_index])) for truck_route_index in
         range(len(routes_data['solution']))])
    plt2.show()
    pass
