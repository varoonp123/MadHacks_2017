
# mylist = [-5, 500, 300, 200]
def bounds(mylist = []):
	l = len(mylist)
	total = 0.0
	maxE = 100

	for i in range(0,l):
		mylist[i] = max(min(mylist[i], 100), 0)
		total += mylist[i]
	
	for i in range(0,l):
		mylist[i] = int(mylist[i] / total * maxE)

# print mylist 
# print total