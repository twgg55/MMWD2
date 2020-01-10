from typing import List, Dict, Tuple
import random
import statistics
from copy import deepcopy
import MatrixSegregation
import ShowSolutions
from random import seed, randint
import Raportowanie

# inf = float('nan')
inf = -1

# lokacja 0 to baza
# bin_locations - macierz kosztow
# bin_point_list - lista wspolrzednych (x, y) punktow
# ilosc_punktow_na_strefe - ile punktow jest w kazdej ze stref (podzial ukladu wspolrzednych na strefy wg kata)
#
# Liczba iteracji calego algorytmu
iterations = 10 * 1000
# Maksymalna ilosc iteracji bez polepszenia wartosci
iterations_without_change_max_value = 257

seed(1)
min_rubbish = 1  # Minimalna ilosc smieci w lokalizacji
max_rubbish = 10  # Maksymalna ilosc smieci w lokalizacji

liczba_lokacji = 250
liczba_smieciarek = 4

bin_locations, bin_point_list, ilosc_punktow_na_strefe = MatrixSegregation.make_cost_matrix(
    liczba_lokacji, liczba_smieciarek, function_id=2)


rubbish_in_location = [0] + [randint(min_rubbish, max_rubbish) for i in range(liczba_lokacji-1)]
# trucks_volume = [1000] * liczba_smieciarek
trucks_volume = [10*randint(20, 80) for i in range(liczba_smieciarek)]
trucks_returns = [0] * len(trucks_volume)


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

    for i in range(0, len(locations)):
        trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]  # zaladowanie smieci

        if i + 1 >= len(locations):  # jesli ostatni
            ride_cost += bin_locations[locations[i]][0]
            return ride_cost

        if trucks_volume[num_truck] < trucks_filled_volume[num_truck] + rubbish_in_location[locations[i+1]]:  # wroc do bazy jesli smieciarka pelna
            ride_cost += bin_locations[locations[i]][0]
            trucks_filled_volume[num_truck] = 0
            ride_cost += bin_locations[0][locations[i + 1]]
            trucks_returns[num_truck] = trucks_returns[num_truck] + 1

        else:
            ride_cost += bin_locations[locations[i]][locations[i + 1]]

    return ride_cost


solution = first_solution_areas(trucks=trucks_volume, points_per_area=ilosc_punktow_na_strefe)
ShowSolutions.show_routes(solution, bin_point_list, arrow=True, separate_plots=False)

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

    new_solution[truck_min].append(new_solution[truck_max][-1])
    del (new_solution[truck_max][-1])

    #sprawdz czy kosz ktory funkcja chce zmienic nie jest w TABU
    if check_ban_t1(new_solution[truck_max][-1]):
        # Sprawdzanie czy nowe rozwiazanie jest dozwolone
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution

    if (aspiration(solution,new_solution)): #jesli aspiracja zadziala
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
# tabu_iteration = 10 pozostalosp po ban_max2
# add_to_TABU(TABU, [od, do, tabu_iteration], 2)


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
    random_truck = random.randint(0, len(new_solution))

    random_bin_index = random.randint(0, len(_solution[random_truck]))
    random_bin = new_solution[random_bin_index]

    # znajdz najblizszy
    bins_distances_from_point = {}
    for bin_nr in _solution[random_truck]:
        bins_distances_from_point[bin_nr] = bin_locations[random_bin][bin_nr]

    del bins_distances_from_point[random_bin]

    min_from_point = min(bins_distances_from_point.items(), key=lambda x: x[1])
    closest_bin = min_from_point[0]

    new_index = random_bin_index + 1
    old_index = _solution[random_truck].index(5)

    new_solution[random_truck].insert(random_bin_index+1 , new_solution[random_truck].pop(old_index))
    # list1.insert(new_index, list1.pop(old_index))


''' Funkcjie zabraniajace:
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
            print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            print(od, do)
            print(p2p_values.index(max(p2p_values)))

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


def ban_max3(_solution: List):
    Raportowanie.used_function('ban_max3')
    # TODO Brak kodu
    print(max(solution))


'''Sprawdz czy nie zabronione
    dla danego rozwiazania, sprawdz czy TABU nie zabrania
