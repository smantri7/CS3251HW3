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
        self.currentRound = 1 #current round

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
                    node.addValue(second,int(dist),0)
                    node.addValue(first,0,0)
                elif(node.getName() == second):
                    node.addValue(first,int(dist),0)
                    node.addValue(second,0,0)
        f.close()
        for node in self.network:
            for name in self.nodeNames: 
                if(node.contains(name) is False):
                    node.addValue(name,-1,-1)
        #queue future updates for network events
        f = open(self.eventFile,"r")
        for line in f.readlines():
            line = line.split(" ")
            time = int(line[0])
            dist = int(line[3])
            self.events.append([time,line[1],line[2],dist]) 
        f.close()

    #finds best path using Bellman Ford with each router sharing only each other's DV
    def updateVectorTable(self,node):
        for n in node.getVector():
            neighbor = self.getNodeByName(n[0])
            for vector in neighbor.getVector():
                current = n[1]
                vector = vector[1]
                other = n.getVectorByName(n[0])[1]
                if(current < other + vector):
                    #update

    def doEvent(self,curRound):
        for i in range(len(self.events)):
            if self.events[i][0] == curRound:
                self.updateEvent(self.events[i])
                #remove event after use
                del self.events[i]
                return True
        return False

    def updateEvent(self,event):
        first = event[1]
        second = event[2]
        dist = event[3]
        for node in self.network:
            if(node.getName() == first):
                if(dist == -1):
                    #kill the link with the other node
                    node.updateValue(second,-1,-1)
                else:
                    #else update the other link
                    print("Updated path: ", node.getName() + " - " + second)
                    node.updateValue(second,dist,0)
                    print("New Vector: ", node.getVector())
            elif(node.getName() == second):
                if(dist == -1):
                    node.updateValue(first,-1,-1)
                else:
                    print("Updated path: ", node.getName() + " - " + first)
                    node.updateValue(first,dist,0)
    
    def basic(self):
        self.setup("basic")
        converged = False
        while self.currentRound < 5:
            if(self.flag == 1):
                #print("At Round: ",self.currentRound)
                #self.getVectors()
                pass
            e = self.doEvent(self.currentRound)
            for node in self.network:
                self.updateVectorTable(node)
            self.currentRound += 1

        """TO DO IMPLEMENT Basic"""

        #Reset Values for Next Algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round

    def splitHorizon(self):
        self.setup("splith")

        """TO DO IMPLEMENT SPLIT HORIZON"""

        #Reset values for next algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round

    def splitHorizonPV(self):
        self.setup("splithpv")

        """TO DO IMPLEMENT SPLIT HORIZON POISONED REVERSE"""

        #Reset values for next algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round

    def getNodeByName(self,name):
        for node in self.network:
            if(node.getName() == name):
                return node

    def getVectors(self):
        print("Round: ",self.currentRound)
        col = "   "
        for i in range(len(self.network)):
            col += str(i + 1) + "    "
        print(col)
        for node in self.network:
            print(node.printVector(len(self.network)))

if __name__ == "__main__":
    m = Main("initial.txt","event.txt",1)
    m.basic()
