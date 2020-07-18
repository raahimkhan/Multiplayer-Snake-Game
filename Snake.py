
from Constants import *

class snake:
	
	def __init__(self, id, height, width):
		self.list = []
		self.edges = []
		
		self.direction = VEC_RIGHT
		self.length = 5
		initialPos = [id * height/6,   width/2]
		for i  in range(self.length):
			self.list.append([initialPos[0], initialPos[1] + i])
		self.updateEdges()
	
	def updateSnake(self, direction):
		
		new_direction = [self.direction[0] + direction[0], self.direction[1] + direction[1]]

		cy = new_direction[0]
		cx = new_direction[1]

		head = self.list[-1]

		
		if [cy, cx] == [0,0]:
			pass
		else:
			self.direction = direction

		new_head = [head[0] + self.direction[0], head[1] + self.direction[1]]
		
		self.list.insert(self.length, new_head) 
		
		self.list.pop(0)

		self.updateEdges()

	def isAlive(self, allSnakes, height, width):
		head = self.list[self.length - 1]

		count = 0 #keeps count of the number of times head is found in allSnakes

		if height <= head[0] or head[0] <= 0:
			return False
		elif width <= head[1] or head[1] <= 0:
			return False

		for snk in allSnakes:
			count = count + snk.list.count(head)

		if(count > 1):
			return False

		return True

	def resurrect(self): #, edges): ONLY TEMPORARILY IN THE SNAKE CLASS. IS INTEDED TO BE TRANSFERED TO THE CLIENT FILE
		newList = []

		constant = 0
		varriableAxis = 1


		for i in range(len(self.edges) - 1):

			thisEdge = self.edges[i]
			nextEdge = self.edges[i + 1]

			if thisEdge[0] == nextEdge[0]:
				constant = thisEdge[0]
				varriableAxis = 1
			
			elif thisEdge[1] == nextEdge[1]:
				constant = thisEdge[1]
				varriableAxis = 0

			step = 1 

			if thisEdge[varriableAxis] > nextEdge[varriableAxis]:
				step = -1

			for varriableVal in range(thisEdge[varriableAxis],nextEdge[varriableAxis], step):
				if varriableAxis == 0:
					newList.append([varriableVal, constant])
				else:
					newList.append([constant, varriableVal])

		newList.append(self.edges[len(self.edges) - 1])


	def updateEdges(self):

		newEdgeList = []

		newEdgeList.append(self.list[0])

		currentConstant = 0

		if self.list[0][0] == self.list[1][0]:
			currentConstant = 0
		else:
			currentConstant = 1

		reclist = []
		reclist.append(self.list[0])
		#reclist.append(self.list[1])

		for i in range(1, len(self.list)):
			if(reclist[len(reclist) - 1][currentConstant] == self.list[i][currentConstant]):
				reclist.append(self.list[i])
			else:
				newEdgeList.append(reclist[len(reclist) - 1])
				reclist = []

				currentConstant = currentConstant ^ 1

				reclist.append(self.list[i])

		if self.list[len(self.list) - 1] in newEdgeList:
			pass
		else:
			newEdgeList.append(self.list[len(self.list) - 1])

		self.edges = newEdgeList
