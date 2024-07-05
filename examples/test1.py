from mpi4py import MPI
import numpy as np


def communication(variable_to_share):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print("process = %d" % rank + " variable shared  = %d " % variable_to_share)
    data = range(16)
    send_data = np.array(data[rank * 4 : rank * 4 + 4], dtype="i")
    recv_data = np.empty((2, 4), dtype="i")
    req = []
    for i in range(size):
        if i != rank:
            comm.Isend(
                np.array(data[rank * 4 : rank * 4 + 4], dtype="i")[i : i + 1], dest=i
            )
    for i in range(size):
        if i != rank:
            req.append(comm.Irecv(recv_data[0][i : i + 1], i))
        else:
            recv_data[0][i : i + 1] = send_data[i : i + 1]
    for i in req:
        i.Wait()
    print(rank)
    print(recv_data)


def divide():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        print("start")
        variable_to_share = 100
    else:
        variable_to_share = None
    variable_to_share = comm.bcast(variable_to_share, root=0)
    return variable_to_share
