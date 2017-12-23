import numpy as np

import StreamExecutor as SExec

lam = 1
print(1/lam)
print('-')
arr = []
# print(np.random.rand())
query_num = 10000
# for _ in range(query_num):
#     arr.append(1/lam * np.log(1/np.random.rand()))
# print(np.mean(arr))

stream_num = 1
p = 0.5
mu = 2

order = [1 for _ in range(query_num)]
se = SExec.StreamExecuter(stream_num, [lam], 1/mu, query_num)
rez = se.run_execution(p, [], order)
print('rez')
print(rez)
print(1/(mu-lam))
