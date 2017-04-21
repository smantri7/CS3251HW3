from Node import Node
import queue
import math
class Main:
    
    def __init__(self,initial,events,flag):
        self.initial = initial #file with initial 
        self.eventFile = events
        self.flag = flag #string with algorithm to use
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round
        self.previous = [] #keep track of previous vectors, used to check for convergence

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
                    node.addValue(second,int(dist),second,1)
                    node.addValue(first,0,first,0)
                    node.addNeighbor(second)
                elif(node.getName() == second):
                    node.addValue(first,int(dist),first,1)
                    node.addValue(second,0,second,0)
                    node.addNeighbor(first)
        f.close()
        for node in self.network:
            for name in self.nodeNames: 
                if(node.contains(name) is False):
                    node.addValue(name,-1,"-1",-1)
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
            if n[0] in node.getNList():
                neighbor = self.getNodeByName(n[0])
                for vector in neighbor.getVector():
                    print("Current Node to Update: ",node.getName())
                    print("Current vector: ",vector[0])
                    print("Current n vec: ",n[0])

                    old = node.getVectorByName(vector[0])[1]
                    new = vector[1] + n[1]
                    print("Old: ",old)
                    print("New: ",new)
                    if(vector[1] != -1 and vector[0] != n[2]):
                        if(new < old or old == -1):
                            newHops = n[3]
                            newHops += 1
                            print("Updated!")
                            node.updateVectorByName((vector[0], new, neighbor.getName(),newHops))
                    print("_____")

    def updateVectorTableSplitHorizon(self,node):
        for n in node.getVector():
            if n[0] in node.getNList():
                neighbor = self.getNodeByName(n[0])
                for vector in neighbor.getVector():
                    new = vector[1] + n[1]
                    old = node.getVectorByName(vector[0])[1]
                    if(vector[2] == node.getName()):
                        if(vector[1] != -1):
                            if(new < old or old == -1):
                                #print("Updated: ",(vector[0], new, str(neighbor.getName())))
                                newHops = n[3]
                                newHops += 1
                                node.updateVectorByName((vector[0], new, neighbor.getName(),newHops))
    
    def updateVectorTableSplitHorizonPoisonReverse(self,node):
        for n in node.getVector():
            if n[0] in node.getNList():
                neighbor = self.getNodeByName(n[0])
                for vector in neighbor.getVector():
                    new = vector[1] + n[1]
                    old = node.getVectorByName(vector[0])[1]
                    if(vector[2] != node.getName()):
                        new = math.inf
                    if(vector[1] != -1):
                        if(new < old or old == -1):
                            #print("Updated: ",(vector[0], new, str(neighbor.getName())))
                            newHops = n[3]
                            newHops += 1
                            node.updateVectorByName((vector[0], new, neighbor.getName(),newHops))

    def doEvent(self,curRound):
        for i in range(len(self.events)):
            if self.events[i][0] == curRound:
                self.updateEvent(self.events[i])
                #remove event after use
                del self.events[i]
                return True
        return False

    def updateEvent(self,event):
        print("Event Occurred")
        first = event[1]
        second = event[2]
        dist = event[3]
        for node in self.network:
            if(node.getName() == first):
                if(dist == -1):
                    #kill the link with the other node
                    node.updateValue(second,-1,-1,-1)
                    #kill neighbor pointer
                    node.delNeighbor(second)
                else:
                    #else update the other link
                    #print("Updated path: ", node.getName() + " - " + second)
                    node.updateValue(second,dist,second,0)
                    #add as neighbor if not in list
                    node.addNeighbor(second)
                    #print("New Vector: ", node.getVector())
            elif(node.getName() == second):
                if(dist == -1):
                    node.updateValue(first,-1,-1,-1)
                    node.delNeighbor(first)
                else:
                    #print("Updated path: ", node.getName() + " - " + first)
                    node.updateValue(first,dist,first,0)
                    node.addNeighbor(first)
        for node in self.network:
            print("For node " + str(node.getName()) , node.getVector())
    def checkConvergence(self):
        temp = []
        if(len(self.previous) == 0):
            for node in self.network:
                temp += node.getVector()
            self.previous = temp
            return False
        for node in self.network:
            temp += node.getVector()
        for x in range(len(temp)):
            if(temp[x] != self.previous[x]):
                self.previous = temp
                return False
        return True

    def basic(self):
        self.setup("basic")
        converged = False
        count = 0
        while True:
            if(self.flag == 1):
                print("At Round: ",self.currentRound)
                for node in self.network:
                    print("For node " + str(node.getName()) , node.getVector())
                self.getVectors()
            if(self.checkConvergence() and converged):
                print("OUT")
                break
            self.doEvent(self.currentRound)
            if(len(self.events) == 0):
                converged = True
                count = self.currentRound
            for node in self.network:
                self.updateVectorTable(node)
            if(self.currentRound - count > 100):
                print("Error: Count to infinity Problem detected. Ending this program.")
                return
            self.currentRound += 1
        print("Converged at Round: ", self.currentRound)
        self.getVectors()
        print("Convergence Delay: ", self.currentRound - count + 1)

        #Reset Values for Next Algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round
        self.previous = []

    def splitHorizon(self):
        self.setup("splith")

        """TO DO IMPLEMENT SPLIT HORIZON"""
        converged = False
        count = 0
        while True:
            if(self.flag == 1):
                print("At Round: ",self.currentRound)
                self.getVectors()
            self.doEvent(self.currentRound)
            if(len(self.events) == 0):
                converged = True
                count = self.currentRound
            for node in self.network:
                self.updateVectorTableSplitHorizonPoisonReverse(node)
            if(self.currentRound - count > 100):
                print("Error: Count to infinity Problem detected. Ending this program.")
                return
            if(self.checkConvergence() and converged):
                break
            self.currentRound += 1
        print("Converged at Round: ", self.currentRound)
        self.getVectors()
        print("Convergence Delay: ", self.currentRound - count + 1)
        #Reset values for next algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round
        self.previous = []

    def splitHorizonPV(self):
        self.setup("splithpv")

        converged = False
        count = 0
        while True:
            if(self.flag == 1):
                print("At Round: ",self.currentRound)
                self.getVectors()
            self.doEvent(self.currentRound)
            if(self.checkConvergence() and converged):
                break
            if(len(self.events) == 0):
                converged = True
                count = self.currentRound
            for node in self.network:
                self.updateVectorTableSplitHorizonPoisonReverse(node)
            if(self.currentRound - count > 100):
                print("Error: Count to infinity Problem detected. Ending this program.")
                return
            self.currentRound += 1
        print("Converged at Round: ", self.currentRound)
        self.getVectors()
        print("Convergence Delay: ", self.currentRound - count + 1)
        #Reset values for next algorithm
        self.network = [] #list of nodes
        self.events = [] #list of events and their descriptions
        self.nodeNames = [] # a list of names of all nodes
        self.currentRound = 1 #current round
        self.previous = []

    def getNodeByName(self,name):
        for node in self.network:
            if(node.getName() == name):
                return node

    def getVectors(self):
        #print("Round: ",self.currentRound)
        col = "   "
        for i in range(len(self.network)):
            col += str(i + 1) + "    "
        print(col)
        for node in self.network:
            print(node.printVector(len(self.network)))

if __name__ == "__main__":
    m = Main("initial.txt","event.txt",1)
    ma = Main("initial.txt","event.txt",1)
    ma.basic()
    #m.splitHorizonPV()
