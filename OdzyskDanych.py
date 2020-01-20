import ShowSolutions, pickle


def load_obj(file_name: str):
    # TODO Sprawdzic, czy plik istnieje
    is_it_done = False
    while not is_it_done:
        try:
            with open(file_name + '.pkl', 'rb') as my_file:
                is_it_done = True
                return pickle.load(my_file)

        except FileNotFoundError:
            f = open(file_name + '.pkl', "w+")
            f.close()
            print('Nie wczytano pliku o nazwie: ', file_name)


dict_function_usage = load_obj('sym_RoznePrawdopodobienstwa_PodstawoweWartowsci_ROZWIAZANIE_dict_function_usage[klucz_slowny_lista_koszt_od_iteracji]')
klucz_slowny_optymalnego_kosztu_rozwiazania = 'optymalny_koszt_rozwiazania'
klucz_slowny_lista_koszt_od_iteracji = 'koszt_rozw_od_iteracji_lista'
klucz_slowny_kosztu_rozwiazania = 'koszt_rozwiazania'
klucz_rozmiar_tabu_1 = 'tabu_1_rozmiar'
klucz_rozmiar_tabu_2 = 'tabu_2_rozmiar'
klucz_rozmiar_tabu_3 = 'tabu_3_rozmiar'


print(dict_function_usage)


print('Wyswietlanie klucz_slowny_lista_koszt_od_iteracji: ', klucz_slowny_lista_koszt_od_iteracji)
x = [elem[0] for elem in dict_function_usage]
y = [elem[1] for elem in dict_function_usage]
ShowSolutions.plt.plot(x, y)
del x, y
ShowSolutions.plt.grid()
ShowSolutions.plt.title('')
ShowSolutions.plt.xlabel('')
ShowSolutions.plt.ylabel('')
ShowSolutions.plt.show()