'''


#jesli funkcja chce zmienic i ty kosz to zwroc False
def check_ban_t1(point: int) -> bool:
    Raportowanie.used_function('check_ban_t1')
    if TABU[1] == []:
        return True
    banned_points = []
    for pair in TABU[1]:
        banned_points.append(pair[0])
    if point in banned_points:
        return False
    else:
        return True


# jesli w nowym rozwiazaniu kosze z Tabu sa obok siebie zroci False
def check_ban_t2(solution: List) -> bool:
    Raportowanie.used_function('check_ban_t2')
    if TABU[2] == []:
        return True
    for triple in TABU[2]:
        pos_point1 = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        pos_point2 = [(index, row.index(triple[1])) for index, row in enumerate(solution) if triple[1] in row]

        # print(pos_point1[0], pos_point2[0])
        if pos_point1[0][0] == pos_point2[0][0]:  # jesli w tej samej śmieciarce
            if abs(pos_point1[0][1] - pos_point2[0][1]) == 1: # jeśli sa obok siebie
                return False
    return True


# jesli w nowym rozwiazaniu kosz jesz w zabronionej smieciarce zwroc False
def check_ban_t3(solution: List) -> bool:
    Raportowanie.used_function('check_ban_t3')
    if TABU[3] == []:
        return True
    for triple in TABU[3]:
        pos_point = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        if pos_point[0][0] == triple[1]:  # czy kosz jest w zabronionej smieciarce
            return False
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
print('TYLE')

# ### PART FOUR ####
# Memories

medium_term_memory = {} # lista najlepszych rozwiązan
iterations_without_change = 0


# Aspiration
def aspiration(solution:List, new_solution:List):  # zwroci TRUE jesli aspiracja ma zadzialac
    for j in range(0,len(solution)):
        if truck_ride_cost(solution[j],j) < truck_ride_cost(new_solution[j],j):
            return True
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
for i in range(0, iterations):
    Raportowanie.counter += 1
    if i % 1000 == 0:
        pass
        # print(i)

    '''zmien rozwiazanie'''
    x0 = deepcopy(x_opt)
    change_probability = random.randint(1, 100)

    if i < iterations * 3 / 4:
        if change_probability in range(1, 40):
            x0 = ch_move_tail(x0)

    # if(change_probability in range(1,60)):
    # print('1')
    # x0 = ch_returns(x0)
    if change_probability in range(1, 20):
        # print('2')
        x0 = ch_swap(x0)
    if change_probability in range(50, 60):
        # print('3')
        x0 = ch_truck(x0)
    if change_probability in range(40, 80):
        # print('4')
        x0 = ch_bins(x0)
    if change_probability in range(1,100):
        x0 = ch_del_max(x0)
    # x = deepcopy(x0)

    # print(x, " -> ", count_cost(x))

    cost_x0 = count_cost(x0)
    # print("nowy koszt: ",cost_x0)
    # ShowSolutions.show_routes(x0, bin_point_list)
    cost_x_opt = count_cost(x_opt)


    if cost_x0 < cost_x_opt:
        # print("xopt",x_opt, " --> ", cost_x_opt)
        # print("x0", x0, " --> ", cost_x0)

        x_opt = deepcopy(x0)

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
    if tabu_probability in (1, 40):
        pass
        #ban_min(x_opt)
    elif tabu_probability in (20, 30):
         pass
    elif tabu_probability in (40, 50):
        pass
    elif tabu_probability in (50, 100):
        pass

    '''Pamiec srednioterminowa i kryterium aspiracji'''
    if iterations_without_change >= iterations_without_change_max_value:
        medium_term_memory[count_cost(x_opt)] = x_opt

        iterations_without_change = 0
        liczba_opcji = 2  # Ile mamy sposobow na wyjscie z minimum lokalnego
        if i % liczba_opcji == 0:
            x_opt = deepcopy(x0)  # Bierzemy rozwiaznie, ktore akurat sie pojawilo
        elif i % liczba_opcji == 1:
            x_opt = deepcopy(solution)  # Rozwiazanie z poczatku

        # dywersyfikacja jeśli sie nie poprawi przez n iteracji to wez nowe (gorsze)rozwiazanie
        # obecnie- wroc do poczatku

    '''przedstawianie wyniku'''
    if solution_change:
        # ShowSolutions.show_routes(x_opt, bin_point_list)
        solution_change = False

    # Dodanie do raportu aktualnie liczone rozwiazania
    Raportowanie.used_function(Raportowanie.klucz_slowny_optymalnego_kosztu_rozwiazania, cost_x_opt)
    # Raportowanie.used_function(Raportowanie.klucz_slowny_kosztu_rozwiazania, cost_x0)


if medium_term_memory:
    min_road = min(medium_term_memory.keys())
    x_opt = deepcopy(medium_term_memory[min_road])


print("Wynik:")
print("medium_term_memory :\n")
[print(sol, medium_term_memory[sol]) for sol in medium_term_memory.keys()]

print("iterations_without_change ->", iterations_without_change)
print("x_opt ->", x_opt, "\n count_cost(x_opt) ->", count_cost(x_opt))

print('Wyswietlono wykres ostatecznego rozwiazania.')
ShowSolutions.show_routes(x_opt, bin_point_list)


Raportowanie.show_raport()
Raportowanie.show_solution_cost(Raportowanie.klucz_slowny_kosztu_rozwiazania,
                                plot_title='Koszt rozwiazania w danej iteracji')
Raportowanie.show_solution_cost(Raportowanie.klucz_slowny_optymalnego_kosztu_rozwiazania,
                                plot_title='Koszt optymalnego rozwiazania w danej iteracji')

ShowSolutions.show_routes(x_opt, bin_point_list)

Raportowanie.real_route_from_solution(
    _solution=x_opt,
    cost_matrix=bin_locations,
    rubbish_in_location=rubbish_in_location,
    trucks_max_volumes=trucks_volume,
    xy_points=bin_point_list
)



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
