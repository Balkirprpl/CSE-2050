# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta
import dateparser
import requests
import bs4
import urllib


class Ui_MainWindow(object):
   def setupUi(self, MainWindow):
      self.current_appointments = ["6:30 am-7:00 am", "7:00 am-7:15am", "7:20 am-7:30 am", "8:00 am-8:25 am"]
      self.booking_dict = {}
      MainWindow.setObjectName("MainWindow")
      MainWindow.resize(1500, 1000)
      self.centralwidget = QtWidgets.QWidget(MainWindow)
      self.centralwidget.setObjectName("centralwidget")


      ###################### Selected Time ######################
      self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
      self.groupBox_2.setGeometry(QtCore.QRect(50, 10, 741, 100))
      self.groupBox_2.setTitle("")
      self.groupBox_2.setObjectName("groupBox_2")
      self.label = QtWidgets.QLabel(self.groupBox_2)
      self.label.setGeometry(QtCore.QRect(20, 10, 700, 80))
      self.label.setObjectName("label")
      self.label.setFont(QtGui.QFont('Arial', 15))

      ###################### Calendar ######################
      def dateChanged():
         self.label.setText(str(self.calendarWidget.selectedDate().toPyDate().strftime("%A, %B %d, %Y")))
         update_list()

      self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
      self.groupBox.setGeometry(QtCore.QRect(40, 120, 780, 390))
      self.groupBox.setObjectName("groupBox")
      self.calendarWidget = QtWidgets.QCalendarWidget(self.groupBox)
      self.calendarWidget.setGeometry(QtCore.QRect(10, 30, 750, 330))
      self.calendarWidget.setObjectName("calendarWidget")
      self.calendarWidget.selectionChanged.connect(dateChanged)
      self.current_date = str(self.calendarWidget.selectedDate().toPyDate().strftime("%Y:%m:%d"))


      ###################### Booking List ######################
      def update_list():
         self.listWidget.clear()
         try:
            self.listWidget.addItems(self.booking_dict[self.calendarWidget.selectedDate().toPyDate().strftime("%m:%d:%Y")])
         except:
            self.listWidget.addItem("No appointments for the selected date")
            return


      self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
      self.groupBox_3.setGeometry(QtCore.QRect(900, 100, 450, 900))
      self.groupBox_3.setObjectName("groupBox_3")
      self.listWidget = QtWidgets.QListWidget(self.groupBox_3)
      self.listWidget.setGeometry(10, 30, 430, 850)
      
      

      ###################### Single Booking ######################
      def single_booking():
         day = str(self.calendarWidget.selectedDate().toPyDate().strftime("%m:%d:%Y"))
         compare = str(self.calendarWidget.selectedDate().toPyDate().strftime("%Y:%m:%d"))
         single_start = dateparser.parse("%s:%s %s" % (self.comboBox.currentText(), self.comboBox_2.currentText(), self.comboBox_3.currentText()))
         length = self.comboBox_4.currentText()
         single_end = single_start + timedelta(0,int(length.replace(" minutes", '')) * 60, 0)
         single_end = prsdtime(single_end)
         single_time = '%s - %s %s' % (single_start.strftime("%H:%M %p"), str(single_end), length)
         if compare < self.current_date:
            showDialog(single_start.strftime("%H:%M %p"), str(single_end), "sorry, %s %s is not available. The date cannot be in the past.", False)
            return
         if day not in self.booking_dict:
            self.booking_dict[day] = []

         # add limitation of time scheduling seen in homework 2
         if self.spring_holidays.is_holiday(self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d")) or self.fall_holidays.is_holiday(self.calendarWidget.selectedDate().toPyDate().strftime("%m-%d")):
            showDialog(single_start.strftime("%H:%M %p"), str(single_end), "sorry, %s %s is not available. It is a holiday.", False)
            return

         # adding check overlap
         
         # setting both ranges of time
         ss = int(single_start.strftime('%H%M'))
         se = single_end.replace(':', '').replace(' AM','')
         se = int(se.replace(' PM', ''))
         range1 = range(ss, se)
         for i in self.booking_dict[day]:
            i = i[0:len(i) - 11]
            i = i.replace('AM', '').replace('PM', '').replace(' ','')
            i = i.split('-')
            s = int(i[0].replace(':',''))
            e = int(i[1].replace(':','')) - 1
            range2 = range (int(s), int(e))
            # checking if the ranges overlap
            if s in range1 or e in range1 or ss in range2 or se in range2:
               showDialog(single_start.strftime("%H:%M %p"), str(single_end), "sorry, %s %s is not available. It overlaps.", False)
               return

         self.booking_dict[day].append(single_time)
         showDialog(single_start.strftime("%H:%M %p"), str(single_end), "An appointment for %s - %s was booked successfully", True)
         update_list()
      
      def prsdtime(time):
         st = str(time)
         st = st.split()
         date = st[0].split('-')
         time = st[1].split(':')
         return datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).strftime("%H:%M %p")


      self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
      self.groupBox_4.setGeometry(QtCore.QRect(40, 560, 550, 80))
      self.groupBox_4.setObjectName("groupBox_4")
      self.comboBox = QtWidgets.QComboBox(self.groupBox_4)
      self.comboBox.setGeometry(QtCore.QRect(20, 40, 70, 22))
      self.comboBox.setObjectName("comboBox")
      self.comboBox.addItems(['01', '02', '03', '04', '05', '06', '07', '08', '09'])
      self.comboBox.addItems([str(x) for x in range(10, 13)])
      self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_4)
      self.comboBox_2.setGeometry(QtCore.QRect(100, 40, 70, 22))
      self.comboBox_2.setObjectName("comboBox_2")
      self.comboBox_2.addItems(['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'])
      self.comboBox_2.addItems([str(x) for x in range(10, 60)])
      self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_4)
      self.comboBox_3.setGeometry(QtCore.QRect(180, 40, 70, 22))
      self.comboBox_3.setObjectName("comboBox_3")
      self.comboBox_3.addItems(['AM', 'PM'])
      self.comboBox_4 = QtWidgets.QComboBox(self.groupBox_4)
      self.comboBox_4.setGeometry(QtCore.QRect(260, 40, 150, 22))
      self.comboBox_4.setObjectName("comboBox_4")
      self.comboBox_4.addItems(['10 minutes', '15 minutes', '20 minutes', '25 minutes', '30 minutes', ])
      self.pushButton = QtWidgets.QPushButton(self.groupBox_4)
      self.pushButton.setGeometry(QtCore.QRect(450, 40, 80, 35))
      self.pushButton.setObjectName("pushButton")
      self.pushButton.clicked.connect(single_booking)
      
      day = str(self.calendarWidget.selectedDate().toPyDate().strftime("%m:%d:%Y"))
      bookings = self.current_appointments
      if day not in self.booking_dict:
         self.booking_dict[day] = []
      for times in bookings:
         times = times.split("-")
         start_int = dateparser.parse(times[0])
         start_str = dateparser.parse(times[0]).strftime('%H:%M %p')
         end_int = dateparser.parse(times[1])
         end_str = dateparser.parse(times[1]).strftime('%H:%M %p')
         length = str(end_int - start_int)
         single_time = "%s - %s %s %s" % (start_str, end_str, length.split(':')[1], 'minutes')
         # add limitation of time scheduling seen in homework 2

         self.booking_dict[day].append(single_time)
         #6:30 am - 7:00 am, 8:00 am - 8:15 am
      update_list()


      ###################### Multiple Bookings ######################
      def multiple_bookings():
         day = str(self.calendarWidget.selectedDate().toPyDate().strftime("%m:%d:%Y"))
         bookings = self.plainTextEdit.text().split(",")
         if day not in self.booking_dict:
            self.booking_dict[day] = []
         for times in bookings:
            times = times.split("-")
            start_int = dateparser.parse(times[0])
            start_str = dateparser.parse(times[0]).strftime('%H:%M %p')
            end_int = dateparser.parse(times[1])
            end_str = dateparser.parse(times[1]).strftime('%H:%M %p')
            length = str(end_int - start_int)
            single_time = "%s - %s %s %s" % (start_str, end_str, length.split(':')[1], 'minutes')
            # add limitation of time scheduling seen in homework 2

            self.booking_dict[day].append(single_time)
         update_list()


      self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
      self.groupBox_5.setGeometry(QtCore.QRect(40, 770, 550, 80))
      self.groupBox_5.setObjectName("groupBox_5")
      self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_5)
      self.pushButton_2.setGeometry(QtCore.QRect(450, 40, 80, 35))
      self.pushButton_2.setObjectName("pushButton_2")
      self.pushButton_2.clicked.connect(multiple_bookings)
      self.label_2 = QtWidgets.QLabel(self.groupBox_5)
      self.label_2.setGeometry(QtCore.QRect(20, 40, 47, 20))
      self.label_2.setObjectName("label_2")
      self.plainTextEdit = QtWidgets.QLineEdit(self.groupBox_5)
      self.plainTextEdit.setGeometry(QtCore.QRect(100, 30, 251, 40))
      self.plainTextEdit.setObjectName("plainTextEdit")
      MainWindow.setCentralWidget(self.centralwidget)
      self.menubar = QtWidgets.QMenuBar(MainWindow)
      self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 22))
      self.menubar.setObjectName("menubar")
      self.menuType_what = QtWidgets.QMenu(self.menubar)
      self.menuType_what.setObjectName("menuType_what")
      MainWindow.setMenuBar(self.menubar)
      self.statusbar = QtWidgets.QStatusBar(MainWindow)
      self.statusbar.setObjectName("statusbar")
      MainWindow.setStatusBar(self.statusbar)

      self.retranslateUi(MainWindow)
      QtCore.QMetaObject.connectSlotsByName(MainWindow)


      def showDialog(start, end, message, worked):
         msgBox = QtWidgets.QMessageBox()
         if not worked:
            msgBox.setIcon(QMessageBox.Warning)
         else:
            msgBox.setIcon(QMessageBox.Information)
         msgBox.setText(message % (start, end))
         msgBox.setWindowTitle("")
         msgBox.exec()

      class HolidayChecker:

         def pring(self, x):
            for i in x:
               print(i)

         def get_holiday_desc(self, i):
            if len(i) > 0:
               return i[1].lower()
            else:
               return 'nope'

         def scrape_data(self, url):
            response = urllib.request.urlopen(url)
            doc = bs4.BeautifulSoup(response, features="lxml")
            count = 0

            tables = doc.find_all('tr')
            return self.get_data_table(tables)

         def get_holidays(self):
            data_table = []
            holiday_table = []
            for i in self.data:
               if 'no classes' in self.get_holiday_desc(i):
                  if i not in data_table:
                     date = i[0]
                     if '-' in date:
                        month = date.split()[0]
                        day = date.split()[1]
                        for k in range(int(day.split('-')[0]), int(day.split('-')[1]) + 1):
                           holiday_table.append(dateparser.parse(month + str(k)))
                     else:
                        holiday_table.append(dateparser.parse(date))

                     data_table.append(i)
            return holiday_table

         def get_data_table(self, tables):
            data_table = []
            
            for i in tables:
               i = i.find_all("td")
               i = [ele.text.strip() for ele in i]
               data_table.append(i)
            return data_table

         def is_holiday(self, date):
            date = dateparser.parse(date)
            for i in self.holidays:
               if date.day == i.day:
                  if date.month == i.month:
                     return True
            return False

         def __init__(self, url):
            self.url = url
            self.data = self.scrape_data(url)
            self.holidays = self.get_holidays()
               
      self.spring_holidays = HolidayChecker('https://www.fit.edu/registrar/academic-calendar/spring-2023/') 
      self.fall_holidays = HolidayChecker('https://www.fit.edu/registrar/academic-calendar/fall-2022/') 


   def retranslateUi(self, MainWindow):
      _translate = QtCore.QCoreApplication.translate
      MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
      self.groupBox.setTitle(_translate("MainWindow", "Calendar Preview"))
      self.label.setText(_translate("MainWindow", str(self.calendarWidget.selectedDate().toPyDate().strftime("%A, %B %d, %Y"))))
      self.label.setStyleSheet('background-color: lightblue')
      self.groupBox_3.setTitle(_translate("MainWindow", "Current Bookings"))
      self.groupBox_4.setTitle(_translate("MainWindow", "Book Single Appointment"))
      self.pushButton.setText(_translate("MainWindow", "Book"))
      self.groupBox_5.setTitle(_translate("MainWindow", "Book Multiple Appointments"))
      self.pushButton_2.setText(_translate("MainWindow", "Book"))
      self.label_2.setText(_translate("MainWindow", "Times:"))
      self.plainTextEdit.setText(_translate("MainWindow", "Input times"))


if __name__ == "__main__":
   import sys

   app = QtWidgets.QApplication(sys.argv)
   MainWindow = QtWidgets.QMainWindow()
   ui = Ui_MainWindow()
   ui.setupUi(MainWindow)
   MainWindow.show()
   sys.exit(app.exec_())