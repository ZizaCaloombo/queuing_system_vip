import numpy as np

import StreamModeller as SMod


def create_exec_order(rand_arr, p):
    exec_order = np.zeros(len(rand_arr))
    rand_arr = np.array(rand_arr)
    j = 1
    if type(p) == type(list):
        for i in sorted(p):
            exec_order[rand_arr <= i] = j
            rand_arr[rand_arr <= i] = np.inf
            j += 1
    else:
        exec_order[rand_arr <= p] = j
        rand_arr[rand_arr <= p] = np.inf
        j += 1
    exec_order[rand_arr <= 1] = j
    return exec_order.astype(int).tolist()


class StreamExecuter:
    def __init__(self, streams_num, lambdas, init_serv_time, query_num, in_times=[]):
        if streams_num == len(lambdas):
            self.streams = streams_num
            self.t_proc = init_serv_time  # Время обработки заявки
            self.sm = [0 for _ in range(streams_num)]  # Лист с экземплярами моделируемых потоков.
            self.query_num = query_num
            self.served_num = [0, 0]  # Индекс заявок
            self.min_num_queries = 1000  # Минимально необходимое число заявок для обработки
            self.lambdas = lambdas
            service_times = np.random.exponential(self.t_proc, self.query_num).tolist()
            for i in range(streams_num):
                self.sm[i] = SMod.StreamModeller(np.cumsum(np.random.exponential(1 / self.lambdas[i],
                                                                                 self.query_num)).tolist()
                                                 if len(in_times) == 0 else in_times[i],
                                                 service_times)
        else:
            raise ValueError("Wrong size of the arrays")

    def run_execution(self, p, rand_arr, ex_order=[]):

        last_served_time = 0  # Время обработки последней заявки
        self.served_num = [0, 0]  # Индекс заявок
        # rand_arr = np.random.rand(2*self.query_num)

        exec_order = create_exec_order(rand_arr, p) if len(ex_order) == 0 else ex_order
        exec_order = exec_order[:self.query_num]

        # print(exec_order)
        # while sum(self.served_num) < self.query_num:  # Пока не обработано нужное количество заявок
        by_order = 0
        while min(self.served_num) <= self.min_num_queries:
            # Вот тут менять при количестве потоков > 2
            order_val = exec_order[by_order] - 1
            not_order_val = (1 + order_val) % 2
            # Если ОУ не занято и заявка не по порядку пришла раньше порядковой - запуск непорядковой в обработку.
            if last_served_time < self.sm[order_val].income_times[0] and \
                    self.sm[order_val].income_times[0] > self.sm[not_order_val].income_times[0] and \
                    self.streams > 1:
                self.served_num[exec_order[not_order_val] - 1], last_served_time = \
                    self.sm[not_order_val].serve_request(last_served_time)
            else:
                self.served_num[order_val], last_served_time = \
                    self.sm[order_val].serve_request(last_served_time)

        # for i in range(len(exec_order)):  # Для каждой заявки в списке для обработки
        #     self.served_num[exec_order[i] - 1], last_served_time = \
        #         self.sm[exec_order[i] - 1].serve_request(last_served_time)
        # print('Завершена обработка для mu = ' + str(1/self.t_proc) + " (t_proc = " + str(self.t_proc) + ")")
        return self.get_average_result()

    def get_average_result(self):
        rez = []
        for streamModel in self.sm:
            rez.append(np.mean(streamModel.in_sys))
        return rez

    def get_full_result(self):
        rez = []
        for streamModel in self.sm:
            rez.append(streamModel.in_sys)
        return rez
