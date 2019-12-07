from typing import List, Dict, Tuple
import random
import statistics
from copy import deepcopy
import MatrixSegregation
import ShowSolutions

inf = float('nan')
inf = -1

# lokacja 0 to baza
bin_locations = [[inf, 3,   6,   8,  10,  15,  20, 21],
                 [3,   inf, 4,   7,   9,  11,  16, 17],
                 [6,   4, inf,   2,   5,   9,  10, 11],
                 [8,   7,   2, inf,   1,   5,   8,  9],
                 [10,  9,   5,   1, inf,   7,   6,  7],
                 [15,  11,  9,   5,   7, inf,   4,  5],
                 [20,  16, 10,   8,   6,   4, inf,  5],
                 [21,  17, 11,   9,   7,   5,   5, inf]
                 ]

bin_locations, bin_point_list = MatrixSegregation.make_cost_matrix(14, 3)  # 7 punktow, 3 smieciarki

rubbish_in_location = [0, 40, 30, 30, 50, 90, 60, 50]*2  # ilosc smieci od kazdego miasta
                                                        # index 0 baza
trucks_volume = [50, 100,60]  # pojemnosci
# koniec danych wejsciowych

trucks_filled_volume = [0] * len(trucks_volume)
trucks_returns = [0] * len(trucks_volume)


def first_solution(location: List, trucks: List) -> List:  # rozdziel po rowno
    solution = [0] * len(trucks)  # przyjmuje globalne bin_location, garbage_trucks
    bins_amount = int((len(location) - 1) / len(trucks))  # zwraca poczatkowe solution
    rest = (len(location) - 1) % len(trucks)
    _from = 1
    _to = 1
    for i in range(0, len(trucks)):
        _to += bins_amount
        if rest != 0:
            _to += 1
            rest -= 1
        solution[i] = list(range(_from, _to))
        _from = _to
    # print(solution)
    return solution

def count_cost(solution: List):  # funkcja kosztu dla sollution
    cost = 0
    for num_truck in range(0, len(solution)):
        cost += truck_ride_cost(solution[num_truck], num_truck)
        #print("koszt przejazdu", cost)
    return cost

def truck_ride_cost(locations: List, num_truck: int):  # zwraca koszt dla jednej śmieciarki
    # print(locations)
    trucks_returns[num_truck] = 0
    ride_cost = bin_locations[0][locations[0]]  # od bazy 0 do pierwszego na liscie

    for i in range(0, len(locations)):
        trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]  # zaladowanie smieci
        #print(trucks_filled_volume)
        if (i + 1 >= len(locations)):  # jesli ostatni
            ride_cost += bin_locations[locations[i]][0]
            return ride_cost

        #print("pojemnosc smieciarki", i,":", trucks_volume[num_truck])
        #print("pojemnosc zajeta smieciarki", i,":", trucks_filled_volume[num_truck])
        #print("ilosc smieci w nastepnej lokacji",rubbish_in_location[locations[i+1]])

        if (trucks_volume[num_truck] < trucks_filled_volume[num_truck] + rubbish_in_location[locations[i+1]]):  # wroc do bazy jesli smieciarka pelna
            ride_cost += bin_locations[locations[i]][0]
            trucks_filled_volume[num_truck]=0
            ride_cost += bin_locations[0][locations[i + 1]]
            trucks_returns[num_truck] = trucks_returns[num_truck] + 1
            #print("powrot")

        else:
            ride_cost += bin_locations[locations[i]][locations[i + 1]]

    return ride_cost


# rozwiazanie = first_solution(list(range(0,6)),list(range(0,3)))

solution = first_solution(bin_locations, trucks_volume)
#print(solution)
cost = count_cost(solution)
#print(cost)

#### END OF PART TWO ####


