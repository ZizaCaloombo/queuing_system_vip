import copy
import numpy as np

import StreamExecutor as SExec


def print_results(avg_times, rez_time, srv_mu):
    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.xlabel('t_vip')
    plt.ylabel('t_oth')
    plt.plot(avg_times[0], avg_times[1], 'rx')
    i = 0
    for times in rez_time:
        plt.plot(times[0, :], times[1, :], label="Mu = " + "{0:.2f}".format(srv_mu[i]))
        i += 1
    plt.legend(loc='best')
    plt.grid()
    plt.show()


stream_num = 2

# in_times = [[1, 2, 4, 9, 10],
#             [3, 4, 5, 6, 9]]


# query_num = len(in_times[0])*len(in_times)

# exec_order = [1, 2, 1, 1, 1, 2, 2, 1, 2, 2]
# p = 0.5


# Avg_time
avg_times = [0.5, 0.5]  # Среднее время для каждой категории заявок

# Lambda
lambdas = [2, 3]
print('in times are ' + str(1/lambdas[0]) + ' and ' + str(1/lambdas[1]))

mu = 5
t_proc = 1/mu  # Request processing time
print('Начальные значения mu = ' + str(mu) + " (t_proc = " + str(t_proc) + ")")

query_num = 10000

# p_val = np.concatenate([np.arange(0.1, 0.4, 0.1), np.arange(0.4, 0.61, 0.001), np.arange(0.7, 1, 0.1)])
p_val = np.arange(0, 1.1, 0.1)    # Распределение вероятностей для соблюдения среднего времени выполнения заявок
# p_val = np.array([0, 0.3, 0.5, 0.8, 1])    # Распределение вероятностей для соблюдения среднего времени выполнения заявок
# p_val = np.arange(0.2,0.9,0.1)
# p_val = np.array([0, 1])

# todo Обернуть в класс с параметрами. Сокрыть лишнее, упростить доступ.

test_num = 1
rez_time = []
srv_mu = []
avg_est = np.zeros([2, len(p_val)])
while True:
    rand_arr = []
    for i in range(test_num):
        rand_arr.append(np.random.rand(query_num))

    avg_est = np.zeros([2, len(p_val)])
    for val in range(len(p_val)):
        p = p_val[val]
        # SE( streams_num, lambdas, init_serv_time, query_num, in_times = []  )
        for k in range(test_num):
            se = SExec.StreamExecuter(stream_num, lambdas, t_proc, query_num)
            rez = se.run_execution(p, copy.deepcopy(rand_arr[k]))
            for i in range(stream_num):
                avg_est[i, val] += rez[i]
        print('p=' + str(p_val[val])+' successfully processed')
    avg_est /= test_num
    rez_time.append(avg_est)
    srv_mu.append(1 / t_proc)
    algo_finish = False

    opt_val = 0
    for i in range(len(p_val)):
        if avg_est[0, i] < avg_times[0] and avg_est[1, i] < avg_times[1]:
            opt_val = i
            print('avg_rez')
            print(avg_est[:, i])
            print('p='+str(p_val[i]))
            algo_finish = True
            break
    if algo_finish:
        break
    print('avg')
    avg1 = avg_est[0, :].tolist().index(min(avg_est[0, :]))
    avg2 = avg_est[1, :].tolist().index(min(avg_est[1, :]))
    print([avg_est[0, avg1], avg_est[1, avg1]])
    print([avg_est[0, avg2], avg_est[1, avg2]])
    print('t_proc')
    print(t_proc)
    if t_proc <= 1:
        t_proc /= 2
    else:
        t_proc -= 1
    if t_proc < 1e-5:
        break
print_results(avg_times, rez_time, srv_mu)
print('rez')
print(np.mean(avg_est[:, opt_val]))
print(1/(srv_mu[-1]-sum(lambdas)))


# avg_est = np.zeros(2, len(p_val)).fill(max(avg_times)+1)
#
# while np.argmax(avg_est[0, ] > avg_times[0]) and np.argmax(avg_est[0, ] > avg_times[0]):
#     rand_arr = np.random.rand(2*query_num)
#     for val in range(len(p_val)):
#         p = p_val[val]
#         # SE( streams_num, lambdas, init_serv_time, query_num, in_times = []  )
#         se = SMod.StreamExecuter(stream_num, lambdas, t_proc, query_num)
#         rez = se.run_execution(p, copy.deepcopy(rand_arr))
#         for i in range(stream_num):
#             avg_est[i, val] = rez[i]
