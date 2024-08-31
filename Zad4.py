import math as m
import random as rand
import numpy as np
import threading
import time
import queue
xp = []
buffer = []
results_queue = queue.Queue()
"""
Przerobiony program do algorytmu genetycznego ważonego.
Multiprocessing dodany w funkcji rodzice (turniej rycerski) i mutacja, cyli do przygotowania populacji do wytwarzania potomków. Nie miałem okacji dodać warunku, bu program tego nie wymagał.
Program generuje plik hist.txt!
"""
def popinit(xp, lch, lg):
    xp = np.random.randint(2, size=(lch, lg + 1))
    xp[:, 0] = 0
    wag1 = [15,2,2,3,15,1,4,5,6]  
    wag = np.zeros(lg+1)
    wag[:lg+1] = wag1[:lg+1]
    wart1 = [40,160,70,300,70,25,25,180]
    wart = np.zeros(lg)
    wart[:lg] = wart1[:lg]
    print(wart)
    print(wag)
    return xp, wag, wart

def ocena(xp, wag, wart):
    ceny = np.multiply(wart, xp[:, 1:])
    xp[:, 0] = np.sum(ceny, axis=1)
    waga = np.zeros((lch+1, 1))
    for i in range(1, lg + 1):
        waga[1:, 0] += xp[:, i] * wag[i]
    waga[0,0] = wag[0]
    return xp, waga

def historia (xp,waga):
    fp = xp[:, 0]
    max_fp = np.max(fp)
    min_fp = np.min(fp)
    sr_fp = np.mean(fp)
    
    
    max_waga = waga[0, 0]
    max_dfp = 0
    
    for i in range(len(xp)):
        chrom = xp[i]
        wagac = waga[(i+1)]
        if wagac<=max_waga:
            if chrom[0] > max_dfp:
                max_dfp = chrom[0]
                winnerh=chrom
                w_nr = i
                wagah = wagac
    with open('hist.txt', 'a') as file:
        file.write(f"MAX {max_fp:<4}\t MIN {min_fp:<5} \t srednia {sr_fp:<5}\t Najlepszy chromosom ma wage {wagah}\t watosc {max_dfp}\t postac {winnerh[1:]} i pozycje w xp nr {w_nr}\n")
    return winnerh, wagah   
#t1
def rodzice(xp, waga):
    max_waga = waga[0, 0]
    for _ in range(len(xp)):  
        ind1, ind2 = np.random.choice(range(1, len(waga)), 2, replace=False)
        chrom1, chrom2 = xp[ind1 - 1], xp[ind2 - 1]
        waga1, waga2 = waga[ind1], waga[ind2]
        empty_slots.acquire()
        
        with buffer_lock:
            if waga1 > max_waga and waga2 > max_waga:
                winner = chrom1 if waga1 < waga2 else chrom2
            elif waga1 <= max_waga and waga2 > max_waga:
                winner = chrom1
            elif waga1 > max_waga and waga2 <= max_waga:
                winner = chrom2
            else:  
                winner = chrom1 if chrom1[0] > chrom2[0] else chrom2
            buffer.append(winner[1:])
            print(f"Dodano do semafora: {winner[1:]}")
        full_slots.release()
        time.sleep(rand.random()/10)
#t2
def mutacja(buffer, pm,lch,lg):
    nrxp1 = []
    for _ in range(lch):
        full_slots.acquire()
        with buffer_lock:
            for j in range(lg):
                r = rand.random()
                if r < pm:
                    buffer[0][j] = 1 - buffer[0][j]  # Flip the bit
            item = buffer.pop(0)
            nrxp1.append(item)
            print(f"Usunięto z semafora: {item}")
        empty_slots.release()
        time.sleep(rand.random()/5)
    result = np.array(nrxp1)
    results_queue.put(result)

def potomek(nrxp1, pk,lch,lg):
    parent_pool = list(range(nrxp1.shape[0]))
    offspring = []

    while parent_pool:
        if len(parent_pool) == 1:
            offspring.append(nrxp1[parent_pool[0]])
            break

        ind1, ind2 = rand.sample(parent_pool, 2)
        parent1, parent2 = nrxp1[ind1], nrxp1[ind2]

        r = rand.random()
        if r < pk:
            crossover_point = rand.randint(1, nrxp1.shape[1] - 2)
            child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
            offspring.append(child1)
            offspring.append(child2)
            parent_pool.remove(ind1)
            parent_pool.remove(ind2)

    offspring = np.array(offspring)
    xp = np.zeros((lch, lg + 1))
    xp[:, 0] = 0
    xp[:, 1:] = offspring
    
    return xp
def fwynik (Wynik,waga1):
    order = np.arange(0, Wynik.shape[0]).reshape(-1, 1)
    Wynik1 = np.hstack((order, Wynik))
    sorted_wynik = np.argsort(-Wynik1[:, 1].astype(int))
    sorted_data = Wynik1[sorted_wynik]
    index = int(sorted_data[0, 0])
    wagac = waga1[index]
    with open('hist.txt', 'a') as file:
        file.write(f"Najlepszy chromosom ma wage = {wagac}, wartosc przystosowania = {sorted_data[0,1]} i postac: {sorted_data[0,2:]}")

def Main (xp,lg,lch,lpop,pm,pk):
    Wynik=[]
    waga1=[]
    with open('hist.txt', 'w') as file:
        pass
    xp,wag,wart = popinit(xp,lch,lg)
    for i in range(lpop):
        xp, waga = ocena(xp,wag,wart)
        winnerh, wagah = historia(xp,waga)
        Wynik.append(winnerh)
        waga1.append(wagah)
        #
        #
        #
        # Wywołanie
        t1 = threading.Thread(target=rodzice, args=(xp,waga))
        t2 = threading.Thread(target=mutacja, args=(buffer,pm,lch,lg))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        nrxp1=np.array(results)
        print(nrxp1)
        xp = potomek(nrxp1,pk,lch,lg)
        print("nr pokolenia",i+1)
    xp, waga = ocena(xp,wag,wart)
    Wynik = np.array(Wynik)
    waga1 = np.array(waga1)
    fwynik(Wynik,waga1)   



    
# liczba genów w chromosomie (max. 10)
lg = int(input("Podaj liczbę genów w chromosomie (max. 10): "))
# liczba chromosomów w populacji (max. 50)
lch = int(input("Podaj liczbę chromosomów w populacji (max. 50): "))
lpop = int(input("liczba pokoleń (max. 500)[Proponuję max 20, bo sztuczne opóźnienie sprawia, że to trochę trwa]: "))
pm = float(input("prawdopodobieństwo zajścia mutacji (0 - 0.1)"))
pk = float(input("prawdopodobnieństwo zajścia krzyżowania (0.6 - 1.0)"))
BUFFER_SIZE = int(input("Podaj rozmiar buffora (semafora) (max. 10): "))
buffer_lock = threading.Lock()
empty_slots = threading.Semaphore(BUFFER_SIZE)
full_slots = threading.Semaphore(0)
Main(xp,lg,lch,lpop,pm,pk)