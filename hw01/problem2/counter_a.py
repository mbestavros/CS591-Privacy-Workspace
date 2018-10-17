# -*- coding: utf-8 -*-
"""
Implementation of Question 2, Part A on Homework 1.

@author: markb
"""
import numpy as np
from scipy.spatial.distance import hamming

# Implementation of the counter attack scenario, as outlined in problem 2.
def counter_attack(n):
    # Generate x, random in {0,1}, that represents which users clicked on the ad.
    x = np.random.randint(2, size=n)
    
    # Now, we begin the adversary code. For each element in x, run the release function, and see what we can reconstruct given that.
    reconstructed_x = [a(x, 0)]
    previous_fuzzed_bit = None
    
    for i in range(1,len(x)):
        fuzzed_bit = None
        a_i = a(x, i)
        difference = a_i - sum(reconstructed_x)
        
        if(difference == -1):
            reconstructed_x[i-1] = 0
            reconstructed_x += [0]
            fuzzed_bit = 0
        elif(difference == 2):
            reconstructed_x[i-1] = 1
            reconstructed_x += [1]
            fuzzed_bit = 1
        elif(previous_fuzzed_bit is None):
            reconstructed_x += [difference]
        elif(difference == 0):
            if(previous_fuzzed_bit == 0):
                reconstructed_x += [0]
                fuzzed_bit = 0
            elif(previous_fuzzed_bit == 1):
                reconstructed_x += [difference]
        elif(difference == 1):
            if(previous_fuzzed_bit == 0):
                reconstructed_x += [difference]
            elif(previous_fuzzed_bit == 1):
                reconstructed_x += [1]
                fuzzed_bit = 1
        previous_fuzzed_bit = fuzzed_bit
    print("original")
    print()
    print(x)
    print("new")
    print()
    print(reconstructed_x)
    print("Hamming")
    print()
    print(1-hamming(x, reconstructed_x))
    
        
 
    # Implementation of the release function: a random bit added to the running sum of bits in x.
def a(x, i):
    fuzzed_sum = np.random.randint(2)
    for j in range(i):
        fuzzed_sum += x[j]
    return fuzzed_sum
        

counter_attack(100)
    