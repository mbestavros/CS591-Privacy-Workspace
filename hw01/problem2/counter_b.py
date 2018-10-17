# -*- coding: utf-8 -*-
"""
Implementation of Question 2, Part B on Homework 1.

@author: markb
"""
import numpy as np
from scipy.spatial.distance import hamming
import matplotlib.pyplot as plt

# Implementation of the counter attack scenario, as outlined in problem 2b. Since this code is largely the same as in Part A, comments in this file will focus on differences.
def counter_attack(n):
    # Generate x, random in {0,1}, that represents which users clicked on the ad.
    x = np.random.randint(2, size=n)
    
    # Now, we begin the adversary code. 
    
    # For part B, we assume the adversary has some extra information: a "guess" vector w that has 2/3 probability of matching x.
    w = np.array([i if np.random.uniform() < 2.0/3.0 else abs(i-1) for i in x])
            
    # For each element in x, run the release function, and see what we can reconstruct given that.
    reconstructed_x = [a(x, 0)]
    previous_fuzzed_bit = None
    a_i_previous = 0
    
    for i in range(1,len(x)):
        fuzzed_bit = None
        a_i = a(x, i)
        difference = a_i - a_i_previous
        
        if(difference == -1):
            reconstructed_x[i-1] = 0
            reconstructed_x += [0]
            fuzzed_bit = 0
        elif(difference == 2):
            reconstructed_x[i-1] = 1
            reconstructed_x += [1]
            fuzzed_bit = 1
        
        # The major difference from part A: now that the adversary has some extra information, they can use that extra information to make a more informed guess.
        elif(previous_fuzzed_bit is None):
            # Instead of a 50/50 chance of being correct, the appropriate bit from the guess vector has a 2/3 chance of being corrrect, which should improve results.
            reconstructed_x += [w[i]]
            
            #Additionally, we can use the guess vector and difference together to have an informed guess at what the fuzz bit might be.
            fuzzed_bit = probabilistic_fuzz_bit_guess(w[i], difference)
        elif(difference == 0):
            if(previous_fuzzed_bit == 0):
                reconstructed_x += [0]
                fuzzed_bit = 0
            elif(previous_fuzzed_bit == 1):
                # Same guessing logic applied here.
                reconstructed_x += [w[i]]
                fuzzed_bit = probabilistic_fuzz_bit_guess(w[i], difference)
        elif(difference == 1):
            if(previous_fuzzed_bit == 0):
                reconstructed_x += [w[i]]
                fuzzed_bit = probabilistic_fuzz_bit_guess(w[i], difference)
            elif(previous_fuzzed_bit == 1):
                # And here.
                reconstructed_x += [1]
                fuzzed_bit = 1
        previous_fuzzed_bit = fuzzed_bit
        a_i_previous = a_i
        
    return (reconstructed_x, x)  

# Helper function to make an informed guess at what the fuzz bit may be given a guess and the release mechanism difference.
def probabilistic_fuzz_bit_guess(w, difference):
    fuzzed_bit = 0
    if(w == 0  and difference == 0):        
        fuzzed_bit = 1
    elif(w == 1 and difference == 0):
        fuzzed_bit = 0
    elif(w == 0 and difference == 1):
        fuzzed_bit = 1
    else:
        fuzzed_bit = 0
    return fuzzed_bit
 
# Implementation of the release function: a random bit added to the running sum of bits in x.
def a(x, i):
    fuzzed_sum = np.random.randint(2)
    for j in range(i):
        fuzzed_sum += x[j]
    return fuzzed_sum
        
# Run the counter attack twenty times and compute relevant statistics (Hamming distance, specified in Problem 1, and mean/stdev of combined results).
def run_counter_attacks(n):
    results = []
    # Run the counter attack 20 times, recording the results for each run.
    for i in range(20):
        counter_result = counter_attack(n)
        results += [1 - hamming(counter_result[0], counter_result[1])]
    # Compute and return mean and standard deviation of results.
    return (np.mean(results), np.std(results))

# Run the mean/stdev code for different settings, and graph the results.
def run_settings_and_plot():
    # Possible values for n
    n = [100,500,1000,5000]
    
    # Store the data in axes
    x_axis = []
    y_axis = []
    error = []
    
    for i in n:
        print("Now testing n =", i)
        results = run_counter_attacks(i)
        x_axis += ["{0}".format(i)]
        y_axis += [results[0]]
        error += [results[1]]
    plt.errorbar(range(len(x_axis)), y_axis, error, linestyle='None', marker='o', capsize=6)
    plt.xticks(range(len(x_axis)), x_axis, rotation=90)
    plt.show()
            
run_settings_and_plot()