""" 
Copyright 2021 Isaac Markovitz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """
triplets = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

class node:
    def __init__(self, layer, parent, board):
        self.layer = layer
        self.parent = parent
        self.board = board
        self.children = []
        self.isTerminal = False
        self.value = None
        for indexlist in triplets:
            k = []
            for j in indexlist:
                k.append(self.board[j])
            if (k[0] == k[1]) and (k[0] == k[2]):# runs if all of the elements in k are equal (ie there is only one type of mark in that triplet)
                if self.board[j] == 1 or self.board[j] == -1:
                    self.isTerminal = True
                    self.value = self.board[j]
        if not(self.isTerminal):
            try:
                a = self.board.index(0)
            except ValueError:
                self.isTerminal = True
                self.value = 0
        if not(self.isTerminal):
            playIndex = 0
            for i in self.board:
                if i == 0:
                    self.tmpBoard = []
                    for j in self.board:
                        self.tmpBoard.append(j)
                    self.playcode = 0
                    if self.layer % 2 == 0:
                        self.playcode = 1
                    else:
                        self.playcode = -1
                    self.tmpBoard[playIndex] = self.playcode
                    self.children.append([playIndex, node((self.layer + 1), self, self.tmpBoard)])
                playIndex += 1
        
                    

root = node(0, None, [0,0,0,0,0,0,0,0,0])

def findValue(node):
    if node.isTerminal:
        return(node.value)
    if node.value == None:
        node.childValues = []
        for child in node.children:
            node.childValues.append(findValue(child[1]))
    if node.layer % 2 == 0:
        node.value = max(node.childValues)
    else:
        node.value = min(node.childValues)
    return(node.value)

findValue(root)

gameOver = False
currentNode = root
int2strMap = {-1: "X", 0: " ", 1: "O"}
while not(gameOver):
    currentMap = currentNode.board
    j = 0
    for i in currentMap:
        currentMap[j] = int2strMap[i]
        j += 1
    print(" ", end="")
    print(*currentMap[0:3], sep=' | ')
    print('---+---+---')
    print(" ", end="")
    print(*currentMap[3:6], sep=' | ')
    print('---+---+---')
    print(" ", end="")
    print(*currentMap[-3:], sep=" | ")
    print()
    if currentNode.isTerminal:
        gameOver = True
        if currentNode.value == 0:
            print('Draw!')
        else:
            if currentNode.value == -1:
                winner = 'player'
            if currentNode.value == 1:
                winner = 'computer'
            print(winner, 'wins!')
    else:
        if currentNode.layer % 2 == 0:
            print('Computer to play...')
            j = 0
            for i in currentNode.childValues:
                if i == 1:
                    if currentNode.children[j][1].isTerminal:
                        nextNode = currentNode.children[j][1]
                else:
                    nextNode = currentNode.children[currentNode.childValues.index(max(currentNode.childValues))][1]
                j += 1

        else:
            print('Human to play...')
            invalid = True
            while invalid:
                humanMoveStr = input("input a number between 0 and 8 inclusive to indicate which position you would like to play: ")
                try:
                    humanMoveInt = int(humanMoveStr)
                except:
                    print('input provided in an invalid format')
                    continue
                if (humanMoveInt < 0) or (humanMoveInt > 8):
                    print('input out of range')
                    continue
                playIndices = []
                posTaken = True
                for i in currentNode.children:
                    if i[0] == humanMoveInt:
                        nextNode = i[1]
                        posTaken = False
                        invalid = False
                if posTaken:
                    print('position already occupied')

        currentNode = nextNode
    
