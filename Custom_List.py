import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Custom_List_GUI import *

import pdb




class CustomList(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.CustomUi = Ui_Custom_List_Widget()
        self.CustomUi.setupUi(self)


    def setUpMainUiFunction(self):
        pass

    def setUpProjectNumber(self,ProjectNumber):
        self.CustomUi.text_ProjectNumber_CHANGE.setText(ProjectNumber)

    def setUpProjectName(self,ProjectName):
        self.CustomUi.text_Project_Name_Change.setText(ProjectName)

    def setUpMainName(self,Name):
        self.CustomUi.text_Name_Change.setText(Name)

    def setUpMainNumber(self,Number):
        self.CustomUi.text_PhoneNumber_CHANGE.setText(Number)

    def setupDate(self,Date):
        self.CustomUi.text_Date_CHANGE.setText(Date)

    def setupNextDate(self,Date):
        self.CustomUi.text_NextDeliverible_CHANGE.setText(Date)

    def setupProjectFoler(self,ProjectFolder):
        self.CustomUi.text_ProjectFolder_CHANGE.setText(ProjectFolder)
        self.CustomUi.text_ProjectFolder_CHANGE.setOpenExternalLinks(True)
