class tree:
    
    def __init__(self, move, parent = None, depth = 0, stats = [0,0,0], metadata = None,isendnode = True, count = 1):
        self.move = move
        self.children = []
        self.depth = depth
        self.metadata = metadata
        self.isendnode = isendnode
        self.count = count
        self.isroot = False
        self.parent = parent
        self.stats = stats
        
    def addChild(self, child):
        self.children.append(child)
        if self.getChildren() != []:
            self.setIsEndNode(False)
            self.setStats([0,0,0])
        
    def setRoot(self, isroot):
        self.isroot = isroot
        self.count = 0
    
    def getRoot(self):
        return self.isroot
    
    def addChildren(self, children):
        self.children.extend(children)
        if self.getChildren() != []:
            self.setIsEndNode(False)
            self.setStats([0,0,0])

    
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
    
    def setStats(self, stats):
        self.stats = stats
    
    def getStats(self):
        return self.stats
    
    def addwin(self):
        self.stats[0] += 1
    
    def addloss(self):
        self.stats[1] += 1
    
    def adddraw(self):
        self.stats[2] += 1
    
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
        color = ""
        for parent in self.getParents():
            if parent.getDepth()%2 == 0:
                color = "B"
            else:
                color = "W"
            parent_moves.append(f"{color}, {parent.getMove()}")
        parent_moves.reverse()
        if self.getDepth()%2 == 0:
            color = "B"
        else:
            color = "W"
        self.setStats(self.getstatsfromchildren())
        metadata = f"depth: {self.getDepth()}, previous moves: {parent_moves}, move: {color} {self.getMove()}, counted: {self.getCount()}, Whitewins: {self.getStats()[0]}, Blackwins: {self.getStats()[1]}, draws: {self.getStats()[2]}"
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

    def createChildren(self, move, stat):
        for child in self.getChildren():
            if child.getMove() == move:
                child.setCount(child.getCount() + 1)
                if child.getIsEndNode():
                    cstats = child.getStats()
                    child.setStats([cstats[0] + stat[0], cstats[1] + stat[1], cstats[2] + stat[2]])
                return
        self.addChild(tree(move, self, self.getDepth() + 1, stat))
    
    def getstatsfromchildren(self):
        if self.getIsEndNode():
            return self.getStats()
        else:
            stats = [0,0,0]
            for child in self.getChildren():
                cstats = child.getstatsfromchildren()
                stats[0] += cstats[0]
                stats[1] += cstats[1]
                stats[2] += cstats[2]
            return stats
        
    
    def printTreetodepth(self, depth = 0):
        if self.getRoot():
            print("root node")
            for child in self.getChildren():
                child.printTreetodepth(depth)
        elif self.getDepth() <= depth:
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetodepth(depth)

    def printTreetocount(self, limit = 0, document = None):
        if self.getRoot():
            print("root node")
            table = document.getdocument().add_table(rows=1, cols=1)
            table.cell(0,0).text = "root node"
            for child in self.getChildren():
                child.printTreetocount(limit, table)
        elif self.getCount() >= limit:
            if document != None:
                new_row = document.add_row()
                new_row.cells[0].text = self.getMetadata()
            print(self.getMetadata())
            for child in self.getChildren():
                child.printTreetocount(limit, document)
        if document != None and self.getRoot():
            document.getdocument().add_page_break()