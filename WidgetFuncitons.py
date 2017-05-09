import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Load_Input_GUI import *
from Voltage_Drop_GUI import *
import Functions
import math
import pdb

class LoadInput(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.LoadInputGUI = Ui_LoadInput()
        self.LoadInputGUI.setupUi(self)
        self.setUpLoadInputUi()
        self.LoadInputGUI.comboBox_Voltage.addItems(["120", "240", "277", "480"])
        self.LoadInputGUI.comboBox_Utility.addItems(["Xcel"])
        self.LoadInputGUI.tableWidget.setHorizontalHeaderLabels(('Load Name', 'Voltage', 'Wattage', 'Power Factor', 'VA', 'Utility'))
        self.LoadInputGUI.UserInput_Wattage.setFixedWidth(50)
        self.LoadInputGUI.UserInput_Power_Factor.setFixedWidth(50)
        self.getLoadValues()
        self.modifyTableIndex = 0


    def setUpLoadInputUi(self):
        self.LoadInputGUI.Button_Add_To_Window.clicked.connect(self.sendToLoadTable)
        self.LoadInputGUI.UserInput_Wattage.textChanged[str].connect(self.getVA)
        self.LoadInputGUI.UserInput_Power_Factor.textChanged[str].connect(self.getVA)
        self.LoadInputGUI.Button_Remove_Load.clicked.connect(self.removeTableItem)
        self.LoadInputGUI.tableWidget.doubleClicked.connect(self.modifyValues)
        self.LoadInputGUI.Button_Modify_Load.clicked.connect(self.sendModified)
        self.LoadInputGUI.Button_Modify_Load.hide()

    def sendToLoadTable(self):

        LoadName = self.LoadInputGUI.UserInput_Load_Name.text()
        Voltage = self.LoadInputGUI.comboBox_Voltage.currentText()
        Wattage = self.LoadInputGUI.UserInput_Wattage.text()
        PF = self.LoadInputGUI.UserInput_Power_Factor.text()
        VA = self.LoadInputGUI.Text_VA_RESULTS.text()
        Utility = self.LoadInputGUI.comboBox_Utility.currentText()

        rowPosition = self.LoadInputGUI.tableWidget.rowCount()
        self.LoadInputGUI.tableWidget.insertRow(rowPosition)
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(LoadName))
        self.LoadInputGUI.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(Voltage))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(Wattage))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(PF))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(VA))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(Utility))

        Functions.Loads['LoadName'].append(LoadName)
        Functions.Loads['Voltage'].append(Voltage)
        Functions.Loads['Wattage'].append(Wattage)
        Functions.Loads['PF'].append(PF)
        Functions.Loads['VA'].append(VA)
        Functions.Loads['Utility'].append(Utility)
        #pdb.set_trace()

    def removeTableItem(self):
        #rowTotal = self.LoadInputGUI.tableWidget.rowCount()
        try:
            model = self.LoadInputGUI.tableWidget
            index_list = []
            for model_index in self.LoadInputGUI.tableWidget.selectionModel().selectedRows():
                index = QtCore.QPersistentModelIndex(model_index)
                index_list.append(index)

            for index in index_list:
                Functions.Loads['LoadName'].pop(index.row())
                Functions.Loads['Voltage'].pop(index.row())
                Functions.Loads['Wattage'].pop(index.row())
                Functions.Loads['PF'].pop(index.row())
                Functions.Loads['VA'].pop(index.row())
                Functions.Loads['Utility'].pop(index.row())
                model.removeRow(index.row())

        except:
            pass


    def modifyValues(self):

        self.LoadInputGUI.Button_Modify_Load.show()
        self.LoadInputGUI.Button_Add_To_Window.hide()
        self.LoadInputGUI.Button_Remove_Load.hide()

        indices = self.LoadInputGUI.tableWidget.selectionModel().selectedRows()
        for index in sorted(indices):
            LoadName = self.LoadInputGUI.tableWidget.item(index.row(),0).text()
            Voltage = self.LoadInputGUI.tableWidget.item(index.row(),1).text()
            Wattage = self.LoadInputGUI.tableWidget.item(index.row(),2).text()
            PF = self.LoadInputGUI.tableWidget.item(index.row(),3).text()
            VA = self.LoadInputGUI.tableWidget.item(index.row(),4).text()
            Utility = self.LoadInputGUI.tableWidget.item(index.row(),5).text()
            self.modifyTableIndex = index.row()

        self.LoadInputGUI.UserInput_Load_Name.setText(LoadName)
        indexVoltage = self.LoadInputGUI.comboBox_Voltage.findText(Voltage, QtCore.Qt.MatchFixedString)
        if indexVoltage >= 0:
            self.LoadInputGUI.comboBox_Voltage.setCurrentIndex(indexVoltage)
        self.LoadInputGUI.UserInput_Wattage.setText(Wattage)
        self.LoadInputGUI.UserInput_Power_Factor.setText(PF)
        indexUtility = self.LoadInputGUI.comboBox_Utility.findText(Utility, QtCore.Qt.MatchFixedString)
        if indexUtility >= 0:
            self.LoadInputGUI.comboBox_Utility.setCurrentIndex(indexUtility)


    def sendModified(self):
        self.LoadInputGUI.Button_Modify_Load.hide()
        self.LoadInputGUI.Button_Add_To_Window.show()
        self.LoadInputGUI.Button_Remove_Load.show()

        LoadName = self.LoadInputGUI.UserInput_Load_Name.text()
        Voltage = self.LoadInputGUI.comboBox_Voltage.currentText()
        Wattage = self.LoadInputGUI.UserInput_Wattage.text()
        PF = self.LoadInputGUI.UserInput_Power_Factor.text()
        VA = self.LoadInputGUI.Text_VA_RESULTS.text()
        Utility = self.LoadInputGUI.comboBox_Utility.currentText()

        rowPosition = self.modifyTableIndex
        #self.LoadInputGUI.tableWidget.insertRow(rowPosition)
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(LoadName))
        self.LoadInputGUI.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(Voltage))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(Wattage))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(PF))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(VA))
        self.LoadInputGUI.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(Utility))


        Functions.Loads['LoadName'][self.modifyTableIndex] = LoadName
        Functions.Loads['Voltage'][self.modifyTableIndex] = Voltage
        Functions.Loads['Wattage'][self.modifyTableIndex] = Wattage
        Functions.Loads['PF'][self.modifyTableIndex] = PF
        Functions.Loads['VA'][self.modifyTableIndex] = VA
        Functions.Loads['Utility'][self.modifyTableIndex] = Utility

        pdb.set_trace()

    def getVA(self):

        try:
            Voltage = float(self.LoadInputGUI.comboBox_Voltage.currentText())
            Wattage = float(self.LoadInputGUI.UserInput_Wattage.text())
            PF = float(self.LoadInputGUI.UserInput_Power_Factor.text())
            VA = Wattage/PF
            VA = math.ceil(VA/5)*5
            self.LoadInputGUI.Text_VA_RESULTS.setText(str(VA))
        except:
            VA = 0
            self.LoadInputGUI.Text_VA_RESULTS.setText(str(VA))

    def getLoadValues(self):
        try:
            numberPreviousEnteredLoads = len(Functions.Loads['Voltage'])
            if numberPreviousEnteredLoads > 0:
                for i in range(0,numberPreviousEnteredLoads):
                    rowPosition = self.LoadInputGUI.tableWidget.rowCount()
                    self.LoadInputGUI.tableWidget.insertRow(rowPosition)
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(Functions.Loads['LoadName'][i]))
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(Functions.Loads['Voltage'][i]))
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(Functions.Loads['Wattage'][i]))
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(Functions.Loads['PF'][i]))
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(Functions.Loads['VA'][i]))
                    self.LoadInputGUI.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(Functions.Loads['Utility'][i]))
                    #Loads = {'LoadName' : [], 'Voltage': [], 'Wattage': [], 'PF': [], 'VA': [], 'Utility':[]}
        except:
            pass
class VoltageDrop(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.VoltageDropGUI = Ui_VoltageDrop()
        self.VoltageDropGUI.setupUi(self)
