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
klucz_slowny_kosztu_rozwiazania = 'koszt_rozwiazania'


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
