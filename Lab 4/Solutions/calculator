import operator
import sys
from enum import Enum


def getPriorityOperator(value):
    if value == '-' or value == '+':
        return 1
    elif value == '*' or value == '/':
        return 2
    else:
        return 0

def getOperation(value):
    if value == '+':
        return operator.add
    elif value == '-':
        return operator.sub
    elif value == '*':
        return operator.mul
    else:
        return operator.truediv


def isOperator(value):
    if value == '+' or value == '-' or value == '*' or value == '/':
        return True
    return False

def infixToPrefix(infix):
    stack = []
    prefix = []

    infix=infix[::-1]
    infix=infix.replace(')',"_")
    infix=infix.replace('(',")")
    infix=infix.replace('_',"(")

    exp=infix

    numberReady=True
    if isOperator(exp[0]) or exp[0]==')' or exp[0]=='(':
        numberReady=False

    for i in range(0, len(exp)):

        if exp[i] == '(':
            numberReady=True
            stack.append(exp[i])
        elif exp[i] == ')':
            numberReady = True
            value = stack.pop()
            while value is not '(':
                prefix.append(value)
                value = stack.pop()
        elif isOperator(exp[i]):

            numberReady = True
            if(len(stack)==0):
                stack.append(exp[i])
            else:
                value=stack.pop()

                if (getPriorityOperator(exp[i]) >= getPriorityOperator(value)):
                    stack.append(value)
                    stack.append(exp[i])
                else:
                    while len(stack) is not 0:

                        if getPriorityOperator(exp[i]) <= getPriorityOperator(value):
                            prefix.append(value)
                        else:
                            stack.append(value)
                            stack.append(exp[i])
                            break
                        value = stack.pop()

                    else:
                        if getPriorityOperator(exp[i]) <= getPriorityOperator(value):
                            prefix.append(value)
                        else:
                            stack.append(value)
                            stack.append(exp[i])
                            break
                        stack.append(exp[i])
        else:
            number = ""
            if numberReady==True:
                for j in range(i, len(exp)):
                    if isOperator(exp[j]) or exp[j]==')' or exp[j]=='(':
                        break;
                    number+=exp[j]
                numberReady=False
                number=number[::-1]

                prefix.append(number)


    while len(stack) is not 0:
        prefix.append(stack.pop())

    prefix=prefix[::-1]
    return prefix


class Node:
    def __init__(self,value):
        self.value=value
        self.lChild=None
        self.rChild=None

    def printNodes(self,str,start):
        print(start+str+"  "+self.value)
        start+=" "
        if self.lChild is not None:
            self.lChild.printNodes(start+str+"─",start)
        if self.rChild is not None:
            self.rChild.printNodes(start+str+"─",start)

    def solve(self):

        if isOperator(self.value):
            return getOperation(self.value)(self.lChild.solve(),self.rChild.solve())
        else:
            return float(self.value)

class Tree:
    def __init__(self):
        self.root=None

    def addNode(self,value):
        if self.root is None:
            self.root = Node(value)
        else:
            current=self.root
            path = list()

            while current is not None:
                if isOperator(current.value):

                    if current.lChild is None:
                        current.lChild = Node(value)
                        current=None
                    elif isOperator(current.lChild.value):
                        path.append(current)
                        current = current.lChild
                    elif current.rChild is None:
                        current.rChild = Node(value)
                        current = None
                    elif isOperator(current.rChild.value):
                        path.append(current)
                        current = current.rChild
                    else:
                        parent = path.pop()
                        if parent.rChild is None:
                            parent.rChild = Node(value)
                            current = None
                        else:
                            current = parent.rChild


    def buildTree(self,prefix):
         for elem in prefix:
             self.addNode(elem)


    def printTree(self):
        self.root.printNodes("├──","   ")
        print()

    def solve(self):
        print(infix+" = " + str(self.root.solve()))



#infix = input("Wpisz równanie:")
infix = sys.argv[1]
tree = Tree()
tree.buildTree(infixToPrefix(infix))
tree.printTree()
tree.solve()
