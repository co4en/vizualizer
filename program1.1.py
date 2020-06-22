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
import time
import matplotlib.pyplot as plt

import numpy as np
import math
from random import randint
import requests
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class MainWindow(QtWidgets.QMainWindow):

        
    def __init__(self, *args, **kwargs):
        
        new_data = {'id': 2, 'ax': 0, 'ay': 0, 'az': 0, 'gx': 0, 'gy': 0, 'gz': 0, 'mx': 0, 'my': 0, 'mz': 0};
        requests.post("http://127.0.0.1:8000/api/v1/esp/create/", data=new_data) # выставление всего на ноль
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.graphicsAx.setBackground('w')
        self.ui.graphicsAy.setBackground('w')  # настройка УИшки
        self.ui.graphicsAz.setBackground('w')

        self.ui.pushButton.clicked.connect(self.clear_plot_data)
        self.ui.pushButton_2.clicked.connect(self.data_printing)
    
        
        
    def data_printing(self):
        n=50; # тут сколько по оси х в графике делений
        pen = pg.mkPen(color=(255, 0, 0))
        
        #setup start
        
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
        
        #setup end
        
    def clear_plot_data(self):
         self.timer.stop()
         self.ui.pushButton_2.setEnabled(True);
         self.data_lineX.clear();
         self.data_lineY.clear(); #очистка от кнопки
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

class ApplicationWindow(QtWidgets.QMainWindow): # это 3дэ окно
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
#        button1 = QtWidgets.QPushButton(self._main)
#        button2 = QtWidgets.QPushButton(self._main) # work in progress
#        button1.clicked.connect(self.clear_canvas)
#        button2.clicked.connect(self.start_canvas)
        
        # canvas setup
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        dynamic_canvas = FigureCanvas(Figure(figsize=(20, 12)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        n=50; # тут сколько по оси х в графике делений
        
        #data setup
        self.time1 = 0
        self.x = [0 for i in range(n)]
        self.y = [0 for i in range(n)]
        self.z = [0 for i in range(n)]
        
        self.vx = [0 for i in range(n)]
        self.vy = [0 for i in range(n)]
        self.vz = [0 for i in range(n)]
        
        self.gx = [0 for i in range(n)]
        self.gy = [0 for i in range(n)]
        self.gz = [0 for i in range(n)]
        
        self.ax = [0 for i in range(n)]
        self.ay = [0 for i in range(n)]
        self.az = [0 for i in range(n)]

        # timer setup
        self._dynamic_ax = dynamic_canvas.figure.gca(projection='3d')
        self._timer = dynamic_canvas.new_timer(
            30, [(self._update_canvas, (), {})])
        self._timer.start()

    def start_canvas(self): # work in progress
        self._timer = dynamic_canvas.new_timer(
            30, [(self._update_canvas, (), {})])
        self._timer.start() 
        
    def clear_canvas(self):
        self._timer.stop()
    
    
    def _update_canvas(self): 
        
        # расчет координат
        def coord_comp(x0,u0,a0,dt):
            return x0+u0*dt+a0*math.pow(dt,2)/2;
        
        # расчет скорости 
        def velo_comp(u,a,dt):
            return (int(u)+int(a)*dt)
        
        
        self._dynamic_ax.clear()
        
        response = requests.get("http://127.0.0.1:8000/api/v1/esp/last?format=json") # тут ссыль на сервер
        current_data = json.loads(response.text)
        
        dt = 0.03 # частота выполнения расчетов по траектории, он же задает частоту таймера, менять их вместе (а лучше вообще не менять)
        self.time1 = self.time1 + 1
        self.gx.append( current_data['gx'] )
        self.gy.append( current_data['gy'] ) # чтение сервера
        self.gz.append( current_data['gz'] )
        
        self.ax.append( current_data['ax'] )
        self.ay.append( current_data['ay'] )
        self.az.append( current_data['az'] )
        
        self.vx.append( velo_comp( self.vx[-1] , self.ax[-1] , dt))
        self.vy.append( velo_comp( self.vy[-1] , self.ay[-1] , dt))
        self.vz.append( velo_comp( self.vz[-1] , self.az[-1] , dt))
        
        self.x.append( coord_comp( self.x[-1] , self.vx[-2] , self.ax[-1] , dt))
        self.y.append( coord_comp( self.y[-1] , self.vy[-2] , self.ay[-1] , dt))
        self.z.append( coord_comp( self.z[-1] , self.vz[-2] , self.az[-1] , dt))
        
        self._dynamic_ax.plot( self.x , self.y , self.z , label='parametric curve' ) # отрисовка
        self._dynamic_ax.figure.canvas.draw()
        if self.time1==300 : # сколько данных с сервера возьмет 3d, пока что так, костыльно, можно менять как хочешь, это по времени примерно 10 секунд
            self._timer.stop()

        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
d = ApplicationWindow()
d.show()
sys.exit(app.exec_())



if __name__ == '__main__':
    main()