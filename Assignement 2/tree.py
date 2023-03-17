class tree:
    
    def __init__(self, move, parent = None, depth = 0, metadata = None, isendnode = True, count = 1):
        self.move = move
        self.children = []
        self.depth = depth
        self.metadata = metadata
        self.isendnode = isendnode
        self.count = count
        self.isroot = False
        self.parent = parent
        
    def addChild(self, child):
        self.children.append(child)
        if self.getChildren() != []:
            self.setIsEndNode(False)
        
    def setRoot(self, isroot):
        self.isroot = isroot
        self.count = 0
    
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
        parent_moves = []
        for parent in self.getParents():
            parent_moves.append(parent.getMove())
        parent_moves.reverse()
        metadata = f"depth: {self.getDepth()}, previous moves: {parent_moves}, move: {self.getMove()}, counted: {self.getCount()}"
        self.setMetadata(metadata)
    
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

    def getParent(self):
        return self.parent
    
    def setParent(self, parent):
        self.parent = parent
    
    def getParents(self):
        parentsmove = []
        if self.getParent().getRoot():
            return parentsmove
        if self.getParent() != None:
            parentsmove.append(self.getParent())
            parentsmove.extend(self.getParent().getParents())
        return parentsmove

    def createChildren(self, move):
        for child in self.getChildren():
            if child.getMove() == move:
                child.setCount(child.getCount() + 1)
                return
        self.addChild(tree(move, self, self.getDepth() + 1, self.metadata))
    
    def printTreetodepth(self, depth = 0):
        if self.getRoot():
            print("root node")
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