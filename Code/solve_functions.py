#!/usr/bin/env python

import time

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