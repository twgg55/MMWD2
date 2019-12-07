# Tomasz Molęda

import MatrixSegregation
import ShowSolutions
import time
import matplotlib.pyplot as plt


x = False
if x:
    Punkty = [(0, 0), (44, 8), (56, 66), (43, 99), (11, 40), (15, 42), (1, 10)]
    Trasy = [[0, 1, 2, 5, 6, 0],
             [0, 3, 4, 0]]

    ShowSolutions.show_routes(Trasy, Punkty, separate_plots=True, arrow=True)

# Wszystko ponizej dotyczy MatrixSegregation
x = True
if x:
    #Parametry symulacji
    Wykonac_MatrixSegregation = False
    czy_pokazac_wykresy = False
    czy_pokazac_macierze_w_konsoli = False
    min_value = -500
    max_value = 500
    ilosc_punktow = 100

    punkty = MatrixSegregation.random_2dim_points(ilosc_punktow, max_value, min_value)
    # print(punkty)
    macierz_przed = MatrixSegregation.create_cost_matrix(punkty)

    plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r', marker='.')

    macierz_kosztow, kolejnosc = MatrixSegregation.sort_matrix_areas(macierz_przed, punkty, 10, 0, 0, list_of_lists=False)
    ShowSolutions.show_routes([kolejnosc], punkty, separate_plots=False, arrow=True)



    print(kolejnosc) ##################################
    # print_matrix(macierz_przed)


x = False
if x:
    # Stworzenie macierzy
    print("Parametry symulacji:")
    print("Ilosc_punktow: " + str(ilosc_punktow))
    print("Najmniejsza wartość wspolrzednych dla punktow: " + str(min_value))
    print("Najwieksza wartość wspolrzednych dla punktow: " + str(max_value))

    print("\nRozpoczecie symulacji:")
    start = time.time()
    punkty = MatrixSegregation.random_2dim_points(ilosc_punktow, max_value, min_value)
    czas_losowania = time.time() - start
    print("Losowanie punktow zajelo: " + str(czas_losowania) + " sekund")
    macierz_przed = MatrixSegregation.create_cost_matrix(punkty)
    print("Stworzenie macierzy kosztow zajelo: " + str(time.time() - start - czas_losowania) + " sekund")
    koszt_przed = MatrixSegregation.cost(macierz_przed)

    # Sposob nr 1
    czas_sortowania_f1 = time.time()
    macierz_po, odwiedzone = MatrixSegregation.sort_matrix_by_distance(macierz_przed)
    czas_sortowania_f1 = time.time() - czas_sortowania_f1
    print("\nCzas sortowania dla F1: " + str(czas_sortowania_f1) + " sekund")
    koszt_po = MatrixSegregation.cost(macierz_po)
    roznica = koszt_przed - koszt_po
    print("Poprawa o: " + str(roznica) + ", czyli o " + str(round(roznica*100/koszt_przed)) + "%.")

    #Sposob nr 2
    czas_sortowania_f2 = time.time()
    macierz_po_od_0_0, odwiedzone_0_0 = MatrixSegregation.sort_matrix_by_distance(macierz_przed, 0)
    czas_sortowania_f2 = time.time() - czas_sortowania_f2
    print("\nCzas sortowania dla F2: " + str(czas_sortowania_f2) + " sekund")
    koszt_po = MatrixSegregation.cost(macierz_po_od_0_0)
    roznica = koszt_przed - koszt_po
    print("Poprawa o: " + str(roznica) + ", czyli o " + str(round(roznica*100/koszt_przed)) + "%.")

    if czy_pokazac_wykresy:
        #print("Lista punktow (x,y), ktore sa docelowymi lokalizacjami")
        print(punkty)
        print(MatrixSegregation.sort_points_list(punkty, odwiedzone_0_0))
        if czy_pokazac_macierze_w_konsoli:
            print("Macierz wylosowana: ")
            MatrixSegregation.print_matrix(macierz_przed)
            print("\n\n")
            print("Macierz posortowana F1 (od najkrotszego polaczenia): ")
            MatrixSegregation.print_matrix(macierz_po)
            print("\n\n")
            print("Macierz posortowana F2 (od bazy): ")
            MatrixSegregation.print_matrix(macierz_po_od_0_0)
            print("\n\n")

        # Parametry wyswietlania wykresow
        y_min = min_value - 1
        y_max = max_value + 1
        x_min = min_value - 1
        x_max = max_value + 1

        plt.subplot(2, 2, 1)
        plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r', marker='.')
        plt.xlabel('Wylosowane punkty')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid()

        plt.subplot(2, 2, 2)
        plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
        plt.plot([i[0] for i in punkty], [i[1] for i in punkty])
        plt.plot([i[0] for i in punkty[0:2]], [i[1] for i in punkty[0:2]], c='r')
        plt.xlabel('Losowa kolejnosc')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid()

        plt.subplot(2, 2, 3)
        plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
        plt.plot([punkty[i][0] for i in odwiedzone], [punkty[i][1] for i in odwiedzone])
        plt.plot([punkty[i][0] for i in odwiedzone[0:2]], [punkty[i][1] for i in odwiedzone[0:2]], c='r')
        plt.xlabel('F1: Start od najkrotszego polaczenia w calej macierzy')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid()

        plt.subplot(2, 2, 4)
        plt.scatter([i[0] for i in punkty], [i[1] for i in punkty], c='r')
        plt.plot([punkty[i][0] for i in odwiedzone_0_0], [punkty[i][1] for i in odwiedzone_0_0])
        plt.plot([punkty[i][0] for i in odwiedzone_0_0[0:2]], [punkty[i][1] for i in odwiedzone_0_0[0:2]], c='r')
        plt.xlabel('F2: Start od bazy do najblizszego punktu')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.grid()
        plt.show()