#!/usr/bin/python
import time
import sys
import numpy as np

# YOUR FUNCTIONS GO HERE -------------------------------------
# 1. Populate the scoring matrix and the backtracking matrix

# ------------------------------------------------------------
def populate_scoring_backtracking(seq1,seq2):
    i=0
    seq1_index = 0    
    while i<len(seq1):
        index = 0
        for character in seq2:
            if character ==seq1[i] and character =='A':
                c_score = 4
            elif character ==seq1[i] and character=='C':
                c_score = 3
            elif character==seq1[i] and character=='G':
                c_score = 2
            elif character==seq1[i] and character=='T':
                c_score = 1
            else:
                c_score = -3

            c_score = c_score + scoring_matrix[seq1_index,index]
            left = scoring_matrix[seq1_index+1,index] -2
            up = scoring_matrix[seq1_index,index+1] -2

            score = max(c_score, up, left)

            scoring_matrix[seq1_index+1,index+1] = score

            if score == c_score:
                backtracking_matrix[seq1_index+1,index+1] = 'D'

            elif score == up:
                backtracking_matrix[seq1_index+1,index+1] = 'U'

            else:
                backtracking_matrix[seq1_index+1,index+1] = 'L'
            index +=1
        i+=1
        seq1_index += 1   

# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Intialise the scoring matrix and backtracking matrix and call the function to populate them
# Use the backtracking matrix to find the optimal alignment 
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 


#Initializing scoring matrix
scoring_matrix = np.zeros(shape=(len(seq1)+1, len(seq2)+1), dtype=int)


#Initialize scoring matrix values along first row and column; s(i,0) = -2i, s(0,j) = -2j
i = 0 
index = 0
for score in scoring_matrix[0,:]:
    scoring_matrix[0,index] = i
    index +=1
    i += -2
    
i = 0 
index = 0
for score in scoring_matrix[:,0]:
    scoring_matrix[index,0] = i
    index +=1
    i += -2

#Initializing backtracking matrix
backtracking_matrix = np.zeros(shape=(len(seq1)+1, len(seq2)+1), dtype=str)
#Initialize backtracking matrix values along first row and column

index = 0
for score in backtracking_matrix[0,:]:
    backtracking_matrix[0,index] = 'L'
    index +=1

index = 0
for score in backtracking_matrix[:,0]:
    backtracking_matrix[index,0] = 'U'
    index +=1

backtracking_matrix[0,0] = 'E'

#Populate scoring and backtracking matrices by calling above function
populate_scoring_backtracking(seq1,seq2)


#Find optimal alignment using backtracking matrix

index1 = len(seq1)-1
index2 = len(seq2)-1


#Intialize two empty strings for output
string1=''
string2=''

#Set position in backtracking matrix to bottom right hand corner
position = backtracking_matrix[index1+1,index2+1]

#Follow path in backtracking matrix until the end (upper left hand corner) is reached. While backtracking, append appropriate nucleotides to front of output strings.
while position != 'E':
    if position == 'D':
        string1 = seq1[index1] + string1
        string2 = seq2[index2] + string2
        position = backtracking_matrix[index1,index2]
        index1 -= 1
        index2 -=1

    elif position == 'U':
        string1 = seq1[index1] + string1
        string2 = '-' + string2
        position = backtracking_matrix[index1,index2+1]
        index1 -= 1

    elif position == 'L':
        string1 = '-' + string1
        string2 = seq2[index2] + string2
        position = backtracking_matrix[index1+1,index2]
        index2 -=1

#Find the score of optimal alignment
best_score = scoring_matrix[len(seq1),len(seq2)]
best_alignment = [string1,string2]

#-------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best score: ' +str(best_score))
#-------------------------------------------------------------

