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

    def updateValue(self,name,value):
        for v in self.vector:
            if(v[0] == name):
                v[1] = value
                return

    def deleteValue(self,name):
        for v in self.vector:
            if(v[0] == name):
                self.vector.remove(v)

    def addValue(self,name,dist):
        tup = (name,dist)
        if tup not in self.vector:
            self.vector.append(tup)

    def getVector(self):
        return self.vector

    def updateVector(self,newVec):
        self.vector = newVec
