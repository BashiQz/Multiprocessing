import threading
import time

# Dwie blokady
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1_routine():
    print("Wątek 1: próba uzyskania lock1")
    with lock1:
        print("Wątek 1: uzyskał lock1")
        time.sleep(1)  # Symulacja długotrwałej operacji
        print("Wątek 1: próba uzyskania lock2")
        with lock2:
            print("Wątek 1: uzyskał lock2")

def thread2_routine():
    print("Wątek 2: próba uzyskania lock2")
    with lock2:
        print("Wątek 2: uzyskał lock2")
        time.sleep(1)
        print("Wątek 2: próba uzyskania lock1")
        with lock1:
            print("Wątek 2: uzyskał lock1")

def thread3_routine():
    print("Wątek 3: próba uzyskania lock1")
    with lock1:
        print("Wątek 3: uzyskał lock1")
        time.sleep(1)
        print("Wątek 3: próba uzyskania lock2")
        with lock2:
            print("Wątek 3: uzyskał lock2")
            # Wykonanie operacji po uzyskaniu obu blokad
            print("Wątek 3: wykonuje operację")

def thread4_routine():
    print("Wątek 4: próba uzyskania lock1")
    with lock1:
        print("Wątek 4: uzyskał lock1")
        time.sleep(1)
        print("Wątek 4: próba uzyskania lock2")
        with lock2:
            print("Wątek 4: uzyskał lock2")
            print("Wątek 4: wykonuje operację")

# Aby funkcja się wykonała wymagany jest dostęp do obu blokad. Niestety dzieje się to równocześnie i oba procesy czekają na siebie.
def deadlock():
    # Tworzenie dwóch wątków
    thread1 = threading.Thread(target=thread1_routine)
    thread2 = threading.Thread(target=thread2_routine)

    # Startowanie wątków
    thread1.start()
    thread2.start()

    # Czekanie na zakończenie wątków
    thread1.join()
    thread2.join()

    print("Program zakończył działanie")
# Rozwiązanie problemu poprzez odpowiednią sekwencję odwołania do blokad.
def nodeadlock():
    thread1 = threading.Thread(target=thread3_routine)
    thread2 = threading.Thread(target=thread4_routine)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Program zakończył działanie")
    
# Wywołanie deadlock nie pozwoli na wykonanie programu   
#deadlock()
nodeadlock()