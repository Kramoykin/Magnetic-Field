import numpy as np
import math


# Функция gen_sinus() позволяет рассчитывать мгновенные значения тока в первой 
# катушке (с частотой freq1 и амплитудой amp1) и тока во второй катушке (с 
# частотой freq2 и амплитудой amp2) на
# интервале в nPer периодов минимальной из двух частот с шагом дискретизации
# в step (nStep делит наименьший из двух периодов генераторов, соответствующий
# наибольше частоте, на nStep шагов)

class Sinus:
    def __init__(self, freq1, amp1, freq2, amp2, nPer, nStep):
        self.freq1 = freq1
        self.freq2 = freq2
        self.amp1 = amp1
        self.amp2 = amp2
        self.nPer = nPer
        self.nStep = nStep
    # Возвращает массив значений времени на рассматриваемом интервале
    def get_times(self):
        # Выбираем большую и меньшую частоту
        if self.freq1 >= self.freq2:
            self.freqMax = self.freq1
            self.freqMin = self.freq2
        else:
            self.freqMax = self.freq2
            self.freqMin = self.freq1
        # Вычисляем время, на котором рассматриваем сигнал, учитывая число периодов
        #, которое хотим наблюдать и выбирая для расчета наибольший период
        time = 1. / self.freqMin * self.nPer
        # Составляем массив чисел, соответствующих точке на временной прямой, в
        # которую оцифровывается синус
        self.times =  np.linspace(0, time, self.nStep * self.nPer\
                                  *int(self.freqMax / self.freqMin))
        return self.times
    # Возвращает массивы значения токов
    def get_currents(self):
        # Вычисляем угловые частоты (омеги)
        w1 = 2 * math.pi * self.freq1
        w2 = 2 * math.pi * self.freq2
        # Возвращаемые массивы токов
        curr1 = []
        curr2 = []
        # Вычисляем мгновенные значения токов
        for t in self.times:
            i1 = self.amp1 * math.sin(w1*t)
            i2 = self.amp2 * math.sin(w2*t)
            curr1.append(i1)
            curr2.append(i2)
        # Возвращаем списки:
        # 1й (curr1) - значения тока 1й катушки на временах times
        # 2й (curr2) - значения тока 2й катушки на временах times
        return [curr1, curr2]
    # Возвращаем максимальную частоту
    def get_freqMax(self):
        return self.freqMax
    # Возвращаем минимальную частоту
    def get_freqMin(self):
        return self.freqMin
    