from typing import List
from copy import deepcopy
import random  # Testowanie
inf = float('nan')
M = [[inf, 4, 5, 6, inf, 8, 9],
     [],
     [],
     [],
     []]


helper = deepcopy(M[0])  # Usuniecie inf z tablicy pomocniczej (funkcje min/max maja z tym problem, gdy stoi na poczatku)

print(helper.count(inf))
print(helper.index(inf))
# helper.pop(helper.index(inf))
print(helper)
print(helper.index(inf))
to_del = []
for i in range(len(helper), 0):
    if helper[i] is inf:
        to_del.append(i)
for i in to_del:
    helper.pop(i)

_min_cost = max(helper)  # Znalezienie najwiekszej wartosci w tej liscie
print(_min_cost)
print(helper)