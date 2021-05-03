"""
    The Error Handling Module.
    in this module we will deal with errors: specifically - Input type errors.
"""
import argparse

def check_input(K,N,Random):
    if(not Random):
        if(K == -5):
            print("Please input K!")
            exit(1)
        elif(K < 0):
            print("Please choose a positive K")
            exit(1)
        elif(N == -5):
            print("Please input N!")
            exit(1)
        elif(N < 0):
            print("Please choose a positive N")
            exit(1)
        elif(N < K):
            print("N can not be smaller than K")
            exit(1)
        else:
            return True
    return True

def checker(a):
    try:
        num = int(a)
    except ValueError:
        print('invalid int value!')
        exit(1)
    return num