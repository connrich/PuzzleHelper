from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sudoku import Sudoku
import sys
import math
import random
import json
import requests
from collections import Counter

dictionary_api_url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'

# TODO:
#   Refactor lengthDictionary for less memory use
#   MirriamWebster backup api
#   Calculation thread for killer/mathdoku recursion
#   Definition widget html formatting
#   Change colour of notes??
#   Difficulty selection
#   Highlight wrong cells


class AppTheme:
    tabs_ss = ('QTabWidget::pane#Tabs > QWidget{' 
               '    background: lightblue;'
               '    border: 2px solid #C4C4C3;'
               '}'
               'QTabWidget QTabBar{'
               '    border: 2px solid rgb(240, 240, 240);'
               '}'
               'QTabBar::tab:disabled {'
               '    width: 78px;' 
               '    color: transparent;'
               '    background: white;}'
               'QTabWidget::tab-bar{'
               '    left: 1px;'
               '}')

    action_button_ss = ('QPushButton{'
                        '    background-color: rgb(130, 130, 130);'
                        '    font: bold;'
                        '    color: white;'
                        '    border-radius: 5px;'
                        '    height: 30px;'
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

    options_widget_ss = ('QWidget#optionsWidget{'
                         '      background-color: white; '
                         '      border: 2px solid rgb(150, 150, 150);'
                         '      border-radius: 10px;'
                         '};')

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

    given_cell_default_ss = ('QLabel{'
                             '    background-color: white;'
                             '    font: bold;'
                             '    color: black' 
                             ' }')

    cell_default_ss = ('QLabel{'
                       '    background-color: white;'
                       '    font: bold;'
                       '    color: #0080FF;'
                       ' }')

    given_cell_focus_in_ss = ('QLabel{'
                              '    background-color: rgba(120, 120, 120, 100);'
                              '    font: bold;'
                              ' }')

    cell_focus_in_ss = ('QLabel{'
                        '    background-color: rgba(120, 120, 120, 100);'
                        '    font: bold;'
                        '    color: #0080FF;'
                        ' }')

    cell_default_font = QFont('Arial', 20, QFont.Bold)

    cell_note_font = QFont('Arial', 11, QFont.Bold)

    note_button_ss = action_button_ss + 'QPushButton:checked{' \
                                        '   background-color: rgb(50, 50, 50); ' \
                                        '   border: 2px solid white;' \
                                        '}'

    default_note_tab_font = QFont('Yu Gothic Medium', 15, QFont.Bold)

    definition_font = QFont('Yu Gothic Medium', 13, QFont.Bold)


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
        self.Tabs.setStyleSheet(AppTheme.tabs_ss)
        self.setCentralWidget(self.Tabs)
        self.initTabs()

        self.show()

        # font, valid = QFontDialog.getFont()


    # Initializes QWidget subclasses for tabs
    def initTabs(self):
        self.killerTab = KillerTab()
        self.mathdokuTab = MathdokuTab()
        self.solverTab = SolverTab()
        self.crosswordTab = CrosswordTab()
        self.anagramTab = AnagramTab()
        self.notesTab = NotesTab()
        self.spacerTab = QWidget()
        self.closeTab = QWidget()

        self.Tabs.addTab(self.killerTab, 'Killer Sudoku')
        self.Tabs.addTab(self.mathdokuTab, 'Mathdoku')
        self.Tabs.addTab(self.solverTab, 'Sudoku Solver')
        self.Tabs.addTab(self.crosswordTab, 'Crossword')
        self.Tabs.addTab(self.anagramTab, 'Anagrams')
        self.Tabs.addTab(self.notesTab, 'Notes')
        # Add disabled spacing tab for alignment (made transparent in QTabWidget style sheet)
        self.Tabs.addTab(self.spacerTab, 'Spacer Tab')
        self.Tabs.setTabEnabled(6, False)
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
        self.calculateButton.clicked.connect(self.logSearch)
        self.settingLayout.addWidget(self.calculateButton)

        # Create label for recent searches
        self.recentLabel = QLabel('Recent Searches')
        self.recentLabel.setAlignment(Qt.AlignHCenter)
        self.recentLabel.setFont(AppTheme.title_label_font)
        self.settingLayout.addWidget(self.recentLabel)

        # Create widget to store recent searches
        self.recentWidget = QWidget()
        self.recentWidget.setMinimumHeight(350)
        self.recentWidget.setObjectName('optionsWidget')  # Needed to use stylesheet
        self.recentWidget.setStyleSheet(AppTheme.options_widget_ss)
        self.recentLayout = QVBoxLayout()
        self.recentLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.recentLayout.setDirection(QBoxLayout.BottomToTop)
        self.recentWidget.setLayout(self.recentLayout)
        self.settingLayout.addWidget(self.recentWidget)

    # Adds a push button to recent search area with the current setting info
    def logSearch(self):
        if self.recentLayout.count() >= 9:
            self.recentLayout.takeAt(0)

        button = QPushButton(self.getSettingsString())
        button.setMinimumWidth(240)
        button.setFont(AppTheme.action_button_font)
        button.setStyleSheet(AppTheme.action_button_ss)
        button.clicked.connect(lambda: self.populateSettings(button.text()))
        self.recentLayout.addWidget(button)

    # Returns a formatted string of the current info in the settings
    def getSettingsString(self):
        info_list = []
        info_list.append(str(self.cageSpin.value()))
        info_list.append(str(self.totalSpin.value()))
        return '           '.join(info_list)

    # Populates the combo boxes and spin boxes in settings with the recent search info
    def populateSettings(self, settings):
        l = settings.split('           ')
        self.cageSpin.setValue(int(l[0]))
        self.totalSpin.setValue(int(l[1]))
        self.calculateOptions()

    # Function to construct area where options will be populated after 'Calculate' is pressed
    def initOptionsWidget(self):
        # Create widget to store valid combinations once calculated
        self.combinationsWidget = QWidget()
        self.combinationsWidget.setStyleSheet(AppTheme.options_widget_ss)
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
        self.optionsWidget.setStyleSheet(AppTheme.options_widget_ss)
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

        self.optionsRefreshButton = QPushButton('Clear Selections')
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
            label = QLabel('No valid options')
            label.setFont(AppTheme.subtitle_label_font)
            self.optionsLayout.addWidget(label)
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
        self.settingLabel.setFont(AppTheme.title_label_font)
        self.settingLabel.setAlignment(Qt.AlignCenter)
        self.settingLayout.addWidget(self.settingLabel)

        # Create puzzle size combo box
        self.sizeLabel = QLabel('Puzzle Size')
        self.sizeLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.sizeLabel)
        self.sizeCombo = QComboBox()
        self.sizeCombo.addItems(['3x3', '4x4', '5x5', '6x6', '7x7', '8x8', '9x9'])
        self.settingLayout.addWidget(self.sizeCombo)
        self.sizeCombo.currentIndexChanged.connect(self.adjustSettings)

        # Create cage size label and spin box
        self.cageLabel = QLabel('Cage Size')
        self.cageLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.cageLabel)
        self.cageSpin = QSpinBox()
        self.cageSpin.setMaximum(6)
        self.cageSpin.setMinimum(2)
        self.settingLayout.addWidget(self.cageSpin)

        # Create operation(+, -, /, *) label and combo box
        self.operationLabel = QLabel('Operation Type')
        self.operationLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.operationLabel)
        self.operationCombo = QComboBox()
        self.operationCombo.addItems(['+', '-', '/', '*'])
        self.settingLayout.addWidget(self.operationCombo)

        # Create total lable and spinbox
        self.totalLabel = QLabel('Total')
        self.totalLabel.setFont(AppTheme.subtitle_label_font)
        self.settingLayout.addWidget(self.totalLabel)
        self.totalSpin = QSpinBox()
        self.totalSpin.setMaximum(120)
        self.totalSpin.setMinimum(2)
        self.settingLayout.addWidget(self.totalSpin)

        # Create button for calculate
        self.calculateButton = CalculateButton('Calculate')
        self.calculateButton.clicked.connect(self.calculateOptions)
        self.calculateButton.clicked.connect(self.logSearch)
        self.settingLayout.addWidget(self.calculateButton)

        # Create label for recent searches
        self.recentLabel = QLabel('Recent Searches')
        self.recentLabel.setAlignment(Qt.AlignHCenter)
        self.recentLabel.setFont(AppTheme.title_label_font)
        self.settingLayout.addWidget(self.recentLabel)

        # Create widget to store recent searches
        self.recentWidget = QWidget()
        self.recentWidget.setMinimumHeight(240)
        self.recentWidget.setObjectName('optionsWidget')  # Needed to use stylesheet
        self.recentWidget.setStyleSheet(AppTheme.options_widget_ss)
        self.recentLayout = QVBoxLayout()
        self.recentLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.recentLayout.setDirection(QBoxLayout.BottomToTop)
        self.recentWidget.setLayout(self.recentLayout)
        self.settingLayout.addWidget(self.recentWidget)

    # Adjusts the settings to reflect the puzzle size when it is changed
    def adjustSettings(self):
        val = int(self.sizeCombo.currentText()[0])
        self.cageSpin.setMaximum(val)
        self.totalSpin.setMaximum(math.factorial(val))

    # Adds a push button to recent search area with the current setting info
    def logSearch(self):
        if self.recentLayout.count() >= 6:
            self.recentLayout.takeAt(0)

        button = QPushButton(self.getSettingsString())
        button.setMinimumWidth(240)
        button.setFont(AppTheme.action_button_font)
        button.setStyleSheet(AppTheme.action_button_ss)
        button.clicked.connect(lambda: self.populateSettings(button.text()))
        self.recentLayout.addWidget(button)

    # Returns a formatted string of the current info in the settings
    def getSettingsString(self):
        info_list = []
        info_list.append(self.sizeCombo.currentText())
        info_list.append(str(self.cageSpin.value()))
        info_list.append(self.operationCombo.currentText())
        info_list.append(str(self.totalSpin.value()))
        return '      '.join(info_list)

    # Populates the combo boxes and spin boxes in settings with the recent search info
    def populateSettings(self, settings):
        l = settings.split('      ')
        self.sizeCombo.setCurrentText(l[0])
        self.cageSpin.setValue(int(l[1]))
        self.operationCombo.setCurrentText(l[2])
        self.totalSpin.setValue(int(l[3]))
        self.calculateOptions()

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
        self.combinationsLabel.setFont(AppTheme.title_label_font)
        self.combinationsLayout.addWidget(self.combinationsLabel)
        self.combinationsLabel.setAlignment(Qt.AlignHCenter)

        # Create area to store correct combinations
        self.optionsWidget = QWidget()
        self.optionsWidget.setMinimumSize(240, 500)
        self.optionsWidget.setObjectName('optionsWidget')
        self.optionsWidget.setStyleSheet(AppTheme.options_widget_ss)
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.optionsWidget.setLayout(self.optionsLayout)
        self.combinationsLayout.addWidget(self.optionsWidget)

        # Create button to clear currently selected buttons
        self.optionsRefreshButton = QPushButton('Clear Selections')
        self.optionsRefreshButton.setStyleSheet(AppTheme.action_button_ss)
        self.optionsRefreshButton.setFont(AppTheme.action_button_font)
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
            label = QLabel('No valid options')
            label.setFont(AppTheme.subtitle_label_font)
            self.optionsLayout.addWidget(label)
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
        self.setStyleSheet(AppTheme.note_button_ss)
        self.pencilIcon = QIcon('pencil.png')
        self.noteButton.setIcon(self.pencilIcon)
        self.noteButton.setFixedSize(self.noteButton.iconSize().grownBy(QMargins(4, 4, 4, 4)))
        self.buttonLayout.addWidget(self.noteButton)

        # Create button for generating random puzzle
        self.randomButton = QPushButton('Random Puzzle')
        self.randomButton.setStyleSheet(AppTheme.action_button_ss)
        self.randomButton.setFont(AppTheme.action_button_font)
        self.randomButton.clicked.connect(self.generateRandomPuzzle)
        self.buttonLayout.addWidget(self.randomButton)

        # Create button for clearing grid
        self.clearGridButton = QPushButton('Clear Grid')
        self.clearGridButton.setStyleSheet(AppTheme.action_button_ss)
        self.clearGridButton.setFont(AppTheme.action_button_font)
        self.clearGridButton.clicked.connect(self.clearGrid)
        self.buttonLayout.addWidget(self.clearGridButton)

        # Create button for solving current grid
        self.solveGridButton = QPushButton('Solve')
        self.solveGridButton.setStyleSheet(AppTheme.action_button_ss)
        self.solveGridButton.setFont(AppTheme.action_button_font)
        self.solveGridButton.clicked.connect(self.sudokuGrid.solveCurrentGrid)
        self.buttonLayout.addWidget(self.solveGridButton)

    # Triggered when noteButton is pushed to update the note mode
    def toggleNoteMode(self):
        self.sudokuGrid.noteMode = self.noteButton.isChecked()

    # Generates a random puzzle and populates the grid with it
    def generateRandomPuzzle(self):
        random.seed()
        num = random.uniform(0.4, 0.7)
        puzzle = Sudoku(3, 3, seed=random.randint(0, 9999999999999)).difficulty(num)
        self.sudokuGrid.close()
        self.sudokuGrid = SudokuGrid(puzzle.board)
        self.solveGridButton.clicked.connect(self.sudokuGrid.solveCurrentGrid)
        self.solverLayout.addWidget(self.sudokuGrid, 0, 0)
        self.toggleNoteMode()

    def clearGrid(self):
        self.sudokuGrid.close()
        self.sudokuGrid = SudokuGrid()
        self.solverLayout.addWidget(self.sudokuGrid, 0, 0)


