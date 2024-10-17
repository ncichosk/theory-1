Team name: Nick's Team \\
Names of all team members: Nicholas Cichoski \\
Link to github repository: https://github.com/ncichosk/theory-1 \\
Which project options were attempted: Implementing a polynomial time 2-SAT solver \\
Approximately total time spent on project: 7 hours \\
The language you used, and a list of libraries you invoked: python; time, sys, csv, matplotlib \\
How would a TA run your program (did you provide a script to run a test case?): \\
    They would run "python 2sat_solver.py input.csv {0,1,2}" in the terminal where input.csv is a csv file containin the problems and {0,1,2} refers to the algorithm to be ran. 0 will run dumbSAT, 1 will run the polynomial time 2SAT, and 2 will run both. \\
A brief description of the key data structures you used, and how the program functioned: \\
    I used a 2D array to store each problem and a dictionary to store all 100 test cases. I iterated through the dictionary to solve each wff individually. In order to create a polynomial time solver, I first initialized a solution array to -1. I then went through iteratively and assigned values to the variable checking the wff after each assignment. If an assignement made a clause in the wff false, I would backtrack out of that "branch" of solutions and change the previous assignments. \\
A discussion as to what test cases you added and why you decided to add them (what did they tell you about the correctness of your code). Where did the data come from? (course website, handcrafted, a data generator, other): \\
    I used
An analysis of the results, such as if timings were called for, which plots showed what? What was the approximate complexity of your program?
A description of how you managed the code development and testing.
Did you do any extra programs, or attempted any extra test cases
