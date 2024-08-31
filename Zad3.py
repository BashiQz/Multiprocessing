import threading
import time
import random as rand

# Ustawienia
BUFFER_SIZE = 5  # Pojemność bufora
NUM_PRODUCERS = 4  # Liczba producentów
NUM_CONSUMERS = 4  # Liczba konsumentów
NUM_ITEMS = 50  # Liczba elementów do wyprodukowania i skonsumowania

# Bufor
buffer = []  # Bufor do przechowywania elementów
buffer_lock = threading.Lock()  # Mutex do ochrony dostępu do bufora
buffer_condition = threading.Condition(buffer_lock)  # Zmienna warunkowa do synchronizacji dostępu do bufora

producers_done = threading.Event()  # Flaga sygnalizująca zakończenie pracy producentów. Program z zamkami nie chciał się zakończyć, więc byłem zmuszony zmienić podejście

def producer(producer_id):
    for _ in range(NUM_ITEMS // NUM_PRODUCERS):
        item = rand.randint(1, 100)  # Generowanie losowego elementu
        consumer_id = rand.randint(0, NUM_CONSUMERS - 1)  # Wybór losowego konsumenta
        
        with buffer_condition:  # Wejście do sekcji krytycznej z użyciem Condition, wcześniej with lock
            while len(buffer) >= BUFFER_SIZE:
                buffer_condition.wait()  # Czekaj, jeśli bufor jest pełny
            
            buffer.append((consumer_id, item))  # Dodanie elementu do bufora z identyfikatorem konsumenta
            print(f"Producent {producer_id} wyprodukował {item} dla konsumenta {consumer_id}")
            buffer_condition.notify_all()  # Powiadom wszystkich konsumentów, że pojawił się nowy element w buforze
        
        time.sleep(rand.random() / 10)  # Symulacja czasu produkcji
    
    with buffer_condition:
        if producers_done.is_set() is False:
            producers_done.set()
            buffer_condition.notify_all()  # Powiadom wszystkich konsumentów, że produkcja została zakończona

def consumer(consumer_id):
    while True:
        with buffer_condition:  
            while len(buffer) == 0 and not producers_done.is_set():
                buffer_condition.wait()  # Czekaj, jeśli bufor jest pusty i producenci jeszcze pracują
            
            if len(buffer) == 0 and producers_done.is_set():
                break  # Wyjdź, jeśli bufor jest pusty i wszyscy producenci skończyli pracę
            
            for i, (cid, item) in enumerate(buffer):
                if cid == consumer_id:
                    buffer.pop(i)  # Usuń element z bufora
                    print(f"Konsument {consumer_id} skonsumował {item}")
                    buffer_condition.notify_all()  # Powiadom producentów, że zwolniło się miejsce w buforze
                    break
        
        time.sleep(rand.random() / 8)
    

# Tworzenie i uruchamianie wątków producentów
threads = []
for i in range(NUM_PRODUCERS):
    t = threading.Thread(target=producer, args=(i,))
    threads.append(t)
    t.start()

# Tworzenie i uruchamianie wątków konsumentów
for i in range(NUM_CONSUMERS):
    t = threading.Thread(target=consumer, args=(i,))
    threads.append(t)
    t.start()

# Czekanie na zakończenie wszystkich wątków
for t in threads:
    t.join()

print("Wszytkie zadania zakończone.")
