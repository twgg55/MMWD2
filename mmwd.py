from typing import List

inf = float('nan')

bin_location = [ [ inf, 3,   6,   8,   10   ],
                 [ 3,   inf, 5,   7,   9    ],
                 [ 6,   4,   inf, 2,   5    ],
                 [ 8,   5,  2,    inf, 1    ],
                 [10,   9,  5,    1,   inf  ],
                 ]

print(bin_location)

rubbish_amount = [ 20, 30, 50, 60,15]   # ilosc smieci od kazdego miasta

garbage_trucks = [50, 100, 100] # pojemnosci

def first_sollotion( location: List, trucks:List ):
    for truckin in trucks:
        print(" D")
    return 0