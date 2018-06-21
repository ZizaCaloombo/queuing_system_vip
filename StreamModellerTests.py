import unittest
import copy

import StreamModeller as SMod


class SMTests(unittest.TestCase):
    # Тесты на расчёт времени выполнения заявки
    def test_query_service_free_processing(self):
        self.assertEqual(SMod.query_servicing(3, 2, 2), 2)

    def test_query_service_busy_processing(self):
        self.assertEqual(SMod.query_servicing(1, 2, 2), 3)

    # Тесты на создание и обработку заявки
    def request_serving(self):
        t_proc = 2
        times = [1, 3, 4, 5, 10]
        times_len = len(times)
        sm = SMod.StreamModeller(t_proc, times)

        cur_time = 0
        ctimes = [times[0]]
        ind = 0
        while ind < times_len:
            ind, cur_time = sm.serve_request(cur_time)
            ctimes.append(cur_time)
        self.assertEqual([2, 2, 3, 4, 2], sm.in_sys)
        self.assertEqual([1, 3, 5, 7, 9, 12], ctimes)


if __name__ == '__main__':
    unittest.main()
