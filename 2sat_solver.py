#!/usr/bin/env python3

# Theory of Computing 2SAT solver

import time
import random
import string
import sys
import csv

def DPLL_check(Wff, solution):
    for pair in Wff:
        if (solution[pair[0]] == 0 and solution[pair[1]] == 0):
            return False
    return True


def DPLL (Wff, Nvars, Nclauses, solution, Pos):
    found = False
    if Pos == Nvars:
        return False
    solution[Pos] = 0
    solution[-Pos] = 1
    val = DPLL_check(Wff, solution)
    if (val and (Nvars == Pos - 1)):
        return True
    elif (val):
        found = DPLL(Wff, Nvars, Nclauses, solution, Pos)
        if found == True:
            return True
    else:
        return False
    
    solution[Pos] = 1
    solution[-Pos] = 0
    val = DPLL_check(Wff, solution)
    if (val and (Nvars == Pos - 1)):
        return True
    elif (val):
        found = DPLL(Wff, Nvars, Nclauses, solution, Pos)
        if found == True:
            return True
    else:
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
    #Assignment=list((0 for x in range(Nvars+2))) # Original Check
    Assignment = list((-1 for x in range(Nvars*2))) # DPLL Check
    start = time.time() # Start timer
    #SatFlag=check(wff,Nvars,Nclauses,Assignment)
    SatFlag=DPLL(wff, Nvars, Nclauses, Assignment)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]

def main():
    wffs = {}  
    wff_num = 1
    current_wff = "wff_1"

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
    
    for key, wff in wffs.items():
        nvars = int(wff[1][2])
        nclauses = int(wff[1][3])
        assignment = wff[0][3]
        data = wff[2:]
        data = [row[:2] for row in data]
        data = [list(map(int, row)) for row in data]

        output = test_wff(data, nvars, nclauses)
        print(output)
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
    else:
        main()
