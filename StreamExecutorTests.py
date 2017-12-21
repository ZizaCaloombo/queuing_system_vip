import unittest
import copy

import StreamExecutor as SExec


class SETests(unittest.TestCase):
    # Тест на создание очереди выполнения
    def test_exec_order(self):
        rand_arr = [0.3, 0.7, 0.3, 0.3, 0.3, 0.7, 0.7, 0.3, 0.7, 0.7]
        exp_order = [1, 2, 1, 1, 1, 2, 2, 1, 2, 2]

        r1 = [0.5, 1, 0, 0.1]
        ex2 = [1, 2, 1, 1]
        p = [0.5]
        print(' ')
        self.assertEqual(exp_order, SExec.create_exec_order(rand_arr, p))
        self.assertEqual(ex2, SExec.create_exec_order(r1, p))


    # Тесты на моделирование нескольких входных потоков
    def test_multirequest_execution(self):
        stream_num = 2
        lambdas = [1, 1]
        init_t_proc = 2
        in_times = [[1, 2, 4, 9, 10],
                    [3, 4, 5, 6, 9]]
        query_num = len(in_times[0])*len(in_times)
        # streams_num, lambdas, init_serv_time, query_num, in_times = []
        se = SExec.StreamExecuter(stream_num, lambdas, init_t_proc, query_num, copy.deepcopy(in_times))

        exec_order = [1, 2, 1, 1, 1, 2, 2, 1, 2, 2]
        p = 0.5

        se.run_execution(p, [i*p for i in exec_order], exec_order)
        self.assertEqual([[2, 5, 5, 2, 7], [2, 9, 10, 13, 12]], se.get_full_result())
        self.assertEqual([4.2, 9.2], se.get_average_result())

        se = SExec.StreamExecuter(stream_num, lambdas, init_t_proc, query_num, copy.deepcopy(in_times))
        self.assertEqual([4.2, 9.2], se.run_execution(p, [0.3, 0.7, 0.3, 0.3, 0.3, 0.7, 0.7, 0.3, 0.7, 0.7]))


if __name__ == '__main__':
    unittest.main()
