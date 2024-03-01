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

    def get_image(self, shot_num: int, name: str):
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

def get_image(shot: int, name: str) -> str:
    mast_client = MASTClient()
    try:
        signal = mast_client._get_image(shot, name)
        return 'Got image for shot number ' + str(shot)
    except Exception as e:
        return str(e)

def get_signal(shot: int, name: str) -> str:
    mast_client = MASTClient()
    try:
        signal = mast_client.get_signal(shot, name)
        # x = signal.data
        # t = signal.time
        return 'Got signal for shot number ' +  str(shot)
    except Exception as e:
        return str(e)


def read_shot_file(shot_file: str) -> list[int]:
    with open(shot_file) as f:
        shot_nums = f.readlines()[1:]
        shot_nums = map(lambda x: x.strip(), shot_nums)
        shot_nums = list(sorted(map(int, shot_nums)))
    return shot_nums