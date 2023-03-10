class tree:
    
    def __init__(self, move, depth = 1, metadata = None, isendnode = False, count = 1):
        self.move = move
        self.children = []
        self.depth = depth
        self.metadata = metadata
        self.isendnode = isendnode
        self.count = count
        
    def addChild(self, child):
        self.children.append(child)
    
    def addChildren(self, children):
        self.children.extend(children)
    
    def getChildren(self):
        return self.children
    
    def setChildren(self, children):
        self.children = children
    
    def getDepth(self):
        return self.turn
    
    def setDepth(self, depth):
        self.turn = depth
    
    def getMetadata(self):
        return self.metadata
    
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
    
    def createChildren(self, move, endnode = False):
        for child in self.getChildren():
            if child.getMove() == move:
                child.setCount(child.getCount() + 1)
                return
        self.addChild(tree(move, self.getDepth() + 1, self.metadata, endnode))
    
    
    # def printTree(self):
    #     print(self.getMetadata())
    #     for child in self.getChildren():
    #         child.printTree()