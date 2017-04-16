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
			print("TODO")
		elif protocol == "splith":
			print("TODO")
		elif protocol == "splithpv":
			print("TODO")

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
if __name__ == "__main__":
	m = Main("initial.txt","","")
	m.setup()
