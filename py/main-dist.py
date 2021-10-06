# Python - библиотеки
import magpylib as mag3
import matplotlib.pyplot as plt
import numpy as np
import yaml
# Рукописные файлы с классами
from src.CoilLoops import CoilLoops
from src.Plane import Plane
from src.CoilRect import CoilRect

# Сечение многослойной каушки:
#
# о о о о о о о о    - нечетный слой (начинаются с единицы). Первый - всегда нечетный
#  о о о о о о о     - четный слой (витки по Х расположены между витками нечетного)
# о о о о о о о о    - нечетный слой
#
# число витков в четном слое на 1 меньше чем в нечетном

"-------------Подключаем и считываем YAML-конфигурационный файл---------------"
configPath = "/home/ivan/Projects/MagneticField/config-rect.yaml"
stream = open(configPath, 'r')
Val = yaml.load(stream)   #  Python-словарь со значениями из config.yaml
"------------------Начальные значения для первой катушки----------------------"
isLeft1 = Val["isLeft1"]
coilWidth1 = Val["coilWidth1"] 
coilHeight1 = Val["coilHeight1"]  
currentAmp1 = Val["currentAmp1"]
nLayers1 = Val["nLayers1"]
layerStep1 = Val["layerStep1"]
nLoops1 = Val["nLoops1"]
loopStep1 = Val["loopStep1"]
distance1 = Val["distance1"]
"------------------Начальные значения для второй катушки----------------------"
isLeft2 = Val["isLeft2"]
coilWidth2 = Val["coilWidth2"] 
coilHeight2 = Val["coilHeight2"]
currentAmp2 = Val["currentAmp2"]
nLayers2 = Val["nLayers2"]
layerStep2 = Val["layerStep2"]
nLoops2 = Val["nLoops2"]
loopStep2 = Val["loopStep2"]
distance2 = Val["distance2"]
"------------------Начальные значения для сетки-------------------------------"
planeSide = Val["planeSide"]
cellNumber = Val["cellNumber"]
zonesNumber = Val["zonesNumber"]
dirPref = Val["dirPref"]
"-------Значения для итераций в циклах (менять не нужно)----------------------"
zones = np.linspace(1, zonesNumber\
                     , zonesNumber) # массив номеров секущих плоскостей
planeNames = ["XY"]# , "XZ", "YZ"]  # секущие плоскости
"~~~~~~~~~~~~~~____Итерируем по расстояниям____~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
for step in range(1, 50, 1):
    distance1 += 25
    distance2 += 25
    planeSide += 50    
    "------------------Создаем катушки----------------------------------------"
    c1 = CoilRect(isLeft1, coilWidth1, coilHeight1, currentAmp1\
                , nLayers1, layerStep1, nLoops1, loopStep1, distance1)
    coil1 = c1.make_coil()
    c2 = CoilRect(isLeft2, coilWidth2, coilHeight2, currentAmp2\
                , nLayers2, layerStep2, nLoops2, loopStep2, distance2)
    coil2 = c2.make_coil()
    SYS = mag3.Collection(coil1, coil2)  # Объединяем катушки в коллекцию
    "~~~~~~~~~~~~~~~~__Цикл, итерирующий по плоскостям__~~~~~~~~~~~~~~~~~~~~~~"
    for name in planeNames:
        "~~~~~~~~~~~~~~~~__Цикл, итерирующий по секущим зонам__~~~~~~~~~~~~~~~"
        if zonesNumber > 1:
            position = planeSide / 2                    # позиция плоскости
            posStep = planeSide / (zonesNumber - 1)     # шаг смещения позиции
        else:
            position = 0
            posStep = 0
        for num in zones:
            "------------------Создаем секущую плоскость----------------------"
            p1 = Plane(name, planeSide, cellNumber, position, SYS)
            "------------------Рисуем поле в секущей плоскости и катушку------"
            # Значения интервалов изменения магнитного поля
            X = p1.get_side()
            Y = p1.get_side()
            # Значения компонент магнитного поля, соответствующих секущей плоскости
            U = p1.get_U()
            V = p1.get_V()
            # Массив значений всех компонент магнитного поля
            Bs = p1.get_B()
            # Создаем фигуру и оси
            fig=plt.figure(figsize=(20,10))
            ax1 = fig.add_subplot(121, projection='3d')
            ax2 = fig.add_subplot(122)
            # Отрисовываем катушку
            SYS.display(axis=ax1)   
            # Отрисовываем секущую плоскость
            xCut = p1.get_Xcut()
            yCut = p1.get_Ycut()
            zCut = p1.get_Zcut()
            ax1.plot(xCut,yCut,zCut)
            # Названия осей секущей плоскости
            horAx,vertAx = p1.get_axes()
            # Название секущей плоскости
            planeName = p1.get_planeName()
            # Отрисовываем поле   
            ax2.streamplot(X, Y, U, V, color='k')
            ax2.pcolor(X,Y,np.linalg.norm(Bs,axis=2)\
                      ,cmap=plt.cm.get_cmap('coolwarm'))
            ax2.set_xlabel(horAx + ", mm")
            ax2.set_ylabel(vertAx + ", mm")
            dist = str(distance1 + distance2)
            ax2.set_title("Ширина прохода = " + dist)
            # сохраняем график в соответствующей директории
            plt.savefig(dirPref + "/" + planeName + "/" + dist + ".png")
            # сдвигаем плоскость для следующей итерации
            position -= posStep
       