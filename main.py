from dask_mpi import initialize
initialize()

import argparse
import pyuda
from dask.distributed import Client, as_completed


class MASTClient:
    def __init__(self) -> None:
        pass

    def _get_client(self):
        import pyuda

        client = pyuda.Client()
        client.set_property("get_meta", True)
        client.set_property("timeout", 10)
        return client

    def get_signal(self, shot_num: int, name: str) -> pyuda.Signal:
        client = self._get_client()
        signal_name = name[:23]
        signal = client.get(signal_name, shot_num)
        return signal


def get_signal(shot: int, name: str) -> str:
    mast_client = MASTClient()
    signal = mast_client.get_signal(shot, name)
    return signal.name

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

    args = parser.parse_args()
    shots = read_shot_file(args.shot_file)

    client = Client()

    tasks = []
    for shot in shots:
        print(f"Submitting jobs {shot}")
        task = client.submit(get_signal, shot, args.name)

    for task in as_completed(tasks):
        name = task.result()
        print(name)
    

if __name__ == "__main__":
    main()