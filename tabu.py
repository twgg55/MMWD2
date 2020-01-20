from typing import List, Dict, Tuple
import random
from copy import deepcopy
import MatrixSegregation
from random import seed, randint
import Raportowanie
from datetime import time, datetime
import pickle  # Zapisywanie danych do plikow

czy_uzywac_tabu = True

czy_wczytac_plik = True
znacznik_wczytywanego_pliku = 'sym_RoznePrawdopodobienstwa'
czy_zapisac_plik = True
znacznik_zapisywanego_pliku = 'sym_RoznePrawdopodobienstwa_WartosciNR2'

czas_start = datetime.utcnow()

# inf = float('nan')
inf = -1
#

aspiration_procentowy_prog = 0.05

# lokacja 0 to baza
# bin_locations - macierz kosztow
# bin_point_list - lista wspolrzednych (x, y) punktow
# ilosc_punktow_na_strefe - ile punktow jest w kazdej ze stref (podzial ukladu wspolrzednych na strefy wg kata)
#
# Liczba iteracji calego algorytmu
iterations = 1200 * 1000
# Maksymalna ilosc iteracji bez polepszenia wartosci
iterations_without_change_max_value = 512

# seed(1)
min_rubbish = 60  # Minimalna ilosc smieci w lokalizacji
max_rubbish = 550  # Maksymalna ilosc smieci w lokalizacji

min_XY_value = -500  # Minimalna wartość wspolrzednych X,Y dla losowanych punktow
max_XY_value = 500  # Maksymalna wartość wspolrzednych X,Y dla losowanych punktow


liczba_lokacji = 350
liczba_smieciarek = 4


def save_obj(object_name, file_name: str, rozszerzenie: str = '.pkl'):
    # TODO Sprawdzic, czy plik istnieje
    is_it_done = False
    while not is_it_done:
        try:
            with open(file_name + rozszerzenie, 'wb') as my_file:
                pickle.dump(object_name, my_file, pickle.HIGHEST_PROTOCOL)
            is_it_done = True
        except FileNotFoundError:
            f = open(file_name + rozszerzenie, "w+")
            f.close()

    pass


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


def zapisz_dane(file_name: str = znacznik_zapisywanego_pliku):
    """

    :param file_name: Znacznik pliku, do ktorego dopisana zostanie koncowka
    :return:
    """
    dict_helper = {
        'bin_locations': bin_locations,
        'bin_point_list': bin_point_list,
        'ilosc_punktow_na_strefe': ilosc_punktow_na_strefe,
        'rubbish_in_location': rubbish_in_location,
        'trucks_volume': trucks_volume,
        'koszty_uruchomienia_smieciarki': koszty_uruchomienia_smieciarki,
        'koszty_rozladunku_smieciarki': koszty_rozladunku_smieciarki,
        'trucks_returns': trucks_returns
    }
    for key in dict_helper:
        save_obj(file_name=file_name+'_'+key, object_name=dict_helper[key])
        print('Zapisano: ', file_name + '_' + key)

    raport = '\n\nParametry symulacji:' + '\nMinimalna ilosc smieci = ', str(min_rubbish)\
             + '\nMaksymalna ilosc smieci = ', str(max_rubbish) + '\nilosc punktow = ' + str(liczba_lokacji)\
             + '\nilosc smieciarek = ' + str(liczba_smieciarek) + '\nPojenosc smieciarek = ' + str(trucks_volume)\
             + '\nmin_xy_value = ' + str(min_XY_value) + '\nmax_xy_value = ' + str(max_XY_value)\
             + '\nkoszty_uruchomienia_smieciarki' + str(koszty_uruchomienia_smieciarki)\
             + '\nkoszty_rozladunku_smieciarki' + str(koszty_rozladunku_smieciarki)\
             + '\n\n'
    save_obj(file_name=file_name + '_raport', object_name=raport, rozszerzenie='.txt')

    print('\n\n')
    pass


def wczytaj_dane(object_name: str, file_name: str = znacznik_wczytywanego_pliku):
    """

    :param object_name: Oczytywana zmienna
    :param file_name: Znacznik pliku
    :return:
    """
    return load_obj(file_name=file_name+'_'+object_name)


if czy_wczytac_plik is False:
    print('\nLosowanie punktow.\n')
    bin_locations, bin_point_list, ilosc_punktow_na_strefe = MatrixSegregation.make_cost_matrix(
        liczba_lokacji, liczba_smieciarek, function_id=2, min_val=min_XY_value, max_val=max_XY_value)

    rubbish_in_location = [0] + [randint(min_rubbish, max_rubbish) for i in range(liczba_lokacji - 1)]
    trucks_volume = [100*70] + [100 * randint(120, 150) for i in range(liczba_smieciarek-2)] + [100*150]
    # Dodanie kosztu startu i kosztu rozladunku
    koszty_uruchomienia_smieciarki = [volume/10 for volume in trucks_volume]
    koszty_rozladunku_smieciarki = [2*min(trucks_volume)/100 for volume in trucks_volume]
    trucks_returns = [0] * len(trucks_volume)
    if czy_zapisac_plik:
        zapisz_dane()
        pass
