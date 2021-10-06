import magpylib as mag3
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt


#
# Класс CoilLoops предназначен для создания в геометрическом пространстве 
# многовитковых катушек. Катушки параметризуются числом слоев, числоем витков 
# в слое, расстоянием между витками в слое и расстоянием между слоями
#
# Сечение многослойной каушки:
#
# о о о о о о о о    - нечетный слой (начинаются с единицы). Первый - всегда нечетный
#  о о о о о о о     - четный слой (витки по Х расположены между витками нечетного)
# о о о о о о о о    - нечетный слой
#
class CoilLoops:
    def __init__(self, isLeft, rad, cur, nLay, layStep, nLoops, loopStep, dist):
        # Если флаг isLeft проходит проверку, 
        # значит экземпляр катушки двигаем влево
        if isLeft:
            self.loopStep = -loopStep
            self.dist = -dist
        # иначе двигаем вправо
        else:
            self.loopStep = loopStep
            self.dist = dist
        # Параметры не зависящие от положения катушки
        self.layStep = layStep
        self.rad = rad
        self.cur = cur
        self.nLay = nLay
        self.nLoops = nLoops
        
    # Создаем катушку по заданным параметрам и делаем 
    # необходимые геометрические преобразования. Возвращает экземляр 
    # системы/коллекции, состоящей из объединенных слоёв со множеством витков
    # в каждм слое
    def make_coil(self):
        Loops = []   # Массив витков, которые потом собираются в коллекцию
        # Массив номеров нечетных витков
        oddLoops = np.linspace(1,self.nLoops, self.nLoops)
        # Массив номеров четных витков
        evenLoops = np.linspace(1,self.nLoops - 1, self.nLoops - 1)
        i = 1  # Итератор по числу слоёв
        # Цикл по слоям
        while i <= self.nLay:
            # Четный или нечетный слой
            if (i % 2) == 0:
                loops = evenLoops
            else:
                loops = oddLoops
            # Переменная увеличивается с каждым витком на шаг витков
            loopStep = 0
            # Цикл по виткам
            for l in loops:
                # Создаем виток
                loop = mag3.current.Circular( current = self.cur\
                                            , diameter = self.rad*2)
                # Поворачиваем виток параллельно плоскости YZ
                rotation_object = R.from_euler('y', 90, degrees=True)
                loop.rotate(rotation_object)
                # Обрабатываем случай первого и не первого витка в четном слое
                if ((len(loops) == (len(evenLoops))) and l == 1):
                    # Раздвигаем витки на расстояние dist от центра координат
                    # плюс некоторая длина, соответствующая шагу витков и их числу
                    loopStep = self.loopStep/2
                    loop.move((self.dist + loopStep, 0, 0))
                else: 
                    loop.move((self.dist + loopStep, 0, 0))
                loopStep += self.loopStep
                # Добавляем виток в массив
                Loops.append(loop) 
            i += 1  # Инкрементируем слой
            self.rad += self.layStep       # Увеличиваем радиус следующего слоя
        coil = mag3.Collection(Loops)     # Собираем все витки в одну коллекцию
        return coil
                