class CrosswordTab(QWidget):
    def __init__(self):
        super(CrosswordTab, self).__init__()

        # Loads the dictionary of words sorted by length
        self.lengthDictionary = self.loadLengthDictionary()

        # Master layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        # Sets a label for search bar
        self.searchLabel = QLabel('Search: ')
        self.searchLabel.setFont(AppTheme.subtitle_label_font)
        self.layout.addWidget(self.searchLabel, 0, 0)

        # Search bar for word entry
        self.searchLineEdit = QLineEdit()
        font = QFont('yu Gothic Medium', 12, QFont.Bold)
        font.setLetterSpacing(QFont.PercentageSpacing, 115)
        self.searchLineEdit.setFont(font)
        self.layout.addWidget(self.searchLineEdit, 0, 1)

        # Search button for generating the list of potential words
        self.searchButton = QPushButton('Search')
        self.searchButton.setStyleSheet(AppTheme.action_button_ss)
        self.searchButton.setFont(AppTheme.action_button_font)
        self.searchButton.clicked.connect(self.populateWordList)
        self.searchButton.setShortcut(QKeySequence('Return'))
        self.layout.addWidget(self.searchButton, 0, 2)

        # Sets label to inform user of search syntax
        self.searchSyntaxLabel = QLabel('Use any symbol to denote a space/blank square (i.e. testing = t!s_in#)')
        self.searchSyntaxLabel.setFont(AppTheme.subtitle_label_font)
        self.layout.addWidget(self.searchSyntaxLabel, 1, 0, 1, 0, Qt.AlignCenter)

        # Create horizontal layout for potential words/definition area
        self.mainLayout = QHBoxLayout()
        self.layout.addLayout(self.mainLayout, 2, 0, 1, 0)

        # List widget to store all potential words
        self.wordList = QListWidget()
        self.wordList.setMaximumWidth(210)
        self.wordList.setFont(AppTheme.default_note_tab_font)
        self.wordList.itemClicked.connect(self.getApiDefinition)
        self.mainLayout.addWidget(self.wordList)

        # Widget to display definiton and information about a word
        self.definitionWidget = QTextEdit()
        self.definitionWidget.setReadOnly(True)
        self.mainLayout.addWidget(self.definitionWidget)

    def populateWordList(self):
        # Get current text that was entered
        given_word = self.searchLineEdit.text().lower()

        # Gets list of letters and their location within the word
        indexed_letters = [(char, index) for index, char in enumerate(given_word) if char.isalpha()]

        # Iterates through the list stored at the appropriate length key
        # If the word has letters in matching locations it appends it to possible_words
        possible_words = []
        for word in self.lengthDictionary[len(given_word)]:
            for letter, index in indexed_letters:
                if word[index] != letter:
                    break
            else:
                possible_words.append(word)

        # Refresh the list with all current potential words
        self.wordList.clear()
        if possible_words:
            self.wordList.setEnabled(True)
            self.wordList.addItems(possible_words)
        else:
            # Display message if no valid words were found
            self.wordList.setEnabled(False)
            none_found = ['', 'No', 'matching', 'words', 'found']
            for word in none_found:
                item = QListWidgetItem(word)
                item.setTextAlignment(Qt.AlignHCenter)
                self.wordList.addItem(item)

    def loadLengthDictionary(self):
        # Opens dictionary file and parses into a dictionary with word length as the key
        # length_dict[2] = ['am', 'be', 'do']
        with open('words_alpha.txt') as word_file:
            valid_words = list(word_file.read().split())
            length_dict = {length: [] for length in range(1, 46, 1)}
            for word in valid_words:
                length_dict[len(word)].append(word)
        del valid_words
        return length_dict

    def getApiDefinition(self, list_item):
        self.setDefinitionWidgetLoading()

        word = list_item.text()
        url = dictionary_api_url + word

        self.apiThread = ApiThread(self.requestDefinition, self.populateDefinitionWidget, url)

    # Sets the definition widget to loading state
    def setDefinitionWidgetLoading(self):
        # Set widget to 'loading...'
        self.definitionWidget.setText('Loading...')
        self.definitionWidget.setFont(AppTheme.title_label_font)
        self.definitionWidget.setAlignment(Qt.AlignCenter)

    # Used with apiThread to get the definition using http request
    def requestDefinition(self, url):
        request_definition = requests.get(url)
        return request_definition.json()

    # Called once the defintion request is fulfilled. Used to fill the definition widget with the defintion information.
    def populateDefinitionWidget(self, def_json):
        print('request data: ')
        print(json.dumps(def_json, indent=4, sort_keys=True))

        formatted_definiton_html = self.formatDefinitionJson(def_json)
        self.definitionWidget.setHtml(formatted_definiton_html)
        self.definitionWidget.setFont(AppTheme.definition_font)
        self.definitionWidget.setAlignment(Qt.AlignLeft)

    # Returns a formatted html string which is used to populate the definitions widget
    def formatDefinitionJson(self, def_json):
        formatted_html = ''
        for word_info in def_json:
            kwargs = {}
            kwargs['word'] = word_info['word']
            kwargs['phonetic'] = word_info['phonetic']
            html = self.word_info_html.format(**kwargs)

            for meaning in word_info['meanings']:
                kwargs = {}
                kwargs['word_type'] = meaning['partOfSpeech']
                for definition in meaning['definitions']:
                    kwargs['definition'] = definition['definition']
                    kwargs['synonyms'] = definition['synonyms']
                    html = html + self.meaning_html.format(**kwargs)
            print(word_info.keys())
            formatted_html = formatted_html + html
        return formatted_html

    word_info_html = (
                        '<header>'
                        '   <h1>{word}</h1>'
                        '   <span>({phonetic})<span>'
                        '</header>'
                        )

    meaning_html = (
                    '<div>'
                    '   <h3>Definition</h3>'
                    '   <p>{word_type} - {definition}</p>'
                    '   <h3>Synonyms</h3>'
                    '   <p>{synonyms}</p>'
                    '</div>'
                    )


