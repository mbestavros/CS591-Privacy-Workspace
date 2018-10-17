# -*- coding: utf-8 -*-
"""
Implementation of Question 2, Part A on Homework 1.

@author: markb
"""
import numpy as np
from scipy.spatial.distance import hamming
import matplotlib.pyplot as plt

# Implementation of the counter attack scenario, as outlined in problem 2a.
def counter_attack(n):
    # Generate x, random in {0,1}, that represents which users clicked on the ad.
    x = np.random.randint(2, size=n)
    
    # Now, we begin the adversary code. For each element in x, run the release function, and see what we can reconstruct given that.
    reconstructed_x = [a(x, 0)]
    previous_fuzzed_bit = None
    a_i_previous = 0
    
    for i in range(1,len(x)):
        # If we can figure out what the fuzzed bit for this iteration is, we will keep it to help us in the next one.
        fuzzed_bit = None
        
        # Run the release function.
        a_i = a(x, i)
        
        # The crux of the attack is going to focus on the difference between the current and previous iterations of the release function.
        difference = a_i - a_i_previous
        
        # The obvious cases: when the difference goes down, or increases by 2, we can know for certain what both the actual bit and the fuzzed bit are. We can also infer what the previous iteration's values were.
        if(difference == -1):
            reconstructed_x[i-1] = 0
            reconstructed_x += [0]
            fuzzed_bit = 0
        elif(difference == 2):
            reconstructed_x[i-1] = 1
            reconstructed_x += [1]
            fuzzed_bit = 1
        
        # If not an extreme, the difference will be either 0 or 1; we cannot make claims outright about those values, but we can infer things if we knew what the previous iteration's fuzzed bit was.
        # If we don't know the fuzzed bit, we have to make a guess.
        elif(previous_fuzzed_bit is None):
            reconstructed_x += [difference]
        # If we do have a previous fuzzed bit, we can infer about values in some, but not all, cases. All the exceptions will be, again, guesses.
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
                
        # Pass on the fuzzed bit to the next iteration.
        previous_fuzzed_bit = fuzzed_bit
        
        # Pass on the current value of the release function to the next iteration.
        a_i_previous = a_i
        
    return (reconstructed_x, x)
 
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
    