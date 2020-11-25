#region Imports
import operator
import sys
from enum import Enum
from math import sqrt, fabs, log10, fmod, factorial
import tkinter as tk
from tkinter import font
#endregion

#region GlobalVar
PRINT_TREE = True
#endregion

#region GlobalFunc
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
    elif value == '/':
        return operator.truediv
    else:
        return operator.pow

def isOperator(value):
    if value == '+' or value == '-' or value == '*' or value == '/' or value == '^':
        return True
    return False

def infixToPrefix(infix):
    stack = []
    prefix = []

    infix = infix[::-1]
    infix = infix.replace(')', "_")
    infix = infix.replace('(', ")")
    infix = infix.replace('_', "(")

    exp = infix

    numberReady = True
    if isOperator(exp[0]) or exp[0] == ')' or exp[0] == '(':
        numberReady = False

    for i in range(0, len(exp)):

        if exp[i] == '(':
            numberReady = True
            stack.append(exp[i])
        elif exp[i] == ')':
            numberReady = True
            value = stack.pop()
            while value is not '(':
                prefix.append(value)
                value = stack.pop()
        elif isOperator(exp[i]):

            numberReady = True
            if (len(stack) == 0):
                stack.append(exp[i])
            else:
                value = stack.pop()

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
            if numberReady == True:
                for j in range(i, len(exp)):
                    if isOperator(exp[j]) or exp[j] == ')' or exp[j] == '(':
                        break;
                    number += exp[j]
                numberReady = False
                number = number[::-1]

                prefix.append(number)

    while len(stack) is not 0:
        prefix.append(stack.pop())

    prefix = prefix[::-1]
    return prefix
#endregion

#region NodeTree
class Node:
    def __init__(self, value):
        self.value = value
        self.lChild = None
        self.rChild = None

    def printNodes(self, str, start):
        print(start + str + "  " + self.value)
        start += " "
        if self.lChild is not None:
            self.lChild.printNodes(start + str + "─", start)
        if self.rChild is not None:
            self.rChild.printNodes(start + str + "─", start)

    def solve(self):
        if isOperator(self.value):
            if self.rChild == None:
                if isOperator(self.lChild.value):
                    return self.lChild.solve()
                else:
                    return -1 * float(self.lChild.value)
            else:
                return getOperation(self.value)(self.lChild.solve(), self.rChild.solve())
        else:
            return float(self.value)

