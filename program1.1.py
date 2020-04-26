# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 23:11:12 2020

@author: Warsars
"""
from PyQt5 import QtWidgets, QtCore, uic
from UI import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  
import os
import json
import numpy as np
import math
from random import randint
import requests
class MainWindow(QtWidgets.QMainWindow):

        
    def __init__(self, *args, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.graphicsAx.setBackground('w')
        self.ui.graphicsAy.setBackground('w')
        self.ui.graphicsAz.setBackground('w')

        self.ui.pushButton.clicked.connect(self.clear_plot_data)
        self.ui.pushButton_2.clicked.connect(self.data_printing)
    
        
        
    def data_printing(self):
        n=50; # тут сколько по оси х в графике делений
        pen = pg.mkPen(color=(255, 0, 0))
        
        self.xx = list(range(n))
        self.xy = list(range(n))
        self.xz = list(range(n))
        
        self.yx = [0 for i in range(n)]
        self.yy = [0 for i in range(n)]
        self.yz = [0 for i in range(n)]
        
        
        self.data_lineX =  self.ui.graphicsAx.plot(self.xx, self.yx, pen=pen)
        self.data_lineY =  self.ui.graphicsAy.plot(self.xy, self.yy, pen=pen)
        self.data_lineZ =  self.ui.graphicsAz.plot(self.xz, self.yz, pen=pen)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(30) # тут частота обновления графика в мс
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
        self.ui.pushButton.setEnabled(True);
        self.ui.pushButton_2.setEnabled(False);
        
    def clear_plot_data(self):
         self.timer.stop()
         self.ui.pushButton_2.setEnabled(True);
         self.data_lineX.clear();
         self.data_lineY.clear();
         self.data_lineZ.clear();
         self.ui.pushButton.setEnabled(False);
         
         
    def update_plot_data(self):
        #if data_current <> data_memory:
        #    data_memory=data_current;
        response = requests.get("http://127.0.0.1:8000/api/v1/esp/last?format=json") # тут ссыль на сервер
        current_data = json.loads(response.text);
        self.xx = self.xx[1:] 
        self.xy = self.xy[1:]
        self.xz = self.xz[1:] 
        self.xx.append(self.xx[-1] + 1)
        self.xy.append(self.xy[-1] + 1)
        self.xz.append(self.xz[-1] + 1)

        self.yx = self.yx[1:]
        self.yy = self.yy[1:]   
        self.yz = self.yz[1:]   
        self.yx.append( current_data['ax'] );
        self.yy.append( current_data['ay'] );
        self.yz.append( current_data['az'] );
        self.data_lineX.setData(self.xx, self.yx)
        self.data_lineY.setData(self.xy, self.yy)
        self.data_lineZ.setData(self.xz, self.yz)# Update


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())



if __name__ == '__main__':
    main()