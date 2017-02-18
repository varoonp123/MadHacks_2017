# @Author: Varoon Pazhyanur <varoon>
# @Date:   18-02-2017
# @Filename: pipe_multiprocessing_ex.py
# @Last modified by:   varoon
# @Last modified time: 18-02-2017



import multiprocessing

def f1():
  while True:
    #listen for info from f2 and return 1+ that value back to f2


def f2():
  while True:
    #listen for info from f1 and return 1+ that value back to f1

if __name__ == '__main__':
  Process(target=f1).start
  Process(target=f2).start
