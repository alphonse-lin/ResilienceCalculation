from pypims import flood
import os
import time

def timeCount(calcMode, t_start):
    t_end = time.time()
    final_time = round((t_end - t_start), 4)
    print("{0}: {1} s".format(calcMode, final_time))

if __name__=='__main__':

    t_start = time.time()

    ngpus = 1
    case_folder = os.path.join(os.getcwd(), 'hipims_case')
    print(case_folder)

    if ngpus > 1:
        flood.run_mgpus(case_folder)
    else:
        flood.run(case_folder)

    print('finished')
    timeCount('', t_start)