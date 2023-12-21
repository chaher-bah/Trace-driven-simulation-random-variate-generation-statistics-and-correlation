import simpy
import math
import numpy as np

def load_arrival_trace(lambda_value):
    with open(f"arrival trace {lambda_value}.txt", 'r') as f:
        arrival_trace = np.loadtxt(f)
    return arrival_trace

def load_service_trace(service_model):
    with open(f"{service_model}.txt", 'r') as file:
        service_trace = np.loadtxt(file)
    return service_trace

def run_simulation(lambda_value, service_model):
    env = simpy.Environment()
    booth = simpy.Resource(env, capacity=1)
    total_wait_time = 0
    max_wait_time = 0
    data = []

    arrival_trace = load_arrival_trace(lambda_value)
    service_trace = load_service_trace(service_model)

    def car(env, name, booth, arrival_time, service_time):
        yield env.timeout(arrival_time)
        with booth.request() as req:
            yield req
            start_time = env.now
            yield env.timeout(service_time)
            end_time = env.now
            waiting_time = end_time - start_time
            nonlocal total_wait_time, max_wait_time, data
            data.append(waiting_time)
            max_wait_time = max(max_wait_time, waiting_time)
            total_wait_time += waiting_time

    def car_generator(env, booth, arrival_trace, service_trace):
        for i in range(len(arrival_trace)):
            arrival_time = arrival_trace[i]
            service_time = service_trace[i]
            yield env.process(car(env, f'Car {i}', booth, arrival_time, service_time))

    env.process(car_generator(env, booth, arrival_trace, service_trace))
    env.run()

    num_cars = 10000
    average_waiting_time = total_wait_time / num_cars
    std_waiting_time = math.sqrt(sum(((x - average_waiting_time) ** 2 for x in data)) / num_cars)

    return num_cars, average_waiting_time, std_waiting_time, max_wait_time

# Exemple d'utilisation pour exécuter les simulations
lambda_values = [0.5, 0.55, 0.6, 0.65]
service_models = ["deterministic_service_time", "exponential_service_times", "hyper_exponential_service_times", "correlated_exponential_service_times"]

for lambda_value in lambda_values:
    for service_model in service_models:
        num_cars, avg_wait_time, std_wait_time, max_wait_time = run_simulation(lambda_value, service_model)
        print(f"Lambda: {lambda_value}, Service Model: {service_model}")
        print(f"Nombre de voitures : {num_cars}")
        print(f"Temps d'attente moyen : {avg_wait_time:.2f}")
        print(f"Ecart type du temps d'attente : {std_wait_time:.2f}")
        print(f"Temps d'attente maximum : {max_wait_time:.2f}")
        print("----------------------------------------")