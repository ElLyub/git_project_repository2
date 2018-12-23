# -*- coding: utf-8 -*-
import sys
import math

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QLabel, QLCDNumber, QLineEdit, QToolButton, QGridLayout, QVBoxLayout

    
 
class Calculator(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.resize(400, 400)
        self.z = QLCDNumber(self) #поле
        self.z.setDigitCount(10) #кол-во десятичных разрядов, размер поля

        self.label = QLabel(self)
        self.label.setText("MR = 0 ")
        self.label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
        self.label.move(20, 15)
        self.label.setStyleSheet('QLabel {background-color: rgb(249, 249, 249); color: transparent;}')
        self.z.setStyleSheet("background-color: rgb(249, 249, 249);")#SS - таблица стилей; свойство: значение св-ва
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)

        self.count = 0 #текущее число
        self.exponent = -1
        self.a = 0 #первое введенное число
        self.memory = 0
        self.oper = ''
        
        self.digitButtons = []
        self.operButtons = []
        self.grid = QGridLayout() #сетка
        self.grid.addWidget(self.z, 0, 0, 1, 4) #окно вывода
        operation = ['C', "←", "+", "-", "*", "/",
                     "F", u"x\N{SUPERSCRIPT LATIN SMALL LETTER N}", "√", "=",
                     "MC", "M+", "M-", "MR",
                     'sin', 'cos', 'tan', 'log'] 
        row = 1
        for i in range(2):
            self.operButtons.append(self.createButton(operation[i],
                    self.operClicked))
        self.grid.addWidget(self.operButtons[0],row, 0, 1, 2)
        self.grid.addWidget(self.operButtons[1],row, 2, 1, 2)
        row = 3
        for i in range(2, 6):
            self.operButtons.append(self.createButton(operation[i],
                    self.operClicked))
            self.grid.addWidget(self.operButtons[i],row, 3)
            row += 1
        row = 3
        col = 0
        
        n = 0
        for i in '987654321':
            self.digitButtons.append(self.createButton(i,
                    self.digitClicked))
            self.grid.addWidget(self.digitButtons[n],row, col)
            n += 1
            if col < 2:
                col += 1
            else:
                col = 0
                row += 1
        self.digitButtons.append(self.createButton("0",
                    self.digitClicked))
        self.grid.addWidget(self.digitButtons[n],row, 0, 1, 2)
        self.digitButtons.append(self.createButton(".",
                    self.PointClicked))
        self.grid.addWidget(self.digitButtons[n+1],row, 2)
        row += 1
        for i in range(6, 10):
            self.operButtons.append(self.createButton(operation[i],
                    self.operClicked))
            self.grid.addWidget(self.operButtons[i], 7, i-6)
        for i in range(10, 14):
            self.operButtons.append(self.createButton(operation[i],
                    self.operClicked))
            self.grid.addWidget(self.operButtons[i], 2, i-10)
        for i in range(14, 18):
            self.operButtons.append(self.createButton(operation[i],
                    self.operClicked))
            self.grid.addWidget(self.operButtons[i], 8, i-14)
 
        self.setLayout(self.grid) # Передаем ссылку родителю
        self.show()
    #до этого момента дизайн   
 
    def digitClicked(self):
        if type(self.count) == int:
            self.count =  int(self.count) * 10 + int(self.sender().text())
        else:
            self.count += int(self.sender().text()) * 10**self.exponent
            self.exponent -= 1
        if self.flag:
            self.count = self.count-self.count*2
        self.z.display(self.count)
    
    def PointClicked(self):
        self.count = float(self.count)
        self.z.display(self.count)

    def operClicked(self):
        self.exponent = -1
        if self.sender().text() not in ['C', "M+", "M-", "MR", "MC", "←", "F", '=', '√', 'sin', 'cos', 'tan', 'log']: 
            self.oper = self.sender().text()
            self.a = float(self.count)
            self.count = 0
        elif self.sender().text() == '=':
            if self.oper == '+':
                self.count = self.a + float(self.count)
            elif self.oper == '-':
                self.count = self.a - float(self.count)
            elif self.oper == '*':
                self.count = self.a * float(self.count)
            elif self.oper == '/' and float(self.count) != 0:
                self.count = self.a / float(self.count) # add error
            elif self.oper == '/' and float(self.count) == 0:
                self.count = 'Error'
            elif self.oper == u"x\N{SUPERSCRIPT LATIN SMALL LETTER N}":
                self.count = self.a ** float(self.count)
        elif self.sender().text() == 'C':
            self.count = 0
        elif self.sender().text() == '←':
            self.count = self.count // 10
        elif self.sender().text() == 'F' and float(self.count) >= 0:
            self.count = math.factorial(self.count)
        elif self.sender().text() == 'F' and float(self.count) < 0:
            self.count = 'Error'
        elif self.sender().text() == '√' and float(self.count) >= 0:
            self.count = math.sqrt(self.count)
        elif self.sender().text() == '√' and float(self.count) < 0:
            self.count = 'Error'
        elif self.sender().text() == 'sin':
            self.count = math.sin(self.count)
        elif self.sender().text() == 'cos':
            self.count = math.cos(self.count)
        elif self.sender().text() == 'tan':
            self.count = math.tan(self.count)
        elif self.sender().text() == 'log':
            self.count = math.log(self.count)
        elif self.sender().text() == 'F' and float(self.count) >= 0:
            self.count = math.factorial(self.count)
        elif self.sender().text() == 'MC':
            self.memory = 0
            self.label.setText("MR = {}".format(self.memory)) 
        elif self.sender().text() == 'M+':
            self.memory += self.count
            self.label.setText("MR = {}".format(self.memory))
            self.label.adjustSize()
            self.label.setStyleSheet("QLabel { color: red}")   
        elif self.sender().text() == 'M-':
            self.memory -= self.count
            self.label.setText("MR = {}".format(self.memory))
            self.label.adjustSize()
            self.label.setStyleSheet("QLabel { color: red}")
        elif self.sender().text() == 'MR':
            self.count = self.memory
            self.label.setText("MR = {}".format(self.memory))
            self.label.adjustSize()
            self.label.setStyleSheet("QLabel { color: red}")
            
        self.z.display(self.count)  
 
    def createButton(self, text, member): #создание кнопки
        button = QPushButton(text)
        if text in '9876543210.':
            button.setStyleSheet('QPushButton {background-color: rgb(27, 27, 27); color: white;}')
        else:
            button.setStyleSheet('QPushButton {background-color: black; color: white;}')
        button.clicked.connect(member)
        return button
