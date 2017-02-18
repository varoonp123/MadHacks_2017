# @Author: Varoon Pazhyanur <varoon>
# @Date:   18-02-2017
# @Filename: pipe_multiprocessing_ex.py
# @Last modified by:   varoon
# @Last modified time: 18-02-2017

from multiprocessing import Process, Pipe
import time

x = 1

def f1(conn):
	
	print "F1 Started"
	conn.send(1)
	time.sleep(1)
	while True:
 		time.sleep(1)
 		x=conn.recv()
 		print(x)
 		conn.send(x+1)
	print "sleep finished"
	print conn.recv()
	print "f1 received"
	conn.send(conn.recv())
	conn.close()
	print "f1 conn closed"
# 		conn.close()
	# formerX1 = 0
# 	    #listen for info from f2 and return 1+ that value back to f2
# 	while True:
# 		time.sleep(2)
# 		global x
# 		print "FormerX1 = " + str(formerX1)
# 		if (x != formerX1):
# 			x += 1
# 			formerX1 = x
# 			print "F1 updated X, x = " + str(x) + " formerX1 = " + str(formerX1)

    
def f2(conn):
 	while True:
		time.sleep(1)
		x= conn.recv()
		print(x)
		conn.send(x+1)

	# formerX2 = 0
#     #listen for info from f1 and return 1+ that value back to f1
# 
# 	while True:
# # 		print "Inside F2 while loop"
# 		time.sleep(2)
# 		global x
# 		print "FormerX2 = " + str(formerX2)
# 		if (x != formerX2):
# 			x += 1
# 			formerX2 = x
# 			print "F2 updated X, x = " + str(x) + " formerX2 = " + str(formerX2)
   

if __name__ == '__main__':
  conn1, conn2 = Pipe()
  p1 = Process(target=f1, args = (conn1,))
  p2 = Process(target=f2, args = (conn2,))
  
  p1.start()
  p2.start()
  
  p1.join()
  p2.join()
  
  
