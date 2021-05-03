from invoke import task
import time
from constant import MAX_CAP_2D_K,MAX_CAP_2D_N,MAX_CAP_3D_K,MAX_CAP_3D_N

@task
def run(c,k=-5,n=-5,Random=True):
    c.run("python3.8.5 setup.py build_ext --inplace")

    if(Random):
        c.run("python3.8.5 main.py " + str(k)+" "+ str(n))
    else:
        c.run("python3.8.5 main.py " + str(k) + " " + str(n) + " --Random")


