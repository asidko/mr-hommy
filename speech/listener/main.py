import json
from os import environ
from urllib.request import Request, urlopen

from speech_recognition import Microphone, Recognizer

VOSK_API_URL = environ.get('VOSK_API_URL') or 'http://127.0.0.1:8086'
SAMPLE_RATE = environ.get('SAMPLE_RATE') or 16000
PHRASE_TIME_LIMIT_SEC = environ.get('PHRASE_TIME_LIMIT_SEC') or 20
MICROPHONE_NAME_FROM_CONFIG = 'mic'

SAMPLE_RATE = int(SAMPLE_RATE)
PHRASE_TIME_LIMIT_SEC = float(PHRASE_TIME_LIMIT_SEC)


def print_device_list():
    print("-------------\nGetting microphone devices...\n-------------")

    for index, name in enumerate(Microphone.list_microphone_names()):
        print("----> Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    print("-------------")


def get_mic_index():
    mic_list = Microphone.list_microphone_names()
    mic_index = next((i for i, name in enumerate(mic_list) if name == MICROPHONE_NAME_FROM_CONFIG), -1)

    if mic_index >= 0:
        return mic_index

    if mic_index < 0:
        print(f'Device with name "{MICROPHONE_NAME_FROM_CONFIG}" was not found. Check settings in asoundrc.conf file')

    print('Try to use first device as microphone. Device name: ' + mic_list[0])

    return 0


def stt(data: bytes, url: str) -> str:
    request = Request('{}/stt'.format(url), data=data, headers={'Content-Type': 'audio/wav'})
    result = json.loads(urlopen(request).read().decode('utf-8'))

    if not ('code' in result and 'text' in result):
        raise RuntimeError('Wrong reply from server: {}'.format(result))

    return result['text'] if not result['code'] else 'Server error: [{code}]: {text}'.format(**result)


def pretty_size(size) -> str:
    ends = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB']
    max_index = len(ends) - 1
    index = 0
    while size >= 1024 and index < max_index:
        size /= 1024.0
        index += 1
    size = int(size) if size % 1 < 0.1 else round(size, 1)
    return '{} {}'.format(size, ends[index])


def listener():
    r = None
    mic_device_index = get_mic_index()

    while True:

        print('Initialization')

        if r is None:
            print("Use device_index=%s and sample_rate=%s" % (mic_device_index, SAMPLE_RATE))

        r = Recognizer()

        with Microphone(device_index=mic_device_index, sample_rate=SAMPLE_RATE) as source:
            print('Adjusting for noise')
            r.adjust_for_ambient_noise(source)

            print('Recording')
            audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT_SEC if PHRASE_TIME_LIMIT_SEC else None)

        print('Recognition')
        data = audio.get_raw_data(SAMPLE_RATE, 2)
        print(' {}'.format(pretty_size(len(data))), end='\r', flush=True)
        text = stt(data, VOSK_API_URL)

        print('Result: ' + text)


if __name__ == '__main__':
    try:
        print_device_list()
        listener()
    except Exception as e:
        print('Error occured.')
        raise
