from Node import Node
import queue
class Main:
    
    def __init__(self,initial,events,flag):
        self.initial = initial #file with initial 
        self.eventFile = events
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
                if(node.getName() == first):
                    node.addValue(second,int(dist),"0")
                    node.addValue(first,0,"0")
                elif(node.getName() == second):
                    node.addValue(first,int(dist),"0")
                    node.addValue(second,0,"0")
        f.close()
        for node in self.network:
            for name in self.nodeNames: 
                if(node.contains(name) is False):
                    node.addValue(name,-1,"-1")
        #queue future updates for network events
        f = open(self.eventFile,"r")
        for line in f.readlines():
            line = line.split(" ")
            time = int(line[0])
            dist = int(line[3])
            self.events.append([time,line[1],line[2],dist]) 
        f.close()

    #finds best path using UCS with each router sharing only each other's DV
    def findBestPath(self,node,dest):
        q = []
        atgoal = []
        #Root contains state,actionlist,total cost
        actionList = []
        root = (node,actionList,"0")
        visitedList = []
        q.append((0,root))

        while len(q) != 0:
            n = q.pop()
            noder = n[1][0]
            actionList = n[1][1]
            if noder.getName() == dest:
                return (len(actionList) - 1,n[1][2])
            if noder not in visitedList:
                visitedList = visitedList + [noder]
                for child in noder.getVector():
                    if child[0] not in visitedList:
                        #Calculate the total cost of this so we can add it to priority queue appropriately
                        cost = sum(actionList + [child[1]])
                        newnode = (self.getNodeByName(child[0]),actionList + [child[1]],str(noder.getName()))
                        #Priority Queue takes care of pushing by cost calculations.
                        q.append((cost,newnode))
            q.sort()

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
        for node in self.network:
            print(node.getName() + ": ",node.getVector())
        self.getVectors()

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

    def getVectors(self):
        print("Round: ",self.currentRound)
        col = "   "
        for i in range(len(self.network)):
            col += str(i) + "    "
        print(col)
        for node in self.network:
            print(node.printVector(len(self.network)))

if __name__ == "__main__":
    m = Main("initial.txt","event.txt",0)
    m.basic()