else:
    # if czy_wczytac_plik is True #
    bin_locations = wczytaj_dane('bin_locations')
    bin_point_list = wczytaj_dane('bin_point_list')
    ilosc_punktow_na_strefe = wczytaj_dane('ilosc_punktow_na_strefe')
    trucks_volume = wczytaj_dane('trucks_volume')
    rubbish_in_location = wczytaj_dane('rubbish_in_location')
    koszty_uruchomienia_smieciarki = wczytaj_dane('koszty_uruchomienia_smieciarki')
    koszty_rozladunku_smieciarki = wczytaj_dane('koszty_rozladunku_smieciarki')
    trucks_returns = wczytaj_dane('trucks_returns')

    print('\nPoprawnie wczytano pliki.\n')
    pass

print('--------------------------------\nParametry symulacji:')
print('Liczba iteracji = ', iterations)
print('Liczba iteracji bez zmiany= ', iterations_without_change_max_value)
print('Minimalna ilosc smieci = ', min_rubbish)
print('Maksymalna ilosc smieci = ', max_rubbish)
print('ilosc punktow = ', liczba_lokacji)
print('ilosc smieciarek = ', liczba_smieciarek)
print('Pojenosc smieciarek = ', trucks_volume)
print('koszty_uruchomienia_smieciarki', koszty_uruchomienia_smieciarki)
print('koszty_rozladunku_smieciarki', koszty_rozladunku_smieciarki)
print('Wklej te dane to folderu na dysku!\n--------------------------------------')


def first_solution_areas(trucks: List, points_per_area: List):
    _solution = [0] * len(trucks)  # przyjmuje globalne bin_location, garbage_trucks
    number = 1
    for i in range(len(points_per_area)):
        _solution[i] = list(range(number, number+points_per_area[i]))
        number = number+points_per_area[i]
    return _solution


def first_solution(location: List, trucks: List) -> List:  # rozdziel po rowno
    _solution = [0] * len(trucks)  # przyjmuje globalne bin_location, garbage_trucks
    bins_amount = int((len(location) - 1) / len(trucks))  # zwraca poczatkowe solution
    rest = (len(location) - 1) % len(trucks)
    _from = 1
    _to = 1
    for i in range(0, len(trucks)):
        _to += bins_amount
        if rest != 0:
            _to += 1
            rest -= 1
        _solution[i] = list(range(_from, _to))
        _from = _to
    return _solution


def count_cost(_solution: List):  # funkcja kosztu dla sollution
    _cost = 0
    for num_truck in range(0, len(_solution)):
        _cost += truck_ride_cost(_solution[num_truck], num_truck)
    return _cost


def truck_ride_cost(locations: List, num_truck: int):  # zwraca koszt dla jednej śmieciarki
    Raportowanie.used_function('truck_ride_cost')
    # print(locations)
    if locations == []:
        return 0
    trucks_returns[num_truck] = 0
    trucks_filled_volume = [0] * len(trucks_volume)
    ride_cost = bin_locations[0][locations[0]]  # od bazy 0 do pierwszego na liscie
    # Dodanie kosztu uruchomienia
    ride_cost += koszty_uruchomienia_smieciarki[num_truck]

    mnoznik_zalezny_pojemnosci = trucks_volume[num_truck]/max(trucks_volume)
    powrotow = 0

    for i in range(0, len(locations)):
        trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]  # zaladowanie smieci

        if i + 1 >= len(locations):  # jesli ostatni
            ride_cost += bin_locations[locations[i]][0] * mnoznik_zalezny_pojemnosci
            return ride_cost

        if trucks_volume[num_truck] < trucks_filled_volume[num_truck] + rubbish_in_location[locations[i+1]]:  # wroc do bazy jesli smieciarka pelna
            powrotow += 1
            ride_cost += bin_locations[locations[i]][0] * mnoznik_zalezny_pojemnosci
            trucks_filled_volume[num_truck] = 0
            ride_cost += bin_locations[0][locations[i + 1]] * mnoznik_zalezny_pojemnosci
            trucks_returns[num_truck] = trucks_returns[num_truck] + 1
            # Dodanie Kosztu rozladnuku
            # ride_cost += (powrotow - 1)**2 * koszty_rozladunku_smieciarki[num_truck]
            ride_cost += powrotow**3 * koszty_rozladunku_smieciarki[num_truck]

        else:
            ride_cost += bin_locations[locations[i]][locations[i + 1]] * mnoznik_zalezny_pojemnosci

    return ride_cost


