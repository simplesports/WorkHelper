import sys
from PyQt5.QtCore import *
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

        #pdb.set_trace()

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
    VoltageDropSignal = pyqtSignal()
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
        self.current_Panel = {'cktNumber':[],'cktInfo':[]}


    def setUpVoltageDropUi(self):
        self.hideOptions()
        self.VoltageDropGUI.comboBox_Panel_Voltage.activated[str].connect(self.phaseTotalShow)
        self.VoltageDropGUI.Button_Show_more_Options.clicked.connect(self.hideShowOptions)
        self.VoltageDropGUI.UserInput_Length.textChanged[str].connect(self.Voltage_Drop_Change_Values)
        self.VoltageDropGUI.comboBox_Wire_Type.activated[str].connect(self.Voltage_Drop_Change_Values)
        self.VoltageDropGUI.comboBox_Wire_Size.activated[str].connect(self.WireSelect_Voltage_Drop)
        self.VoltageDropGUI.comboBox_Phase.activated[str].connect(self.WireSelect_Voltage_Drop)
        self.VoltageDropGUI.Button_Save.clicked.connect(self.saveVoltageDrop)
        self.VoltageDropGUI.Button_Add_To_Table.clicked.connect(self.addToTable)
        self.VoltageDropGUI.tableWidget.doubleClicked.connect(self.reloadData_editCircuit)
        self.VoltageDropGUI.Button_Update_Circuit.clicked.connect(self.Update_Circuit)
        self.VoltageDropGUI.Button_Cancel.clicked.connect(self.cancel_Update)

        self.VoltageDropGUI.Button_Update_Circuit.hide()
        self.VoltageDropGUI.Button_Cancel.hide()

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
                self.VoltageDropGUI.text_Load_Name.setObjectName("text_Load_Name-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Name, i, 0, 1, 1)
                self.VoltageDropGUI.text_Load_Name.setText(Functions.Loads['LoadName'][i])

                self.VoltageDropGUI.text_equal = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_equal.setObjectName("text_equal-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_equal, i, 1, 1, 1)
                self.VoltageDropGUI.text_equal.setText("=")

                self.VoltageDropGUI.text_Load_Value = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Load_Value.setObjectName("text_Load_Value-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Value, i, 2, 1, 1)
                self.VoltageDropGUI.text_Load_Value.setText(Functions.Loads['VA'][i])

                self.VoltageDropGUI.text_VA = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_VA.setObjectName("text_VA-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_VA, i, 3, 1, 1)
                self.VoltageDropGUI.text_VA.setText("VA X")

                self.VoltageDropGUI.UserInput_Num_Load = QtWidgets.QLineEdit(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.UserInput_Num_Load.setObjectName("UserInput_Num_Load-"+str(i))
                self.VoltageDropGUI.UserInput_Num_Load.textChanged[str].connect(self.TotalVA)
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.UserInput_Num_Load, i, 4, 1, 1)

                self.VoltageDropGUI.text_at = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_at.setObjectName("text_at"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_at, i, 5, 1, 1)
                self.VoltageDropGUI.text_at.setText("at")

                self.VoltageDropGUI.text_Load_Voltage = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Load_Voltage.setObjectName("text_Load_Voltage-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Load_Voltage, i, 6, 1, 1)
                self.VoltageDropGUI.text_Load_Voltage.setText(Functions.Loads['Voltage'][i])

                self.VoltageDropGUI.text_Voltage = QtWidgets.QLabel(self.VoltageDropGUI.scrollAreaWidgetContents)
                self.VoltageDropGUI.text_Voltage.setObjectName("text_Voltage-"+str(i))
                self.VoltageDropGUI.gridLayout_Load_List.addWidget(self.VoltageDropGUI.text_Voltage, i, 7, 1, 1)
                self.VoltageDropGUI.text_Voltage.setText("V")

        except:
            # add message box to alert the user they need to add loads first

            pass

    def TotalVA(self):
        Total_Number_of_Loads = len(Functions.Loads['Voltage'])
        total = 0

        try:
            for i in range(0,Total_Number_of_Loads):
                numLoads_textBox = self.findChildren(QLineEdit, "UserInput_Num_Load-"+str(i))[0]
                VA_text = self.findChildren(QLabel, "text_Load_Value-"+str(i))[0]
                if numLoads_textBox.text() == '':
                    numLoads_textBox = 0
                else:
                    numLoads_textBox = int(numLoads_textBox.text())
                VA_text = int(VA_text.text())
                subtotal= numLoads_textBox * VA_text
                total = subtotal + total
        except:
            total = 0

        self.VoltageDropGUI.text_Total_VA_RESULTS.setText(str(total))
        voltage = self.circuitVoltage(Total_Number_of_Loads)
        self.VoltageDropGUI.text_Circuit_Voltage_RESULTS.setText(str(voltage))

        try:
            current = round(total/voltage,2)
            self.VoltageDropGUI.text_Total_Current_RESULTS.setText(str(current))
        except:
            self.VoltageDropGUI.text_Total_Current_RESULTS.setText(str(0))

        try:
            self.Voltage_Drop_Change_Values()
        except:
            pass

    def circuitVoltage(self,totalLoads):
        total = 0
        try:
            for i in range(0, totalLoads):
                Voltage_of_Circuit = self.findChildren(QLabel, "text_Load_Voltage-"+str(i))[0]
                Voltage_of_Circuit = int(Voltage_of_Circuit.text())
                total = Voltage_of_Circuit + total
                #pdb.set_trace()
        except:
            total = 0

        try:
            CheckVoltage = total/totalLoads
        except:
            CheckVoltage = 0

        return CheckVoltage

            #print(str(total))

    def Voltage_Drop_Calc_Auto_Wire_Size(self,Distance,wireType,Phase,Current,circuitVoltage):

        for i in range(0,len(Functions.wireSizeCircularMill)):
            VoltageDrop = round((self.PhaseCheck(Phase) * self.CUorAL(wireType) * float(Current) * float(Distance))/Functions.wireSizeCircularMill[i],2)
            VoltageDropPre = VoltageDrop/float(circuitVoltage)

            if VoltageDropPre < 0.03:
                break

            #print('Phase: ' +str(self.PhaseCheck(Phase)))
            #print('CUorAL:' +str(self.CUorAL(wireType)))
            #print('Current: '+ str(Current))
            #print('Distance: '+ str(Distance))
            #print('Wire Size Mills' + str(wireSizeCircularMill[i]))

        return [VoltageDrop,VoltageDropPre,i]

    def CUorAL(self,input):
        if input == 'CU':
            output = 12.9
        else:
            output = 21.2
        return output

    def PhaseCheck(self,input):
        if input == '1':
            output = 2
        else:
            output = 1.732
        return output

    def Voltage_Drop_Change_Values(self):
        # This is for it automaticaly selecting the wire size and changing the values on the form
        try:
            Distance = self.VoltageDropGUI.UserInput_Length.text()
            wireType = self.VoltageDropGUI.comboBox_Wire_Type.currentText()
            Phase = self.VoltageDropGUI.comboBox_Phase.currentText()
            Current = self.VoltageDropGUI.text_Total_Current_RESULTS.text()
            circuitVoltage = self.VoltageDropGUI.text_Circuit_Voltage_RESULTS.text()

            Voltage_calcs = self.Voltage_Drop_Calc_Auto_Wire_Size(Distance,wireType,Phase,Current,circuitVoltage)

            self.VoltageDropGUI.text_Total_Voltage_Drop_RESULTS.setText(str(Voltage_calcs[0]))
            self.VoltageDropGUI.text_Pre_Voltage_Drop_2.setText(str(round(Voltage_calcs[1]*100,2)))
            self.VoltageDropGUI.comboBox_Wire_Size.setCurrentIndex(Voltage_calcs[2])
            self.VoltageDropGUI.Text_Wire_Size_RESULTS.setText(self.VoltageDropGUI.comboBox_Wire_Size.currentText())
        except:
            pass

    def Voltage_Drop_Calc(self,Distance,wireType,Phase,Current,circuitVoltage,WireSizeIndex):
        #This is just the pure VoltageDrop Calculation
        if Distance == '':
            Distance = 0

        VoltageDrop = round((self.PhaseCheck(Phase) * self.CUorAL(wireType) * float(Current) * float(Distance))/Functions.wireSizeCircularMill[WireSizeIndex],2)

        VoltageDropPre = VoltageDrop/float(circuitVoltage)
        return [VoltageDrop,VoltageDropPre]

    def WireSelect_Voltage_Drop(self):

        if self.VoltageDropGUI.Button_Show_more_Options.text() =='Hide Options':
            Distance = self.VoltageDropGUI.UserInput_Length.text()
            wireType = self.VoltageDropGUI.comboBox_Wire_Type.currentText()
            Phase = self.VoltageDropGUI.comboBox_Phase.currentText()
            Current = self.VoltageDropGUI.text_Total_Current_RESULTS.text()
            circuitVoltage = self.VoltageDropGUI.text_Circuit_Voltage_RESULTS.text()
            currentWireSize = self.VoltageDropGUI.comboBox_Wire_Size.currentIndex()

            Voltage_calcs = self.Voltage_Drop_Calc(Distance,wireType,Phase,Current,circuitVoltage,currentWireSize)
            self.VoltageDropGUI.text_Total_Voltage_Drop_RESULTS.setText(str(Voltage_calcs[0]))
            self.VoltageDropGUI.text_Pre_Voltage_Drop_2.setText(str(round(Voltage_calcs[1]*100,2)))
            self.VoltageDropGUI.Text_Wire_Size_RESULTS.setText(self.VoltageDropGUI.comboBox_Wire_Size.currentText())

    def addToTable(self):
#To add:
#change order of table so that wire size is closer to the front
        Check = self.errorCheck_addToTable()

        ErrorFree = Check[0]
        ErrorMessage = Check[1]

        if ErrorFree == 1:

            circuitNumber = self.VoltageDropGUI.UserInput_Circuit_Number.text()
            length = self.VoltageDropGUI.UserInput_Length.text()
            total_VA = self.VoltageDropGUI.text_Total_VA_RESULTS.text()
            circuitVoltage = self.VoltageDropGUI.text_Circuit_Voltage_RESULTS.text()
            current = self.VoltageDropGUI.text_Total_Current_RESULTS.text()
            wire_size = self.VoltageDropGUI.comboBox_Wire_Size.currentText()
            wire_type = self.VoltageDropGUI.comboBox_Wire_Type.currentText()
            wire_insulation = self.VoltageDropGUI.comboBox_Wire_Insulation.currentText()
            phase = self.VoltageDropGUI.comboBox_Phase.currentText()
            total_voltage_drop = self.VoltageDropGUI.text_Total_Voltage_Drop_RESULTS.text()
            pre_V_Drop = self.VoltageDropGUI.text_Pre_Voltage_Drop_2.text()
            load_type = self.VoltageDropGUI.comboBox_Load_Type.currentText()
            phase = self.VoltageDropGUI.comboBox_Phase.currentText()


            num_of_lum = {'Lum_name':[],'lum_QTY':[]}

            for i in range(0, len(Functions.Loads['Voltage'])):
                numLoads = self.findChildren(QLineEdit, "UserInput_Num_Load-"+str(i))[0]
                Load_Name = self.findChildren(QLabel, "text_Load_Name-"+str(i))[0]
                num_of_lum['Lum_name'].append(Load_Name.text())
                num_of_lum['lum_QTY'].append(numLoads.text())

            current_circuit = {'Length':length,'total_VA':total_VA,'circuit_Voltage':circuitVoltage,'current':current,'wire_size':wire_size,'wire_type':wire_type,'wire_insulation':wire_insulation,'phase':phase,'total_voltage_drop':total_voltage_drop,'pre_V_Drop':pre_V_Drop,'load_type':load_type,'Num_of_lum':num_of_lum}
            self.current_Panel['cktNumber'].append(self.VoltageDropGUI.UserInput_Circuit_Number.text())
            self.current_Panel['cktInfo'].append(current_circuit)

            rowPosition = self.VoltageDropGUI.tableWidget.rowCount()
            self.VoltageDropGUI.tableWidget.insertRow(rowPosition)
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(circuitNumber))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(length))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(total_VA))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(circuitVoltage))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(current))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(wire_size))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(wire_type))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 7, QTableWidgetItem(wire_insulation))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 8, QTableWidgetItem(phase))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 9, QTableWidgetItem(total_voltage_drop))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 10, QTableWidgetItem(pre_V_Drop))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 11, QTableWidgetItem(load_type))


            self.VoltageDropGUI.UserInput_Circuit_Number.setText("")
            self.VoltageDropGUI.UserInput_Length.setText("")
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: black")
            self.VoltageDropGUI.text_Length.setStyleSheet("color: black")

            self.updateTotalPhaseLoad()
            #pdb.set_trace()


        else:
            #Make sure to add an error so that they can't type in a circuit greater than 80
            QMessageBox.about(self, "Something isn't right", ErrorMessage)

            #print(":(")

    def updateTotalPhaseLoad(self):
        totalPhase1VA = 0
        totalPhase2VA = 0
        if self.VoltageDropGUI.comboBox_Panel_Voltage.currentText() == "120/240V-1PH-3W" or self.VoltageDropGUI.comboBox_Panel_Voltage.currentText() == "240/480-1PH-3W":

            for row in range(self.VoltageDropGUI.tableWidget.rowCount()):
                cktNumber = int(self.VoltageDropGUI.tableWidget.item(row,0).text())
                if cktNumber in Functions.phase1:
                    currentPhase1VA = int(self.VoltageDropGUI.tableWidget.item(row,2).text())
                    totalPhase1VA = totalPhase1VA + currentPhase1VA
                else:
                    currentPhase2VA = int(self.VoltageDropGUI.tableWidget.item(row,2).text())
                    totalPhase2VA = totalPhase2VA + currentPhase2VA

            self.VoltageDropGUI.UserInput_Phase_A.setText(str(totalPhase1VA))
            self.VoltageDropGUI.UserInput_Phase_C.setText(str(totalPhase2VA))
        else:
            pass
            # This section will be for the 3 phase panels.

    def reloadData_editCircuit(self):
        global editIndex
        global editRow

        #Get values from table****************************************************************************************************
        #
        #indices = self.VoltageDropGUI.tableWidget.selectionModel().selectedRows()
        #for index in sorted(indices):
        row = self.VoltageDropGUI.tableWidget.currentRow()
        editRow = row
        cktNumber = self.VoltageDropGUI.tableWidget.item(row,0).text()
        Length = self.VoltageDropGUI.tableWidget.item(row,1).text()
        wireSize = self.VoltageDropGUI.tableWidget.item(row,5).text()
        wireType = self.VoltageDropGUI.tableWidget.item(row,6).text()
        wireInsulation = self.VoltageDropGUI.tableWidget.item(row,7).text()
        phase = self.VoltageDropGUI.tableWidget.item(row,8).text()
        LoadType = self.VoltageDropGUI.tableWidget.item(row,11).text()
            #self.modifyTableIndex = index.row()
        #***************************************************************************************************************************
        #Update Buttons text and hide the rest button*******************************************************************************
        self.VoltageDropGUI.Button_Update_Circuit.show()
        self.VoltageDropGUI.Button_Cancel.show()
        self.VoltageDropGUI.Button_Add_To_Table.hide()
        self.VoltageDropGUI.Button_Remove_Circuit.hide()
        self.VoltageDropGUI.Button_Reset.hide()
        #**************************************************************************************************************************
        #Load all the values*******************************************************************************************************
        selectedCircuitidex = self.current_Panel['cktNumber'].index(cktNumber)
        editIndex = selectedCircuitidex
        #pdb.set_trace()
        selectedCircuitValues = self.current_Panel['cktInfo'][selectedCircuitidex]['Num_of_lum']

        Total_Number_of_Loads = len(Functions.Loads['Voltage'])


        try:
            for i in range(0,Total_Number_of_Loads):
                Loads_textBox = self.findChildren(QLineEdit, "UserInput_Num_Load-"+str(i))[0]
                loadName_text = self.findChildren(QLabel, "text_Load_Name-"+str(i))[0]
                for k in range(0, len(selectedCircuitValues['Lum_name'])):
                    if selectedCircuitValues['Lum_name'][k] == loadName_text.text():
                        Loads_textBox.setText(selectedCircuitValues['lum_QTY'][k])
                        break

        except:
            pass

        self.VoltageDropGUI.UserInput_Circuit_Number.setText(cktNumber)
        self.VoltageDropGUI.UserInput_Length.setText(Length)

        indexWireType = self.VoltageDropGUI.comboBox_Wire_Type.findText(wireType, QtCore.Qt.MatchFixedString)
        if indexWireType >= 0:
            self.VoltageDropGUI.comboBox_Wire_Type.setCurrentIndex(indexWireType)

        indexLoadType = self.VoltageDropGUI.comboBox_Load_Type.findText(LoadType, QtCore.Qt.MatchFixedString)
        if indexLoadType >= 0:
            self.VoltageDropGUI.comboBox_Load_Type.setCurrentIndex(indexLoadType)

        indexPhase = self.VoltageDropGUI.comboBox_Phase.findText(phase, QtCore.Qt.MatchFixedString)
        if indexPhase >= 0:
            self.VoltageDropGUI.comboBox_Phase.setCurrentIndex(indexPhase)

        indexWireInsulation = self.VoltageDropGUI.comboBox_Wire_Insulation.findText(wireInsulation, QtCore.Qt.MatchFixedString)
        if indexWireInsulation >= 0:
            self.VoltageDropGUI.comboBox_Wire_Insulation.setCurrentIndex(indexWireInsulation)

        indexWireSize = self.VoltageDropGUI.comboBox_Wire_Size.findText(wireSize, QtCore.Qt.MatchFixedString)
        if indexWireSize >= 0:
            self.VoltageDropGUI.comboBox_Wire_Size.setCurrentIndex(indexWireSize)
        #***************************************************************************************************************************
        #pdb.set_trace()
    def Update_Circuit(self):
        #set variable mode to 1 to avoid it checking for the same circuit number, but change the error so that it saves the original ckt number and will compare the rest.
        Check = self.errorCheck_addToTable(1)

        ErrorFree = Check[0]
        ErrorMessage = Check[1]

        if ErrorFree == 1:

            circuitNumber = self.VoltageDropGUI.UserInput_Circuit_Number.text()
            length = self.VoltageDropGUI.UserInput_Length.text()
            total_VA = self.VoltageDropGUI.text_Total_VA_RESULTS.text()
            circuitVoltage = self.VoltageDropGUI.text_Circuit_Voltage_RESULTS.text()
            current = self.VoltageDropGUI.text_Total_Current_RESULTS.text()
            wire_size = self.VoltageDropGUI.comboBox_Wire_Size.currentText()
            wire_type = self.VoltageDropGUI.comboBox_Wire_Type.currentText()
            wire_insulation = self.VoltageDropGUI.comboBox_Wire_Insulation.currentText()
            phase = self.VoltageDropGUI.comboBox_Phase.currentText()
            total_voltage_drop = self.VoltageDropGUI.text_Total_Voltage_Drop_RESULTS.text()
            pre_V_Drop = self.VoltageDropGUI.text_Pre_Voltage_Drop_2.text()
            load_type = self.VoltageDropGUI.comboBox_Load_Type.currentText()
            phase = self.VoltageDropGUI.comboBox_Phase.currentText()



            for i in range(0, len(Functions.Loads['Voltage'])):
                numLoads = self.findChildren(QLineEdit, "UserInput_Num_Load-"+str(i))[0]
                Load_Name = self.findChildren(QLabel, "text_Load_Name-"+str(i))[0]
                self.current_Panel['cktInfo'][editIndex]['Num_of_lum']['Lum_name'][i]=Load_Name.text()
                self.current_Panel['cktInfo'][editIndex]['Num_of_lum']['lum_QTY'][i]=numLoads.text()

            self.current_Panel['cktInfo'][editIndex]['Length'] = length
            self.current_Panel['cktInfo'][editIndex]['total_VA'] = total_VA
            self.current_Panel['cktInfo'][editIndex]['circuit_Voltage'] = circuitVoltage
            self.current_Panel['cktInfo'][editIndex]['current'] = current
            self.current_Panel['cktInfo'][editIndex]['wire_size'] = wire_size
            self.current_Panel['cktInfo'][editIndex]['wire_type'] = wire_type
            self.current_Panel['cktInfo'][editIndex]['wire_insulation'] = wire_insulation
            self.current_Panel['cktInfo'][editIndex]['phase'] = phase
            self.current_Panel['cktInfo'][editIndex]['total_voltage_drop'] = total_voltage_drop
            self.current_Panel['cktInfo'][editIndex]['pre_V_Drop'] = pre_V_Drop
            self.current_Panel['cktInfo'][editIndex]['load_type'] = load_type
            self.current_Panel['cktNumber'][editIndex] = circuitNumber

            #rowPosition = self.modifyTableIndex
            rowPosition = editRow
            #pdb.set_trace()

            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(circuitNumber))
            #pdb.set_trace()
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(length))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(total_VA))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(circuitVoltage))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(current))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(wire_size))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(wire_type))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 7, QTableWidgetItem(wire_insulation))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 8, QTableWidgetItem(phase))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 9, QTableWidgetItem(total_voltage_drop))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 10, QTableWidgetItem(pre_V_Drop))
            self.VoltageDropGUI.tableWidget.setItem(rowPosition, 11, QTableWidgetItem(load_type))

            #pdb.set_trace()

            self.VoltageDropGUI.UserInput_Circuit_Number.setText("")
            #pdb.set_trace()
            self.VoltageDropGUI.UserInput_Length.setText("")
            #pdb.set_trace()
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: black")
            #pdb.set_trace()
            self.VoltageDropGUI.text_Length.setStyleSheet("color: black")
            #pdb.set_trace()

            self.updateTotalPhaseLoad()
            #pdb.set_trace()

            self.VoltageDropGUI.Button_Update_Circuit.hide()
            self.VoltageDropGUI.Button_Cancel.hide()
            self.VoltageDropGUI.Button_Add_To_Table.show()
            self.VoltageDropGUI.Button_Remove_Circuit.show()
            self.VoltageDropGUI.Button_Reset.show()
            #pdb.set_trace()


        else:
            #Make sure to add an error so that they can't type in a circuit greater than 80
            QMessageBox.about(self, "Something isn't right", ErrorMessage)

            #print(":(")

    def cancel_Update(self):
        Total_Number_of_Loads = len(Functions.Loads['Voltage'])
        try:
            for i in range(0,Total_Number_of_Loads):
                Loads_textBox = self.findChildren(QLineEdit, "UserInput_Num_Load-"+str(i))[0]
                Loads_textBox.setText('')

        except:
            pass

        self.VoltageDropGUI.Button_Update_Circuit.hide()
        self.VoltageDropGUI.Button_Cancel.hide()
        self.VoltageDropGUI.Button_Add_To_Table.show()
        self.VoltageDropGUI.Button_Remove_Circuit.show()
        self.VoltageDropGUI.Button_Reset.show()

        self.VoltageDropGUI.UserInput_Circuit_Number.setText('')
        self.VoltageDropGUI.UserInput_Length.setText('')
        self.VoltageDropGUI.comboBox_Wire_Type.setCurrentIndex(0)
        self.VoltageDropGUI.comboBox_Load_Type.setCurrentIndex(0)
        self.VoltageDropGUI.comboBox_Wire_Insulation.setCurrentIndex(1)
        self.VoltageDropGUI.comboBox_Wire_Size.setCurrentIndex(1)

    def errorCheck_addToTable(self,mode=0):
        goodToGo = 1
        message = ''

        if len(self.VoltageDropGUI.UserInput_Circuit_Number.text()) == 0 and len(self.VoltageDropGUI.UserInput_Length.text()) == 0:
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: red")
            self.VoltageDropGUI.text_Length.setStyleSheet("color: red")
            message = 'You need to enter a unique circuit number and a distance.'
            goodToGo = 0
            return [goodToGo,message]
        elif len(self.VoltageDropGUI.UserInput_Circuit_Number.text()) == 0:
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: red")
            self.VoltageDropGUI.text_Length.setStyleSheet("color: black")
            message = 'You need to enter a unique circuit number'
            goodToGo = 0
            return [goodToGo,message]
        elif len(self.VoltageDropGUI.UserInput_Length.text()) == 0:
            self.VoltageDropGUI.text_Length.setStyleSheet("color: red")
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: black")
            message = 'You need to enter a distance for this circuit'
            goodToGo = 0
            return [goodToGo,message]

        try:
            cktNumber = int(self.VoltageDropGUI.UserInput_Circuit_Number.text())
        except:
            goodToGo = 0
            message = 'The circuit number must only be a whole number'
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: red")
            self.VoltageDropGUI.text_Length.setStyleSheet("color: black")
            return [goodToGo,message]

        try:
            distance = int(self.VoltageDropGUI.UserInput_Length.text())
        except:
            goodToGo = 0
            message = 'The Distance must be a whole number. Round up if you have to'
            self.VoltageDropGUI.text_Length.setStyleSheet("color: red")
            self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: black")
            return [goodToGo,message]

        if mode == 0:
            items = self.VoltageDropGUI.tableWidget.findItems(self.VoltageDropGUI.UserInput_Circuit_Number.text(), Qt.MatchExactly)
            for i in range(0, len(items)):
                if items[i].column() == 0:
                    if items[i].text() == self.VoltageDropGUI.UserInput_Circuit_Number.text():
                        goodToGo = 0
                        message = 'You need to have a unique circuit number. This one is already taken'
                        self.VoltageDropGUI.text_Circuit_Number.setStyleSheet("color: red")
                        self.VoltageDropGUI.text_Length.setStyleSheet("color: black")
                        break


        return [goodToGo,message]


    def saveVoltageDrop(self):
            tempVoltageDropValues = {}
        #try:
            if len(self.VoltageDropGUI.UserInput_Panel_Name.text()) > 0:
                tempVoltageDropValues.update({'panelInfo':self.current_Panel,'Panel_Voltage':self.VoltageDropGUI.comboBox_Panel_Voltage.currentText()})
                Functions.Voltage_Drop_Panels.update({self.VoltageDropGUI.UserInput_Panel_Name.text():tempVoltageDropValues})
                #newEntry = QListWidgetItem(self.VoltageDropGUI.UserInput_Panel_Name.text())
                #MainUi.listBox_Voltage_Drop.addItem(newEntry)

                self.VoltageDropSignal.emit()
        #except:
            #pass
