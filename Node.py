class Node:
    #Vector is a list of tuples [(name,distance taken,hops needed)]
    def __init__(self, name,vector):
        self.name = name
        self.vector = vector

    def getName(self):
        return self.name

    def getValue(self,name):
        for v in self.vector:
            if(v[0] == name):
                return v
        return None

    def getHops(self):
        return self.vector[2]

    def updateValue(self,name,value,hops):
        newTup = (name,value,hops)
        for v in self.vector:
            if(v[0] == name):
                self.vector.remove(v)
                self.vector.append(newTup)
                return

    def deleteValue(self,name):
        tup = (name,-1,"-1")
        for v in self.vector:
            if(v[0] == name):
                v = tup
                return

    def addValue(self,name,dist,hops):
        tup = (name,dist,hops)
        if tup not in self.vector:
            self.vector.append(tup)

    def getVector(self):
        return self.vector

    def updateVector(self,newVec):
        self.vector = newVec

    def contains(self,name):
        for tup in self.vector:
            if(name in tup[0]):
                return True
        return False

    def getVectorByName(self,name):
        for vec in self.vector:
            if(name == vec[0]):
                return vec
        return None

    def printVector(self,numNodes):
        ans = self.name + " "
        for i in range(numNodes):
            v = self.getVectorByName(str(i + 1))
            if(self.name == v[0]):
                ans += "0,0" + "  "
            else:
                ans += str(v[2]) + "," + str(v[1])  + "  "
        return ans

