import numpy as np
import matplotlib.pyplot as plt

import StreamModeller as smod

# todo Произвести расчёт для 10 чисел
# todo Сделать сравнение результатов в рамках допустимых delta
# Вопросы
# todo Дихотомия p, Mu



# 1000 опытов, 0.00 - 1 знак правильный, 2 - не обязательно
# 10000, 0.000


def chooser(buf_vip, buf_oth, t_vip, t_oth):
    pass


def query_servicing(cur_time_in, last_served_time, t_proc):
    """
    Функция расчёта времени нахождения заявки в системе
    :param cur_time_in: Время поступления текущей заявки в систему
    :param last_served_time: Время выхода последней обслуженной заявки
    :param t_proc: Время обслуживания заявки
    :return:
    """
    return last_served_time - cur_time_in + t_proc if last_served_time > cur_time_in else t_proc


# Avg_time
t_vip = 2
t_oth = 2

# Lambda
lambda_vip = 0.2
lambda_oth = 0.2

mu = 50
t_proc = 1/mu  # Request processing time

query_num = 10000
query_num_vip = int(query_num)
query_num_oth = int(query_num)

# Queries income schedule
vip_times = np.random.exponential(1/lambda_vip, query_num_vip)
oth_times = np.random.exponential(1/lambda_oth, query_num_oth)

vip_requests = np.cumsum(vip_times)  # Time format as 2.1, 3.7, 15, 459.3, ...
oth_requests = np.cumsum(oth_times)


p_val = np.arange(0.1, 1.0, 0.1)    # Распределение вероятностей для соблюдения среднего времени выполнения заявок
# p_val = np.array([0, 0.3, 0.5, 0.8, 1])    # Распределение вероятностей для соблюдения среднего времени выполнения заявок

rez_time = []
srv_mu = []
serviced_queries = []
while True:
    avg_vip, avg_oth = np.zeros(len(p_val)), np.zeros(len(p_val))
    sq = []
    for val in range(len(p_val)):
        p = p_val[val]
        in_sys_vip = np.zeros(query_num_vip)
        in_sys_oth = np.zeros(query_num_oth)
        rand_arr = np.random.rand(query_num_vip + query_num_oth + 1)
        last_served_time = 0    # Время обработки последней заявки
        i, j = 0, 0     # Индекс заявок
        while i < query_num_vip and j < query_num_oth:  # Пока не обработано нужное количество заявок
            if rand_arr[i + j] < p:  # Если рандом меньше, тогда в обработку vip
                in_sys_vip[i] = query_servicing(vip_requests[i], last_served_time, t_proc)

                last_served_time = vip_requests[i] + in_sys_vip[i]
                i += 1  # Обработка заявки
            else:   # иначе oth
                in_sys_oth[j] = query_servicing(oth_requests[j], last_served_time, t_proc)
                # Расчёт времени завершения работы заявки
                last_served_time = oth_requests[j] + in_sys_oth[j]
                j += 1  # Обработка заявки

        sq.append([i, j])
        avg_vip[val] = in_sys_vip[:i+1].mean()
        print('p')
        print(p)
        print(in_sys_vip[:i+1].mean())
        print(in_sys_oth[:j+1].mean())
        avg_oth[val] = in_sys_oth[:j+1].mean()
        print('i+j')
        print(i/(i+j))
        # print(len(in_sys_oth==0))
        # print(sum(in_sys_vip == 0))
        # print('---')
    serviced_queries.append(sq)
    print(serviced_queries)
    rez_time.append([avg_vip, avg_oth])
    srv_mu.append(1/t_proc)
    algo_finish = False
    for i in range(len(p_val)):
        if avg_oth[i] < t_oth and avg_vip[i] < t_vip:
            print('avg')
            print(avg_vip[i])
            print(avg_oth[i])
            algo_finish = True
            break
    if algo_finish or t_proc < 1:
        break
    print('t_proc')
    print(t_proc)
    t_proc -= 1
    if t_proc == 0: break

    # print("Текущее время обработки заявки", t_proc)
    #
    # print("Oth")
    # print(t_oth)
    # print(avg_oth)
    # print("Vip")
    # print(t_vip)
    # print(avg_vip)
    # print(avg_vip / (avg_vip + avg_oth))
    # abs(avg_oth - t_oth) < success_rate * t_oth or
    # print('diff')
    # print(abs(avg_vip - t_vip))
    # print(success_rate * t_vip)
    # break
    # if abs(avg_vip - t_vip) < t_vip:
    #     break
    # if avg_vip < t_vip:
    #     t_proc += 1
    # else:
    #     t_proc -= 1

    # if abs(avg_oth - t_oth) < success_rate * t_oth:
    #     break
    # if avg_oth < t_oth:
    #     t_proc += 1
    # else:
    #     t_proc -= 1

print(rez_time)

plt.figure(1)
plt.xlabel('t_vip')
plt.ylabel('t_oth')
plt.plot(t_vip, t_oth, 'rx')
i = 0
for times in rez_time:
    plt.plot(times[0], times[1],  label="Mu = "+"{0:.2f}".format(srv_mu[i]))
    i += 1
plt.legend(loc='best')
plt.show()