#### PART THREE ####
'''######LISTA TABU#########
# {typ_zabronienia1:[ konkretne zabronienia ], typ_zabronienia2: [ konkretne zabronienia ] itd.
# typ1 (i,n)zakaz zmiany i tego kosza na n iteracji
# typ2 (i,j,n) elementu i, j nie moga byc koło siebie przez n iteracji
# typ3 (i,j,n) i-ty kosz nie w j-tej smieciarce przez n kadencji
#...
'''
#TABU = {1: [[1, 10], [3, 2], [4, 5]], 2: [[1, 2, 3], [3, 5, 6]], 3: [[3,0,10], [2,1,15],[5,2,12]]}
TABU = {1:[], 2:[],3:[]}


def add_to_TABU(TABU: Dict, new_TABU: List,type: int) -> Dict:  # jako argument ogonie TABU, nowe pojedyncze zabronienie i jego typ(patrz komentarz wyzej)
    #mozna zaimplementować blokowanie dopisywania tych samych list
    TABU[type].append(new_TABU)
    return TABU

def print_TABU(TABU: Dict):
    for type in TABU:
        print(type, '->', TABU[type])


''' Funkcje zmieniajace rozwiazanie:
    ch - change + w jaki sposob
#1)
'''
def ch_returns(solution: List) -> List:
    new_solution = deepcopy(solution)
    truck_max=trucks_returns.index(max(trucks_returns)) # zwraca ktora smieciarka wykonala najwiecej powrotow
    truck_min= trucks_returns.index(min(trucks_returns))  # zwraca ktora smieciarka wykonala najmniej powrotow

    #sprawdz czy kosz ktory funkcja chce zmienic nie jest w TABU
    if check_ban_t1(new_solution[truck_max][-1]):
        new_solution[truck_min].append(new_solution[truck_max][-1])
        del(new_solution[truck_max][-1])

        # Sprawdzanie czy nowe rozwiazanie jest dozwolone
        if check_ban_t2(new_solution) and check_ban_t3(new_solution):
            return new_solution
    return solution

def ch_swap(solution: List) -> List:
    new_solution = deepcopy(solution)
    for route in new_solution:
        if(len(route)>=2):
            pair = random.sample(range(0,len(route)), 2)
            route[pair[0]],route[pair[1]]=route[pair[1]],route[pair[0]]
    return new_solution

def ch_truck(solution: List) -> List:   #zamien smieciarki jesli ta o mniejszej pojemnosci wykonala wiecej powrotow
    new_solution = deepcopy(solution)
    truck_max = trucks_returns.index(max(trucks_returns))   # zwraca ktora smieciarka wykonala najwiecej powrotow
    truck_min = trucks_returns.index(min(trucks_returns))    # zwraca ktora smieciarka wykonala najmniej powrotow
    if trucks_volume[truck_max] < trucks_volume[truck_min]:
        new_solution[truck_max],new_solution[truck_min] = new_solution[truck_min],new_solution[truck_max]
    return new_solution

print(solution)
ch_swap(solution)
print("koniec")

#print(solution)
#print(trucks_returns)
#ch_swap(solution)
#print(solution)

''' Funkcjie zabraniajace:
    ban - zabron rozwiazaie
1) policz max przejazd dla smieciarki i zabron go
'''

def ban_max(solution: List):
    for route in solution:
        if (len(route) > 2):
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

