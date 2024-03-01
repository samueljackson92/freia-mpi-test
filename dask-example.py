import math
import socket
import argparse
from dask_mpi import initialize
from dask.distributed import Client, as_completed
from utils import read_shot_file, get_signal, get_image


def main():
    initialize()

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

    client = Client() 

    epochs  = int(args.epochs)
    for i in range(epochs):
        tasks = []
        for shot in shots:
            print(f"Submitting jobs {shot}")
            if args.image:
                task = client.submit(get_image, shot, args.name)
            else:
                task = client.submit(get_signal, shot, args.name)
            tasks.append(task)

        for task in as_completed(tasks):
            output = task.result()
            print(f"Output '{output}'")


if __name__ == "__main__":
    main()