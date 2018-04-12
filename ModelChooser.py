import copy
import numpy as np
import math

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
    # plt.show()
    plt.savefig('results.pdf')


def choose_model(stream_num, avg_times, lambdas, mu, query_num, test_num, comp_accur, p_val, get_result=False):
    t_proc = 1 / mu  # Request processing time
    print('Начальные значения mu = ' + str(mu) + " (t_proc = " + str(t_proc) + ")")
    print('tau = ' + str(avg_times))
    print('Среднее время между поступлением заявок в 1 буфер = ' + str(1 / lambdas[0]) + ' и во 2 = ' + str(
        1 / lambdas[1]))
    if sum(lambdas) > mu:
        print('Возможно возникновение ошибки, при которой не будет обработано достаточное количество заявок \n'
              'из каждого буфера потока.')


    # p_val = np.concatenate([np.arange(0.1, 0.4, 0.1), np.arange(0.4, 0.61, 0.001), np.arange(0.7, 1, 0.1)])

    # p_val = np.array([0, 0.3, 0.5, 0.8, 1])    # Распределение вероятностей для соблюдения среднего времени выполнения заявок
    # p_val = np.arange(0.2,0.9,0.1)
    # p_val = np.array([0, 1])

    # todo Обернуть в класс с параметрами. Сокрыть лишнее, упростить доступ.
    rez_time = []
    srv_mu = []
    algo_revers = False
    cur_accur = 1e2
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
            #print('p=' + str(p_val[val]) + ' successfully processed')
        avg_est /= test_num
        if not algo_revers:
            rez_time.append(avg_est)
            srv_mu.append(1 / t_proc)

        # print('avg')
        # avg1 = avg_est[0, :].tolist().index(min(avg_est[0, :]))
        # avg2 = avg_est[1, :].tolist().index(min(avg_est[1, :]))
        # print([avg_est[0, avg1], avg_est[1, avg1]])
        # print([avg_est[0, avg2], avg_est[1, avg2]])
        # print('t_proc = ', t_proc, ' mu=', 1 / t_proc)

        # Обратный проход с целью максимально приблизится к требуемым значениям среднего времени
        if algo_revers:
            flag = False  # Флаг нахождения значения, подходящего под заданные критерии
            for i in range(len(p_val)):
                if avg_est[0, i] < avg_times[0] and avg_est[1, i] < avg_times[1]:
                    flag = True
                    opt_val = i

                    # print('\navg_rez')
                    # print(avg_est[:, i])
                    # print('p=' + str(p_val[i]))
                    break
            if flag:  # Если значение критерия всё ещё есть
                # Нужно увеличивать t_proc или уменьшать mu
                temp_est = avg_est
                temp_t_p = t_proc
                t_proc = 1 / (1 / t_proc - cur_accur)
                while t_proc <= 0:
                    t_proc = 1 / (1 / t_proc + cur_accur)
                    cur_accur /= 10
                    t_proc = 1 / (1 / t_proc - cur_accur)
                if get_result:
                    print('mu='+str(1/t_proc))
            else:
                avg_est = temp_est  # Возвращаем предыдущий набор данных с подходящим под условия значением
                t_proc = temp_t_p

                if cur_accur <= comp_accur:
                    rez_time.append(avg_est)
                    srv_mu.append(round(1 / t_proc, -int(math.log10(comp_accur))))
                    break
                else:
                    t_proc = 1 / (1 / t_proc + cur_accur)  # Возвращаем предыдущее значение
                    cur_accur /= 10  # Увеличиваем точность
                    t_proc = 1 / (1 / t_proc - cur_accur)  # Приближаем время обслуживания к необходимым параметрам
        else:
            opt_val = 0
            for i in range(len(p_val)):
                if avg_est[0, i] < avg_times[0] and avg_est[1, i] < avg_times[1]:
                    opt_val = i
                    if get_result:
                        print('\navg_rez')
                        print(avg_est[:, i])
                        print('p=' + str(p_val[i]))
                    print('===Reverse time===')
                    algo_revers = True
                    temp_est = avg_est
                    temp_t_p = t_proc
                    break
            if not algo_revers:
                # if t_proc <= 1:
                #     t_proc /= 2
                # else:
                #     t_proc -= 1
                t_proc /= 2
                if t_proc < 1e-5:
                    print('Заданные требования достижимы лишь при малых значениях alpha')
                    break
    if get_result:
        print_results(avg_times, rez_time, srv_mu)
    # avg_times - tao1,2 (needed times)
    # rez_time

    print('rez')
    print(np.mean(avg_est[:, opt_val]))
    print(1 / (srv_mu[-1] - sum(lambdas)))
    print('p = ', p_val[opt_val])
    return rez_time, srv_mu


if __name__ == '__main__':
    stream_num = 2      # Количество потоков
    # Время в 2 раза больше
    # Интенсивность в 2 раза меньше
    avg_times = [4, 7.5]  # Среднее время для каждой категории заявок
    mu = 0.7
    # avg_times = [2, 1]  # Среднее время для каждой категории заявок
    # mu = 0.1
    lambdas = [0.15, 0.35]  # Интенсивности поступления заявок в каждый буфер
    query_num = 50000  # Общее количество заявок, которые поступят в каждый буфер. т.е. q_n в 1 и во 2.
    comp_accur = 1e-3  # Точность вычислений при обратном проходе (кол-во знаков после запятой)
    test_num = 10  # Количество тестов с разными рандомами (сглаживает графики?)
    prob = np.arange(0, 1.1, 0.1)  # Распределение вероятностей для соблюдения среднего времени выполнения заявок

    x, y = choose_model(stream_num, avg_times, lambdas, mu, query_num, test_num, comp_accur, prob, get_result=True)

    x1 = x[-1]
    y1 = y[-1]
    val_num = len(x1[-1])
    opt = [0] * val_num
    for i in range(val_num):
        opt[i] = abs(x1[0][i] - avg_times[0]) + abs(x1[1][i] - avg_times[1])
    print('Final!!!Opt')
    print(prob[np.argmin(opt)])
    print(np.min(opt))
