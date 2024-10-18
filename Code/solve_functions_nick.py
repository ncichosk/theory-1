#!/usr/bin/env python

import time

def DPLL_check(Wff, solution):
# This checks if a current assignment will make any clauses in the wff false
# This will only return false if all varaibles in a clause have been assigned and that clause is false

    for pair in Wff: # Check for each clause in the wff
        a = pair[0]
        b = pair[1]
        
        if a > 0: # If there is no negation on a variable
            a_val = solution[a-1] # Adjust because variables start at 1 not 0
        else:
            a_val = 1 - solution[abs(a)-1] if solution[abs(a)-1] != -1 else -1 # Flip any 0 or 1 otherwise leave any values of -1 the same
        
        if b > 0: # If there is no negation on a variable
            b_val = solution[b-1] # Adjust because variables start at 1 not 0
        else:
            b_val = 1 - solution[abs(b)-1] if solution[abs(b)-1] != -1 else -1 # Flip any 0 or 1 otherwise leave any values of -1 the same
        
        if a_val == 0 and b_val == 0: # Check if both parts fo the clause are false
            return False
    return True # Default to a true return value


def DPLL (Wff, Nvars, Nclauses, solution, Pos):
# This is a recursive implementation of the DPLL algorithm

    if Pos == Nvars: # Base case - all variables have been assigned
        return DPLL_check(Wff, solution)
    
    solution[Pos] = 0 # Sets a variable to true
    if DPLL_check(Wff, solution): # If partial assignment does not make any clauses false
        if DPLL(Wff, Nvars, Nclauses, solution, Pos + 1): # Recursive call to assign next variable
            return True

    solution[Pos] = 1 # Sets a variable to false
    if DPLL_check(Wff, solution): # If partial assignment does not make any clauses false
        if DPLL(Wff, Nvars, Nclauses, solution, Pos + 1): # Recursive call to assign next variable
            return True
    
    solution[Pos] = -1 # Resets variable to unassiagned on backtrack
    return False

def check(Wff,Nvars,Nclauses,Assignment):
### This is a a direct copy of the dumbSAT algorithm provided on Canvas
# I did not develop this code, instead it is used as a baseline to compare to the DPLL algorithm

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
### This is a copy of the test_wff function provided in the dumbSAT code on Canvas
# It times the execution of the dumbSAT solver and returns the wff, its assignment, solvability, and execution time

    Assignment=list((0 for x in range(Nvars+2))) # Original Check
    start = time.time() # Start timer
    SatFlag=check(wff,Nvars,Nclauses,Assignment)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]

def test_wff_DPLL(wff,Nvars,Nclauses):
# This is an adjusted version of the test_wff provided on canvas
# The initial assingment method has been modified and it calls the DPLL solver
# It times the execution of the DPLL solver and returns the wff, its assignment, solvability, and execution time

    Assignment = list((-1 for x in range(Nvars))) # DPLL Check
    start = time.time() # Start timer
    SatFlag=DPLL(wff, Nvars, Nclauses, Assignment, 0)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]