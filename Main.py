class Main:
	
	def __init__(self,initial,events,flag):
		self.initial = initial #file with initial 
		self.events = event #file with events
		self.flag = flag #string with algorithm to use
		self.network = [] #list of nodes
		self.events = [] #list of events and their descriptions
		self.nodeNames = [] # a list of names of all nodes
		self.currentRound = 0 #current round

	def setup(self,protocol):
		f = open(self.initial,"r")
		lines = f.readlines()
		#preprocess
		num = int(lines[0])
		del lines[0]
		#set up the network
		for i in range(num):
			self.network.append(Node(str(i + 1),[]))
			self.nodeNames.append(str(i + 1))
		#update connections
		for line in lines:
			first,second,dist = line.split()
			for node in self.network:
				if node.getName() == first:
					node.addValue(second,int(dist),0)
				elif node.getName() == second:
					node.addValue(first,int(dist),0)
		f.close()

		#queue future updates for network events
		f = open(self.events,"r")
		for line in f.readlines():
			time = int(line[0])
			dist = int(line[3])
			self.events.append([time,line[1],line[2],dist])	
		f.close()
		updateNetwork(protocol)

	def updateNetwork(self,protocol):
		if protocol == "basic":
			for node in network:
				vector = node.getVector()
				for name in nodeNames:
					#add noes 
					if(name not in vector and name != node.getName()):
						hops,dist = self.findBestPath(node,name)
						node.updateValue(name,dist,hops)
		elif protocol == "splith":
			print("TODO")
		elif protocol == "splithpv":
			print("TODO")
	#finds best path using UCS with each router sharing only each other's DV
	def findBestPath(self,node,dest):
		queue = util.PriorityQueue()
	    atgoal = []
	    #Root contains state,actionlist,total cost
	    actionList = []
	    root = (node,actionList,0)
	    visitedList = []
	    queue.push(root,0)

	    while queue.isEmpty() is False:
	        n = queue.pop()
	        current = n[0][0]
	        actionList = n[1]
	        if current == dest:
	        	#FIX THIS
	            return (len(actionList),n[2])
	        if n[0][0] not in visitedList:
	            visitedList = visitedList + [n[0][0]]
	            for child in self.getNodeByName(n[0][0]).getVector():
	                if child[0] not in visitedList:
	                    #Calculate the total cost of this so we can add it to priority queue appropriately
	                    cost = sum(actionList + [child[1]])
	                    newnode = (self.getNodeByName(child[0]),actionList + [child[1]],cost)
	                    #Priority Queue takes care of pushing by cost calculations.
	                    queue.push(newnode,cost)

	def hasEvent(self,curRound):
		for i in range(len(self.events)):
			if self.events[i][0] == curRound:
				self.updateEvent(self.events[i])
				#remove event after use
				del self.events[i]

	def updateEvent(self,event):
		first = event[1]
		second = event[2]
		dist = event[3]
		for node in self.network:
			if(node.getName() == first):
				if(dist == -1):
					#kill the link with the other node
					node.deleteValue(second)
				else:
					#else update the other link
					node.updateValue(second,dist)
			elif(node.getName() == second):
				if(dist == -1):
					node.deleteValue(first)
				else:
					node.updateValue(first,dist)
	
	def basic(self):
		self.setup("basic")


		"""TO DO IMPLEMENT Basic"""

		#Reset Values for Next Algorithm
		self.network = [] #list of nodes
		self.events = [] #list of events and their descriptions
		self.nodeNames = [] # a list of names of all nodes
		self.currentRound = 0 #current round

	def splitHorizon(self):
		self.setup("splith")

		"""TO DO IMPLEMENT SPLIT HORIZON"""

		#Reset values for next algorithm
		self.network = [] #list of nodes
		self.events = [] #list of events and their descriptions
		self.nodeNames = [] # a list of names of all nodes
		self.currentRound = 0 #current round

	def splitHorizonPV(self):
		self.setup("splithpv")

		"""TO DO IMPLEMENT SPLIT HORIZON POISONED REVERSE"""

		#Reset values for next algorithm
		self.network = [] #list of nodes
		self.events = [] #list of events and their descriptions
		self.nodeNames = [] # a list of names of all nodes
		self.currentRound = 0 #current round

	def getNodeByName(self,name):
		for node in self.network:
			if(node.getName() == name):
				return node
if __name__ == "__main__":
	m = Main("initial.txt","","")
	m.setup()
