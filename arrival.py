import numpy as np
from scipy.stats import poisson

#number of cars 
nbr=10000
lambdas=[0.5,0.55,0.6,0.65]
for lambda_ in lambdas:
    #applaying the Poisson ariival process with the seed 619 to generate the inter arrival times 
    inter_ar_t=poisson.rvs(lambda_,size=nbr,random_state=np.random.seed(619))
    #generate the arrival times =cum sum of inter 
    ar_times=np.cumsum(inter_ar_t)
    np.savetxt(f"arrival trace {lambda_}.txt",ar_times)
