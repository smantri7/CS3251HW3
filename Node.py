import math
class Node:
    #Vector is a 2D list [[name,distance taken,next hop, hops needed]]
    def __init__(self, name,vector):
        self.name = name
        self.vector = vector
        self.neighbors = {} #dictionary (neighborname, direct distance) DO NOT USE FOR Optimization!
        self.previous = []

    def advertise(self,n):
        for tup in self.vector:
            if(tup[0] == n):
                return tup
                
    def getName(self):
        return self.name

    def getValue(self,name):
        for v in self.vector:
            if(v[0] == name):
                return v
        return None

    def getPrevious(self):
        return self.previous

    def setPrevious(self,vectors):
        self.previous = vectors
    def getNList(self):
        return self.neighbors

    def addNeighbor(self,neigh,val):
        self.neighbors[neigh] = val        

    def delNeighbor(self,neigh):
        del self.neighbors[neigh]

    def getHopsTo(self,nodeName):
        for vec in self.vector:
            if(vec[0] == nodeName):
                return vec[3]

    def updateValue(self,name,value,hops,hopsneeded):
        newTup = [name,value,hops,hopsneeded]
        for v in self.vector:
            if(v[0] == name):
                self.vector.remove(v)
                self.vector.append(newTup)
                return

    def deleteValue(self,name):
        tup = (name,-1,"-1",-1)
        for v in self.vector:
            if(v[0] == name):
                v = tup
                return

    def addValue(self,name,dist,hops,hopsneeded):
        tup = [name,dist,hops,hopsneeded]
        if tup not in self.vector:
            self.vector.append(tup)

    def getVector(self):
        return self.vector

    def updateVector(self,newVec):
        self.vector = newVec

    def updateVectorByName(self, newVec):
        for i in range(len(self.vector)):
            if(newVec[0] == self.vector[i][0]):
                self.vector[i] =  newVec

    def contains(self,name):
        for tup in self.vector:
            if(name == tup[0][0]):
                return True
        return False

    def getVectorByName(self,name):
        for vec in self.vector:
            if(name == vec[0]):
                return vec
        return None

    def getDistanceTo(self,nodeName):
        for vec in self.vector:
            if(nodeName == vec[0]):
                return vec[1]
        return None

    def printVector(self,numNodes):
        ans = self.name + " "
        for i in range(numNodes):
            v = self.getVectorByName(str(i + 1))
            #ans += str(v[2]) + "," + str(v[3])  + "  "
            ans += str(v[2]) + "," + str(v[3])  + "," + str(v[1]) + "  "
        return ans

