from typing import List, Dict, Tuple
import random
import statistics

inf = float('nan')

# lokacja 0 to baza
bin_locations =  [[inf, 3,   6,   8,   10,  15,   20,   21],
                 [ 3,   inf, 4,   7,   9 ,  11,   16,   17],
                 [ 6,   4,   inf, 2,   5,   9,    10,   11],
                 [ 8,   7,   2,   inf, 1,    5,    8,    9],
                 [10,   9,   5,   1,   inf,  3,    6,    7],
                 [15,   11,  9,   5,   3,   inf,   4,    5],
                 [20,   16, 10,   8,   6,    4,  inf,    5],
                 [21,   17, 11,   9,   7,    5,     5,   inf]
                 ]




rubbish_in_location = [20, 20, 10, 50, 40, 90]   # ilosc smieci od kazdego miasta
                                                 # index 0 baza
trucks_volume = [50, 100,100] # pojemnosci
# koniec danych wejsciowych

trucks_filled_volume = [0] * len(trucks_volume)
trucks_returns = [0] * len(trucks_volume)

def first_solution( location: List, trucks:List )-> List:   # rozdziel po rowno
    solution = [0]*len(trucks)                              # przyjmuje globalne bin_location, garbage_trucks
    bins_amount = int((len(location)-1) / len(trucks))      # zwraca poczatkowe solution
    rest = (len(location)-1) % len(trucks)
    _from = 1
    _to = 1
    for i in range(0, len(trucks)):
        _to += bins_amount
        if rest != 0:
            _to +=1
            rest -= 1
        solution[i] = list(range(_from,_to))
        _from = _to
    #print(solution)
    return solution
def count_cost(solution:List):      # funkcja kosztu dla sollution
    cost = 0
    for num_truck in range (0,len(solution)-1):
        cost += truck_ride_cost(solution[num_truck],num_truck)
        #print(cost)
    return cost
def truck_ride_cost(locations:List,num_truck:int): # zwraca koszt dla jednej śmieciarki
    #print(locations)
    ride_cost = bin_locations[0][locations[0]] # od bazy 0 do pierwszego na liscie

    for i in range(0, len(locations)):
        trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]# zaladowanie smieci
        #print(trucks_filled_volume)
        if( i+1 >= len(locations)): # jesli ostatni
            ride_cost += bin_locations[locations[i]][0]
            return ride_cost

        if (trucks_volume[num_truck] <= trucks_filled_volume[num_truck] + rubbish_in_location[i + 1]): # wroc do bazy jesli smieciarka pelna
            ride_cost += bin_locations[locations[i]][0]
            ride_cost += bin_locations[0][locations[i+1]]
            trucks_returns[num_truck]=trucks_returns[num_truck]+1

        else:
            ride_cost += bin_locations[ locations[i] ][ locations[i + 1] ]

    return ride_cost

#rozwiazanie = first_solution(list(range(0,6)),list(range(0,3)))
solution = first_solution(bin_locations, trucks_volume)
print(solution)
print(count_cost(solution))

#### END OF PART TWO ####


#### PART THREE ####
'''######LISTA TABU#########
# {typ_zabronienia1:[ konkretne zabronienia ], typ_zabronienia2: [ konkretne zabronienia ] itd.
# typ1 (i,n)zakaz zmiany i tego kosza na n iteracji
# typ2 (i,j,n) elementu i, j nie moga byc koło siebie przez n iteracji
# typ3 (i,j,n) i-ty kosz nie w j-tej smieciarce przez n kadencji
#...
'''
# Wymyslic na jakiej podstawie ma blokowac
TABU = {1:[[1,10],[3,2],[4,5]], 2:[[1,2,3],[3,5,6]], 3:[[],[]]}
#TABU = {1:[], 2:[],3:[]}
#chyba najlepiej blokować w funkcji wybierajacej nowe rozwiazanie


def add_to_TABU(TABU:Dict,new_TABU:List,type:int)->Dict:  #jako argument ogonle TABU, nowe pojedyncze zabronienie i jego typ(patrz komentarz wyzej)
    TABU[type].append(new_TABU)
    return TABU

def print_TABU(TABU:Dict):
    for type in TABU:
        print(type, '->', TABU[type])


''' Funkcje zmieniajace rozwiazanie:
    ch - change + w jaki sposob
#1)
'''
def ch_returns(solution:List)->List:
    new_solution = []


    return new_solution

''' Funkcjie zabraniajace:
    ban - zabron rozwiazaie
1) policz max przejazd dla smieciarki i zabron go
'''
def ban_max(solution:List)->List:
    new_solution = []

    for route in solution:
        if (len(route)>2):
            p2p_values = []
            for i in range(len(route) - 1):
                p2p_values.append(bin_locations[route[i]][route[i + 1]])
                # print(p2p_values)

            od = route[p2p_values.index(max(p2p_values))]
            do = route[p2p_values.index(max(p2p_values)) + 1]
            #print(od, do)
            #print(p2p_values.index(max(p2p_values)))

            tabu_iteration = 5 #mozna wybrac na ile iteracji
            # zabroń i zmień(opcjonalnie)
            add_to_TABU(TABU, [od, do, tabu_iteration], 2)  # zabron


    return new_solution

'''Sprawdz czy nie zabronione
    dla danego rozwiazania, sprawdz czy TABU nie zabrania
'''
def check_ban(solution:List)->bool:
    for type in TABU:
        #print(type, TABU[type])
        if(type==1):
            pass
        elif (type==2):
            for single_tabu in TABU[type]:
                print(single_tabu[0])
        elif (type == 3):
            pass

    return True


''' ALE!!!
#lepiej sprawdzać przy wyborze nowego rozwiązania, a nie po !!!!
def check_new_solution(solution:List,new_solution:List,TABU:Dict)->bool:
    for type, T_list in TABU.items():
        if(type == 1):
            
            if( solution[] != new_solution[]:
                return False
                
#znqjdz w jedym, sprawdz czy jest na tym miejscu w 2. solution

        print( T_list) 

    return 1
#check_new_solution([],TABU)'''

#### END OF PART THREE ####

#tabu search
x = solution
x_opt = solution
for i in range (0,20):
#    x = change_solution(x)  # w kazdej funckj change sprawdzamy czy ruch dozwolony
                             # plus uwzględnienie aspiracji

    if count_cost(x) < count_cost(x_opt):
        x_opt = x


    '''skroc o 1 kadencje'''
    for type in TABU:
        for single_tabu in TABU[type]:
            #print(" A", single_tabu)

            if(len(single_tabu)==0 or single_tabu[-1]==1):# jesli kadencja = 0 to usun zabronienie
                TABU[type].remove(single_tabu)
            else:
                single_tabu[-1]=single_tabu[-1]-1

    '''Dodaj nowe elementy do listy TABU'''
    #ban_max(x_opt)
    print(TABU)





'''
#srednoirweminowa sprawdz rozwizazania zanim zapisesz do pamieci
#rozwiazania podobne nie zapisujemy na liscie
# zapisać np 5 na roznych górkach

#długotermiowa
#smieciarki kosze ile razy dany kosz był w śmieciarce
#gromadzenie wiedzy
#jeśi nie poprawi to nie opłaca się korzystać
#np możana klika pomysłów, potem sprawdzić który lepszy
'''
