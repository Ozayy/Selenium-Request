import requests
from bs4 import BeautifulSoup
import sqlite3
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette,QColor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from kayit_ara import Ui_MainWindow
from PyQt5.QtCore import Qt


class veri_cekme(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect = sqlite3.connect('C:\python_veri_cekme_veritabani\python_job_veritabani.db')
        self.im = self.connect.cursor()
        veritabani = """CREATE TABLE IF NOT EXISTS PythonJob(id INTEGER PRIMARY KEY AUTOINCREMENT,Uzmanlık TEXT,Sirket TEXT,Ulke TEXT,Tarih TEXT)"""
        # im.execute("""DROP TABLE PythonJob""")
        self.im.execute(veritabani)

        #self.ui.tableWidget.itemSelectionChanged.connect(self.doldur)
        self.ui.tableWidget.horizontalHeader().setSectionsClickable(False)


        self.ui.pushButton.clicked.connect(self.table_calistir)
        self.ui.pushButton_2.clicked.connect(self.table_add)
        self.ui.lineEdit.textChanged.connect(self.ara)
        self.ui.lineEdit_4.textChanged.connect(self.ara1)
        self.ui.lineEdit_3.textChanged.connect(self.ara2)
        self.ui.lineEdit_2.textChanged.connect(self.ara3)
        self.calistirilacak_kod()

    def table_add(self):
        '''
        row = self.ui.tableWidget.currentRow()  # Index of Row
        firstColumnInRow = self.ui.tableWidget.item(row, 0)  # returns QTableWidgetItem
        text = firstColumnInRow.text()  # content of this
        print(text)
        return str(text)  # if this is a index, you propably dont want it as text
        '''










    def ara3(self,tarih):
        try:
            col=3
            rows=self.ui.tableWidget.rowCount()
            for row in range(rows):
                item=self.ui.tableWidget.item(row,col)
                if item is not None:
                    if tarih.lower() in item.text().lower():
                        self.ui.tableWidget.showRow(row)
                    else:
                        self.ui.tableWidget.hideRow(row)
        except Exception as Hata:
            print("hata")

    def ara2(self,ulke):
        try:
            col=2
            rows=self.ui.tableWidget.rowCount()
            for row in range(rows):
                item=self.ui.tableWidget.item(row,col)
                if item is not None:
                    if ulke.lower() in item.text().lower():
                        self.ui.tableWidget.showRow(row)
                    else:
                        self.ui.tableWidget.hideRow(row)
        except Exception as Hata:
            print("hata")


    def ara1(self,sirket):
        try:
            col=1
            rows=self.ui.tableWidget.rowCount()
            for row in range(rows):
                item=self.ui.tableWidget.item(row,col)
                if item is not None:
                    if sirket.lower() in item.text().lower():
                        self.ui.tableWidget.showRow(row)
                    else:
                        self.ui.tableWidget.hideRow(row)
        except Exception as Hata:
            print("hata")

    def ara(self,uzmanlik):

        try:
            col=0
            rows=self.ui.tableWidget.rowCount()
            for row in range(rows):
                item=self.ui.tableWidget.item(row,col)
                if item is not None:
                    if uzmanlik.lower() in item.text().lower():
                        self.ui.tableWidget.showRow(row)
                    else:
                        self.ui.tableWidget.hideRow(row)
        except Exception as Hata:
            print("hata")
    def calistirilacak_kod(self):
        url = "https://www.python.org/jobs"


        #veriyi_getir = self.im.execute("SELECT * FROM PythonJob WHERE Uzmanlık='" + + "' ")
        #karsilastir = veriyi_getir.fetchall()

        deneme=self.im.execute("""SELECT Uzmanlık,Count(Uzmanlık)
        From PythonJob
        Group By Uzmanlık
        Having Count (Uzmanlık) > 1""")
        deneme1=deneme.fetchall()
        print(deneme1)

        if deneme1:
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Kayıtlar Çekildi")
            messagebox.setText(
                "Veriler başarıyla çekildi")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()
        else:




            r = requests.get(url)
            soup = BeautifulSoup(r.content,"lxml")
            pages = len(soup.find_all("ul",attrs={"class":"pagination"})[0].find_all("li")) - 2
            totalJobs = 0
            for pageNumber in range(1,pages + 1):
                pageRequest = requests.get("https://www.python.org/jobs/?page=" + str(pageNumber))
                pageSource = BeautifulSoup(pageRequest.content,"lxml")
                jobs = pageSource.find("div",attrs={"class":"row"}).ol.find_all("li")
                # Tüm işleri çektik, döngü ile ilan detaylarını alalım.
                for job in jobs:
                    name = job.h2.find("a").text
                    location = job.find("span",attrs={"class":"listing-location"}).text
                    company = job.find("span",attrs={"class":"listing-company-name"}).br.next.strip()
                    publish_time = job.find("time").text
                    totalJobs += 1
                    print(name,company,location,publish_time,sep="\n")
                    self.im.execute("""INSERT INTO PythonJob(Uzmanlık,Sirket,Ulke,Tarih) VALUES (?,?,?,?)""", [name,company,location,publish_time])
                    self.connect.commit()

                    print("-"*60)

            print("Toplam {} iş bulundu.".format(totalJobs))

    def doldur(self):
        try:
            secili=self.ui.tableWidget.selectedItems()

            self.ui.lineEdit.setText(secili[0].text())
            self.ui.lineEdit_2.setText(secili[1].text())
            self.ui.lineEdit_3.setText(secili[2].text())
            self.ui.lineEdit_4.setText(secili[3].text())

            if secili==[]:
                return

        except Exception as Hata:
            self.ui.statusbar.showMessage("Hata var",2000)
    def table_calistir(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(('Uzmanlık','Sirket','Ulke','Tarih'))
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setAlternatingRowColors(True)

        pallete = self.ui.tableWidget.palette()
        pallete.setColor(QPalette.Background, QColor(60, 60, 60))
        pallete.setColor(QPalette.AlternateBase, QColor("darkkhaki"))
        pallete.setColor(QPalette.Base, QColor('#bbb'))

        self.ui.tableWidget.setPalette(pallete)

        sec=self.im.execute("SELECT Uzmanlık,Sirket,Ulke,Tarih FROM PythonJob")
        okuma=sec.fetchall()

        self.ui.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(okuma):
            self.ui.tableWidget.insertRow(row_number)
            for columb_number, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_number, columb_number, QTableWidgetItem(str(data)))







