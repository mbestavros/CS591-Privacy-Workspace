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
    
    print(x_hat, x)
    
    return (x_hat, x)
 
# Run the Hadamard attack once and return the Hamming distance parameter (specified in Problem 1).
def run_hadamard_attack_once(n, sigma):
    results = hadamard_attack(n, sigma)
    return hamming(results[0], results[1])/n

n = 16
print(run_hadamard_attack_once(n, .5))