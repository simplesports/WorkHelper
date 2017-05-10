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
        self.VoltageDropGUI.comboBox_Wire_Type.addItems(["CU", "AL"])
        self.VoltageDropGUI.comboBox_Load_Type.addItems(["Lighting", "Receptacles", "Motor", "Electrical Heating", "Electrical Misc"])
        self.VoltageDropGUI.comboBox_Wire_Size.addItems(["14","12","10","8","6","4","3","2","1","1/0","2/0","3/0","4/0","250","300","350","400","500","600","700","750","1000"])
        self.VoltageDropGUI.comboBox_Wire_Insulation.addItems(["THHN","THWN","THWN-2","THHW","THW","THW-2","XHHW","XHHW-2","XHH","RHH","RHW","RHW-2"])
        self.VoltageDropGUI.comboBox_Phase.addItems(["1","3"])
        self.VoltageDropGUI.comboBox_Panel_Voltage.addItems(["120/240V-1PH-3W","240/480-1PH-3W","208Y/120V-3PH-4W","480Y/277-3PH-4W"])

        self.VoltageDropGUI.comboBox_Wire_Insulation.setCurrentIndex(1)
        self.VoltageDropGUI.comboBox_Wire_Size.setCurrentIndex(1)

        self.setUpVoltageDropUi()
        self.phaseTotalShow()
        self.LoadInputs()


    def setUpVoltageDropUi(self):
        self.hideOptions()
        self.VoltageDropGUI.comboBox_Panel_Voltage.activated[str].connect(self.phaseTotalShow)
        self.VoltageDropGUI.Button_Show_more_Options.clicked.connect(self.hideShowOptions)


    def phaseTotalShow(self):

        if self.VoltageDropGUI.comboBox_Panel_Voltage.currentText() == "120/240V-1PH-3W" or self.VoltageDropGUI.comboBox_Panel_Voltage.currentText() == "240/480-1PH-3W":
            self.VoltageDropGUI.UserInput_Phase_B.hide()
            self.VoltageDropGUI.text_Phase_B.hide()
            self.VoltageDropGUI.text_Phase_A.setText("Phase 1")
            self.VoltageDropGUI.text_Phase_C.setText("Phase 2")
        else:
            self.VoltageDropGUI.UserInput_Phase_B.show()
            self.VoltageDropGUI.text_Phase_B.show()
            self.VoltageDropGUI.text_Phase_A.setText("Phase A")
            self.VoltageDropGUI.text_Phase_C.setText("Phase C")

    def hideShowOptions(self):
        if self.VoltageDropGUI.Button_Show_more_Options.text()=="Show more Options":
            self.showOptions()
            self.VoltageDropGUI.Button_Show_more_Options.setText("Hide Options")
        else:
            self.hideOptions()
            self.VoltageDropGUI.Button_Show_more_Options.setText("Show more Options")

    def hideOptions(self):
        self.VoltageDropGUI.text_Phase.hide()
        self.VoltageDropGUI.comboBox_Phase.hide()
        self.VoltageDropGUI.text_Wire_Size.hide()
        self.VoltageDropGUI.comboBox_Wire_Size.hide()
        self.VoltageDropGUI.text_Wire_Insulation.hide()
        self.VoltageDropGUI.comboBox_Wire_Insulation.hide()

    def showOptions(self):
        self.VoltageDropGUI.text_Phase.show()
        self.VoltageDropGUI.comboBox_Phase.show()
        self.VoltageDropGUI.text_Wire_Size.show()
        self.VoltageDropGUI.comboBox_Wire_Size.show()
        self.VoltageDropGUI.text_Wire_Insulation.show()
        self.VoltageDropGUI.comboBox_Wire_Insulation.show()

    def LoadInputs(self):

        try:
            for i in range(0, len(Functions.Loads['Voltage'])):
                self.VoltageDropGUI.text_Load_Name = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Load_Name.setObjectName("text_Load_Name")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Name, i, 0, 1, 1)
                self.VoltageDropGUI.text_Load_Name.setText("Test Load1")

                self.VoltageDropGUI.text_equal = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_equal.setObjectName("text_equal")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_equal, i, 1, 1, 1)
                self.VoltageDropGUI.text_equal.setText("=")

                self.VoltageDropGUI.text_Load_Value = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Load_Value.setObjectName("text_Load_Value")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Value, i, 2, 1, 1)
                self.VoltageDropGUI.text_Load_Value.setText("200")

                self.VoltageDropGUI.text_VA = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_VA.setObjectName("text_VA")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_VA, i, 3, 1, 1)
                self.VoltageDropGUI.text_VA.setText("VA X")

                self.VoltageDropGUI.UserInput_Num_Load = QtWidgets.QLineEdit(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.UserInput_Num_Load.setObjectName("UserInput_Num_Load")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.UserInput_Num_Load, i, 4, 1, 1)

                self.VoltageDropGUI.text_at = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_at.setObjectName("text_at")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_at, i, 5, 1, 1)
                self.VoltageDropGUI.text_at.setText("at")

                self.VoltageDropGUI.text_Load_Voltage = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Load_Voltage.setObjectName("text_Load_Voltage")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Voltage, i, 6, 1, 1)
                self.VoltageDropGUI.text_Load_Voltage.setText("120")

                self.VoltageDropGUI.text_Voltage = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Voltage.setObjectName("text_Voltage")
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Voltage, i, 7, 1, 1)
                self.VoltageDropGUI.text_Voltage.setText("V")

        except:
            # add message box to alert the user they need to add loads first

            pass
