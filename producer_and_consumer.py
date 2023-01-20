import threading
import time
import random

# Shared Memory variables
CAPACITY = 10
buffer = [-1 for i in range(CAPACITY)]
in_index = 0
out_index = 0

# Declaring Semaphores
mutex = threading.Semaphore()
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)


# Producer Thread Class
class Producer(threading.Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full
        items_produced = 0
        counter = 0
        while items_produced < 20:
            try:
                empty.acquire()
                mutex.acquire()
                counter += 1
                buffer[in_index] = counter
                in_index = (in_index + 1) % CAPACITY
                print("Producer has produced : ", counter)
                mutex.release()
                full.release()

                # Sleep for a random amount of time
                time.sleep(random.uniform(1, 5))
                items_produced += 1
            except Exception as e:
                print("Error: ", e)


# Consumer Thread Class
class Consumer(threading.Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index, counter
        global mutex, empty, full
        items_consumed = 0
        while items_consumed < 20:
            try:
                full.acquire()
                mutex.acquire()
                item = buffer[out_index]
                out_index = (out_index + 1) % CAPACITY
                print("Consumer has consumed item : ", item, "\n")
                mutex.release()
                empty.release()
                # Sleep for a random amount of time
                time.sleep(random.uniform(2.5, 7.5))
                items_consumed += 1
            except Exception as e:
                print("Error: ", e)


# Creating Threads
producer = Producer()
consumer = Consumer()

# Starting Threads
consumer.start()
producer.start()

# Waiting for threads to complete
producer.join()
consumer.join()
