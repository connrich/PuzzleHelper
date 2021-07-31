from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import math
import random
from sudoku import Sudoku

# TODO:
#   Refresh button for combinations widget
#   Recent searches list
#   Solve button for Sudoku
#   Notepad??
#   Change colour of notes??
#   Difficulty selection
#   Toggle buttons size, curved edges and font
#   Shortcut for calculate using numpad enter
#   Bigger digits, better colour and nicer font for sudoku
#   Style buttons on sudoku tab
#   Arrow key movement for sudoku


class AppTheme:
    action_button_ss = ('QPushButton{'
                        '    background-color: rgb(130, 130, 130 );'
                        '    font: bold;'
                        '    color: white;'
                        '    border-radius: 5px;'
                        '    height: 25px;'
                        '}'
                        'QPushButton:hover{'
                        '    border: 2px solid rgb(255, 255, 255);'
                        '    background-color: rgb(110, 110, 110);'
                        '}')
    action_button_font = QFont('yu Gothic Medium', 9, QFont.Bold)

    title_ss = ('QLabel{'
                '   color: rgb(50, 50, 50);'
                '}')

    title_label_font = QFont('Yu Gothic Medium', 20, QFont.Bold)

    subtitle_label_font = QFont('yu Gothic Medium', 9, QFont.Bold)

    toggle_button_ss = ('QPushButton{'
                           '    color: rgb(0, 0, 0);'
                           '    background-color: rgb(200, 200, 200);'
                           '    border-radius: 5px;'
                           '    height: 35px;'
                           '}'
                           'QPushButton:checked{'
                           '    color: rgb(255, 255, 255);'
                           '    background-color: rgb(120, 120, 120);'
                           '    border: none;'
                           '}')

    toggle_button_font = QFont('Yu Gothic Medium', 10, QFont.Bold)

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
        self.Tabs.setStyleSheet('QTabWidget::pane#Tabs > QWidget{background: lightblue; '
                                '                                border: 2px solid #C4C4C3;}'
                                'QTabWidget QTabBar{border: 2px solid rgb(240, 240, 240);}'
                                'QTabBar::tab:disabled {width: 278px;' 
                                                        'color: transparent;'
                                                        'background: white;}'
                                'QTabWidget::tab-bar{left: 1px;}')
        self.setCentralWidget(self.Tabs)
        self.initTabs()

        self.show()

        # font, valid = QFontDialog.getFont()


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
        self.setStyleSheet('QTabBar::tab{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,'
                                'stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,'
                                'stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);'
                                'border: 2px solid #C4C4C3;'
                                'border-bottom-color: #C4C4C3;'
                                'border-top-left-radius: 4px;'
                                'border-top-right-radius: 4px;'
                                'min-width: 8px;'
                                'padding: 6px;}'
                           'QTabBar::tab:selected{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,'
                                'stop: 0 #fafafa, stop: 0.4 #f4f4f4,'
                                'stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);'
                                'border-bottom-color: white;}')

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
        # self.settingLabel.setStyleSheet('QLabel{font: bold;}')
        self.settingLabel.setFont(AppTheme.title_label_font)
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        # Create label and spin box for cage size
        self.cageLabel = QLabel('Cage Size (Max. 9)')
        self.cageLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.cageLabel)
        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(9)
        self.cageSpin.setMinimum(1)
        self.settingLayout.addWidget(self.cageSpin)

        # Create label and spin box for total
        self.totalLabel = QLabel('Sum Total (Max. 45)')
        self.totalLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.totalLabel)
        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(45)
        self.totalSpin.setMinimum(1)
        self.settingLayout.addWidget(self.totalSpin)

        # Create button for calculate
        self.calculateButton = CalculateButton('Calculate')
        self.calculateButton.clicked.connect(self.calculateOptions)
        self.settingLayout.addWidget(self.calculateButton)

        # fontLayout = QVBoxLayout()
        # self.settingLayout.addLayout(fontLayout)
        # fonts = ['Barlow Condensed', 'Dosis', 'Dosis ExtraBold', 'Yu Gothic Medium', 'Yu Gothic']
        # for font in fonts:
        #     f = QFont(font, 20)
        #     label = QLabel('Settings')
        #     label.setStyleSheet('QLabel{font: bold;}')
        #     label.setFont(f)
        #     fontLayout.addWidget(label)





    # Function to construct area where options will be populated after 'Calculate' is pressed
    def initOptionsWidget(self):
        # Create widget to store valid combinations once calculated
        self.combinationsWidget = QWidget()
        self.combinationsWidget.setStyleSheet('QWidget{border-radius: 10px;}')
        self.combinationsLayout = QVBoxLayout()
        self.combinationsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.combinationsWidget.setLayout(self.combinationsLayout)
        self.combinationsLayout.addWidget(self.combinationsWidget)
        self.layout.addWidget(self.combinationsWidget)

        # Create label for combinations
        self.combinationsLabel = QLabel('Combinations')
        self.combinationsLabel.setFont(AppTheme.title_label_font)
        self.combinationsLayout.addWidget(self.combinationsLabel)
        self.combinationsLabel.setAlignment(Qt.AlignHCenter)

        # Create area to store combinations
        self.optionsWidget = QWidget()
        self.optionsWidget.setMinimumSize(240, 500)
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{'
                                         '      background-color: white; '
                                         '      border: 2px solid rgb(150, 150, 150);'
                                         '};')
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

        self.optionsRefreshButton = QPushButton('Refresh')
        self.optionsRefreshButton.setStyleSheet(AppTheme.action_button_ss)
        self.optionsRefreshButton.setFont(AppTheme.action_button_font)
        self.optionsRefreshButton.clicked.connect(self.refreshOptions)
        self.combinationsLayout.addWidget(self.optionsRefreshButton)

    def refreshOptions(self):
        for i in range(self.optionsLayout.count()):
            self.optionsLayout.itemAt(i).widget().setChecked(False)

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
        self.calculateButton = CalculateButton('Calculate')
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
        self.optionsWidget.setMinimumSize(240, 500)
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet('QWidget#optionsWidget{'
                                         '      background-color: white; '
                                         '      border: 2px solid rgb(150, 150, 150);'
                                         '};')
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

        self.optionsRefreshButton = QPushButton('Refresh')
        self.optionsRefreshButton.setStyleSheet(AppTheme.action_button_ss)
        self.optionsRefreshButton.clicked.connect(self.refreshOptions)
        self.combinationsLayout.addWidget(self.optionsRefreshButton)

    def refreshOptions(self):
        for i in range(self.optionsLayout.count()):
            self.optionsLayout.itemAt(i).widget().setChecked(False)

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


