#!/usr/bin/env python3

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

import time
import sys
import csv
import matplotlib.pyplot as plt

def plot(x,y, name, truths):
    colors = ['green' if truth else 'red' for truth in truths]

    plt.scatter(x, y, c=colors, marker='o')

    plt.title(f"Time Complexity for {name}")

    plt.xlabel("Variables in SAT Problem")
    plt.ylabel("Time to Compute (microseconds)")

    plt.savefig(f"graphs/{name}_time_complexity_plot.pdf", format='pdf')

    plt.show()

def plot_both(x,y1, y2):
    fig, ax = plt.subplots()

    ax.scatter(x, y2, label='DumbSAT', marker='s')
    ax.scatter(x, y1, label='DPLL', marker='^')

    ax.set_xlabel('Variables in SAT Problem')
    ax.set_ylabel('Time to Compute (microseconds)')
    ax.set_title('Time Complexity for DumbSAT v DPLL')
    ax.legend()

    plt.savefig(f"graphs/both_time_complexity_plot.pdf", format='pdf')
    plt.show()

def DPLL_check(Wff, solution):
    for pair in Wff:
        a = pair[0]
        b = pair[1]
        
        if a > 0:
            a_val = solution[a-1]
        else:
            a_val = 1 - solution[abs(a)-1] if solution[abs(a)-1] != -1 else -1
        
        if b > 0:
            b_val = solution[b-1]
        else:
            b_val = 1 - solution[abs(b)-1] if solution[abs(b)-1] != -1 else -1
        
        if a_val == 0 and b_val == 0:
            return False
    return True


def DPLL (Wff, Nvars, Nclauses, solution, Pos):
    if Pos == Nvars:
        return DPLL_check(Wff, solution)
    
    solution[Pos] = 0
    if DPLL_check(Wff, solution):
        if DPLL(Wff, Nvars, Nclauses, solution, Pos + 1):
            return True

    solution[Pos] = 1
    if DPLL_check(Wff, solution):
        if DPLL(Wff, Nvars, Nclauses, solution, Pos + 1):
            return True
    
    solution[Pos] = -1
    return False

def check(Wff,Nvars,Nclauses,Assignment):
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments
    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Clause=Wff[i]
            Satisfiable=False
            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable

def test_wff(wff,Nvars,Nclauses):
    Assignment=list((0 for x in range(Nvars+2))) # Original Check
    start = time.time() # Start timer
    SatFlag=check(wff,Nvars,Nclauses,Assignment)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]

def test_wff_DPLL(wff,Nvars,Nclauses):
    Assignment = list((-1 for x in range(Nvars))) # DPLL Check
    start = time.time() # Start timer
    SatFlag=DPLL(wff, Nvars, Nclauses, Assignment, 0)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]

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

    for key, wff in wffs.items():
        nvars = int(wff[1][2])
        nclauses = int(wff[1][3])

        data = wff[2:]
        data = [row[:2] for row in data]
        data = [list(map(int, row)) for row in data]


        if mode  == 0:
            output = test_wff(data, nvars, nclauses)
            print(f"Is {key} satisfiable? {'Yes' if output[2] else 'No'}")
            if output[2]:
                print(f'Solution: {output[1][1:-1]}')
            else:
                print(f'Solution: None')
            print(f'Time: {output[3]}')

            reg_time += output[3]
            vars.append(nvars)
            time_reg.append(output[3])
            truths.append(output[2])

        elif mode == 1:
            output_DPLL = test_wff_DPLL(data, nvars, nclauses)
            print(f"Is {key} satisfiable? {'Yes' if output_DPLL[2] else 'No'}")
            if output_DPLL[2]:
                print(f'Solution: {output_DPLL[1]}')
            else:
                print(f'Solution: None')
            print(f'Time: {output_DPLL[3]}')

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
            print(f'{key} of {len(wffs)}:\n')
            print(f'DumbSAT Output: {output[2]} \t DPLL Output: {output_DPLL[2]}\n')
            print(f'DumbSAT Time: {output[3]} \t DPLL Time: {output_DPLL[3]}\n')

            vars.append(nvars)
            time_dp.append(output_DPLL[3])
            time_reg.append(output[3])


    if mode == 0:
        print(f'DumbSAT Total Time: {reg_time}')
        name = "DumbSAT"
        plot(vars, time_reg, name, truths)
    elif mode == 1:
        print(f'DPLL Total Time: {dp_time}')
        name = "DPLL"
        plot(vars, time_dp, name, truths)
    elif mode == 2:
        print(f'DumbSAT Total Timae: {reg_time} \t DPLL Total Time: {dp_time}\n')
        print(f'Conflicting Outputs: {issues}')
        plot_both(vars, time_dp, time_reg)

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
    else:
        main()
