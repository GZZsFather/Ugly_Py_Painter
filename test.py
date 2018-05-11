from util import convexhull

if __name__ == '__main__':
	listpoint=[(0,0),(1,0),(2,1),(3,2),(2,2),(1,2),(1,1)]
	mydist=convexhull(listpoint)
	print(mydist)