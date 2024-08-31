import multiprocessing

# Funkcja zwiększająca licznik
def increment_counter(shared_counter, iterations):
    for _ in range(iterations):
        shared_counter.value += 1
        
# Funkcja zwiększająca licznik z blokadą
def increment_counter_lock(shared_counter, lock, iterations):
    for _ in range(iterations):
        with lock:
            shared_counter.value += 1



if __name__ == '__main__':
    # Współdzielona zmienna
    shared_counter = multiprocessing.Value('i', 0)

    # Liczba iteracji dla każdego procesu, używana w obu wersjach programu
    ITERATIONS = 100000
    
    # Tworzenie dwóch procesów
    process1 = multiprocessing.Process(target=increment_counter, args=(shared_counter, ITERATIONS))
    process2 = multiprocessing.Process(target=increment_counter, args=(shared_counter, ITERATIONS))

    # Startowanie procesów
    process1.start()
    process2.start()

    # Czekanie na zakończenie procesów
    process1.join()
    process2.join()
    
    print(f'Końcowa wartość licznika bez blokady: {shared_counter.value}')
    
    # Zerowanie licznika dla wersji z blokadą
    shared_counter = multiprocessing.Value('i', 0)
    
    # Blokada
    lock = multiprocessing.Lock()

    # Tworzenie dwóch procesów
    process3 = multiprocessing.Process(target=increment_counter_lock, args=(shared_counter, lock, ITERATIONS))
    process4 = multiprocessing.Process(target=increment_counter_lock, args=(shared_counter, lock, ITERATIONS))

    # Startowanie procesów
    process3.start()
    process4.start()

    # Czekanie na zakończenie procesów
    process3.join()
    process4.join()

    print(f'Końcowa wartość licznika z blokadą: {shared_counter.value}')