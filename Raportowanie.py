import ShowSolutions
import timeit
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
klucz_slowny_kosztu_rozwiazania = 'koszt_rozwiazania'
czas_uruchomienia = timeit.timeit()


def used_function(f_name: str, number: int = counter):
    if f_name not in dict_function_usage.keys():
        # Stworz w slowniku odpowiednie pole
        dict_function_usage[f_name] = list()
        dict_function_usage[f_name].append(number)
    else:
        # dodaj numer iteracji programu do pamieci wywolan
        dict_function_usage[f_name].append(number)
    pass


def show_raport():
    print('\nRaport uzycia funkcji:')
    max_length = 0
    for key in dict_function_usage.keys():
        if max_length < len(key):
            max_length = len(key)

    for key in dict_function_usage.keys():
        tekst_wyrownawczy = '-'*(max_length-len(str(key)))
        procentowe_wykorzystanie = round(10000*len(dict_function_usage[key])/counter)/100
        print('- "' + str(key) + '"' + tekst_wyrownawczy + '\t->\t', len(dict_function_usage[key]),
              ' '*(10-len(str(len(dict_function_usage[key])))) + ' ~ ', procentowe_wykorzystanie, '%')

    print('Program wykonal ', counter, ' iteracji.\n')
    pass


def show_solution_cost(name_key: str, plot_title: str = None, plot_x_label: str = None, plot_y_label: str = None):
    # ShowSolutions.plt.scatter(range(counter), dict_function_usage[klucz_slowny_kosztu_rozwiazania], marker='.', c='r')
    if name_key not in dict_function_usage.keys():
        print('Brak takiego klucza w slowniku. Szukana fraza: "'+str(name_key)+'", type->', type(name_key))
        return
    ShowSolutions.plt.plot(dict_function_usage[name_key])
    ShowSolutions.plt.grid()
    ShowSolutions.plt.title(plot_title)
    ShowSolutions.plt.xlabel(plot_x_label)
    ShowSolutions.plt.ylabel(plot_y_label)
    ShowSolutions.plt.show()
    pass


def real_route_from_solution(_solution: List, cost_matrix: List, rubbish_in_location: List, trucks_max_volumes: List,
                             xy_points: List) -> (List, List, List):
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

        print('---------------------------------------')
        print('truck_route_index\t', truck_route_index)
        print('pojemnosc tej smieciarki ', trucks_max_volumes[truck_route_index])
        print('real_route_solution[truck_route_index]', real_route_solution[truck_route_index])
        print('truck_returns[truck_route_index]', truck_returns[truck_route_index])
        print('trucks_filled_volume[truck_route_index]', trucks_filled_volume[truck_route_index])
        print('ride_cost[truck_route_index])', ride_cost[truck_route_index])


    # Testowanie
    ShowSolutions.show_routes(routes_lists=real_route_solution, xy_points=xy_points, arrow=True, separate_plots=False,
                              title='Trasa z zaznaczonymi powrotami')


def detailed_raport_last_solution():
    """
    Wypisanie szczegolowych informacji o rozwiazaniu:
        Numer smieciarki, jej pojemnosc,
        Ilosc punktow do odwiedzenia, ile powrotow jest przewidzianych,
        Wyrysowanie dokladnej trasy wraz z powrotami
    :return:
    """


    pass