class Tree:
    def __init__(self):
        self.root = None

    def addNode(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            current = self.root
            path = list()

            while current is not None:
                if isOperator(current.value):

                    if current.lChild is None:
                        current.lChild = Node(value)
                        current = None
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

    def buildTree(self, prefix):
        for elem in prefix:
            self.addNode(elem)

    def printTree(self, firstOperator=""):
        if PRINT_TREE == False:
            return

        prefixStr = "├──"

        if firstOperator != "":
            if firstOperator != "mod":
                print("   ├──" + firstOperator)
            prefixStr = "   ├──"

        self.root.printNodes(prefixStr, "   ")

    def solve(self):
        return self.root.solve()
#endregion

#region GUI

class GUI:
    def __init__(self):
        self.isError = False
        self.input = ""
        self.gui_buttons = ['sqrt(x)', 'x^y', 'x!', 'C', '/',
                            '|x|', '7', '8', '9', '*',
                            'mod(x)', '4', '5', '6', '-',
                            '1/x', '1', '2', '3', '+',
                            'log(x)', '(', ')', '0', '.',
                            '=']

        self.mathFunctionsString = ["sqrt", "|", "mod", "log", "!"]
        # |-abs
        # !-factorial

        self.functions = [self.buttonSqrtClick, self.buttonPowClick, self.buttonFactorialClick, self.buttonClearClick,
                          self.buttonDivClick
            , self.buttonAbsClick, self.button7Click, self.button8Click, self.button9Click, self.buttonMulClick
            , self.buttonModClick, self.button4Click, self.button5Click, self.button6Click, self.buttonSubClick
            , self.buttonInvClick, self.button1Click, self.button2Click, self.button3Click, self.buttonAddClick
            , self.buttonLogClick, self.buttonBracketLClick, self.buttonBracketRClick, self.button0Click,
                          self.buttonDotClick
            , self.buttonResultClick]

    def changeInputLabelValue(self, start="", end=""):
        if self.isError:
            return
        str = start
        str += self.text.get()
        str += end
        self.text.set(str)

    def changeIfZeroInInputLabel(self):
        if self.isError:
            return
        if self.text.get() == "0":
            self.text.set("")

    def buttonSqrtClick(self):
        self.changeInputLabelValue("sqrt(", ")")

    def buttonPowClick(self):
        self.changeInputLabelValue("(", ")^")

    def buttonFactorialClick(self):
        self.changeInputLabelValue("(", ")!")

    def buttonClearClick(self):
        self.isError = False
        self.textHistory.set("")
        self.text.set("0")

    def buttonDivClick(self):
        self.changeInputLabelValue(end="/")

    def buttonAbsClick(self):
        self.changeInputLabelValue("|", "|")

    def button7Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='7')

    def button8Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='8')

    def button9Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='9')

    def buttonMulClick(self):
        self.changeInputLabelValue(end="*")

    def buttonModClick(self):
        self.changeInputLabelValue("mod(", ",")

    def button4Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='4')

    def button5Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='5')

    def button6Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='6')

    def buttonSubClick(self):
        self.changeInputLabelValue(end="-")

    def buttonInvClick(self):
        self.changeInputLabelValue("1/(", ")")

    def button1Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='1')

    def button2Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='2')

    def button3Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='3')

    def buttonAddClick(self):
        self.changeInputLabelValue(end="+")

    def buttonLogClick(self):
        self.changeInputLabelValue("log(", ")")

    def buttonBracketLClick(self):
        self.changeInputLabelValue(end="(")

    def buttonBracketRClick(self):
        if self.text.get().find("(") != -1:
            str = self.text.get()
            str += ")"
            self.text.set(str)

    def button0Click(self):
        self.changeIfZeroInInputLabel()
        self.changeInputLabelValue(end='0')

    def buttonDotClick(self):
        if self.isError:
            return
        str = self.text.get()
        str += "."
        self.text.set(str)

    def isMathFunctionsToCalc(self):
        for mathFuncStr in self.mathFunctionsString:
            if self.text.get().find(mathFuncStr) != -1:
                return True, self.mathFunctionsString.index(mathFuncStr)
        return False, 0

    def solveExp(self, infix, firstOperator=""):
        tree = Tree()
        tree.buildTree(infixToPrefix(infix))
        tree.printTree(firstOperator)
        return tree.solve()

    def buttonResultClick(self):
        if self.isError:
            return

        resultExp = 0.0

        resultStr = "Error"

        self.textHistory.set(self.text.get())

        try:
            isMathFunction, calcMode = self.isMathFunctionsToCalc()
            if isMathFunction:
                if calcMode == 0 or calcMode == 3 or calcMode == 4:
                    infix = self.text.get()[self.text.get().find('('):self.text.get().rfind(')') + 1]
                    exp = self.solveExp(infix, self.mathFunctionsString[calcMode])
                    resultExp = sqrt(exp) if calcMode == 0 else log10(exp) if calcMode == 3 else factorial(exp)
                elif calcMode == 1:
                    infix = self.text.get()[self.text.get().find('|') + 1:self.text.get().rfind('|')]
                    exp = self.solveExp(infix, self.mathFunctionsString[calcMode])
                    resultExp = fabs(exp)
                else:
                    xInfix = self.text.get()[self.text.get().find('(') + 1:self.text.get().rfind(',')]
                    if self.text.get().rfind(')') != len(self.text.get()):
                        self.text.set(self.text.get() + ')')
                    yInfix = self.text.get()[self.text.get().find(',') + 1:self.text.get().rfind(')')]

                    if PRINT_TREE:
                        print("   ├──mod")

                    xExp = self.solveExp(xInfix, "mod")
                    yExp = self.solveExp(yInfix, "mod")
                    resultExp = fmod(xExp, yExp)
            else:
                infix = self.text.get()
                resultExp = self.solveExp(infix)

            resultStr = str(resultExp)
        except:
            self.isError = True
        finally:
            self.text.set(resultStr)

    def build(self):

        window = tk.Tk()

        window.resizable(False, False)
        window.title("Calculator")
        font24 = font.Font(family='Times New Roman', size=24, weight=font.BOLD)
        font14 = font.Font(family='Times New Roman', size=14, weight=font.BOLD)

        self.text = tk.StringVar()
        self.textHistory = tk.StringVar()
        self.text.set("0")
        self.inputLabelHistory = tk.Label(justify='right', font=font14, textvariable=self.textHistory)
        self.inputLabelHistory.grid(row=0, column=0, columnspan=5, sticky='E')
        self.inputLabel = tk.Label(justify='right', font=font24, textvariable=self.text)
        self.inputLabel.grid(row=1, column=0, columnspan=5, sticky='E')

        row_value = 2
        column_value = 0
        iterator = 0
        for i in self.gui_buttons:

            columnspan_val = 1
            if i == '=':
                columnspan_val = 5
            tk.Button(text=i, font=font24,
                      command=self.functions[iterator]
                      ).grid(row=row_value, column=column_value, columnspan=columnspan_val, sticky='EWNS')
            column_value += 1
            iterator += 1
            if column_value == 5:
                row_value += 1
                column_value = 0

        window.mainloop()
#endregion

#region Main
if __name__ == "__main__":
    GUI().build()
#endregion
