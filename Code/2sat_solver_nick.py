#!/usr/bin/env python

# Theory of Computing 2SAT solver

# This code is an optimized 2SAT solver
# The code reads in csv files containing 2SAT problems and produces and times the output
# using a dumbSAT algorithm (provided on Canvas) and an optimized 2SAT algorithm

# To read in files you should go into the terminal and call:
# ./2sat_solver.py problem_file.csv {0,1,2}
# The second command line argument determines which algorithm to run
# 0: Only run dumbSAT
# 1: Only run optimized 2SAT solver
# 2: Run both

# At the end of each run, the code produces a plot of the time it took to solve a case vs 
# the complexity of the problem.
# These plots are saved as pdf files in the folder

# In order to create plots you need to install the matplotlib library
# I did this by calling "pip install matplotlib" in the terminal

import sys
import csv
from graph_nick import plot, plot_both
from solve_functions_nick import test_wff, test_wff_DPLL

def main():
    wffs = {}  # Dictionary of all wffs in the csv file
    wff_num = 1
    current_wff = "wff_1"
    mode = int(sys.argv[2]) 

    try: # Processes the wffs from a csv into a 2D array for each wff stored in a dictionary if a valid csv is provided
        with open(sys.argv[1], 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                if len(line) > 0 and line[0] == 'c':  # Creates a new dictionary entry for each wff
                    wff_num += 1
                    current_wff = f'wff_{wff_num}'
                    wffs[current_wff] = []  
                wffs.setdefault(current_wff, []).append(line)
    except FileNotFoundError: # Prints an error if a valid file is not provided
        print(f'Error: File {sys.argv[1]} invalid \n')
        return -1
    
    reg_time = 0 # Counter for the total times across the 100 algorithms
    dp_time = 0
    vars = [] # List of the number of variables in each problem used for graphing
    time_reg = [] # List the times each wff took to use in the graphs
    time_dp = []
    truths = [] # Lists the truth values assigned to each wff for graphing

    if mode == 0: # Sets the output file path based on which algorithm will be run
        outfile_path = '../Output/output_dumbSAT_nick.txt'
    elif mode == 1:
        outfile_path = '../Output/output_2SAT_nick.txt'
    elif mode == 2:
        outfile_path = '../Output/output_both_nick.txt'

    with open(outfile_path, 'w') as outfile:
        for key, wff in wffs.items(): # Solves each wff in the dictionary
            nvars = int(wff[1][2])
            nclauses = int(wff[1][3])

            # Processing wff entries
            # Cuts out the first two lines of each wff, takes the first two variables, and transform into ints.
            data = wff[2:] 
            data = [row[:2] for row in data] #
            data = [list(map(int, row)) for row in data]

            # Runs different algorithm based on which mode was selected
            if mode  == 0: # DumbSAT solution
                output = test_wff(data, nvars, nclauses) # Calls the test and saves reults to output
                outfile.write(f"Is {key} satisfiable? {'Yes' if output[2] else 'No'}\n") # Prints test results
                if output[2]:
                    outfile.write(f'Solution: {output[1][1:-1]}\n')
                else:
                    outfile.write(f'Solution: None\n')
                outfile.write(f'Time (microseconds): {output[3]}\n\n')

                reg_time += output[3] # Adds time to total counter and appends lists used in graphing with reuslts
                vars.append(nvars)
                time_reg.append(output[3])
                truths.append(output[2])

            elif mode == 1: # DPLL solution - same format as above
                output_DPLL = test_wff_DPLL(data, nvars, nclauses)
                outfile.write(f"Is {key} satisfiable? {'Yes' if output_DPLL[2] else 'No'}\n")
                if output_DPLL[2]:
                    outfile.write(f'Solution: {output_DPLL[1]}\n')
                else:
                    outfile.write(f'Solution: None\n')
                outfile.write(f'Time (microseconds): {output_DPLL[3]}\n\n')

                dp_time += output_DPLL[3]
                vars.append(nvars)
                time_dp.append(output_DPLL[3])
                truths.append(output_DPLL[2])

            elif mode == 2: # Runs both dumbSAT and DPLL
                issues = [] # Tracks any conflicting outputs
                output = test_wff(data, nvars, nclauses) # Runs dumbSAT
                output_DPLL = test_wff_DPLL(data, nvars, nclauses) # Runds DPLL
                reg_time += output[3]
                dp_time += output_DPLL[3]
                if (output[2] != output_DPLL[2]):
                    issues.append((output, output_DPLL))
                outfile.write(f'{key} of {len(wffs)}:\n') # Write results to output
                outfile.write(f'DumbSAT Output: {output[2]} \t DPLL Output: {output_DPLL[2]}\n')
                outfile.write(f'DumbSAT Time (microseconds): {output[3]} \t DPLL Time (microseconds): {output_DPLL[3]}\n\n')

                vars.append(nvars)
                time_dp.append(output_DPLL[3])
                time_reg.append(output[3])

        # Graphing portion - calls different graphs based on mode
        if mode == 0:
            outfile.write(f'DumbSAT Total Time (microseconds): {reg_time}')
            name = "DumbSAT"
            plot(vars, time_reg, name, truths) # Plots dumbSAT results
        elif mode == 1:
            outfile.write(f'DPLL Total Time (microseconds): {dp_time}')
            name = "DPLL"
            plot(vars, time_dp, name, truths) # Plots DPLL results
        elif mode == 2:
            outfile.write(f'DumbSAT Total Time (microseconds): {reg_time} \t DPLL Total Time (microseconds): {dp_time}\n')
            outfile.write(f'Conflicting Outputs: {issues}')
            plot_both(vars, time_dp, time_reg) # Plots both results

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3: # Prints error if incorrect amount of input is used
        print("Usage: python script.py <csv_file> {0,1,2}")
    else:
        main()
