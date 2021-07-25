from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import math


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Puzzle Helper')
        self.initTabs()
        self.setCentralWidget(self.Tabs)
        self.show()

    def initTabs(self):
        self.Tabs = QTabWidget()

        self.killerTab = KillerTab()
        self.mathdokuTab = MathdokuTab()

        self.Tabs.addTab(self.killerTab, 'Killer Sudoku')
        self.Tabs.addTab(self.mathdokuTab, 'Mathdoku')


class KillerTab(QWidget):
    def __init__(self):
        super(KillerTab, self).__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumSize(400, 400)

        self.initSettingWidget()
        self.initOptionsWidget()

    def initSettingWidget(self):
        self.settingLayout = QVBoxLayout()
        self.settingLayout.setAlignment(Qt.AlignTop)
        self.settingWidget = QWidget()
        self.settingWidget.setLayout(self.settingLayout)
        self.layout.addWidget(self.settingWidget)

        self.settingLabel = QLabel('Settings')
        self.settingLabel.setStyleSheet('QLabel{font: bold;}')
        self.settingLabel.setFont(QFont('Arial', 13))
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        self.cageLabel = QLabel('Cage Size (Max. 9)')
        self.settingLayout.addWidget(self.cageLabel)

        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(9)
        self.cageSpin.setMinimum(1)
        self.settingLayout.addWidget(self.cageSpin)

        self.sumLabel = QLabel('Sum Total (Max. 45)')
        self.settingLayout.addWidget(self.sumLabel)

        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(45)
        self.totalSpin.setMinimum(1)
        self.settingLayout.addWidget(self.totalSpin)

        self.calculateButton = QPushButton('Calculate')
        self.calculateButton.setStyleSheet('QPushButton{'
                                           '    background-color: rgb(153, 204, 255);'
                                           '    font: bold;'
                                           '}'
                                           'QPushButton:hover{'
                                           '    border: 2px solid rgb(20, 20, 20);'
                                           '}')
        self.calculateButton.clicked.connect(self.calculateOptions)
        self.settingLayout.addWidget(self.calculateButton)

    def initOptionsWidget(self):
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsWidget = QWidget()
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{border: 2px solid rgb(150, 150, 150)};')
        self.optionsWidget.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsWidget)

    def calculateOptions(self):
        self.correct = []
        sum_check = sum([i for i in range(1, self.cageSpin.value() + 1, 1)])
        if (self.totalSpin.value() >= sum_check) and (self.totalSpin.value() >= self.cageSpin.value()):
            if self.cageSpin.value() == 9 and self.totalSpin.value() == 45:
                self.correct = [[i for i in range(1, 10, 1)]]
            else:
                for i in range(1, 10, 1):
                    self.KillerRecursion(self.cageSpin.value(), [])

        for i in reversed(range(self.optionsLayout.count())):
            self.optionsLayout.itemAt(i).widget().setParent(None)
        if self.correct:
            for i in self.correct:
                b = ToggleButton()
                b.setText(', '.join([str(integer) for integer in i]))
                self.optionsLayout.addWidget(b)
        else:
            self.optionsLayout.addWidget(QLabel('No valid options'))
            self.optionsLayout.setAlignment(Qt.AlignCenter)

    def KillerRecursion(self, depth, l):
        for i in range(1, 10, 1):
            if i not in l:
                temp = l.copy()
                temp.append(i)
                if depth == 1:
                    m = ''
                    for num in temp:
                        m = m + str(num) + '+'
                    m = m[:-1]
                    if eval(m) == self.totalSpin.value():
                        if sorted(temp) not in self.correct:
                            self.correct.append(sorted(temp))
                else:
                    self.KillerRecursion(depth - 1, temp)


