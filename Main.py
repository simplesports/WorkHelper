import sys
import os
import sqlite3
import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Main_GUI import *
from Custom_List import *
from Add_Projects import *

import pdb



currentProjects = {}
overDueProjects = {}
Finished_Projects = {}
class MainWindow(QMainWindow):


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self,parent)
        self.MainUi = Ui_MainWindow()
        self.MainUi.setupUi(self)
        self.setUpMainUiFunction()

        self.LoadCurrentProjects()
        self.loadOverDueProjects()
        self.loadFinishedProjects()

        self.loadCurrentCustomWidgets()
        self.loadOverDueCustomWidget()
        self.load_Finished_CustomWidget()

        self.MainUi.mouseReleaseEvent=self.mousePressEvent



    def setUpMainUiFunction(self):
        self.MainUi.groupBox_More_Details.hide()

        self.MainUi.Button_Mark_As_Finish.setEnabled(False)
        self.MainUi.Button_See_More_Details.setEnabled(False)

        self.MainUi.Button_Mark_As_Finish_Past_Due.setEnabled(False)
        self.MainUi.Button_See_More_Details_Past_Due.setEnabled(False)

        self.MainUi.Button_Finished_Projects_Mark_as_Current.setEnabled(False)
        self.MainUi.Button_Finished_Projects_See_More_Details.setEnabled(False)

        self.MainUi.list_Current_Projects.itemClicked.connect(self.Custom_Widget_click)
        self.MainUi.list_Past_Due_Projects.itemClicked.connect(self.Custom_Widget_click)
        self.MainUi.list_Finished_Projects.itemClicked.connect(self.Custom_Widget_click)
        self.MainUi.list_Current_Projects.doubleClicked.connect(self.editProject)
        self.MainUi.list_Past_Due_Projects.doubleClicked.connect(self.editProject)
        self.MainUi.list_Finished_Projects.doubleClicked.connect(self.editProject)

        self.MainUi.Button_See_More_Details.clicked.connect(self.ShowMoreDetails)
        self.MainUi.Button_See_More_Details_Past_Due.clicked.connect(self.ShowMoreDetails)
        self.MainUi.Button_Finished_Projects_See_More_Details.clicked.connect(self.ShowMoreDetails)
        self.MainUi.Button_Hide_Details.clicked.connect(self.HideDetails)
        self.MainUi.Button_Add_Project.clicked.connect(self.AddProjectsShow)
        self.MainUi.Button_Mark_As_Finish.clicked.connect(self.changeStatus)
        self.MainUi.Button_Finished_Projects_Mark_as_Current.clicked.connect(self.changeStatus)
        self.MainUi.Button_Mark_As_Finish_Past_Due.clicked.connect(self.changeStatus)

        self.MainUi.tabWidge.currentChanged.connect(self.changeTab)


    def LoadCurrentProjects(self):
        global currentProjects
        db_filename = '.\DB\ProgramManagerDB.sqlite'
        with sqlite3.connect(db_filename) as conn:
            cursorProject = conn.cursor()
#****************************************************************************************************************************************************************************************************************
            cursorProject.execute(""" SELECT Project, Due_Date FROM DueDates ORDER BY datetime(Due_Date) ASC""")

            curentAllDates = cursorProject.fetchall()
            now = datetime.datetime.now()
            dcheck = []
            for i in curentAllDates:
                #pdb.set_trace()
                dcheck.append(datetime.datetime.strptime(i[1], '%Y-%m-%d'))

            currentOrderkey = []
            for i in range(0, len(dcheck)):
                if dcheck[i] < now:
                    pass
                else:
                    currentOrderkey.append(curentAllDates[i][0])
            global currentfinalKeyOrder

            currentfinalKeyOrder = []
            for i in range(0, len(currentOrderkey)):
                if currentOrderkey[i] in currentfinalKeyOrder:
                    pass
                else:
                    currentfinalKeyOrder.append(currentOrderkey[i])
            #pdb.set_trace()
