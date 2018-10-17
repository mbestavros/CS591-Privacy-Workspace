# -*- coding: utf-8 -*-
"""
Implementation of Question 1, Part A on Homework 1. 

@author: markb
"""
import numpy as np
from scipy.linalg import hadamard
from scipy.spatial.distance import hamming
from scipy.stats import truncnorm
import math

# Actually run the Hadamard attack. The algorithm follows the setup described in Problem 1a.
def hadamard_attack(n, sigma):
    # Generate x, a random bit array of size n.
    x = np.random.randint(2, size=n)
    
    # Generate y, an array of independent normally-distributed numbers in the range (0, sigma^2)
    Y = truncnorm(0, sigma**2).rvs(size=n)
    
    # Precompute the value of Hadamard, since we use it more than once.
    had = hadamard(n)
    
    # Calculate a, the value released by the mechanism.
    a = (1/n) * had.dot(x) + Y
    
    # Compute the attacker's value z. 
    z = had.dot(a)
    
    x_hat = [0 if i < .5 else 1 for i in z]
    
    return (x_hat, x)
 
# Run the Hadamard attack twenty times and compute relevant statistics (Hamming distance, specified in Problem 1, and mean/stdev of combined results).
def run_hadamard_attacks(n, sigma):
    results = []
    # Run the Hadamard attack 20 times, recording the results for each run.
    for i in range(20):
        hadamard_result = hadamard_attack(n, sigma)
        results += [hamming(hadamard_result[0], hadamard_result[1])/n]
    # Compute and return mean and standard deviation of results.
    return (np.mean(results), np.std(results))

n = 16
print(run_hadamard_attacks(n, .5))