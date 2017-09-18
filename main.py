import sys
import datetime

#import Calculation
#import DB_Stat


from PyQt5 import QtCore, QtGui, QtWidgets
from main_window import *


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #starting methods
        self.check_net_connection()
        
        self.today = datetime.date.today()
        self.ui.date_inflation.setDate(datetime.datetime.now())
        self.time_diff()
        
        self.total_counting()
        self.balance_counting()
        self.add_payment_counting()

        #connections
        self.ui.checkBox_diagram.stateChanged.connect(self.draw_diagram)
        self.ui.date_start.dateChanged.connect(self.time_diff)
        self.ui.date_end.dateChanged.connect(self.time_diff)
        self.ui.spinBox_prepayment.valueChanged.connect(self.balance_counting)
        self.ui.SpinBox_square.valueChanged.connect(self.total_counting)
        self.ui.spinBox_price.valueChanged.connect(self.total_counting)
        self.ui.spinBox_mon_pay.valueChanged.connect(self.balance_counting)
        self.ui.checkBox_include_inflation.stateChanged.connect(self.add_payment_counting)
        self.ui.date_inflation.dateChanged.connect(self.add_payment_counting)
        
        
    # FROM DB_Stat: (collecting DB_stat data, checking network)
    def check_net_connection(self):
        print('checking network, DB')
        
    # FROM Calculation:
    def time_diff(self):
        print('calculate time difference')

    # FROM Calculation: 
    def total_counting(self):
        print('total counting...')

    # FROM Calculation:
    def balance_counting(self):     #(self, time_diff)
        print('balance counting...')


    # FROM DB_Stat, Calculation:
    def add_payment_counting(self):
        if self.ui.checkBox_include_inflation.isChecked():
            print('calculate additional payment with inflation')
        else:
            print('calculate additional payment without inflation')
        #get % of inflation (current month), calculate spinBox_mon_uah
        #calculate % of total inflation, calculate spinBox_total_uah
                            

    # DIAGRAM DRAWING METHOD (mathplotlib?)
    def draw_diagram(self):
        if self.ui.checkBox_diagram.isChecked():
            print('Drawing...')
        else:
            print('Clearing')
               
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
