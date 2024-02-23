import math
from mpi4py import MPI

import argparse
import pyuda

class MASTClient:
    def __init__(self) -> None:
        pass

    def _get_client(self):
        client = pyuda.Client()
        client.set_property("get_meta", True)
        client.set_property("timeout", 10)
        return client

    def get_signal(self, shot_num: int, name: str):
        client = self._get_client()
        signal_name = name[:23]
        signal = client.get(signal_name, shot_num)
        # self.reset_connection(client)
        return signal

    def _get_image(self, shot_num: int, name: str):
        client = self._get_client()
        image = client.get_images(name, shot_num)
        return image

    def reset_connection(self, client):
        client.set_property("timeout", 0)
        try:
            _ = client.get('help::ping()','')
        except pyuda.UDAException:
            pass

        client.set_property("timeout", 10)
        client.get('help::ping()','')

def _get_image(shot: int, name: str) -> str:
    mast_client = MASTClient()
    try:
        signal = mast_client._get_image(shot, name)
        return 'hello world' + str(shot)
    except Exception as e:
        return str(e)

def get_signal(shot: int, name: str) -> str:
    mast_client = MASTClient()
    try:
        signal = mast_client.get_signal(shot, name)
        # x = signal.data
        # t = signal.time
        return 'hello world' +  str(shot)
    except Exception as e:
        return str(e)


def read_shot_file(shot_file: str) -> list[int]:
    with open(shot_file) as f:
        shot_nums = f.readlines()[1:]
        shot_nums = map(lambda x: x.strip(), shot_nums)
        shot_nums = list(sorted(map(int, shot_nums)))
    return shot_nums


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

    epochs  = int(args.epochs)
    for i in range(epochs):
        for shot in shots[start_index:start_index+n_per_rank]:
            print(f"Submitting jobs {shot} on rank {world_rank}")
            if args.image:
                output = _get_image(shot, args.name)
            else:
                output = get_signal(shot, args.name)

            print(f"Output '{output}' on rank {world_rank}")



if __name__ == "__main__":
    main()