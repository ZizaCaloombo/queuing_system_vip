import numpy as np
import matplotlib.pyplot as plt

import ModelChooser as MCh

'''
Строит график зависимости оптимальной вероятности от отношения tau1/tau2
'''

stream_num = 2      # Количество потоков
# Время в 2 раза больше
# Интенсивность в 2 раза меньше
avg_times = [4, 5]  # Среднее время для каждой категории заявок
# mu = 0.2
# avg_times = [2, 1]  # Среднее время для каждой категории заявок
# mu = 0.1
lambdas = [0.25, 0.25]  # Интенсивности поступления заявок в каждый буфер
query_num = 1000  # Общее количество заявок, которые поступят в каждый буфер. т.е. q_n в 1 и во 2.
comp_accur = 1e-2  # Точность вычислений при обратном проходе (кол-во знаков после запятой)
test_num = 10  # Количество тестов с разными рандомами (сглаживает графики?)
prob = np.arange(0, 1.1, 0.1)  # Распределение вероятностей для соблюдения среднего времени выполнения заявок

tau = [[1, 4], [1, 2], [1, 1], [2, 1], [4, 1]]

opt = [0] * len(tau)

multi_num = 3
rez = [0] * len(tau)
full_rez = [rez] * 3
mu = 0.7
label_data = []
for f in range(multi_num):
    if f > 0:
        mu *= 2
    for i in range(len(tau)):
        if f > 0:
            tau[i][0] /= 2
            tau[i][1] /= 2

        avg_times = tau[i]

        x, y = MCh.choose_model(stream_num, avg_times, lambdas, mu, query_num, test_num, comp_accur, prob)

        x1 = x[-1]
        y1 = y[-1]
        val_num = len(x1[-1])
        opt = [0] * val_num
        for k in range(val_num):
            opt[k] = abs(x1[0][k] - avg_times[0]) + abs(x1[1][k] - avg_times[1])
        full_rez[f][i] = prob[np.argmin(opt)]
        print('Выполнено:', str(i+1), '/', str(len(tau)))
    label_data.append([mu, [tau[2][0], tau[2][1]]])
    print('=========')
    print('Всего:', str(f + 1), '/', str(multi_num))
    print('=========')

ticks_data = []
for val in tau:
    ticks_data.append(val[0]/val[1])
x = [1, 2, 3, 4, 5]

plt.figure(1)
plt.xlabel('tau1/tau2')
plt.ylabel('p_opt')
plt.xticks(x, ticks_data)
for i in range(multi_num):
    plt.plot(x, full_rez[i], 'x', label="Mu=" + "{0:.2f}".format(label_data[i][0]) + ' ' + "tau=" +
                                        str(label_data[i][1]))
plt.legend(loc='best')
plt.grid()
# plt.show()
plt.savefig('ProbTest.pdf')
