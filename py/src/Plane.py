import magpylib as mag3
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt

#
# Класс Plane представляет возможность создания сечения магнитного поля, в 
# котором на параметризуемой сетке будут вычисляться компоненты магнитного 
# поля, соответствующие этой плоскости (например, для плоскости XY это будут
# Bx и By. Параметризуется создание секущей плоскости строкой XY или XZ или YZ
#

class Plane:
    # planeName = XY | XZ | YZ
    # side - сторона квадратной сетки
    # cellNum - количество делений сетки (ячеек)
    # pos - положение плоскости на оси, которую она пересекает
    # coil - катушка, создающая поле
    def __init__(self, planeName, side, cellNum, pos, coil):
        self.name = planeName
        self.side = side
        self.cellNum = cellNum
        self.pos = pos
        # Массив ячеек вдоль стороны сетки. так как сетка квадратная, то 
        # второго не нужно
        self.ts = np.linspace(-self.side/2,self.side/2, self.cellNum)
        if self.name == "XY":
            self.grid = np.array([(x,y,self.pos) for y in self.ts  \
                                                 for x in self.ts])
        elif self.name == "XZ":
            self.grid = np.array([(x,self.pos,z) for z in self.ts  \
                                                 for x in self.ts])
        elif self.name == "YZ":
            self.grid = np.array([(self.pos,y,z) for z in self.ts  \
                                                 for y in self.ts])
        # Массив значений компонент магнитного поля в точках сетки
        self.Bs =coil.getB(self.grid).reshape(self.cellNum, self.cellNum, 3)
    # Возвращает массив значений трех компонент вектора B в каждой точке сетки
    def get_B(self):
        return self.Bs
    # Возвращает массив ячеек вдоль стороны сетки
    def get_side(self):
        return self.ts
    # Получить значение первой из компонент поля на рассматриваемой сетке
    def get_U(self):
        if self.name == "XY":
            U = self.Bs[:,:,0]
        elif self.name == "XZ":
            U = self.Bs[:,:,0]
        elif self.name == "YZ":
            U = self.Bs[:,:,1]
        return U
     # Получить значение второй из компонент поля на рассматриваемой сетке
    def get_V(self):
        if self.name == "XY":
            V = self.Bs[:,:,1]
        elif self.name == "XZ":
            V = self.Bs[:,:,2]
        elif self.name == "YZ":
            V = self.Bs[:,:,2]
        return V
    # Функции, необходимые для отображения секущей плоскости:
    # Получить массив значений точек на оси х по которым строится плоскость
    def get_Xcut(self):
        edge = self.side / 2
        if self.name == "XY":
            x = [-edge, -edge, edge, edge, -edge]
        elif self.name == "XZ":
            x = [-edge, -edge, edge, edge, -edge]
        elif self.name == "YZ":
            x = [self.pos, self.pos, self.pos, self.pos, self.pos]
        return x
    # Получить массив значений точек на оси у по которым строится плоскость
    def get_Ycut(self):
        edge = self.side / 2
        if self.name == "XY":
            y = [-edge, edge, edge, -edge, -edge]
        elif self.name == "XZ":
            y = [self.pos, self.pos, self.pos, self.pos, self.pos]
        elif self.name == "YZ":
            y = [-edge, -edge, edge, edge, -edge]
        return y
    # Получить массив значений точек на оси z по которым строится плоскость
    def get_Zcut(self):
        edge = self.side / 2
        if self.name == "XY":
            z = [self.pos, self.pos, self.pos, self.pos, self.pos]
        elif self.name == "XZ":
            z = [-edge, edge, edge, -edge, -edge]
        elif self.name == "YZ":
            z = [-edge, edge, edge, -edge, -edge]
        return z
    # Функции, необходимые для создания подписей рисунков:
    # Получить название осей графика (возвращает первым значение литеру 
    # горизонтальной оси, вторым - литеру вертикальной)
    def get_axes(self):
        return [char for char in self.name]
    def get_planeName(self):
        return self.name
        
    