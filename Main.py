from Node import Node
import queue
import math
from operator import itemgetter 
import sys
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
                    node.addNeighbor(second,int(dist))
                elif(node.getName() == second):
                    node.addValue(first,int(dist),first,1)
                    node.addValue(second,0,second,0)
                    node.addNeighbor(first,int(dist))
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
    def updateVectorTable(self,node,updateDict):
        for y in node.getVector():
            routes = []
            for v in node.getNList().keys():
                v = self.getNodeByName(v)
                newdvy = self.getAdvertised(v,y[0])
                dvy = [newdvy[0],newdvy[1],newdvy[2],newdvy[3]]
                neg = (dvy[1] == -1)
                dvy[1] += self.getReal(node,v.getName())
                dvy[3] += 1
                dvy[2] = v.getName()
                if(dvy[0] != node.getName() and not neg): #route to itself should always stay the same
                    routes.append(dvy)
            if(len(routes) != 0): #Make sure routes to that node are existent
                best = sorted(routes,key=itemgetter(1))[0]
                updateDict[node.getName()].append(best)
        return updateDict

    def updateVectorTableSplitHorizon(self,node,updateDict):
        for y in node.getVector():
            routes = []
            for v in node.getNList().keys():
                v = self.getNodeByName(v)
                newdvy = self.getAdvertised(v,y[0])
                dvy = [newdvy[0],newdvy[1],newdvy[2],newdvy[3]]
                neg = (dvy[1] == -1)
                flag = dvy[2]
                dvy[1] += self.getReal(node,v.getName())
                dvy[3] += 1
                dvy[2] = v.getName()
                if(dvy[0] != node.getName() and not neg): #route to itself should always stay the same
                    if flag != node.getName():
                        routes.append(dvy)
            if(len(routes) != 0): #Make sure routes to that node are existent
                best = sorted(routes,key=itemgetter(1))[0]
                updateDict[node.getName()].append(best)
        return updateDict
    
    def updateVectorTableSplitHorizonPoisonReverse(self,node,updateDict):
        for y in node.getVector():
            routes = []
            for v in node.getNList().keys():
                v = self.getNodeByName(v)
                newdvy = self.getAdvertised(v,y[0])
                dvy = [newdvy[0],newdvy[1],newdvy[2],newdvy[3]]
                neg = (dvy[1] == -1)
                flag = dvy[2]
                dvy[1] += self.getReal(node,v.getName())
                dvy[3] += 1
                dvy[2] = v.getName()
                if(dvy[0] != node.getName() and not neg): #route to itself should always stay the same
                    if flag != node.getName():
                        routes.append(dvy)
                    else:
                        dvy[1] = float(math.inf)
                        routes.append(dvy)
            if(len(routes) != 0): #Make sure routes to that node are existent
                best = sorted(routes,key=itemgetter(1))[0]
                updateDict[node.getName()].append(best)
        return updateDict

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
                    #kill neighbor pointer
                    node.delNeighbor(second)
                else:
                    #else update the other link
                    node.addNeighbor(second,dist)
                    #node.updateValue(second,-1,"-1",-1)
                    #print("New Vector: ", node.getVector())
            elif(node.getName() == second):
                if(dist == -1):
                    node.delNeighbor(first)
                else:
                    #print("Updated path: ", node.getName() + " - " + first)
                    node.addNeighbor(first,dist)
                    #node.updateValue(first,-1,"-1",-1)
        #Now we fix any of first's vectors going through second and vice versa
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
        queue = []
        while True:
            if(self.flag == 1):
                #print("At Round: ",self.currentRound)
                vecs = self.getVectors()
                queue.append((self.currentRound,vecs))
            if(self.checkConvergence() and converged):
                break
            event = self.doEvent(self.currentRound)
            if(len(self.events) == 0 and not converged):
                converged = True
                count = self.currentRound

            #Update Code Starts
            #before update, set previous
            updateDict = {}
            for namae in self.nodeNames:
                updateDict[namae] = []
            for node in self.network:
                updateDict = self.updateVectorTable(node,updateDict)

            for y in updateDict.keys():
                swag = self.getNodeByName(y)
                for suc in updateDict[y]:
                    swag.updateVectorByName(suc)
            #Update Code Ends


            if(self.currentRound - count > 100):
                return "Error: Count to infinity Problem detected. Ending this program."
            self.currentRound+= 1
        ans = ""
        for i in range(len(queue) - 1):
            ans += "At round: " + str(queue[i][0]) + "\n"
            ans += queue[i][1] + "\n"
        if(self.flag == 0):
            ans += self.getVectors() + "\n"
        ans += "Converged at Round: " + str(self.currentRound - 1) + "\n"
        ans += "Convergence Delay: " +  str(self.currentRound - count - 1) + "\n"
        return ans
    def splitHorizon(self):
        self.setup("splith")
        converged = False
        count = 0
        queue = []
        while True:
            if(self.flag == 1):
                #print("At Round: ",self.currentRound)
                vecs = self.getVectors()
                queue.append((self.currentRound,vecs))
            if(self.checkConvergence() and converged):
                break
            event = self.doEvent(self.currentRound)
            if(len(self.events) == 0 and not converged):
                converged = True
                count = self.currentRound
            #Update Code Starts
            #before update, set previous
            updateDict = {}
            for namae in self.nodeNames:
                updateDict[namae] = []
            for node in self.network:
                updateDict = self.updateVectorTableSplitHorizon(node,updateDict)

            for y in updateDict.keys():
                swag = self.getNodeByName(y)
                for suc in updateDict[y]:
                    swag.updateVectorByName(suc)
            #Update Code Ends


            if(self.currentRound - count > 100):
                return "Error: Count to infinity Problem detected. Ending this program."
            self.currentRound+= 1
        ans = ""
        for i in range(len(queue) - 1):
            ans += "At round: " + str(queue[i][0]) + "\n"
            ans += queue[i][1] + "\n"
        if(self.flag == 0):
            ans += self.getVectors() + "\n"
        ans += "Converged at Round: " + str(self.currentRound - 1) + "\n"
        ans += "Convergence Delay: " +  str(self.currentRound - count - 1) + "\n"
        return ans

    def splitHorizonPV(self):
        self.setup("splithpv")
        converged = False
        count = 0
        queue = []
        while True:
            if(self.flag == 1):
                #print("At Round: ",self.currentRound)
                vecs = self.getVectors()
                queue.append((self.currentRound,vecs))
            if(self.checkConvergence() and converged):
                break
            event = self.doEvent(self.currentRound)
            if(len(self.events) == 0 and not converged):
                converged = True
                count = self.currentRound
            #Update Code Starts
            #before update, set previous
            updateDict = {}
            for namae in self.nodeNames:
                updateDict[namae] = []
            for node in self.network:
                updateDict = self.updateVectorTableSplitHorizonPoisonReverse(node,updateDict)

            for y in updateDict.keys():
                swag = self.getNodeByName(y)
                for suc in updateDict[y]:
                    swag.updateVectorByName(suc)
            #Update Code Ends
            if(self.currentRound - count > 100):
                return "Error: Count to infinity Problem detected. Ending this program.\n"
            self.currentRound+= 1
        ans = ""
        for i in range(len(queue) - 1):
            ans += "At round: " + str(queue[i][0]) + "\n"
            ans += queue[i][1] + "\n"
        if(self.flag == 0):
            ans += self.getVectors() + "\n"
        ans += "Converged at Round: " + str(self.currentRound - 1) + "\n"
        ans += "Convergence Delay: " +  str(self.currentRound - count - 1) + "\n"
        return ans
    
    def getNodeByName(self,name):
        for node in self.network:
            if(node.getName() == name):
                return node

    def getAdvertised(self,node,neighbor):
        return node.getVectorByName(neighbor)

    def getReal(self,node,neigh):
        maps = node.getNList()
        return maps[neigh]

    def getVectors(self):
        #print("Round: ",self.currentRound)
        ans = ""
        col = "   "
        for i in range(len(self.network)):
            col += " " + str(i + 1) + "     "
        ans += col + "\n"
        for node in self.network:
            ans += node.printVector(len(self.network)) + "\n"
        return ans

if __name__ == "__main__":
    f = open("ans.txt",'w')
    #initial.txt event.txt flag
    m = Main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
    ma = Main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
    maa = Main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
    f.write("Basic: \n")
    f.write(ma.basic())
    f.write("____________________________________\n")
    f.write("Split Horizon: \n")
    f.write(maa.splitHorizon())
    f.write("____________________________________\n")
    f.write("Split Horizon Poison Reverse: \n")
    f.write(m.splitHorizonPV())
    f.write("____________________________________")
    f.close()