class MathdokuTab(QWidget):
    def __init__(self):
        super(MathdokuTab, self).__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumSize(400, 400)

        self.initSettingWidget()
        self.initOptionsWidget()

    def initSettingWidget(self):
        self.settingLayout = QVBoxLayout()
        self.settingLayout.setAlignment(Qt.AlignTop)
        self.settingWidget = QWidget()
        self.settingWidget.setLayout(self.settingLayout)
        self.layout.addWidget(self.settingWidget)

        self.settingLabel = QLabel('Settings')
        self.settingLabel.setStyleSheet('QLabel{font: bold;}')
        self.settingLabel.setFont(QFont('Arial', 13))
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        self.sizeLabel = QLabel('Puzzle Size')
        self.settingLayout.addWidget(self.sizeLabel)

        self.sizeCombo = QComboBox()
        self.sizeCombo.addItems(['3x3', '4x4', '5x5', '6x6', '7x7', '8x8', '9x9'])
        self.settingLayout.addWidget(self.sizeCombo)
        self.sizeCombo.currentIndexChanged.connect(self.adjustSettings)

        self.cageLabel = QLabel('Cage Size')
        self.settingLayout.addWidget(self.cageLabel)

        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(6)
        self.cageSpin.setMinimum(2)
        self.settingLayout.addWidget(self.cageSpin)

        self.operationLabel = QLabel('Operation Type')
        self.settingLayout.addWidget(self.operationLabel)

        self.operationCombo = QComboBox()
        self.operationCombo.addItems(['+', '-', '/', '*'])
        self.settingLayout.addWidget(self.operationCombo)

        self.totalLabel = QLabel('Total')
        self.settingLayout.addWidget(self.totalLabel)

        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(120)
        self.totalSpin.setMinimum(2)
        self.settingLayout.addWidget(self.totalSpin)

        self.calculateButton = QPushButton('Calculate')
        self.calculateButton.setStyleSheet('QPushButton{'
                                           '    background-color: rgb(153, 204, 255);'
                                           '    font: bold;'
                                           '}'
                                           'QPushButton:hover{'
                                           '    border: 2px solid rgb(20, 20, 20);'
                                           '}')
        self.calculateButton.clicked.connect(self.calculateOptions)
        self.settingLayout.addWidget(self.calculateButton)

    # Adjusts the settings to reflect the puzzle size
    def adjustSettings(self):
        val = int(self.sizeCombo.currentText()[0])
        self.cageSpin.setMaximum(val)
        self.totalSpin.setMaximum(math.factorial(val))

    def initOptionsWidget(self):
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsWidget = QWidget()
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{border: 2px solid rgb(150, 150, 150)};')
        self.optionsWidget.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsWidget)

    def calculateOptions(self):
        self.correct = []

        for i in range(1, int(self.sizeCombo.currentText()[0]) + 1, 1):
            self.mathdokuRecurse(self.cageSpin.value() - 1, [i])

        for i in reversed(range(self.optionsLayout.count())):
            self.optionsLayout.itemAt(i).widget().setParent(None)
        for i in self.correct:
            b = ToggleButton()
            b.setText(', '.join([str(integer) for integer in i]))
            self.optionsLayout.addWidget(b)

    def mathdokuRecurse(self, depth, l):
        for i in range(1, int(self.sizeCombo.currentText()[0]) + 1, 1):
            temp = l.copy()
            temp.append(i)

            if depth == 1:
                m = ''
                for num in temp:
                    m = m + str(num) + self.operationCombo.currentText()
                m = m[:-1]
                if eval(m) == self.totalSpin.value():
                    if sorted(temp) not in self.correct:
                        self.correct.append(sorted(temp))
            else:
                self.mathdokuRecurse(depth - 1, temp)


class ToggleButton(QPushButton):
    def __init__(self):
        super(ToggleButton, self).__init__()
        self.setCheckable(True)
        self.setChecked(False)
        self.setStyleSheet('QPushButton{'
                           '    color: rgb(0, 0, 0);'
                           '    background-color: rgb(200, 200, 200);'
                           '}'
                           'QPushButton:checked{'
                           '    color: rgb(255, 255, 255);'
                           '    background-color: rgb(100, 100, 100);'
                           '    border: none;'
                           '}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())

