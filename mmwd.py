from typing import List

inf = float('nan')

# lokacja 0 to baza
bin_locations =  [[inf, 3,   6,   8,   10   ],
                 [ 3,   inf, 4,   7,   9    ],
                 [ 6,   4,   inf, 2,   5    ],
                 [ 8,   7,   2,   inf, 1    ],
                 [10,   9,   5,   1,   inf  ],
                 ]


#print(bin_location)

rubbish_in_location = [ 1, 1, 1, 1,1]   # ilosc smieci od kazdego miasta

trucks_volume = [50, 100, 100] # pojemnosci
trucks_filled_volume = [0] * len(trucks_volume)
print(len(list(range(0,5))))

# rozdziel po rowno
# przyjmuje globalne bin_location, garbage_trucks
# zwraca poczatkowe sollution
def first_sollotion( location: List, trucks:List )-> List:
    sollution = [0]*len(trucks)
    bins_amount = int((len(location)-1) / len(trucks))
    rest = (len(location)-1) % len(trucks)
    _from = 1
    _to = 1
    for i in range(0, len(trucks)):
        _to += bins_amount
        if rest != 0:
            _to +=1
            rest -= 1
        sollution[i] = list(range(_from,_to))
        _from = _to

    print(sollution)
    return sollution

# funkcja kosztu dla sollution
def count_cost(sollution:List):
    cost = 0
    for num_truck in range (0,len(sollution)):  #-1
        #print(sollution[num_truck])
        cost += truck_ride_cost(sollution[num_truck],num_truck)
        #print(cost)

    return cost

def truck_ride_cost(locations:List,num_truck:int): # zwraca koszt dla jednej śmieciarki
    print(locations)
    ride_cost = bin_locations[0][locations[0]]

    for i in range(0, len(locations)):
        print("cost ", ride_cost)
        #trucks_filled_volume[num_truck] += rubbish_in_location[locations[i]]# zaladowanie smieci
        if( i+1 >= len(locations)): # jesli ostatni
            ride_cost += bin_locations[locations[i]][0]
            print("if",ride_cost)
            return ride_cost

        if (trucks_volume[num_truck] < trucks_filled_volume[num_truck] + rubbish_in_location[i + 1]): # wroc do bazy jesli smieciarka pelna
            ride_cost += bin_locations[i][0]
            return ride_cost

        else:
            ride_cost += bin_locations[ locations[i] ][ locations[i + 1] ]

    return ride_cost

#sollution = first_sollotion(list(range(0,20)),list(range(0,6)))
sollution = first_sollotion(bin_locations,trucks_volume )
count_cost(sollution)
