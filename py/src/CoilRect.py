import magpylib as mag3
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt


#
# Класс CoilRect предназначен для создания в геометрическом пространстве 
# многовитковых прямоугольных катушек. Катушки параметризуются числом слоев, 
# числоем витков в слое, расстоянием между витками в слое и расстоянием между слоями
#
# Сечение многослойной каушки:
#
# о о о о о о о о    - нечетный слой (начинаются с единицы). Первый - всегда нечетный
#  о о о о о о о     - четный слой (витки по Х расположены между витками нечетного)
# о о о о о о о о    - нечетный слой
#
class CoilRect:
    def __init__(self, isLeft, width, height, cur\
               , nLay, layStep, nLoops, loopStep, dist):
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
        self.w = width
        self.h = height
        self.cur = cur
        self.nLay = nLay
        self.nLoops = nLoops
        
    # Создаем катушку по заданным параметрам и делаем 
    # необходимые геометрические преобразования. Возвращает экземляр 
    # системы/коллекции, состоящей из объединенных слоёв со множеством витков
    # в каждом слое
    def make_coil(self):
        Loops = []   # Массив витков, которые потом собираются в коллекцию
        # Массив номеров нечетных витков
        oddLoops = np.linspace(1, self.nLoops, self.nLoops)
        # Массив номеров четных витков
        evenLoops = np.linspace(1, self.nLoops - 1, self.nLoops - 1)
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
                # Обрабатываем случай первого и не первого витка в четном слое
                if ((len(loops) == (len(evenLoops))) and l == 1):
                    # Раздвигаем витки на расстояние dist от центра координат
                    # плюс некоторая длина, соответствующая шагу витков и их числу
                    loopStep = self.loopStep/2
                # Создаем линейные токи
                line1 = mag3.current.Line(current = self.cur\
                                        , vertices = [
                                            (self.dist + loopStep, -self.w/2, -self.h/2)\
                                          , (self.dist + loopStep, self.w/2, -self.h/2)\
                                          ] )
                line2 = mag3.current.Line(current = self.cur\
                                        , vertices = [
                                            (self.dist + loopStep, self.w/2, -self.h/2)\
                                          , (self.dist + loopStep, self.w/2, self.h/2)\
                                          ] )
                line3 = mag3.current.Line(current = self.cur\
                                        , vertices = [
                                            (self.dist + loopStep, self.w/2, self.h/2)\
                                          , (self.dist + loopStep, -self.w/2, self.h/2)\
                                          ] )
                line4 = mag3.current.Line(current = self.cur\
                                        , vertices = [
                                            (self.dist + loopStep, -self.w/2, self.h/2)\
                                          , (self.dist + loopStep, -self.w/2, -self.h/2)\
                                          ] )
                # Объединяем линейные токи в рамку/виток
                loop = mag3.Collection(line1, line2, line3, line4)
                loopStep += self.loopStep  # Увеличиваем отступ для следующих витков
                Loops.append(loop)  # Добавляем витки в массив
            i += 1  # Инкрементируем слой
            self.w += self.layStep         # Увеличиваем ширину следующего слоя
            self.h += self.layStep         # Увеличиваем высоту следующего слоя
        coil = mag3.Collection(Loops)     # Собираем все витки в одну коллекцию
        return coil
