from typing import List
import random

inf = float('nan')

# lokacja 0 to baza
bin_locations =  [[inf, 3,   6,   8,   10   ],
                 [ 3,   inf, 4,   7,   9    ],
                 [ 6,   4,   inf, 2,   5    ],
                 [ 8,   7,   2,   inf, 1    ],
                 [10,   9,   5,   1,   inf  ],
                 ]


#print(bin_location)

rubbish_in_location = [0, 50, 10, 50, 40,90]   # ilosc smieci od kazdego miasta
                                                # index 0 baza

trucks_volume = [50, 100, 100] # pojemnosci
trucks_filled_volume = [0] * len(trucks_volume)
print(len(list(range(0,5))))

# rozdziel po rowno
# przyjmuje globalne bin_location, garbage_trucks
# zwraca poczatkowe solution
def first_solution( location: List, trucks:List )-> List:
    solution = [0]*len(trucks)
    bins_amount = int((len(location)-1) / len(trucks))
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
    print(solution)
    return solution

# funkcja kosztu dla sollution
def count_cost(solution:List):
    cost = 0
    for num_truck in range (0,len(solution)):
        cost += truck_ride_cost(solution[num_truck],num_truck)
        print(cost)
    return cost

def truck_ride_cost(locations:List,num_truck:int): # zwraca koszt dla jednej śmieciarki
    print(locations)
    ride_cost = bin_locations[0][locations[0]]

    for i in range(0, len(locations)):

        trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]# zaladowanie smieci
        print(trucks_filled_volume)
        if( i+1 >= len(locations)): # jesli ostatni
            ride_cost += bin_locations[locations[i]][0]
            return ride_cost

        if (trucks_volume[num_truck] <= trucks_filled_volume[num_truck] + rubbish_in_location[i + 1]): # wroc do bazy jesli smieciarka pelna
            ride_cost += bin_locations[locations[i]][0]
            ride_cost += bin_locations[0][locations[i+1]]

        else:
            ride_cost += bin_locations[ locations[i] ][ locations[i + 1] ]

    return ride_cost

first_solution(list(range(0,20)),list(range(0,4)))
solution = first_solution(bin_locations, trucks_volume)
count_cost(solution)

## dotad jest ok

# przuklad TABU list
TABU_list = [(1,10),
             (3,2),
             (4,5)
             ]


#tabu search
x = solution
x_opt = solution

for i in range (0,20):
    while(1)# zmieniaj dopoki x jest zabronione
        x = change_solution(x)
        if(check(x))
            break

    if count_cost(x) < count_cost(x_opt):
        x_opt = x

    # dekrementu drugi element krotki = skroc o 1 kadencje
    # Dodaj nowe elementy do listy TABU
    # jesli kadnecja = 0 to usun zabronienie



def check_solution(x:List)->bool:
    return 1

def change_solution(x:List)->List:
    new_solution = []
    return new_solution

def add_to_TABU():
    TABU_list.append((3, 10))
    return None