class AnagramTab(CrosswordTab):
    def __init__(self):
        super(AnagramTab, self).__init__()
        self.searchSyntaxLabel.deleteLater()

    def populateWordList(self):
        given_word = self.searchLineEdit.text()
        letter_freq = Counter(given_word)

        # Finds words with the same amount of letters using collections.Counter
        # 'but' == 'tub' because each has one b, one u, and one t
        anagrams = []
        for word in self.lengthDictionary[len(given_word)]:
            if Counter(word) == letter_freq:
                anagrams.append(word)

        # Refresh the list with all current potential words
        self.wordList.clear()
        if anagrams:
            anagrams.remove(given_word)  # Remove the word itself from the list
            self.wordList.setEnabled(True)
            self.wordList.addItems(anagrams)
        else:
            # Display message if no valid words were found
            self.wordList.setEnabled(False)
            none_found = ['', 'No', 'matching', 'words', 'found']
            for word in none_found:
                item = QListWidgetItem(word)
                item.setTextAlignment(Qt.AlignHCenter)
                self.wordList.addItem(item)


class NotesTab(QWidget):
    def __init__(self):
        super(NotesTab, self).__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Add button to open font dialog
        self.fontButton = QPushButton('Select Font')
        self.fontButton.setStyleSheet(AppTheme.action_button_ss)
        self.fontButton.setFont(AppTheme.action_button_font)
        self.fontButton.clicked.connect(self.changeFont)
        self.layout.addWidget(self.fontButton, 1, 0)

        # Add text edit for notes area
        self.notesTextEdit = QTextEdit()
        self.notesTextEdit.setFont(AppTheme.default_note_tab_font)
        self.layout.addWidget(self.notesTextEdit, 0, 0, 1, 0)

        # Add button to clear all notes
        self.clearButton = QPushButton('Clear Notes')
        self.clearButton.setStyleSheet(AppTheme.action_button_ss)
        self.clearButton.setFont(AppTheme.action_button_font)
        self.clearButton.clicked.connect(self.notesTextEdit.clear)
        self.layout.addWidget(self.clearButton, 1, 1)


    def changeFont(self):
        font, ok = QFontDialog.getFont(self.notesTextEdit.font())
        if ok:
            self.notesTextEdit.setFont(font)
        # self.notesTextEdit.setFont(QFontDialog.getFont())


