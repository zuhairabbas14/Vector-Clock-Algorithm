from multiprocessing import Process, Pipe


def give_vector(vec):
    return '{}'.format(vec)


def recalculate_vector(recv, vector):
    for i in range(len(vector)):
        vector[i] = max(recv[i], vector[i])
    return vector


def event(pid, vector, last=False, p_name=''):
    vector[pid] += 1
    if last:
        print('Process ' + p_name + ' ' + give_vector(vector))
    return vector


def send_message(pipe, pid, vector, last=False, p_name=''):
    vector[pid] += 1
    pipe.send(('Empty shell', vector))
    if last:
        print('Process ' + p_name + ' ' + give_vector(vector))
    return vector


def recv_message(pipe, pid, vector, last=False, p_name=''):
    vector[pid] += 1
    message, timestamp = pipe.recv()
    vector = recalculate_vector(timestamp, vector)
    if last:
        print('Process ' + p_name + ' ' + give_vector(vector))
    return vector


def process_first(pipe12):
    p_name = 'a'
    pid = 0
    vector = [0, 0, 0]
    vector = send_message(pipe12, pid, vector)
    vector = send_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector, True, p_name)


def process_second(pipe21, pipe23):
    p_name = 'b'
    pid = 1
    vector = [0, 0, 0]
    vector = recv_message(pipe21, pid, vector)
    vector = recv_message(pipe21, pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = recv_message(pipe23, pid, vector)
    vector = event(pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = send_message(pipe23, pid, vector)
    vector = send_message(pipe23, pid, vector, True, p_name)


def process_third(pipe32):
    p_name = 'c'
    pid = 2
    vector = [0, 0, 0]
    vector = send_message(pipe32, pid, vector)
    vector = recv_message(pipe32, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe32, pid, vector, True, p_name)


if __name__ == '__main__':

    firstAndSecond, secondAndFirst = Pipe()
    secondAndThird, thirdAndSecond = Pipe()

    process_a = Process(target=process_first, args=(firstAndSecond,))
    process_b = Process(target=process_second, args=(secondAndFirst, secondAndThird))
    process_c = Process(target=process_third, args=(thirdAndSecond,))

    process_a.start()
    process_b.start()
    process_c.start()

    process_a.join()
    process_b.join()
    process_c.join()