import math
import socket
import argparse
from mpi4py import MPI
from utils import read_shot_file, get_signal, get_image


def main():
    parser = argparse.ArgumentParser(prog='PyUDA Ramp test')
    parser.add_argument('-s', '--shot_file',
                    help='Shot file')
    parser.add_argument('-n', '--name',
                    help='Signal name')
    parser.add_argument('-e', '--epochs',
                    help='Number of epochs')
    parser.add_argument('-i', '--image', action='store_true',
                    help='Use images')

    args = parser.parse_args()
    shots = read_shot_file(args.shot_file)

    comm = MPI.COMM_WORLD
    world_rank = comm.Get_rank()
    world_size = comm.Get_size()

    n = len(shots)
    n_per_rank = math.ceil(n / world_size)
    start_index = n_per_rank * world_rank
    print("Rank", world_rank, "Size", world_size, "Host", socket.gethostname())

    epochs  = int(args.epochs)
    for i in range(epochs):
        for shot in shots[start_index:start_index+n_per_rank]:
            print(f"Submitting jobs {shot} on rank {world_rank}")
            if args.image:
                output = get_image(shot, args.name)
            else:
                output = get_signal(shot, args.name)

            print(f"Output '{output}' on rank {world_rank}")



if __name__ == "__main__":
    main()