class SolverTab(QWidget):
    def __init__(self):
        super(SolverTab, self).__init__()
        self.solverLayout = QGridLayout()
        self.setLayout(self.solverLayout)

        puzzle = Sudoku(3)
        self.sudokuGrid = SudokuGrid(puzzle.board)
        self.solverLayout.addWidget(self.sudokuGrid)

        self.buttonLayout = QHBoxLayout()
        self.solverLayout.addLayout(self.buttonLayout, 1, 0)
        self.initButtons()

    def initButtons(self):
        # Create button to toggle edit mode
        self.noteButton = QPushButton()
        self.noteButton.setShortcut(QKeySequence('p'))
        self.noteButton.setFocusPolicy(Qt.NoFocus)
        self.noteButton.setCheckable(True)
        self.noteButton.setChecked(False)
        self.noteButton.clicked.connect(self.toggleNoteMode)
        self.setStyleSheet('QPushButton{'
                           '    background-color: rgb(200, 200, 200);'
                           '}'
                           'QPushButton:checked{'
                           '    background-color: rgb(100, 100, 100);'
                           '    border: none;'
                           '}')
        self.pencilIcon = QIcon('pencil.png')
        self.noteButton.setIcon(self.pencilIcon)
        self.noteButton.setFixedSize(self.noteButton.iconSize().grownBy(QMargins(4, 4, 4, 4)))
        self.buttonLayout.addWidget(self.noteButton)

        # Create button for generating random puzzle
        self.randomButton = QPushButton('Random Puzzle')
        self.randomButton.setStyleSheet('QPushButton{'
                                        '    font: bold;'
                                        '}')
        self.randomButton.clicked.connect(self.generateRandomPuzzle)
        self.buttonLayout.addWidget(self.randomButton)

        # Create button for clearing grid
        self.clearGridButton = QPushButton('Clear Grid')
        self.clearGridButton.setStyleSheet('QPushButton{'
                                        '    font: bold;'
                                        '}')
        self.clearGridButton.clicked.connect(self.clearGrid)
        self.buttonLayout.addWidget(self.clearGridButton)

    # Triggered when noteButton is pushed to update the note mode
    def toggleNoteMode(self):
        self.sudokuGrid.noteMode = self.noteButton.isChecked()

    # Generates a random puzzle and populates the grid with it
    def generateRandomPuzzle(self):
        random.seed()
        num = random.uniform(0.4, 0.75)
        puzzle = Sudoku(3, 3, seed=random.randint(0, 9999999999999)).difficulty(num)
        self.sudokuGrid.close()
        self.sudokuGrid = SudokuGrid(puzzle.board)
        self.solverLayout.addWidget(self.sudokuGrid, 0, 0)
        self.toggleNoteMode()

    def clearGrid(self):
        self.sudokuGrid.close()
        self.sudokuGrid = SudokuGrid()
        self.solverLayout.addWidget(self.sudokuGrid, 0, 0)