solution = first_solution_areas(trucks=trucks_volume, points_per_area=ilosc_punktow_na_strefe)
#Raportowanie.show_routes(solution, bin_point_list, arrow=True, separate_plots=False)

# solution = first_solution(bin_locations, trucks_volume)
cost = count_cost(solution)
print('Koszt pierwszego rozwiazania = ', cost)

# ### END OF PART TWO ####

# ### PART THREE ####
'''######LISTA TABU#########
# {typ_zabronienia1:[ konkretne zabronienia ], typ_zabronienia2: [ konkretne zabronienia ] itd.
# typ1 (i,n)zakaz zmiany i tego kosza na n iteracji
# typ2 (i,j,n) elementu i, j nie moga byc koło siebie przez n iteracji
# typ3 (i,j,n) i-ty kosz nie w j-tej smieciarce przez n kadencji
#...
'''

TABU = {1: [], 2: [],3: []}


def add_to_TABU(TABU: Dict, new_TABU: List, _type: int) -> Dict:
    # jako argument ogonie TABU, nowe pojedyncze zabronienie i jego typ(patrz komentarz wyzej)
    # mozna zaimplementować blokowanie dopisywania tych samych list
    TABU[_type].append(new_TABU)
    return TABU


def print_TABU(TABU: Dict):
    for _type in TABU:
        print(_type, '->', TABU[_type])


''' 
    Funkcje zmieniajace rozwiazanie:
    ch - change + w jaki sposob
#1)
'''


def ch_returns(solution: List) -> List:
    Raportowanie.used_function('ch_returns')
    new_solution = deepcopy(solution)
    truck_max = trucks_returns.index(max(trucks_returns))  # zwraca ktora smieciarka wykonala najwiecej powrotow
    truck_min = trucks_returns.index(min(trucks_returns))  # zwraca ktora smieciarka wykonala najmniej powrotow

    if len(new_solution[truck_max]) < 1:
        return solution

    last_bin = new_solution[truck_max][-1]
    new_solution[truck_min].append(last_bin)
    # del (new_solution[truck_max][-1])
    new_solution[truck_max].remove(last_bin)

    # sprawdz czy kosz ktory funkcja chce zmienic nie jest w TABU
    if check_ban_t1(last_bin):
        # Sprawdzanie czy nowe rozwiazanie jest dozwolone
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution

    if aspiration(solution, new_solution):  # jesli aspiracja zadziala
        return new_solution
    return solution


def ch_swap(solution: List) -> List:
    Raportowanie.used_function('ch_swap')
    new_solution = deepcopy(solution)
    for route in new_solution:
        if(len(route)>=2):
            pair = random.sample(range(0,len(route)), 2)
            route[pair[0]], route[pair[1]] = route[pair[1]], route[pair[0]]

            if check_ban_t1(route[pair[0]]) and check_ban_t1(route[pair[1]]):
                if check_ban_t2(new_solution) and check_ban_t3(new_solution):
                    return new_solution

    if (aspiration(solution,new_solution)): #jesli aspiracja zadziala
        return new_solution
    return solution

def ch_truck(solution: List) -> List:   #zamien smieciarki jesli ta o mniejszej pojemnosci wykonala wiecej powrotow
    Raportowanie.used_function('ch_truck')
    new_solution = deepcopy(solution)
    truck_max = trucks_returns.index(max(trucks_returns))   # zwraca ktora smieciarka wykonala najwiecej powrotow
    truck_min = trucks_returns.index(min(trucks_returns))    # zwraca ktora smieciarka wykonala najmniej powrotow
    new_solution[truck_max], new_solution[truck_min] = new_solution[truck_min], new_solution[truck_max]

    if trucks_volume[truck_max] < trucks_volume[truck_min]:
        if check_ban_t3(new_solution):
            return new_solution

    if (aspiration(solution,new_solution)): #jesli aspiracja zadziala
        return new_solution
    return solution

def ch_bins(solution: List) -> List:
    Raportowanie.used_function('ch_bins')
    new_solution = deepcopy(solution)
    random_bin = random.randint(1, len(bin_locations)-1)
    bin_pos = [(index, row.index(random_bin)) for index, row in enumerate(new_solution) if random_bin in row][0]
    # bin_pos ->[ktora smieciarka, ktory kosz z kolei] - indexy elementu w macierzy
    # print("binpos",bin_pos)

    del(new_solution[bin_pos[0]][bin_pos[1]])
    random_truck = random.randint(0,len(new_solution)-1)
    new_bin_pos = random.randint(0,len(new_solution[random_truck]))

    new_solution[random_truck].insert(new_bin_pos, random_bin)

    if check_ban_t1(random_bin):
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution

    if aspiration(solution,new_solution): # jesli aspiracja zadziala
        return new_solution
    return solution

