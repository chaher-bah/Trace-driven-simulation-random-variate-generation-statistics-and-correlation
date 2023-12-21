import numpy as np
np.random.seed(619)
deterministic_mean = 1.5
exponential_mean = 1.5
hyper_exponential_means = [1.0, 2.0]
correlated_exponential_mean = 1.5
correlation = 0.2
def correlated_random_numbers (size, mean, correlation_coefficient) :
    cov_matrix = np.array([[1.0, correlation_coefficient],[correlation_coefficient, 1.0]])
    random_numbers = np.random.multivariate_normal ([mean, mean],cov_matrix, size=size)
    return np.abs (random_numbers[:, 0]+0.2*random_numbers[:, 1])
#Generate service times for each model
deterministic_service_times = np.full(10000, deterministic_mean)
exponential_service_times =np.random.default_rng(619).exponential(scale=exponential_mean,size=10000)
hyper_exponential_service_times=np.concatenate((np.random.default_rng(619).exponential(scale=hyper_exponential_means[0],size=5000),
np.random.default_rng(619).exponential(scale=hyper_exponential_means[1],size=5000)))
np.random.shuffle(hyper_exponential_service_times)
correlated_exponential_service_times=correlated_random_numbers(10000,correlated_exponential_mean,correlation)
np.savetxt("deterministic_service_time.txt",deterministic_service_times)
np.savetxt("exponential_service_times.txt",exponential_service_times)
np.savetxt("hyper_exponential_service_times.txt",hyper_exponential_service_times)
np.savetxt("correlated_exponential_service_times.txt",correlated_exponential_service_times)