class SudokuGrid(QWidget):
    # puzzle is a list of 9 rows, each row is a list of 9 digits
    def __init__(self, puzzle=None):
        super(SudokuGrid, self).__init__()
        self.rows = puzzle
        self.constructGrid()
        self.noteMode = False
        if self.rows is not None:
            self.populatePuzzle(self.rows)
        else:
            self.rows = [[0 for _ in range(9)] for _ in range(9)]
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
                cell = Cell(parent=self, coords=(i, j))
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

    # Called to update data structures when a cell value is changed
    def updateDataStructures(self, value, coords):
        row, col = coords
        self.rows[row][col] = value
        self.cols[col][row] = value
        self.boxes[(row // 3) * 3 + (col // 3)][(row%3) * 3 + (col%3)] = value

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
                    cell.setStyleSheet(AppTheme.given_cell_default_ss)
                    cell.setFont(AppTheme.cell_default_font)

    # Helper function to get cell object using coordinates
    def getCell(self, row, col):
        box = self.grid_layout.itemAtPosition(row // 3, col // 3)
        return box.itemAtPosition(row % 3, col % 3).widget()

    # Function for navigating sudoku grid with arrow keys
    def arrowMove(self, coords, move):
        # coords = (row, column) where row 0 is top row and column 0 is left column
        if move == 'Left':
            if coords[1] == 0:
                self.getCell(coords[0], 8).setFocus()
            else:
                self.getCell(coords[0], coords[1]-1).setFocus()
        elif move == 'Right':
            if coords[1] == 8:
                self.getCell(coords[0], 0).setFocus()
            else:
                self.getCell(coords[0], coords[1]+1).setFocus()
        elif move == 'Up':
            if coords[0] == 0:
                self.getCell(8, coords[1]).setFocus()
            else:
                self.getCell(coords[0]-1, coords[1]).setFocus()
        elif move == 'Down':
            if coords[0] == 8:
                self.getCell(0, coords[1]).setFocus()
            else:
                self.getCell(coords[0]+1, coords[1]).setFocus()

    def solveCurrentGrid(self):
        # Checks validity of the current grid before passing it to solver
        valid = True
        for row in self.rows:
            row = [i for i in row if i is not None]
            if len(row) != len(set(row)):
                valid = False
                break
        if valid:
            for col in self.cols:
                col = [i for i in col if i is not None]
                if len(col) != len(set(col)):
                    valid = False
                    break
            if valid:
                for box in self.boxes:
                    box = [i for i in box if i is not None]
                    if len(box) != len(set(box)):
                        valid = False
                        break

        # Solve if valid or display dialog box if invalid
        if valid:
            puzzle = Sudoku(3, 3, board=self.rows).solve()
            self.populatePuzzle(puzzle.solve().board)
        else:
            dialog = QMessageBox()
            dialog.setWindowIcon(QIcon('puzzle_pieces.jpg'))
            dialog.setWindowTitle('Invalid')
            dialog.setText('Invalid Puzzle/No Solution')
            dialog.exec()

    def isNoteModeEnabled(self):
        return self.noteMode


# Label class for setting up sudoku grid
class Cell(QLabel):
    def __init__(self, value=None, parent=None, coords=None):
        super(Cell, self).__init__()
        self.parent = parent
        self.coords = coords
        self.value = value
        self.given = False
        self.notes = []
        if value is not None:
            self.setText(str(value))

        self.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(60, 60)

        self.setFont(AppTheme.cell_default_font)
        self.setStyleSheet(AppTheme.cell_default_ss)
        self.setTextFormat(Qt.RichText)
        self.setWordWrap(True)

    def isGiven(self):
        return self.given

    def focusInEvent(self, event):
        if self.isGiven():
            self.setStyleSheet(AppTheme.given_cell_focus_in_ss)
        else:
            self.setStyleSheet(AppTheme.cell_focus_in_ss)

    def focusOutEvent(self, event):
        self.parent.currentCell = self
        if self.isGiven():
            self.setStyleSheet(AppTheme.given_cell_default_ss)
        else:
            self.setStyleSheet(AppTheme.cell_default_ss)

    # Fills or clears focused cell depending on key stroke
    def keyPressEvent(self, event):
        # Used to fill cells with a value
        if (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9) and (not self.isGiven()):
            # Sets notes in the cell
            if self.parent.isNoteModeEnabled():
                text = self.constructNoteString(str(event.key() - Qt.Key_0))
                self.setFont(AppTheme.cell_note_font)
                self.parent.updateDataStructures(None, self.coords)
            # Sets number in the cell
            else:
                text = str(event.key() - Qt.Key_0)
                if text not in self.notes:
                    self.notes.append(text)
                self.setFont(AppTheme.cell_default_font)
                self.parent.updateDataStructures(int(text), self.coords)
            self.setText(text)
        # Used to clear a cell
        elif (event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete) and (not self.isGiven()):
            self.setText('')
            if self.parent.isNoteModeEnabled():
                self.notes.clear()
            self.parent.updateDataStructures(None, self.coords)
        # Used for cell navigation with arrow keys
        elif (event.key() >= Qt.Key_Left and event.key() <= Qt.Key_Down):
            # Pass coords of current cell and a string containing the move
            self.parent.arrowMove(self.coords, QKeySequence(event.key()).toString())


    # Creates a properly formatted string for the cell
    def constructNoteString(self, num):
        if num not in self.notes:
            self.notes.append(num)
        else:
            self.notes.remove(num)
        note = ''.join(sorted(self.notes))
        # Puts label on 2 lines if it is too long
        l = len(note)
        if l > 5:
            top = note[:-(-l//2)] + ' <br> '
            bottom = note[-(-l//2):]
            note = ''.join((top, bottom))
        return note


class CalculateButton(QPushButton):
    def __init__(self, label):
        super(CalculateButton, self).__init__(label)
        # Set keyboard shortcuts
        for seq in ['Return', 'Enter']:
            shortcut = QShortcut(seq, self)
            shortcut.activated.connect(self.animateClick)
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


# Thread for sending API requests
class ApiThread(QThread):
    finished = pyqtSignal(list)

    # Pass in the request function, the function to call when finished, and the full api url
    def __init__(self, func, on_finish, url):
        super(ApiThread, self).__init__()
        self.func = func
        self.finished.connect(on_finish)
        self.url = url
        self.start()

    def run(self):
        try:
            result = self.func(self.url)
        except Exception as e:
            print('exception in thread is %s' % e)
            result = [e]
        finally:
            self.finished.emit(result)


def get_words_by_length():
    with open('words_alpha.txt') as word_file:
        valid_words = list(word_file.read().split())
        length_dict = {length: [] for length in range(1, 46, 1)}
        for word in valid_words:
            length_dict[len(word)].append(word)
    return length_dict

def anagram_testing():
    import time
    start = time.time()

    words_by_length = get_words_by_length()

    test_word = 'counter'
    letter_freq = Counter(test_word)

    anagrams = []
    for word in words_by_length[len(test_word)]:
        if Counter(word) == letter_freq:
            anagrams.append(word)

    print(anagrams)
    print('time: ', time.time()-start)

def dictionary_testing():
    import time
    start = time.time()

    # Gets English words and stores them in a dictionary where key is the length of the words
    words_by_length = get_words_by_length()

    # Gets a word from the user and finds the locations of the given letters
    test_word = "_p__h____"
    indexed_letters = [(char, index) for index, char in enumerate(test_word) if char.isalpha()]

    # Iterates through the list stored at the appropriate length key
    # If the word has letters in matching locations it appends it to a list
    possible_words = []
    for word in words_by_length[len(test_word)]:
        for letter, index in indexed_letters:
            if word[index] != letter:
                break
        else:
            possible_words.append(word)
    print(possible_words)

    print('time: ', time.time() - start)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())

    # anagram_testing()
    # dictionary_testing()