def ch_del_max(_solution: List):  # usun najdalszy przejazd jaki wystepuje w rozwiazaniu
    Raportowanie.used_function('ch_del_max')
    new_solution = deepcopy(_solution)
    max_p2p_for_truck = [] # maksymalny przejazd dla kazdej smieciarki
    max_p2p_for_truck_value = [] # i jego wartość
    for route in _solution:
        # print("route: ", route)
        if len(route) > 2:
            p2p_values = []
            for i in range( len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
            #print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            max_p2p_for_truck.append([od, do])
            max_p2p_for_truck_value.append(bin_locations[od][do])

        elif len(route) == 2:
            max_p2p_for_truck.append([route[0], route[1]])
            max_p2p_for_truck_value.append(bin_locations[route[0]][route[1]])

    index_of_max = max_p2p_for_truck_value.index(max(max_p2p_for_truck_value)) #zwroci index najdluzszego przejazdu
    [od, do] = max_p2p_for_truck[index_of_max]
    # print(od,do)

    # przenies losowy kosz z wybranej pary [od do] do innej losowej smieciarki
    if random.randint(0, 1):
        random_bin = od
    else:
        random_bin = do

    bin_pos = [(index, row.index(random_bin)) for index, row in enumerate(new_solution) if random_bin in row][0]

    del(new_solution[bin_pos[0]][bin_pos[1]])
    random_truck = random.randint(0,len(new_solution)-1)
    new_bin_pos = random.randint(0,len(new_solution[random_truck]))

    new_solution[random_truck].insert(new_bin_pos, random_bin)

    if check_ban_t1(random_bin):
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution

    if aspiration(_solution,new_solution): #jesli aspiracja zadziala
        return new_solution
    return new_solution


def ch_move_tail(_solution: List):  # usun najdalszy przejazd jaki wystepuje w rozwiazaniu
    Raportowanie.used_function('ch_move_tail')
    new_solution = deepcopy(_solution)
    max_p2p_for_truck = []  # maksymalny przejazd dla kazdej smieciarki
    max_p2p_for_truck_value = []  # i jego wartość
    for route in _solution:
        # print("route: ", route)
        if len(route) > 2:
            p2p_values = []
            for i in range( len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
            # print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            max_p2p_for_truck.append([od, do])
            max_p2p_for_truck_value.append(bin_locations[od][do])

        elif len(route) == 2:
            max_p2p_for_truck.append([route[0], route[1]])
            max_p2p_for_truck_value.append(bin_locations[route[0]][route[1]])

    index_of_max = max_p2p_for_truck_value.index(max(max_p2p_for_truck_value))  # zwroci index najdluzszego przejazdu
    [od, do] = max_p2p_for_truck[index_of_max]
    # print("od , do", od, do)

    # przenies koniec trasy do najblizszej smieciarki
    for i in range(len(new_solution)):
        if od in new_solution[i]:
            # print("solution[",i,"]",new_solution[i])
            bin_start_index = new_solution[i].index(do)

            tail = new_solution[i][bin_start_index:]
            # head = new_solution[i][bin_start_index:]
            # print("tail", tail)
            first_point = do
            end_point = tail[-1]
            # znajdz najblizszy punkt do first_point

            distances_from_first_point = bin_locations[do]
            distances_from_end_point = bin_locations[end_point]

            bins_from_first_point = range(len(bin_locations[do]))
            bins_from_end_point = range(len(bin_locations[end_point]))

            # slownik klucz - nr kosza wartosc odleglosc od niego
            bins_distances_from_first_point = dict(zip(bins_from_first_point, distances_from_first_point))
            bins_distances_from_end_point = dict(zip(bins_from_end_point,distances_from_end_point ))

            new_bins_distances_from_first_point = {}
            new_bins_distances_from_end_point = {}

            for bin_nr in bins_distances_from_first_point:
                if bin_nr not in new_solution[i]:
                    new_bins_distances_from_first_point[bin_nr] = bins_distances_from_first_point[bin_nr]

            for bin_nr in bins_distances_from_end_point:
                if bin_nr not in new_solution[i]:
                    new_bins_distances_from_end_point[bin_nr] = bins_distances_from_end_point[bin_nr]

            del new_bins_distances_from_first_point[0]
            del new_bins_distances_from_end_point[0]

            # znajdz min odleglosc
            min_from_end_point = min(new_bins_distances_from_first_point.items(), key=lambda x: x[1])
            min_from_first_point = min(new_bins_distances_from_end_point.items(), key=lambda x: x[1])

            if min_from_end_point[1] < min_from_first_point[1]:
                closest_bin = min_from_end_point[0]
            else:
                closest_bin = min_from_first_point[0]

            new_solution[i] = new_solution[i][:bin_start_index]

            bin_pos = [(index, row.index(closest_bin)) for index, row in enumerate(new_solution) if closest_bin in row][0] # bin_pos ->[ktora smieciarka, ktory   kosz z kolei]
            new_truck = bin_pos[0]
            new_solution[new_truck] += deepcopy(tail)
    # sprawdz zabronienia
    # if check_ban_t1(random_bin):
    if check_ban_t2(new_solution) and check_ban_t3(new_solution):
        return new_solution

    if aspiration(_solution, new_solution):  # jesli aspiracja zadziala
        return new_solution
    return new_solution


def ch_connect_close(_solution: List):
    Raportowanie.used_function('ch_connect_close')
    new_solution = deepcopy(_solution)
    #print("\nnewsolution: ", new_solution)
    random_truck = random.randint(0, len(new_solution)-1)
    #print("random_truck",random_truck)

    if len(_solution[random_truck]) < 3:
        return solution

    random_bin_index = random.randint(0, len(_solution[random_truck])-1)
    random_bin = new_solution[random_truck][random_bin_index]

    #print("random_bin",random_bin)

    # znajdz najblizszy
    bins_distances_from_point = {}
    for bin_nr in _solution[random_truck]:
        #print("bin_nr",bin_nr)
        bins_distances_from_point[bin_nr] = bin_locations[random_bin][bin_nr]

    del bins_distances_from_point[random_bin]

    min_list_from_point = sorted(bins_distances_from_point.items(), key=lambda x: x[1])
    #print("min_list_from_point",min_list_from_point)

    closest_bin1 = min_list_from_point[0][0]
    closest_bin2 = min_list_from_point[1][0]
    #closest_bin3 = min_list_from_point[2][0]

    #print("closest_bin1",closest_bin1)
    #print("closest_bin2", closest_bin2)

    new_solution[random_truck].remove(closest_bin1)
    new_solution[random_truck].remove(closest_bin2)
    #new_solution[random_truck].remove(closest_bin3)
    #print("\nnewsolution: ", new_solution)

    random_bin_index = new_solution[random_truck].index(random_bin)
    #print(random_bin_index)

    if random.randint(0, 1):
        new_solution[random_truck].insert(random_bin_index, closest_bin1)
        new_solution[random_truck].insert(random_bin_index + 2, closest_bin2)
        #new_solution[random_truck].insert(random_bin_index + 3, closest_bin3)

    else:
        new_solution[random_truck].insert(random_bin_index,closest_bin2)
        new_solution[random_truck].insert(random_bin_index + 2, closest_bin1)
        #new_solution[random_truck].insert(random_bin_index + 3, closest_bin3)

    #print("newsolution: ",new_solution)
    if check_ban_t1(random_bin) and check_ban_t1(closest_bin1) and check_ban_t1(closest_bin2):
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution

    if aspiration(solution, new_solution): # jesli aspiracja zadziala
        return new_solution
    return solution


''' 
    Funkcjie zabraniajace:
    ban - zabron rozwiazaie
1) policz max przejazd dla smieciarki i zabron go
'''


def ban_max(_solution: List):  # zabron najdluższe przejazdy dla kazdej ze smieciarek
    Raportowanie.used_function('ban_max')
    for route in _solution:
        if len(route) > 2:
            p2p_values = []
            for i in range(len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
            # print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            # print(od, do)
            # print(p2p_values.index(max(p2p_values)))

            tabu_iteration = 5  # mozna wybrac na ile iteracji
            # zabroń i zmień(opcjonalnie)
            add_to_TABU(TABU, [od, do, tabu_iteration], 2)  # zabron

    # zapisc nie do tabu tylko zrobić liste i zrobic max dla calosci


def ban_min(_solution: List):  # zabron zmeniac najkrotszych odcinkow
    Raportowanie.used_function('ban_min')
    for route in _solution:
        if len(route) > 2:
            p2p_values = []
            for i in range(len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
            # print(p2p_values)

            od = route[p2p_values.index(min(p2p_values))]
            do = route[p2p_values.index(min(p2p_values)) + 1]
            # print(od, do)
            # print(p2p_values.index(max(p2p_values)))
            tabu_iteration = 100
            add_to_TABU(TABU, [od, tabu_iteration], 1)  # zabron
            add_to_TABU(TABU, [do, tabu_iteration], 1)  # zabron


def ban_max3(_solution: List): #zabron najdalszy kosz w smiecirce do ktorego najdlej z obydwu stron
    Raportowanie.used_function('ban_max3')
    random_truck = random.randint(0, len(_solution) - 1)

    if len(_solution[random_truck]) > 3 :
        do_od_max = 0 #max suma odcinków DO puntu i OD punktu
        isolated_point = -1
        for i in range(1,len(_solution[random_truck])-1):
            do = bin_locations[_solution[random_truck][i-1]][_solution[random_truck][i]]
            od = bin_locations[_solution[random_truck][i]][_solution[random_truck][i+1]]
            do_od = do+od
            if do_od > do_od_max:
                do_od_max = do_od
                isolated_point = _solution[random_truck][i]

        if isolated_point != -1:
            tabu_iteration = 500
            add_to_TABU(TABU, [isolated_point, random_truck ,tabu_iteration], 3)  # zabron


'''Sprawdz czy nie zabronione
    dla danego rozwiazania, sprawdz czy TABU nie zabrania
'''


# jesli funkcja chce zmienic i ty kosz to zwroc False
def check_ban_t1(point: int) -> bool:
    if czy_uzywac_tabu is False:
        return True
    Raportowanie.used_function('check_ban_t1')
    if TABU[1] == []:
        Raportowanie.used_function('check_ban_t1_True')
        return True
    banned_points = []
    for pair in TABU[1]:
        banned_points.append(pair[0])
    if point in banned_points:
        Raportowanie.used_function('check_ban_t1_False')
        return False
    else:
        Raportowanie.used_function('check_ban_t1_True')
        return True


# jesli w nowym rozwiazaniu kosze z Tabu sa obok siebie zroci False
def check_ban_t2(solution: List) -> bool:
    if czy_uzywac_tabu is False:
        return True
    Raportowanie.used_function('check_ban_t2')
    if TABU[2] == []:
        Raportowanie.used_function('check_ban_t2_True')
        return True
    for triple in TABU[2]:
        pos_point1 = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        pos_point2 = [(index, row.index(triple[1])) for index, row in enumerate(solution) if triple[1] in row]

        # print(pos_point1[0], pos_point2[0])
        if pos_point1[0][0] == pos_point2[0][0]:  # jesli w tej samej śmieciarce
            if abs(pos_point1[0][1] - pos_point2[0][1]) == 1:  # jeśli sa obok siebie
                Raportowanie.used_function('check_ban_t2_False')
                return False
    Raportowanie.used_function('check_ban_t2_True')
    return True


# jesli w nowym rozwiazaniu kosz jesz w zabronionej smieciarce zwroc False
def check_ban_t3(solution: List) -> bool:
    if czy_uzywac_tabu is False:
        return True
    Raportowanie.used_function('check_ban_t3')
    if TABU[3] == []:
        Raportowanie.used_function('check_ban_t3_True')
        return True
    for triple in TABU[3]:
        pos_point = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        if pos_point[0][0] == triple[1]:  # czy kosz jest w zabronionej smieciarce
            Raportowanie.used_function('check_ban_t3_False')
            return False
    Raportowanie.used_function('check_ban_t3_True')
    return True


# ### END OF PART THREE ####

print('Tabu -> ', TABU)
print('Solution -> ', solution)
print('Koszt rozwiazania -> ', count_cost(solution))
print('Aktualna iteracja -> ', Raportowanie.counter)
print('koszty')

ban_min(solution)
print('Tabu po wywolaniu "ban_min(solution)"-> ', TABU)

# ch_del_max(solution)
real_route_dict = Raportowanie.real_route_from_solution(
    _solution=solution,
    cost_matrix=bin_locations,
    rubbish_in_location=rubbish_in_location,
    trucks_max_volumes=trucks_volume,
    xy_points=bin_point_list
)
Raportowanie.show_trasa_z_powrotami(real_route_dict, title='Pierwsze rozwiazanie.')
Raportowanie.show_wypelnienie_od_trasy(real_route_dict, title='Pierwsze rozwiazanie.')

#xsolution = ch_connect_close(solution)
#Raportowanie.real_route_from_solution(
#    _solution=xsolution,
#    cost_matrix=bin_locations,
#    rubbish_in_location=rubbish_in_location,
#    trucks_max_volumes=trucks_volume,
#    xy_points=bin_point_list
#)

print('TYLE')

# ### PART FOUR ####
# Memories

medium_term_memory = {}  # lista najlepszych rozwiązan
iterations_without_change = 0


# Aspiration
def aspiration(solution: List, new_solution: List):  # zwroci TRUE jesli aspiracja ma zadzialac
    Raportowanie.used_function('aspiracja')
    for j in range(0, len(solution)):
        cost_old = truck_ride_cost(solution[j], j)
        cost_new = truck_ride_cost(new_solution[j], j)
        if cost_new - cost_old < aspiration_procentowy_prog * cost_old:
            Raportowanie.used_function('aspiracja_True')
            return True
        # if truck_ride_cost(solution[j], j) < truck_ride_cost(new_solution[j], j):
            # Raportowanie.used_function('aspiracja_True')
            # return True
    Raportowanie.used_function('aspiracja_False')
    return False


# ###END OF PART FOUR ####


# ### TABU SEARCH ####

x0 = deepcopy(solution)  # x0 <=> solution
x_opt = deepcopy(solution)

solution_change = True  # Po to aby pokazac pierwsza opcje
# ShowSolutions.show_routes(x_opt, bin_point_list)

print("START")
print("First solution >", solution, count_cost(solution))
# iterations = WARTOSC ^^^^ Na Gorze pliku

co_ile_procent = 1
helper_okres_jednego_procenta = co_ile_procent*iterations/100
helper_procenty = 0

czas_iteracji_1_proc = datetime.utcnow()
for i in range(0, iterations):
    try:
        if i % helper_okres_jednego_procenta == 0:
            time_helper = datetime.utcnow()
            print(str(helper_procenty) + '%\t',
                  'Godzina',  time_helper.hour, ':', time_helper.minute, ':', time_helper.second,
                  '\tOd startu:', (time_helper - czas_start),
                  '\tCzas dla 1%: ', time_helper - czas_iteracji_1_proc)
            helper_procenty += co_ile_procent
            czas_iteracji_1_proc = time_helper
            del time_helper

        Raportowanie.counter += 1






        '''zmien rozwiazanie'''
        x0 = deepcopy(x_opt)
        change_probability = random.randint(1, 140)

        """change_probability = random.randint(1, 100)
        function_name = 'ch_swap_nie_wykonano_zadnej_funkcji'
        if change_probability in range(1, 8):  # losowe
            x0 = ch_swap(x0)
            function_name = 'ch_swap_poprawa'

        if change_probability in range(8, 17):  # losowe
            x0 = ch_bins(x0)
            function_name = 'ch_bins_poprawa'

        if (change_probability in range(17, 27)):  # stała
            x0 = ch_returns(x0)
            function_name = 'ch_returns_poprawa'

        if change_probability in range(27, 40):  # stała
            x0 = ch_del_max(x0)
            function_name = 'ch_del_max_poprawa'

        threshold1 = 60 * (iterations - i) / iterations
        threshold2 = threshold1 + 20 * (iterations - i) / iterations

        if change_probability in range(40, int(threshold1)):  # ma być coraz rzadziej
            x0 = ch_truck(x0)
            function_name = 'ch_truck_poprawa'

        if change_probability in range(int(threshold1), int(threshold2)):  # ma być coraz rzadziej
            x0 = ch_move_tail(x0)
            function_name = 'ch_move_tail_poprawa'

        if change_probability in range(int(threshold2), 100):  # ma być coraz cześciej
            x0 = ch_connect_close(x0)
            function_name = 'ch_connect_close_poprawa'"""

        # if(change_probability in range(1,60)):
        # print('1')
        # x0 = ch_returns(x0)
        function_name = 'ch_swap_nie_wykonano_zadnej_funkcji'
        if change_probability in range(1, 20):
            # print('2')
            function_name = 'ch_swap_poprawa'
            x0 = ch_swap(x0)

        if change_probability in range(21, 40):
            # print('3')
            function_name = 'ch_truck_poprawa'
            x0 = ch_truck(x0)

        if change_probability in range(41, 60):
            # print('4')
            function_name = 'ch_bins_poprawa'
            x0 = ch_bins(x0)

        if change_probability in range(61, 80):
            x0 = ch_del_max(x0)
            function_name = 'ch_del_max_poprawa'

        if change_probability in range(81, 100):
            x0 = ch_connect_close(x0)
            function_name = 'ch_connect_close_poprawa'

        if change_probability in range(101, 120):
            x0 = ch_move_tail(x0)
            function_name = 'ch_move_tail_poprawa'

        if change_probability in range(121, 140):
            x0 = ch_returns(x0)
            function_name = 'ch_returns_poprawa'


        # print(x, " -> ", count_cost(x))

        cost_x0 = count_cost(x0)
        # print("nowy koszt: ",cost_x0)
        # ShowSolutions.show_routes(x0, bin_point_list)
        cost_x_opt = count_cost(x_opt)

        if cost_x0 < cost_x_opt:
            # print("xopt",x_opt, " --> ", cost_x_opt)
            # print("x0", x0, " --> ", cost_x0)

            x_opt = deepcopy(x0)
            Raportowanie.used_function(Raportowanie.klucz_slowny_lista_koszt_od_iteracji, [i, cost_x_opt])
            Raportowanie.used_function(function_name, i)
            solution_change = True
            iterations_without_change = 0
        else:
            iterations_without_change = iterations_without_change + 1

        '''skroc o 1 kadencje'''
        for type_T in TABU:
            for single_tabu in TABU[type_T]:
                if len(single_tabu) == 0 or single_tabu[-1] == 1:  # jesli kadencja = 0 to usuń zabronienie
                    TABU[type_T].remove(single_tabu)
                else:
                    single_tabu[-1] = single_tabu[-1] - 1

        '''Dodaj nowe elementy do listy TABU'''

        tabu_probability = random.randint(1, 100)
        if tabu_probability in (1, 15):
            ban_min(x_opt)
        elif tabu_probability in (15, 20):
            ban_max(x_opt)
        elif tabu_probability in (20, 25):
            ban_max3(x_opt)

        '''Pamiec srednioterminowa i kryterium aspiracji'''
        if iterations_without_change >= iterations_without_change_max_value:
            Raportowanie.used_function('okresow_bez_poprawy', i)
            medium_term_memory[count_cost(x_opt)] = x_opt

            iterations_without_change = 0
            liczba_opcji = 20  # Ile mamy sposobow na wyjscie z minimum lokalnego
            if i % liczba_opcji != 0:
                Raportowanie.used_function('x_opt = deepcopy(x0)', i)
                x_opt = deepcopy(x0)  # Bierzemy rozwiaznie, ktore akurat sie pojawilo
            elif i % liczba_opcji == 0:
                Raportowanie.used_function('x_opt = deepcopy(solution)', i)
                x_opt = deepcopy(solution)  # Rozwiazanie z poczatku

            # dywersyfikacja jeśli sie nie poprawi przez n iteracji to wez nowe (gorsze)rozwiazanie
            # obecnie- wroc do poczatku

        '''przedstawianie wyniku'''
        if solution_change:
            # ShowSolutions.show_routes(x_opt, bin_point_list)
            solution_change = False

        # Dodanie do raportu aktualnie liczone rozwiazania
        # Raportowanie.used_function(Raportowanie.klucz_slowny_optymalnego_kosztu_rozwiazania, cost_x_opt)
        Raportowanie.used_function(Raportowanie.klucz_rozmiar_tabu_1, len(TABU[1]))
        Raportowanie.used_function(Raportowanie.klucz_rozmiar_tabu_2, len(TABU[2]))
        Raportowanie.used_function(Raportowanie.klucz_rozmiar_tabu_3, len(TABU[3]))
        # Raportowanie.used_function(Raportowanie.klucz_slowny_kosztu_rozwiazania, cost_x0)
    except:
        print('Blad')


if medium_term_memory:
    min_road = min(medium_term_memory.keys())
    x_opt = deepcopy(medium_term_memory[min_road])


real_route_dict = Raportowanie.real_route_from_solution(
    _solution=x_opt,
    cost_matrix=bin_locations,
    rubbish_in_location=rubbish_in_location,
    trucks_max_volumes=trucks_volume,
    xy_points=bin_point_list
)


def zapisz_wyniki(file_name: str = znacznik_zapisywanego_pliku):
    dict_helper = {
        'x_opt': x_opt,
        'count_cost(x_opt)': count_cost(x_opt),
        'dict_function_usage[klucz_slowny_lista_koszt_od_iteracji]': Raportowanie.dict_function_usage[Raportowanie.klucz_slowny_lista_koszt_od_iteracji],
        'real_route_dict': real_route_dict
    }
    for key in dict_helper:
        save_obj(file_name=file_name + '_ROZWIAZANIE_' + key, object_name=dict_helper[key])
        print('Zapisano: ', file_name + '_' + key)


"""print("Wynik:")
print("medium_term_memory :\n")
[print(sol, medium_term_memory[sol]) for sol in medium_term_memory.keys()]"""

print("iterations_without_change ->", iterations_without_change)
print("x_opt ->", x_opt, "\n count_cost(x_opt) ->", count_cost(x_opt))

print('Wyswietlono wykres ostatecznego rozwiazania.')
# Raportowanie.show_routes(x_opt, bin_point_list)

Raportowanie.show_solution_cost(Raportowanie.klucz_slowny_optymalnego_kosztu_rozwiazania,
                                plot_title='Koszt rozwiazania')
Raportowanie.show_tabu_size()

# Raportowanie.show_routes(x_opt, bin_point_list)



Raportowanie.show_raport(real_route_dict, title='Ostateczne rozwiazanie.')
zapisz_wyniki()



'''
#srednoirweminowa sprawdz rozwiazania zanim zapiszesz do pamieci
#rozwiazania podobne nie zapisujemy na liscie
# zapisać np 5 na roznych górkach
#długotermiowa
#smieciarki kosze ile razy dany kosz był w śmieciarce
#gromadzenie wiedzy
#jeśi nie poprawi to nie opłaca się korzystać
#np możana klika pomysłów, potem sprawdzić który lepszy
'''