class SudokuGrid(QWidget):
    # puzzle is a list of 9 rows, each row is a list of 9 digits
    def __init__(self, puzzle=None):
        super(SudokuGrid, self).__init__()
        self.rows = puzzle
        self.constructGrid()
        self.noteMode = False
        if self.rows is not None:
            self.populatePuzzle(self.rows)
            self.constructDataStructures()

    def constructGrid(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Construct boxes
        for i in range(3):
            for j in range(3):
                box_layout = QGridLayout()
                box_layout.setSpacing(1)
                self.grid_layout.addLayout(box_layout, i, j)

        # Construct cells
        for i in range(9):
            for j in range(9):
                cell = Cell(parent=self)
                box_layout = self.grid_layout.itemAtPosition(i // 3, j // 3)
                box_layout.addWidget(cell, i % 3, j % 3)

    # Constructs list of columns and boxes using the list of rows
    # Will be used to check correctness of cells
    def constructDataStructures(self):
        self.cols = []
        for i in range(9):
            self.cols.append([])
            for row in self.rows:
                self.cols[i].append(row[i])

        self.boxes = []
        for row in range(0, 7, 3):
            for col in range(0, 7, 3):
                temp = []
                for i in range(row, row+3, 1):
                    for j in range(col, col+3, 1):
                        temp.append(self.rows[i][j])
                self.boxes.append(temp)

    # Fill puzzle using the template provided
    def populatePuzzle(self, puzzle):
        self.rows = puzzle
        self.constructDataStructures()
        for i, row in enumerate(puzzle):
            for j, num in enumerate(row):
                cell = self.getCell(i, j)
                cell.setText('')
                cell.given = False
                if num is not None:
                    cell.setText(str(num))
                    cell.given = True  # Stops the cell from being overwritten i.e. given number
                    cell.setStyleSheet('QLabel{'
                                       '    background-color: white;'
                                       '    font: bold;'
                                       '    color: black;'
                                       ' }')

    # Helper function to get cell object using coordinates
    def getCell(self, row, col):
        box = self.grid_layout.itemAtPosition(row // 3, col // 3)
        return box.itemAtPosition(row % 3, col % 3).widget()

    def isNoteModeEnabled(self):
        return self.noteMode

# Label class for setting up sudoku grid
class Cell(QLabel):
    def __init__(self, value=None, parent=None):
        super(Cell, self).__init__()
        self.parent = parent
        self.value = value
        self.given = False
        self.notes = []
        if value is not None:
            self.setText(str(value))

        self.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(60, 60)

        self.setFont(QFont('Arial', 15))
        self.setStyleSheet('QLabel{'
                           '    background-color: white;'
                           '    font: bold;'
                           '    color: blue;'
                           ' }')
        self.setTextFormat(Qt.RichText)
        self.setWordWrap(True)

    def isGiven(self):
        return self.given

    def focusInEvent(self, event):
        if not self.isGiven():
            self.setStyleSheet('QLabel{'
                               '    background-color: rgba(120, 120, 120, 100);'
                               '    font: bold;'
                               '    color: blue;'
                               ' }')

    def focusOutEvent(self, event):
        if not self.isGiven():
            self.parent.currentCell = self
            self.setStyleSheet('QLabel{'
                               '    background-color: white;'
                               '    font: bold;'
                               '    color: blue;'
                               ' }')

    # Fills or clears focused cell depending on key stroke
    def keyPressEvent(self, event):
        # Used to fill cells with a value
        if (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9) and (not self.isGiven()):
            if self.parent.isNoteModeEnabled():
                text = self.constructNoteString(str(event.key() - Qt.Key_0))
                self.setFont(QFont('Arial', 9))
            else:
                text = str(event.key() - Qt.Key_0)
                if text not in self.notes:
                    self.notes.append(text)
                self.setFont(QFont('Arial', 15))
            self.setText(text)
        elif (event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete) and (not self.isGiven()):
            self.setText('')
            if self.parent.isNoteModeEnabled():
                self.notes.clear()

    # Creates a properly formatted string for the cell
    def constructNoteString(self, num):
        if num not in self.notes:
            self.notes.append(num)
        else:
            self.notes.remove(num)
        note = ''.join(sorted(self.notes))
        # Puts label on 2 lines if it is too long
        if len(note) > 5:
            top = note[:5] + ' <br> '
            bottom = note[5:]
            note = ''.join((top, bottom))
        return note


class CalculateButton(QPushButton):
    def __init__(self, label):
        super(CalculateButton, self).__init__(label)
        self.setShortcut('Return')
        self.setFont(AppTheme.action_button_font)
        self.setStyleSheet(AppTheme.action_button_ss)


# Custom subclass for combination buttons
class ToggleButton(QPushButton):
    def __init__(self):
        super(ToggleButton, self).__init__()
        self.setCheckable(True)
        self.setChecked(False)
        self.setStyleSheet(AppTheme.toggle_button_ss)
        self.setFont(AppTheme.toggle_button_font)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())

