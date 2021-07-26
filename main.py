from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import math


# Create the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Puzzle Helper')
        self.setMinimumSize(500, 500)
        self.setWindowIcon(QIcon('puzzle_pieces.jpg'))
        self.setStyleSheet('QMainWindow{background: white;}')
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create tab widget and populate with tabs
        self.Tabs = TabsWidget()
        # Create tab bar using subclass and pass main window for click events
        self.TabBar = TabBar(self)
        self.Tabs.setTabBar(self.TabBar)
        self.Tabs.setObjectName('Tabs')
        self.Tabs.setStyleSheet(
                                'QTabWidget::pane#Tabs > QWidget{background: rgb(200, 200, 200); '
                                '                                border: 2px solid white;}'
                                'QTabWidget QTabBar{border: 2px solid rgb(240, 240, 240);}'
                                'QTabBar::tab:disabled {width: 120px;' 
                                                        'color: transparent;'
                                                        'background: white;}'
                                )
        self.setCentralWidget(self.Tabs)
        self.initTabs()

        self.show()

    # Initializes QWidget subclasses for tabs
    def initTabs(self):
        self.killerTab = KillerTab()
        self.mathdokuTab = MathdokuTab()
        self.solverTab = SolverTab()
        self.spacerTab = QWidget()
        self.closeTab = QWidget()

        self.Tabs.addTab(self.killerTab, 'Killer Sudoku')
        self.Tabs.addTab(self.mathdokuTab, 'Mathdoku')
        self.Tabs.addTab(self.solverTab, 'Sudoku Solver')
        # Add disabled spacing tab for alignment (made transparent in QTabWidget style sheet)
        self.Tabs.addTab(self.spacerTab, 'Spacer Tab')
        self.Tabs.setTabEnabled(3, False)
        self.Tabs.addTab(self.closeTab, 'Close X')

    def mousePressEvent(self, event):
        # Get click position for window dragging
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        # Window dragging
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


# Old subclass for tab widget
class TabsWidget(QTabWidget):
    def __init__(self):
        super(TabsWidget, self).__init__()


