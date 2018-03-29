def query_servicing(cur_time_in, last_served_time, t_proc):
    """
    Функция расчёта времени нахождения заявки в системе
    :param cur_time_in: Время поступления текущей заявки в систему
    :param last_served_time: Время выхода последней обслуженной заявки
    :param t_proc: Время обслуживания заявки
    :return:
    """
    return last_served_time - cur_time_in + t_proc if last_served_time > cur_time_in else t_proc


class StreamModeller:
    def __init__(self, income_times, service_times):
        self.income_times = income_times
        self.in_sys = []
        self.service_times = service_times

        self.req_come = 0   # Количество пришедших в систему заявок
        self.req_serv = 0   # Количество обслуженных заявок

    def serve_request(self, last_served_time):
        # Время выхода предыдущей обрабатываемой заявки из системы
        ls_time = last_served_time if last_served_time != 0 else self.income_times[0]
        self.in_sys.append(query_servicing(self.income_times[0], ls_time, self.service_times.pop(0)))
        # return number of served queries, last_served_time

        # todo rewrite code without pop
        return len(self.in_sys), self.in_sys[-1] + self.income_times.pop(0)