#**************************************************************************************************************************************************************************************************************
            for key in currentfinalKeyOrder:
                cursorProject.execute(""" select Project_Name, Project_Number, Project_Folder,Add_Comments, Icon from Projects where key = ? and status = 0 """,(key,))
                for row in cursorProject.fetchall():
                    Project = {'Project_Name':[],'Project_Number':[],'Project_Folder':[],'Comments':[],'icon':[]}
                    dueDates = {'Description':[],'Dates':[]}
                    allContacts = {'contactName':[],'contactNumber':[],'title':[], 'company':[],'email':[]}
                    projectName,ProjectNumber,ProjectFolder,Comments,Icon = row
                    Project['Project_Name'].append(projectName)
                    Project['Project_Number'].append(ProjectNumber)
                    Project['Project_Folder'].append(ProjectFolder)
                    Project['Comments'].append(Comments)
                    Project['icon'].append(Icon)

                    cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber from Contacts where Main_Contact = 1 and Project = ?""", (key,))
                    MaincontactName,MaincontactNumber = cursorProject.fetchone()

                    cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber,Title,company,email from Contacts where Project = ?""", (key,))
                    for contacts in cursorProject.fetchall():
                        contactName,contactNumber,title,company,email = contacts
                        allContacts['contactName'].append(contactName)
                        allContacts['contactNumber'].append(contactNumber)
                        allContacts['title'].append(title)
                        allContacts['company'].append(company)
                        allContacts['email'].append(email)

                    cursorProject.execute(""" select Description, Due_Date from DueDates where Project = ?""", (key,))
                    for dateRow in cursorProject.fetchall():
                        Desc,DueDate = dateRow
                        dueDates['Description'].append(Desc)
                        dAll = datetime.datetime.strptime(DueDate, '%Y-%m-%d')
                        dueDates['Dates'].append(dAll)

                    Project.update({'MaincontactName':MaincontactName,'MaincontactNumber':MaincontactNumber,'Contacts':allContacts,'Due_Dates':dueDates})

                    currentProjects.update({ProjectNumber:Project})


            #INSERT INTO "main"."Projects" ("Project_Name","Project_Number","Project_Folder","Add_Comments") VALUES (?1,?2,?3,?4)

    def loadOverDueProjects(self):
        global overDueProjects
        global currentfinalKeyOrder
        global overDueKeyList
        db_filename = '.\DB\ProgramManagerDB.sqlite'
        with sqlite3.connect(db_filename) as conn:
            cursorProject = conn.cursor()
#****************************************************************************************************************************************************************************************************************
            cursorProject.execute(""" select Project, Due_Date from DueDates ORDER BY date(Due_Date) """)

            overDueAllDates = cursorProject.fetchall()
            now = datetime.datetime.now()
            dcheck = []
            for i in overDueAllDates:
                dcheck.append(datetime.datetime.strptime(i[1], '%Y-%m-%d'))

            overdueDates = []
            for dc in dcheck:
                if dc < now:
                    overdueDates.append(dc)
            #soonestDeliverable.append(dt for dt in dcheck if dt < now)
            overDueList=[]
            for j in overdueDates:
                if j in dcheck:
                    overDueList.append(overDueAllDates[dcheck.index(j)][0])

            overDueKeyList = []
            for i in overDueList:
                if i in currentfinalKeyOrder or i in overDueKeyList:
                    pass
                else:
                    overDueKeyList.append(i)

            #pdb.set_trace()
            for key in overDueKeyList:
                cursorProject.execute(""" select Project_Name, Project_Number, Project_Folder,Add_Comments, Icon from Projects where key = ? and status = 0 """,(key,))
                for row in cursorProject.fetchall():
                    Project = {'Project_Name':[],'Project_Number':[],'Project_Folder':[],'Comments':[],'icon':[]}
                    dueDates = {'Description':[],'Dates':[]}
                    allContacts = {'contactName':[],'contactNumber':[],'title':[],'company':[],'email':[]}
                    projectName,ProjectNumber,ProjectFolder,Comments,Icon = row
                    Project['Project_Name'].append(projectName)
                    Project['Project_Number'].append(ProjectNumber)
                    Project['Project_Folder'].append(ProjectFolder)
                    Project['Comments'].append(Comments)
                    Project['icon'].append(Icon)

                    cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber from Contacts where Main_Contact = 1 and Project = ?""", (key,))
                    MaincontactName,MaincontactNumber = cursorProject.fetchone()

                    cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber,Title,company,email from Contacts where Project = ?""", (key,))
                    for contacts in cursorProject.fetchall():
                        contactName,contactNumber,title,company,email = contacts
                        allContacts['contactName'].append(contactName)
                        allContacts['contactNumber'].append(contactNumber)
                        allContacts['title'].append(title)
                        allContacts['company'].append(company)
                        allContacts['email'].append(email)

                    cursorProject.execute(""" select Description, Due_Date from DueDates where Project = ?""", (key,))
                    for dateRow in cursorProject.fetchall():
                        Desc,DueDate = dateRow
                        dueDates['Description'].append(Desc)
                        dAll = datetime.datetime.strptime(DueDate, '%Y-%m-%d')
                        dueDates['Dates'].append(dAll)

                    Project.update({'MaincontactName':MaincontactName,'MaincontactNumber':MaincontactNumber,'Contacts':allContacts,'Due_Dates':dueDates})

                    overDueProjects.update({ProjectNumber:Project})
