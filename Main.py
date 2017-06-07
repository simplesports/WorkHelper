import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Main_GUI import *
from WidgetFuncitons import *
from zipfile import ZipFile
import json
import Functions


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self,parent)
        self.MainUi = Ui_MainWindow()
        self.MainUi.setupUi(self)
        self.setUpMainUiFunction()
        self.setUpToolBar()


    def setUpMainUiFunction(self):
        #Here is where all of the button functions will be definded
        self.MainUi.pushButton_Add_Lum_Load.clicked.connect(self.showLoadInput)
        self.MainUi.Button_New_Voltage_Drop_Calc.clicked.connect(self.showVoltageDrop)
        self.MainUi.actionSaveAs.triggered.connect(self.saveAs)
        self.MainUi.actionSaveAs.setShortcut('Ctrl+Shift+S')
        self.MainUi.actionOpen.triggered.connect(self.open)
        self.MainUi.actionOpen.setShortcut('Ctrl+O')

    def setUpToolBar(self):
        LoadButton = QAction(QIcon("Icons/light.png"),'Edit Project Luminaries', self)
        LoadButton.triggered.connect(self.showLoadInput)
        self.MainUi.toolBar.addAction(LoadButton)

    def showLoadInput(self):
        sub = QtWidgets.QMdiSubWindow()
        Load_Input = LoadInput()
        sub.setWidget(Load_Input)
        sub.setObjectName("Load_Input_window")
        sub.setWindowTitle("Load Input")
        self.MainUi.mdiArea.addSubWindow(sub)
        sub.show()

    def showVoltageDrop(self):
        subVoltage = QtWidgets.QMdiSubWindow()
        Voltage_Drop = VoltageDrop()
        subVoltage.setWidget(Voltage_Drop)
        subVoltage.setObjectName("Voltage_Drop_window")
        subVoltage.setWindowTitle("Voltage Drop Calculator")
        Voltage_Drop.VoltageDropSignal.connect(self.updateVoltageDrop)
        self.MainUi.mdiArea.addSubWindow(subVoltage)
        subVoltage.show()

    def saveAs(self):
        #data = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)

        data = json.dumps(['Loads',Functions.Loads])
        try:
            with ZipFile(fileName, 'w') as myzip:
                myzip.writestr('digest.json', data)
        except:
            pass

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileToOpen, _ = QFileDialog.getOpenFileNames(self,"Open File", "","All Files (*);;Python Files (*.py)", options=options)
        except:
            pass

        if fileToOpen:
            with ZipFile(fileToOpen[0], 'r') as myzip:
                json_data_read = myzip.read('digest.json')
                newdata = json.loads(json_data_read)

        try:
            Functions.Loads = newdata[1]
        except:
            pass


    def updateVoltageDrop(self):
        print("made it")
        #pdb.set_trace()
        for i in Functions.Voltage_Drop_Panels:
            self.MainUi.listBox_Voltage_Drop.addItem(i)
            #pdb.set_trace()
        #self.MainUi.listBox_Voltage_Drop.addItem(newEntry)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
