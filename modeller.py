import numpy as np

def chooser(buf_vip, buf_oth, t_vip, t_oth):
    pass


lambda_vip = 4
t_vip = 0
lambda_oth = 1
t_oth = 0

t_proc = 1

buf_vip = []
buf_oth = []


query_num_oth = 10000
query_num_vip = int(query_num_oth / 4)
# Расписание получения заявок
vip_times = np.random.exponential(lambda_vip, [1, query_num_vip])
oth_times = np.random.exponential(lambda_oth, [1, query_num_oth])

vip_requests = np.cumsum(vip_times)
oth_requests = np.cumsum(oth_times)

cur_time = 0

i, j = 0, 0
while i < query_num_oth and j < query_num_vip:
    if vip_times[0][i] < oth_times[0][j]:
        i += 1
        buf_vip.append(vip_times[0][i])
        cur_time = vip_times[0][i]
    else:
        j += 1
        buf_oth.append(oth_times[0][j])
        cur_time = oth_times[0][j]

# [1 2 3]
# [1 1 2]