def ban_max2(solution: List): # zabronic najdalszy przejazd
    max_p2p_for_truck = [] #maksymalny przejazd dla kazdej smieciarki
    max_p2p_for_truck_value = [] #i jego wartość
    p2p_values = []
    for route in solution:
        if len(route) > 2:
            for i in range(len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
                # print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            max_p2p_for_truck.append([od,do])
            max_p2p_for_truck_value.append(bin_locations[od][do])

        elif len(route) == 2:
            max_p2p_for_truck.append([route[0], route[1]])
            max_p2p_for_truck_value.append(bin_locations[route[0]][route[1]])

    index_of_max = max_p2p_for_truck_value.index(max(max_p2p_for_truck_value)) #zwroci index najdluzzego przejazdu
    [od, do] = max_p2p_for_truck[index_of_max]
    #print(od,do)

    tabu_iteration = 10
    add_to_TABU(TABU, [od, do, tabu_iteration], 2)

def ban_max3(solution: List):
    print(max(solution))


'''Sprawdz czy nie zabronione
    dla danego rozwiazania, sprawdz czy TABU nie zabrania
'''
#jesli funkcja chce zmienic i ty kosz to zwroc False
def check_ban_t1(point:int)-> bool:
    banned_points = []
    for pair in TABU[1]:
        banned_points.append(pair[0])
    if point in banned_points:
        return False
    else:
        return True

#jesli w nowym rozwiazaniu kosze z Tabu sa obok siebie zroci False
def check_ban_t2(solution: List) -> bool:
    for triple in TABU[2]:
        pos_point1 = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        pos_point2 = [(index, row.index(triple[1])) for index, row in enumerate(solution) if triple[1] in row]

        #print(pos_point1[0], pos_point2[0])
        if pos_point1[0][0] == pos_point2[0][0]: #jesli w tej samej śmieciarce
            if abs(pos_point1[0][1] - pos_point2[0][1]) == 1: #jeśli sa obok siebie
                return False
    return True

#jesli w nowym rozwiazaniu kosz jesz w zabronionej smieciarce zwroc False
def check_ban_t3(solution: List) -> bool:
    #print(TABU[3])
    for triple in TABU[3]:
        pos_point = [(index, row.index(triple[0])) for index, row in enumerate(solution) if triple[0] in row]
        if pos_point[0][0] == triple[1]:    #czy kosz jest w zabronionej smieciarce
            return False
    return True



#### END OF PART THREE ####

#### TABU SEARCH ####
x = deepcopy(solution)
x_opt = deepcopy(solution)
solution_change = True  # Po to aby pokazac pierwsza opcje
#ShowSolutions.show_routes(x_opt, bin_point_list)
for i in range(0, 1000):
    #if (i < 5):

    # w kazdej funckj change sprawdzamy czy ruch dozwolony
    # plus uwzględnienie aspiracji
    '''zmien rozwiazanie'''

    change_probability = random.randint(1, 100)
    if(change_probability in (1, 20)):
        x = ch_returns(x_opt)
    elif(change_probability in (20, 50)):
        x = ch_swap(x_opt)
    elif change_probability in (50, 70):
        x = ch_truck(x_opt)
    elif change_probability in (70, 100):
        pass


    if count_cost(x) < count_cost(x_opt):
        print(x_opt, " -> ",count_cost(x))
        x_opt = deepcopy(x)
        solution_change = True

    '''skroc o 1 kadencje'''
    for type in TABU:
        for single_tabu in TABU[type]:
            if (len(single_tabu) == 0 or single_tabu[-1] == 1):  # jesli kadencja = 0 to usun zabronienie
                TABU[type].remove(single_tabu)
            else:
                single_tabu[-1] = single_tabu[-1] - 1

    '''Dodaj nowe elementy do listy TABU'''

    tabu_probability = random.randint(1, 100)
    if tabu_probability in (1,10):
        ban_max(x_opt)
    elif tabu_probability in (20,30):
         pass
    elif tabu_probability in (40, 50):
        pass
    elif tabu_probability in (50, 100):
        pass


    '''przedstawianie wyniku'''
    if solution_change:
        ShowSolutions.show_routes(x_opt, bin_point_list)
        solution_change = False

'''
#srednoirweminowa sprawdz rozwiazania zanim zapisesz do pamieci
#rozwiazania podobne nie zapisujemy na liscie
# zapisać np 5 na roznych górkach

#długotermiowa
#smieciarki kosze ile razy dany kosz był w śmieciarce
#gromadzenie wiedzy
#jeśi nie poprawi to nie opłaca się korzystać
#np możana klika pomysłów, potem sprawdzić który lepszy
'''