import math
#计算凸包问题
def convexhull(listpoint):
	distpoint={}
	for p in listpoint:
		distpoint[p]=2
	length=len(listpoint)
	for i in range(length):
		for j in range(i+1,length):
			if distpoint[listpoint[i]]==1 and distpoint[listpoint[j]]==1:
				break
			num=0
			for k in range(length):
				if k!=i and k!=j:
					x1=listpoint[i][0]
					y1=listpoint[i][1]
					x2=listpoint[j][0]
					y2=listpoint[j][1]
					x3=listpoint[k][0]
					y3=listpoint[k][1]
					n=x1*y2+x3*y1+x2*y3-x2*y1-x1*y3-x3*y2
					if n>=0:
						num+=1
			if num==0 or num==length-2:
				distpoint[listpoint[i]]=1
				distpoint[listpoint[j]]=1
	return distpoint
#在实现
def calculation(p1,p2,p3):
	dy1=p1[1]-p3[1]
	dy2=p2[1]-p3[1]
	#说明两个点在另一个点的上下同侧
	if dy1*dy2>0:
		return 0
	else:
		#两个点在另一个点的异侧
		n=p1[0]*p2[1]+p3[0]*p1[1]+p2[0]*p3[1]-p2[0]*p1[1]-p1[0]*p3[1]-p3[0]*p2[1]
		if n>0:
			#在直线的左边
			return 1
		else:
			#在直线的右边
			return 0
#计算p3在p1->p2的向量的左边还是左边：0 右边：-2π
def getAngle(p1,p2,p3):
	d1=(p1[0]-p3[0],p1[1]-p3[1])
	d2=(p2[0]-p3[0],p2[1]-p3[1])
	length1=math.sqrt(d1[0]*d1[0]+d1[1]*d1[1])
	length2=math.sqrt(d2[0]*d2[0]+d2[1]*d2[1])
	dd12=d1[0]*d2[0]+d1[1]*d2[1]
	if p1==p3 or p2==p3:
		return 6.19
	angle=math.acos(round(dd12/(length1*length2),6))
	n=p1[0]*p2[1]+p3[0]*p1[1]+p2[0]*p3[1]-p2[0]*p1[1]-p1[0]*p3[1]-p3[0]*p2[1]
	if n<0:
		angle=-angle
	return angle
def getPList(y,listpoint):
	length=len(listpoint)
	plist=[]
	p1=p2=0
	#求出与直线相交的点
	for i in range(length):
		if i==length-1:
			p1=listpoint[-1]
			p2=listpoint[0]
		else:
			p1=listpoint[i]
			p2=listpoint[i+1]
		dy1=p1[1]-y
		dy2=p2[1]-y
		if dy1*dy2<0:
			x=((y-p1[1])*(p2[0]-p1[0]))//(p2[1]-p1[1])+p1[0]
			plist.append((x,y))
	#求过点的交点
	for i in range(length):
		p1=listpoint[i]
		p2=listpoint[(i+1)%length]
		if p1[1]==y:
			p3=listpoint[i-1]
			if((p2[1]-y)*(p3[1]-y)<0):
				plist.append(p1)
	#求出平行x轴的线段交点
	paralllist=[]
	for i in range(length):
		p1=listpoint[i]
		p2=listpoint[(i+1)%length]
		if p1[1]==y and p2[1]==y:
			if p1[0]>p2[0]:
				paralllist.append(p1)
			else:
				paralllist.append(p2)
	paralllist.sort()
	plist.sort()
	if len(paralllist)>0 and paralllist[-1][0]>plist[-1][0]:
		plist.append(paralllist[-1])
	return plist
if __name__ == '__main__':
	'''listpoint=[(1,0),(2,0),(2,1),(3,1),
	(3,2),(2,2),(2,3),(1,3),
	(1,2),(0,2),(0,1),(1,1),]
	mydist=convexhull(listpoint)
	print(mydist)
	listpoint1=[(0,0),(1,0),(1,1),(2,1),(2,0),(3,0),(3,2),(0,2)]
	mydist1=convexhull(listpoint1)
	print(mydist1)'''
	p3=(0,0)
	p1=(1,0)
	p2=[(1,0),(2,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(0,0),(1,0)]
	p4=[(2,0),(4,2),(2,4)]
	for item in p2:
		print(item,end='\t')
		print(getAngle(p1,item,p3)/3.14)