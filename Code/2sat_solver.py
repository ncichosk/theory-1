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
from graph import plot, plot_both
from solve_functions import test_wff, test_wff_DPLL

def main():
    wffs = {}  
    wff_num = 1
    current_wff = "wff_1"
    mode = int(sys.argv[2])

    try:
        with open(sys.argv[1], 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                if len(line) > 0 and line[0] == 'c':  
                    wff_num += 1
                    current_wff = f'wff_{wff_num}'
                    wffs[current_wff] = []  
                wffs.setdefault(current_wff, []).append(line)
    except FileNotFoundError:
        print(f'Error: File {sys.argv[1]} invalid \n')
        return -1
    
    reg_time = 0
    dp_time = 0
    vars = []
    time_reg = []
    time_dp = []
    truths = []

    if mode == 0:
        outfile_path = '../Output/dumbSAT_output.txt'
    elif mode == 1:
        outfile_path = '../Output/2SAT_output.txt'
    elif mode == 2:
        outfile_path = '../Output/both_output.txt'

    with open(outfile_path, 'w') as outfile:
        for key, wff in wffs.items():
            nvars = int(wff[1][2])
            nclauses = int(wff[1][3])

            data = wff[2:]
            data = [row[:2] for row in data]
            data = [list(map(int, row)) for row in data]


            if mode  == 0:
                output = test_wff(data, nvars, nclauses)
                outfile.write(f"Is {key} satisfiable? {'Yes' if output[2] else 'No'}\n")
                if output[2]:
                    outfile.write(f'Solution: {output[1][1:-1]}\n')
                else:
                    outfile.write(f'Solution: None\n')
                outfile.write(f'Time (microseconds): {output[3]}\n\n')

                reg_time += output[3]
                vars.append(nvars)
                time_reg.append(output[3])
                truths.append(output[2])

            elif mode == 1:
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

            elif mode == 2:
                issues = []
                output = test_wff(data, nvars, nclauses)
                output_DPLL = test_wff_DPLL(data, nvars, nclauses)
                reg_time += output[3]
                dp_time += output_DPLL[3]
                if (output[2] != output_DPLL[2]):
                    issues.append((output, output_DPLL))
                outfile.write(f'{key} of {len(wffs)}:\n')
                outfile.write(f'DumbSAT Output: {output[2]} \t DPLL Output: {output_DPLL[2]}\n')
                outfile.write(f'DumbSAT Time (microseconds): {output[3]} \t DPLL Time (microseconds): {output_DPLL[3]}\n\n')

                vars.append(nvars)
                time_dp.append(output_DPLL[3])
                time_reg.append(output[3])


        if mode == 0:
            outfile.write(f'\nDumbSAT Total Time (microseconds): {reg_time}')
            name = "DumbSAT"
            plot(vars, time_reg, name, truths)
        elif mode == 1:
            outfile.write(f'\nDPLL Total Time (microseconds): {dp_time}')
            name = "DPLL"
            plot(vars, time_dp, name, truths)
        elif mode == 2:
            outfile.write(f'\nDumbSAT Total Time (microseconds): {reg_time} \t DPLL Total Time (microseconds): {dp_time}\n')
            outfile.write(f'Conflicting Outputs: {issues}')
            plot_both(vars, time_dp, time_reg)

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <csv_file> {0,1,2}")
    else:
        main()
