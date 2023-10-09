import math
import sys
from time import sleep
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication,
)

class Cspray:
    def __init__(self):
        self._list = [] # maakt een list met alle punten
        self._line_list = []
        self._distance_angle_list = []

    def add(self,x,y):
        self._list.append((x,y)) # voegt een y en y punt toe aan de lijst

    def draw(self, scene):
        self._ride = []
        for i in range(len(self._list) - 1):
            point1 = self._list[i]
            point2 = self._list[i+1]
            point1_x = self._list[i][0]
            point1_y = self._list[i][1]
            point2_x = self._list[i+1][0]
            point2_y = self._list[i+1][1]
            delta_x = (point2_x-point1_x)**2
            delta_y = (point2_y-point1_y)**2
            distance = (delta_x+delta_y)**(1/2)
            self._distance_angle_list.append([distance])
            self._line_list.append([point1,point2])

            item = QtWidgets.QGraphicsLineItem(point1_x, point1_y, point2_x, point2_y)
            scene.addItem(item)

        for i in range(len(self._line_list) - 1):
            p1 = self._line_list[i][0]
            p2 = self._line_list[i][1]
            p3 = self._line_list[i+1][1]
            ang = math.degrees(
                math.atan2(p3[1] - p2[1], p3[0] - p2[0]) - math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
            if ang < 0:
                ang = ang + 360
            self._distance_angle_list[i].append(180 - ang)
        self._distance_angle_list[-1].append(0)
        print(self._distance_angle_list)
        print(len(self._distance_angle_list))

Ui_MainWindow, QtBaseClass = uic.loadUiType("ros_line.ui")

class MyApp(QtWidgets.QMainWindow):
    def __init__(self): # zet de variabelen vast van de View
        self._list = []
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self._scene = QtWidgets.QGraphicsScene()
        self.ui.View.setScene(self._scene)
        self._scene.setSceneRect(0, 0, 100, 100)
        self.ui.View.mousePressEvent = self.viewmousehold
        self.ui.View.mouseMoveEvent = self.viewmousemove
        self.ui.View.mouseReleaseEvent = self.viewMouseRelease

    def viewmousehold(self, event):
        self._scene.clear()
        point = self.ui.View.mapToScene(event.pos()) # pakt de x en y van de muispositie
        self._line = Cspray() # maakt een lege classe aan en voert de x en y coordinaten toe.



    def viewmousemove(self, event):
        point = self.ui.View.mapToScene(event.pos())
        self._line.add(point.x(), point.y())
        sleep(.03)

    def viewMouseRelease(self,event):
        point = self.ui.View.mapToScene(event.pos())
        self._line.draw(self._scene)

app = QApplication(sys.argv)
UIWindow = MyApp()
app.exec_()
