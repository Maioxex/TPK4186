class tree:
    
    def __init__(self, move, depth = 1, metadata = None, isendnode = True, count = 1):
        self.move = move
        self.children = []
        self.depth = depth
        self.metadata = metadata
        self.isendnode = isendnode
        self.count = count
        self.isroot = False
        
    def addChild(self, child):
        self.children.append(child)
        if self.getChildren() != []:
            self.setIsEndNode(False)
        
    def setRoot(self, isroot):
        self.isroot = isroot
    
    def getRoot(self):
        return self.isroot
    
    def addChildren(self, children):
        self.children.extend(children)
        if self.getChildren() != []:
            self.setIsEndNode(False)
    
    def getChild(self, move):
        for child in self.getChildren():
            if child.getMove() == move:
                return child
        return None
    
    def getChildren(self):
        return self.children
    
    def setChildren(self, children):
        self.children = children
        if self.getChildren() != []:
            self.setIsEndNode(False)
    
    def getDepth(self):
        return self.depth
    
    def setDepth(self, depth):
        self.depth = depth
    
    def getMetadata(self):
        if self.metadata == None:
            self.createBaseMetadata()
        return self.metadata

    def createBaseMetadata(self):
        self.metadata = f"depth:{self.getDepth()}, {self.getMove()}, counted:{self.getCount()}"
    
    def setMetadata(self, metadata):
        self.metadata = metadata
    
    def getIsEndNode(self):
        return self.isendnode
    
    def setIsEndNode(self, isendnode):
        self.isendnode = isendnode
    
    def getCount(self):
        return self.count
    
    def setCount(self, count):
        self.count = count
    
    def getMove(self):
        return self.move
    
    def setMove(self, move):
        self.move = move
    
    def createChildren(self, move):
        for child in self.getChildren():
            if child.getMove() == move:
                child.setCount(child.getCount() + 1)
                return
        self.addChild(tree(move, self.getDepth() + 1, self.metadata))
    
    def printTreetodepth(self, depth = 0):
        if self.getRoot():
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetodepth(depth)
        elif self.getDepth() <= depth:
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetodepth(depth)

    def printTreetocount(self, limit = 0):
        if self.getRoot():
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetocount(limit)
        elif self.getCount() >= limit:
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetocount(limit)