#**************************************************************************************************************************************************************************************************************

    def loadFinishedProjects(self):
        global overDueProjects
        global currentfinalKeyOrder
        global finishedKeyList
        finishedKeyList = []
        db_filename = '.\DB\ProgramManagerDB.sqlite'
        with sqlite3.connect(db_filename) as conn:
            cursorProject = conn.cursor()
#****************************************************************************************************************************************************************************************************************

            cursorProject.execute(""" select key, Project_Name, Project_Number, Project_Folder,Add_Comments, Icon from Projects where status = 1 ORDER By Project_Number """)

            for row in cursorProject.fetchall():
                Project = {'Project_Name':[],'Project_Number':[],'Project_Folder':[],'Comments':[],'icon':[]}
                dueDates = {'Description':[],'Dates':[]}
                allContacts = {'contactName':[],'contactNumber':[],'title':[],'company':[],'email':[]}
                key,projectName,ProjectNumber,ProjectFolder,Comments,Icon = row
                Project['Project_Name'].append(projectName)
                Project['Project_Number'].append(ProjectNumber)
                Project['Project_Folder'].append(ProjectFolder)
                Project['Comments'].append(Comments)
                Project['icon'].append(Icon)


                cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber from Contacts where Main_Contact = 1 and Project = ?""", (key,))
                try:
                    MaincontactName,MaincontactNumber = cursorProject.fetchone()
                except:
                    MaincontactName = 'None Listed'
                    MaincontactNumber = 'None Listed'

                cursorProject.execute(""" select Contact_Name, Contact_PhoneNumber,Title,company,email from Contacts where Project = ?""", (key,))
                for contacts in cursorProject.fetchall():
                    contactName,contactNumber,title,company,email = contacts
                    allContacts['contactName'].append(contactName)
                    allContacts['contactNumber'].append(contactNumber)
                    allContacts['title'].append(title)
                    allContacts['company'].append(company)
                    allContacts['email'].append(email)

                cursorProject.execute(""" select Description, Due_Date from DueDates where Project = ?""", (key,))
                for dateRow in cursorProject.fetchall():
                    Desc,DueDate = dateRow
                    dueDates['Description'].append(Desc)
                    dAll = datetime.datetime.strptime(DueDate, '%Y-%m-%d')
                    dueDates['Dates'].append(dAll)

                Project.update({'MaincontactName':MaincontactName,'MaincontactNumber':MaincontactNumber,'Contacts':allContacts,'Due_Dates':dueDates})

                Finished_Projects.update({ProjectNumber:Project})
                finishedKeyList.append(key)


    def loadCurrentCustomWidgets(self):
        global current_project_list
        current_project_list =[]
        for i in currentProjects:

            projectName = currentProjects[i]['Project_Name'][0]
            ProjectNumber = currentProjects[i]['Project_Number'][0]
            ProjectFolder = currentProjects[i]['Project_Folder'][0]
            Comments = currentProjects[i]['Comments'][0]
            icon = currentProjects[i]['icon'][0]
            contactName = currentProjects[i]['MaincontactName']
            contactNumber = currentProjects[i]['MaincontactNumber']

            now = datetime.datetime.now()
            NextDeliverableCheck = min(dt for dt in currentProjects[i]['Due_Dates']['Dates'] if dt > now)
            NextDeliverableSTR = NextDeliverableCheck.strftime("%m/%d/%Y")
            oldest = max(currentProjects[i]['Due_Dates']['Dates'])
            FinalDueDate = oldest.strftime("%m/%d/%Y")
            #pdb.set_trace()
            current_project_list.append(ProjectNumber)

            CustomWidget = CustomList()

            CustomWidget.setUpProjectNumber(str(ProjectNumber))
            CustomWidget.setUpProjectName(projectName)
            CustomWidget.setupProjectFoler('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            #remember to replace all spaces with %20 and all \ with / for the project folder and then it will work

            CustomWidget.setUpMainName(contactName)
            CustomWidget.setUpMainNumber(contactNumber)

            CustomWidget.setupNextDate(NextDeliverableSTR)
            CustomWidget.setupDate(FinalDueDate)

            myQListWidgetItem = QListWidgetItem(self.MainUi.list_Current_Projects)
            #pdb.set_trace()
            myQListWidgetItem.setSizeHint(CustomWidget.sizeHint())
            self.MainUi.list_Current_Projects.addItem(myQListWidgetItem)
            self.MainUi.list_Current_Projects.setItemWidget(myQListWidgetItem, CustomWidget)
            self._width = self.MainUi.list_Current_Projects.width()+5
            #self.adjustSize()

    def loadOverDueCustomWidget(self):
        global OverDue_project_list
        OverDue_project_list =[]
        for i in overDueProjects:

            projectName = overDueProjects[i]['Project_Name'][0]
            ProjectNumber = overDueProjects[i]['Project_Number'][0]
            ProjectFolder = overDueProjects[i]['Project_Folder'][0]
            Comments = overDueProjects[i]['Comments'][0]
            icon = overDueProjects[i]['icon'][0]
            contactName = overDueProjects[i]['MaincontactName']
            contactNumber = overDueProjects[i]['MaincontactNumber']

            now = datetime.datetime.now()
            NextDeliverableCheck = min(dt for dt in overDueProjects[i]['Due_Dates']['Dates'] if dt < now)
            NextDeliverableSTR = NextDeliverableCheck.strftime("%m/%d/%Y")
            oldest = max(overDueProjects[i]['Due_Dates']['Dates'])
            FinalDueDate = oldest.strftime("%m/%d/%Y")
            #pdb.set_trace()
            OverDue_project_list.append(ProjectNumber)

            CustomWidget = CustomList()

            CustomWidget.setUpProjectNumber(str(ProjectNumber))
            CustomWidget.setUpProjectName(projectName)
            CustomWidget.setupProjectFoler('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            #remember to replace all spaces with %20 and all \ with / for the project folder and then it will work

            CustomWidget.setUpMainName(contactName)
            CustomWidget.setUpMainNumber(contactNumber)

            CustomWidget.setupNextDate(NextDeliverableSTR)
            CustomWidget.setupDate(FinalDueDate)

            myQListWidgetItem = QListWidgetItem(self.MainUi.list_Past_Due_Projects)
            #pdb.set_trace()
            myQListWidgetItem.setSizeHint(CustomWidget.sizeHint())
            self.MainUi.list_Past_Due_Projects.addItem(myQListWidgetItem)
            self.MainUi.list_Past_Due_Projects.setItemWidget(myQListWidgetItem, CustomWidget)
            self._width = self.MainUi.list_Current_Projects.width()+5
            #self.adjustSize()

    def load_Finished_CustomWidget(self):
        global Finished_project_list
        Finished_project_list =[]
        for i in Finished_Projects:

            projectName = Finished_Projects[i]['Project_Name'][0]
            ProjectNumber = Finished_Projects[i]['Project_Number'][0]
            ProjectFolder = Finished_Projects[i]['Project_Folder'][0]
            Comments = Finished_Projects[i]['Comments'][0]
            icon = Finished_Projects[i]['icon'][0]
            contactName = Finished_Projects[i]['MaincontactName']
            contactNumber = Finished_Projects[i]['MaincontactNumber']

            now = datetime.datetime.now()
            try:
                NextDeliverableCheck = min(dt for dt in Finished_Projects[i]['Due_Dates']['Dates'] if dt < now)
                NextDeliverableSTR = NextDeliverableCheck.strftime("%m/%d/%Y")
            except:
                NextDeliverableSTR = 'error'

            oldest = max(Finished_Projects[i]['Due_Dates']['Dates'])
            FinalDueDate = oldest.strftime("%m/%d/%Y")
            #pdb.set_trace()
            Finished_project_list.append(ProjectNumber)

            CustomWidget = CustomList()

            CustomWidget.setUpProjectNumber(str(ProjectNumber))
            CustomWidget.setUpProjectName(projectName)
            CustomWidget.setupProjectFoler('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            #remember to replace all spaces with %20 and all \ with / for the project folder and then it will work

            CustomWidget.setUpMainName(contactName)
            CustomWidget.setUpMainNumber(contactNumber)

            CustomWidget.setupNextDate(NextDeliverableSTR)
            CustomWidget.setupDate(FinalDueDate)

            myQListWidgetItem = QListWidgetItem(self.MainUi.list_Finished_Projects)
            #pdb.set_trace()
            myQListWidgetItem.setSizeHint(CustomWidget.sizeHint())
            self.MainUi.list_Finished_Projects.addItem(myQListWidgetItem)
            self.MainUi.list_Finished_Projects.setItemWidget(myQListWidgetItem, CustomWidget)
            self._width = self.MainUi.list_Current_Projects.width()+5
            #self.adjustSize()


    def Custom_Widget_click(self):

        try:
            while self.MainUi.tableWidget_Contacts.rowCount() > 0:
                self.MainUi.tableWidget_Contacts.removeRow(0);
        except:
            pass

        try:
            while self.MainUi.tableWidget_DueDates.rowCount() > 0:
                self.MainUi.tableWidget_DueDates.removeRow(0);
        except:
            pass

        if self.MainUi.tabWidge.currentIndex() == 0:
            row = self.MainUi.list_Current_Projects.row(self.MainUi.list_Current_Projects.currentItem())
            project = current_project_list[row]

            projectName = currentProjects[project]['Project_Name'][0]
            ProjectNumber = currentProjects[project]['Project_Number'][0]
            ProjectFolder = currentProjects[project]['Project_Folder'][0]
            Comments = currentProjects[project]['Comments'][0]
            icon = currentProjects[project]['icon'][0]
            contactName = currentProjects[project]['MaincontactName']
            contactNumber = currentProjects[project]['MaincontactNumber']

            self.MainUi.text_ProjectName_CHANGE.setText(projectName)
            self.MainUi.text_ProjectFolder_CHANGE.setText('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            self.MainUi.text_ProjectFolder_CHANGE.setOpenExternalLinks(True)
            self.MainUi.textEdit.setText(Comments)

            for i in range(0,len(currentProjects[project]['Contacts']['contactName'])):
                self.MainUi.tableWidget_Contacts.insertRow(i)
                self.MainUi.tableWidget_Contacts.setItem(i, 0, QTableWidgetItem(currentProjects[project]['Contacts']['contactName'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 1, QTableWidgetItem(currentProjects[project]['Contacts']['contactNumber'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 2, QTableWidgetItem(currentProjects[project]['Contacts']['title'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 3, QTableWidgetItem(currentProjects[project]['Contacts']['company'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 4, QTableWidgetItem(currentProjects[project]['Contacts']['email'][i]))

            for i in range(0,len(currentProjects[project]['Due_Dates']['Dates'])):
                self.MainUi.tableWidget_DueDates.insertRow(i)
                self.MainUi.tableWidget_DueDates.setItem(i, 0, QTableWidgetItem(currentProjects[project]['Due_Dates']['Description'][i]))
                dateStr = currentProjects[project]['Due_Dates']['Dates'][i].strftime("%m/%d/%Y")
                self.MainUi.tableWidget_DueDates.setItem(i, 1, QTableWidgetItem(dateStr))


            self.MainUi.tableWidget_Contacts.resizeColumnsToContents()
            self.MainUi.tableWidget_DueDates.resizeColumnsToContents()
            self.MainUi.Button_Mark_As_Finish.setEnabled(True)
            self.MainUi.Button_See_More_Details.setEnabled(True)

        elif self.MainUi.tabWidge.currentIndex() == 1:

            row = self.MainUi.list_Past_Due_Projects.row(self.MainUi.list_Past_Due_Projects.currentItem())
            project = OverDue_project_list[row]

            projectName = overDueProjects[project]['Project_Name'][0]
            ProjectNumber = overDueProjects[project]['Project_Number'][0]
            ProjectFolder = overDueProjects[project]['Project_Folder'][0]
            Comments = overDueProjects[project]['Comments'][0]
            icon = overDueProjects[project]['icon'][0]
            contactName = overDueProjects[project]['MaincontactName']
            contactNumber = overDueProjects[project]['MaincontactNumber']

            self.MainUi.text_ProjectName_CHANGE.setText(projectName)
            self.MainUi.text_ProjectFolder_CHANGE.setText('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            self.MainUi.text_ProjectFolder_CHANGE.setOpenExternalLinks(True)
            self.MainUi.textEdit.setText(Comments)

            for i in range(0,len(overDueProjects[project]['Contacts']['contactName'])):
                self.MainUi.tableWidget_Contacts.insertRow(i)
                self.MainUi.tableWidget_Contacts.setItem(i, 0, QTableWidgetItem(overDueProjects[project]['Contacts']['contactName'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 1, QTableWidgetItem(overDueProjects[project]['Contacts']['contactNumber'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 2, QTableWidgetItem(overDueProjects[project]['Contacts']['title'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 3, QTableWidgetItem(overDueProjects[project]['Contacts']['company'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 4, QTableWidgetItem(overDueProjects[project]['Contacts']['email'][i]))

            for i in range(0,len(overDueProjects[project]['Due_Dates']['Dates'])):
                self.MainUi.tableWidget_DueDates.insertRow(i)
                self.MainUi.tableWidget_DueDates.setItem(i, 0, QTableWidgetItem(overDueProjects[project]['Due_Dates']['Description'][i]))
                dateStr = overDueProjects[project]['Due_Dates']['Dates'][i].strftime("%m/%d/%Y")
                self.MainUi.tableWidget_DueDates.setItem(i, 1, QTableWidgetItem(dateStr))


            self.MainUi.tableWidget_Contacts.resizeColumnsToContents()
            self.MainUi.tableWidget_DueDates.resizeColumnsToContents()
            self.MainUi.Button_Mark_As_Finish_Past_Due.setEnabled(True)
            self.MainUi.Button_See_More_Details_Past_Due.setEnabled(True)

        elif self.MainUi.tabWidge.currentIndex() == 2:

            row = self.MainUi.list_Finished_Projects.row(self.MainUi.list_Finished_Projects.currentItem())
            project = Finished_project_list[row]

            projectName = Finished_Projects[project]['Project_Name'][0]
            ProjectNumber = Finished_Projects[project]['Project_Number'][0]
            ProjectFolder = Finished_Projects[project]['Project_Folder'][0]
            Comments = Finished_Projects[project]['Comments'][0]
            icon = Finished_Projects[project]['icon'][0]
            contactName = Finished_Projects[project]['MaincontactName']
            contactNumber = Finished_Projects[project]['MaincontactNumber']

            self.MainUi.text_ProjectName_CHANGE.setText(projectName)
            self.MainUi.text_ProjectFolder_CHANGE.setText('<a href=file:///'+ProjectFolder+'>Open Project Folder</a>')
            self.MainUi.text_ProjectFolder_CHANGE.setOpenExternalLinks(True)
            self.MainUi.textEdit.setText(Comments)

            for i in range(0,len(Finished_Projects[project]['Contacts']['contactName'])):
                self.MainUi.tableWidget_Contacts.insertRow(i)
                self.MainUi.tableWidget_Contacts.setItem(i, 0, QTableWidgetItem(Finished_Projects[project]['Contacts']['contactName'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 1, QTableWidgetItem(Finished_Projects[project]['Contacts']['contactNumber'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 2, QTableWidgetItem(Finished_Projects[project]['Contacts']['title'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 3, QTableWidgetItem(Finished_Projects[project]['Contacts']['company'][i]))
                self.MainUi.tableWidget_Contacts.setItem(i, 4, QTableWidgetItem(Finished_Projects[project]['Contacts']['email'][i]))

            for i in range(0,len(Finished_Projects[project]['Due_Dates']['Dates'])):
                self.MainUi.tableWidget_DueDates.insertRow(i)
                self.MainUi.tableWidget_DueDates.setItem(i, 0, QTableWidgetItem(Finished_Projects[project]['Due_Dates']['Description'][i]))
                dateStr = Finished_Projects[project]['Due_Dates']['Dates'][i].strftime("%m/%d/%Y")
                self.MainUi.tableWidget_DueDates.setItem(i, 1, QTableWidgetItem(dateStr))


            self.MainUi.tableWidget_Contacts.resizeColumnsToContents()
            self.MainUi.tableWidget_DueDates.resizeColumnsToContents()
            self.MainUi.Button_Finished_Projects_Mark_as_Current.setEnabled(True)
            self.MainUi.Button_Finished_Projects_See_More_Details.setEnabled(True)

    def ShowMoreDetails(self):
        self.MainUi.groupBox_More_Details.show()
        self.setFixedSize(width*2,height)

    def HideDetails(self):
        self.MainUi.groupBox_More_Details.hide()
        self.setFixedSize(width,height)

    def AddProjectsShow(self):
        global NewProjects
        NewProjects = AddProjects()
        NewProjects.signal.connect(self.refresh)
        #NewProjects.setProjectName('Test Name')
        #NewProjects.setProjectNumber('123456789')
        NewProjects.show()
        #return NewProjects

    def changeStatus(self):
        db_filename = '.\DB\ProgramManagerDB.sqlite'
        with sqlite3.connect(db_filename) as conn:
            cursorProject = conn.cursor()

            if self.MainUi.tabWidge.currentIndex() == 0:
                row = self.MainUi.list_Current_Projects.row(self.MainUi.list_Current_Projects.currentItem())
                key = currentfinalKeyOrder[row]
                cursorProject.execute(""" UPDATE Projects SET status=1 WHERE key=? """, (key,))

            elif self.MainUi.tabWidge.currentIndex() == 1:
                row = self.MainUi.list_Past_Due_Projects.row(self.MainUi.list_Past_Due_Projects.currentItem())
                key = overDueKeyList[row]
                cursorProject.execute(""" UPDATE Projects SET status=1 WHERE key=? """, (key,))

            elif self.MainUi.tabWidge.currentIndex() == 2:
                row = self.MainUi.list_Finished_Projects.row(self.MainUi.list_Finished_Projects.currentItem())
                key = finishedKeyList[row]
                cursorProject.execute(""" UPDATE Projects SET status=0 WHERE key=? """, (key,))

        self.refresh()


    def refresh(self):
        global currentProjects
        global overDueProjects
        global Finished_Projects

        currentProjects = {}
        overDueProjects = {}
        Finished_Projects = {}

        self.MainUi.list_Current_Projects.clear()
        self.MainUi.list_Past_Due_Projects.clear()
        self.MainUi.list_Finished_Projects.clear()

        self.LoadCurrentProjects()
        self.loadOverDueProjects()
        self.loadFinishedProjects()

        self.loadCurrentCustomWidgets()
        self.loadOverDueCustomWidget()
        self.load_Finished_CustomWidget()


    def changeTab(self):
        self.MainUi.list_Current_Projects.clearSelection()
        self.MainUi.list_Past_Due_Projects.clearSelection()
        self.MainUi.list_Finished_Projects.clearSelection()
        self.MainUi.groupBox_More_Details.hide()
        self.MainUi.Button_Mark_As_Finish.setEnabled(False)
        self.MainUi.Button_See_More_Details.setEnabled(False)
        self.MainUi.Button_Mark_As_Finish_Past_Due.setEnabled(False)
        self.MainUi.Button_See_More_Details_Past_Due.setEnabled(False)
        self.MainUi.Button_Finished_Projects_Mark_as_Current.setEnabled(False)
        self.MainUi.Button_Finished_Projects_See_More_Details.setEnabled(False)
        self.setFixedSize(width,height)

    def editProject(self):
        print('Edit project function')
        global NewProjects
        NewProjects = AddProjects()
        NewProjects.signal.connect(self.refresh)
        NewProjects.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.MainUi.list_Current_Projects.clearSelection()
            self.MainUi.list_Past_Due_Projects.clearSelection()
            self.MainUi.list_Finished_Projects.clearSelection()
            self.MainUi.groupBox_More_Details.hide()
            self.MainUi.Button_Mark_As_Finish.setEnabled(False)
            self.MainUi.Button_See_More_Details.setEnabled(False)
            self.MainUi.Button_Mark_As_Finish_Past_Due.setEnabled(False)
            self.MainUi.Button_See_More_Details_Past_Due.setEnabled(False)
            self.MainUi.Button_Finished_Projects_Mark_as_Current.setEnabled(False)
            self.MainUi.Button_Finished_Projects_See_More_Details.setEnabled(False)
            self.setFixedSize(width,height)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width()/5, screen_resolution.height()/2
    MainWindow = MainWindow()
    MainWindow.resize(width,height)
    MainWindow.show()
    sys.exit(app.exec_())