# Custom subclass for tab bar
# Handles click events for closing and dragging main window
class TabBar(QTabBar):
    def __init__(self, MainWindow):
        super(TabBar, self).__init__()
        self.MainWindow = MainWindow

    def mousePressEvent(self, event):
        # Get click position for window dragging
        self.oldPos = event.globalPos()

        # Check if close tab is clicked
        if self.tabAt(event.pos()) == self.count()-1:
            self.MainWindow.close()

        # Call tab bar mouse event
        super(TabBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Enables window dragging when clicking on tab bar
        delta = QPoint(event.globalPos() - self.oldPos)
        self.MainWindow.move(self.MainWindow.x() + delta.x(), self.MainWindow.y() + delta.y())
        self.oldPos = event.globalPos()


# Custom subclass for killer sudoku tab
class KillerTab(QWidget):
    def __init__(self):
        super(KillerTab, self).__init__()
        self.setMinimumSize(400, 400)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.initSettingWidget()
        self.initOptionsWidget()

    # Function to construct the settings widget on the left hand side of tab
    def initSettingWidget(self):
        # Create layout for settings widget
        self.settingLayout = QVBoxLayout()
        self.settingLayout.setAlignment(Qt.AlignTop)
        self.settingWidget = QWidget()
        self.settingWidget.setLayout(self.settingLayout)
        self.layout.addWidget(self.settingWidget)

        # Top 'Settings' label
        self.settingLabel = QLabel('Settings')
        self.settingLabel.setStyleSheet('QLabel{font: bold;}')
        self.settingLabel.setFont(QFont('Arial', 13))
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        # Create label and spin box for cage size
        self.cageLabel = QLabel('Cage Size (Max. 9)')
        self.settingLayout.addWidget(self.cageLabel)
        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(9)
        self.cageSpin.setMinimum(1)
        self.settingLayout.addWidget(self.cageSpin)

        # Create label and spin box for total
        self.totalLabel = QLabel('Sum Total (Max. 45)')
        self.settingLayout.addWidget(self.totalLabel)
        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(45)
        self.totalSpin.setMinimum(1)
        self.settingLayout.addWidget(self.totalSpin)

        # Create button for calculate
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

    # Function to construct area where options will be populated after 'Calculate' is pressed
    def initOptionsWidget(self):
        # Create widget to store valid combinations once calculated
        self.combinationsWidget = QWidget()
        self.combinationsLayout = QVBoxLayout()
        self.combinationsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.combinationsWidget.setLayout(self.combinationsLayout)
        self.combinationsLayout.addWidget(self.combinationsWidget)
        self.layout.addWidget(self.combinationsWidget)

        # Create label for combinations
        self.combinationsLabel = QLabel('Combinations')
        self.combinationsLabel.setFont(QFont('Arial', 13, QFont.Bold))
        self.combinationsLayout.addWidget(self.combinationsLabel)
        self.combinationsLabel.setAlignment(Qt.AlignHCenter)

        # Create area to store combinations
        self.optionsWidget = QWidget()
        self.optionsWidget.setMinimumSize(200, 400)
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{border: 2px solid rgb(150, 150, 150)};')
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

    # Function connected to 'Calculate' button
    def calculateOptions(self):
        # Stores valid options
        self.correct = []
        self.total = self.totalSpin.value()

        # Checks edge cases for improved performance
        sum_check = sum([i for i in range(1, self.cageSpin.value() + 1, 1)])
        if (self.totalSpin.value() >= sum_check) and (self.totalSpin.value() >= self.cageSpin.value()):
            if self.cageSpin.value() == 9 and self.totalSpin.value() == 45:
                self.correct = [[i for i in range(1, 10, 1)]]
            else:
                # Begins recursion for finding correct cage combinations
                depth = self.cageSpin.value()
                for i in range(1, 10, 1):
                    self.KillerRecursion(depth, [])

        # Clears all currently displayed options
        for i in reversed(range(self.optionsLayout.count())):
            self.optionsLayout.itemAt(i).widget().setParent(None)

        # Display valid options or 'No valid options'
        if self.correct:
            for i in self.correct:
                b = ToggleButton()
                b.setText(', '.join([str(integer) for integer in i]))
                self.optionsLayout.addWidget(b)
            self.optionsLayout.setAlignment(Qt.AlignTop)
        else:
            self.optionsLayout.addWidget(QLabel('No valid options'))
            self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

    # Recursion algorithm for finding valid combinations
    # l is a list of currently checked numbers
    def KillerRecursion(self, depth, l):
        for i in range(1, 10, 1):
            # Check if number is already in current cage
            if i not in l:
                temp = l.copy()
                temp.append(i)
                if depth == 1:
                    # Check if full cage equals desired total
                    if sum(temp) == self.total:
                        # Check if option is already in correct list
                        if sorted(temp) not in self.correct:
                            self.correct.append(sorted(temp))
                else:
                    self.KillerRecursion(depth - 1, temp)


# Custom subclass for mathdoku tab
class MathdokuTab(QWidget):
    def __init__(self):
        super(MathdokuTab, self).__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumSize(400, 400)

        self.initSettingWidget()
        self.initOptionsWidget()

    # Function to construct the settings widget on the left hand side of the tab
    def initSettingWidget(self):
        # Create layout for setting widget
        self.settingLayout = QVBoxLayout()
        self.settingLayout.setAlignment(Qt.AlignTop)
        self.settingWidget = QWidget()
        self.settingWidget.setLayout(self.settingLayout)
        self.layout.addWidget(self.settingWidget)

        # Create 'Settings' label at top of widget
        self.settingLabel = QLabel('Settings')
        self.settingLabel.setStyleSheet('QLabel{font: bold;}')
        self.settingLabel.setFont(QFont('Arial', 13))
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        # Create puzzle size combo box
        self.sizeLabel = QLabel('Puzzle Size')
        self.settingLayout.addWidget(self.sizeLabel)
        self.sizeCombo = QComboBox()
        self.sizeCombo.addItems(['3x3', '4x4', '5x5', '6x6', '7x7', '8x8', '9x9'])
        self.settingLayout.addWidget(self.sizeCombo)
        self.sizeCombo.currentIndexChanged.connect(self.adjustSettings)

        # Create cage size label and spin box
        self.cageLabel = QLabel('Cage Size')
        self.settingLayout.addWidget(self.cageLabel)
        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(6)
        self.cageSpin.setMinimum(2)
        self.settingLayout.addWidget(self.cageSpin)

        # Create operation(+, -, /, *) label and combo box
        self.operationLabel = QLabel('Operation Type')
        self.settingLayout.addWidget(self.operationLabel)
        self.operationCombo = QComboBox()
        self.operationCombo.addItems(['+', '-', '/', '*'])
        self.settingLayout.addWidget(self.operationCombo)

        # Create total lable and spinbox
        self.totalLabel = QLabel('Total')
        self.settingLayout.addWidget(self.totalLabel)
        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(120)
        self.totalSpin.setMinimum(2)
        self.settingLayout.addWidget(self.totalSpin)

        # Create button for calculate
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

    # Adjusts the settings to reflect the puzzle size when it is changed
    def adjustSettings(self):
        val = int(self.sizeCombo.currentText()[0])
        self.cageSpin.setMaximum(val)
        self.totalSpin.setMaximum(math.factorial(val))

    # Function to construct area where options will be populated after 'Calculate' is pressed
    def initOptionsWidget(self):
        # Create widget to store correct combinations
        self.combinationsWidget = QWidget()
        self.combinationsLayout = QVBoxLayout()
        self.combinationsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.combinationsWidget.setLayout(self.combinationsLayout)
        self.combinationsLayout.addWidget(self.combinationsWidget)
        self.layout.addWidget(self.combinationsWidget)

        # Create 'Combinations' label
        self.combinationsLabel = QLabel('Combinations')
        self.combinationsLabel.setFont(QFont('Arial', 13, QFont.Bold))
        self.combinationsLayout.addWidget(self.combinationsLabel)
        self.combinationsLabel.setAlignment(Qt.AlignHCenter)

        # Create area to store correct combinations
        self.optionsWidget = QWidget()
        self.optionsWidget.setMinimumSize(200, 400)
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{border: 2px solid rgb(150, 150, 150)};')
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

    # Function connected to 'Calculate' button
    def calculateOptions(self):
        # Stores correct combinations
        self.correct = []
        self.operation = self.operationCombo.currentText()
        self.total = self.totalSpin.value()

        # Starts recursion
        for i in range(1, int(self.sizeCombo.currentText()[0]) + 1, 1):
            self.mathdokuRecurse(self.cageSpin.value() - 1, [i])

        # Clears current layout
        for i in reversed(range(self.optionsLayout.count())):
            self.optionsLayout.itemAt(i).widget().setParent(None)

        # Populates correct options or displays 'No valid options' if there are none
        if self.correct:
            for i in self.correct:
                b = ToggleButton()
                b.setText(', '.join([str(integer) for integer in i]))
                self.optionsLayout.addWidget(b)
            self.optionsLayout.setAlignment(Qt.AlignTop)
        else:
            self.optionsLayout.addWidget(QLabel('No valid options'))
            self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

    # Recursion algorithm for finding valid combinations
    # l is a list of currently checked numbers
    def mathdokuRecurse(self, depth, l):
        for i in range(1, int(self.sizeCombo.currentText()[0]) + 1, 1):
            temp = l.copy()
            temp.append(i)
            if depth == 1:
                m = ''
                # Calculates cage total using the corresponding operation
                for num in temp:
                    m = m + str(num) + self.operation
                m = m[:-1]
                if eval(m) == self.total:
                    # Checks if current cage is already in list
                    if sorted(temp) not in self.correct:
                        self.correct.append(sorted(temp))
            else:
                self.mathdokuRecurse(depth - 1, temp)


# TODO
class SolverTab(QWidget):
    def __init__(self):
        super(SolverTab, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.addWidget(SudokuGrid())
        self.setLayout(self.layout)

# TODO
class SudokuGrid(QWidget):
    def __init__(self):
        super(SudokuGrid, self).__init__()
        self.constructGrid()

    def constructGrid(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        cell = Cell(value=1)
        self.layout.addWidget(cell)

# TODO
# Label class for setting up sudoku grid
class Cell(QLabel):
    def __init__(self, value=None):
        super(Cell, self).__init__()
        self.value = value
        self.setText(str(value))


# Custom subclass for combination buttons
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

