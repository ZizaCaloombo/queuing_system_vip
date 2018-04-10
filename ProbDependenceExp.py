import numpy as np
import matplotlib.pyplot as plt

import ModelChooser as MCh


stream_num = 2      # Количество потоков
# Время в 2 раза больше
# Интенсивность в 2 раза меньше
avg_times = [1, 1]  # Среднее время для каждой категории заявок
# mu = 0.2
# avg_times = [2, 1]  # Среднее время для каждой категории заявок
# mu = 0.1
lambdas = [0.5, 0.5]  # Интенсивности поступления заявок в каждый буфер
query_num = 10000  # Общее количество заявок, которые поступят в каждый буфер. т.е. q_n в 1 и во 2.
comp_accur = 1e-1  # Точность вычислений при обратном проходе (кол-во знаков после запятой)
test_num = 10  # Количество тестов с разными рандомами (сглаживает графики?)
prob = np.arange(0, 1.1, 0.1)  # Распределение вероятностей для соблюдения среднего времени выполнения заявок

tau = [[4, 1], [2, 1], [1, 1], [1, 2], [1, 4]]

opt = [0] * len(tau)

multi_num = 3
rez = [0] * len(tau)
full_rez = [rez] * 3
mu = 1
for f in range(multi_num):
    for i in range(len(tau)):
        if f > 0:
            tau[i][0] /= 2
            tau[i][1] /= 2
            mu *= 2
        avg_times = tau[i]

        x, y = MCh.choose_model(stream_num, avg_times, lambdas, mu, query_num, test_num, comp_accur, prob)

        x1 = x[-1]
        y1 = y[-1]
        val_num = len(x1[-1])
        opt = [0] * val_num
        for k in range(val_num):
            opt[i] = abs(x1[0][k] - avg_times[0]) + abs(x1[1][k] - avg_times[1])
        full_rez[f][i] = prob[np.argmin(opt)]
        print('Выполнено:', str(i+1), '/', str(len(tau)))
    print('=========')
    print('Всего:', str(f + 1), '/', str(multi_num))

plt.figure(1)
plt.xlabel('tau1/tau2')
plt.ylabel('p_opt')
for i in range(multi_num):
    plt.plot(range(1, 5), full_rez[i], 'x', label="Mu = " + "{0:.2f}".format(mu))
plt.legend(loc='best')
plt.grid()
# plt.show()
plt.savefig('ProbTest.pdf')
