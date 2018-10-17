# -*- coding: utf-8 -*-
"""
Implementation of Question 1, Part B on Homework 1. 

@author: markb
"""
import numpy as np
from scipy.linalg import hadamard
from scipy.spatial.distance import hamming
from scipy.stats import truncnorm
import math
import matplotlib.pyplot as plt

# Actually run the Hadamard attack. The algorithm follows the setup described in Problem 1a.
def random_query_attack(n, sigma, m):
    # Generate x, a random bit array of size n.
    x = np.random.randint(2, size=n)
    
    # Generate y, an array of independent normally-distributed numbers in the range (0, sigma^2)
    Y = truncnorm(0, sigma**2).rvs(size=n)
    
    # Generate B, an m * n matrix with uniformly-distributed random bits as elements
    B = np.random.randint(0, 2, size=(m,n))
    
    # Calculate a, the value released by the mechanism.
    a = (1/n) * B.dot(x) + Y
    
    # Compute the attacker's value z. 
    z = had.dot(a)
    
    x_hat = [0 if i < .5 else 1 for i in z]
    
    return (x_hat, x)
 
# Run the Hadamard attack twenty times and compute relevant statistics (Hamming distance, specified in Problem 1, and mean/stdev of combined results).
def run_random_query_attacks(n, sigma, m):
    results = []
    # Run the Hadamard attack 20 times, recording the results for each run.
    for i in range(20):
        hadamard_result = random_query_attack(n, sigma, m)
        results += [hamming(hadamard_result[0], hadamard_result[1])/n]
    # Compute and return mean and standard deviation of results.
    return (np.mean(results), np.std(results))

# Run the mean/stdev code for different settings, and graph the results.
def run_settings_and_plot():
    # Possible values for n
    n = [128,512]#,2048,8192]
    
    # Store the data in axes
    x_axis = []
    y_axis = []
    error = []
    
    # Compute for smaller values of sigma until a combination is found that achieves perfection.
    for i in n:
        print("Now testing n =", i)
        power = 1
        while(True):
            sigma = 1.0/2**power
            results = run_random_query_attacks(i,sigma)
            x_axis += ["{0}, {1}".format(i, sigma)]
            y_axis += [results[0]]
            error += [results[1]]
            if(results[0] == 0 or results[1] == 0):
                break
            power += 1
            if(1.0/2**power < 1/math.sqrt(32*i)):
                break
    plt.errorbar(range(len(x_axis)), y_axis, error, linestyle='None', marker='o', capsize=6)
    plt.xticks(range(len(x_axis)), x_axis, rotation=90)
    plt.show()
            
#run_settings_and_plot()