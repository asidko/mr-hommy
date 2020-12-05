import json
from speech_recognition import Microphone, Recognizer
from urllib.request import Request, urlopen
from os import environ

VOSK_API_URL = environ.get('VOSK_API_URL') or 'http://127.0.0.1:8086'
MICROPHONE_DEVICE_INDEX = int(environ.get('MICROPHONE_DEVICE_INDEX'))
MICROPHONE_DEVICE_INDEX = MICROPHONE_DEVICE_INDEX if MICROPHONE_DEVICE_INDEX >= 0 else None
SAMPLE_RATE = int(environ.get('SAMPLE_RATE')) or 16000
PHRASE_TIME_LIMIT_SEC = environ.get('PHRASE_TIME_LIMIT_SEC') or 20

SAMPLE_RATE = int(SAMPLE_RATE)
PHRASE_TIME_LIMIT_SEC = float(PHRASE_TIME_LIMIT_SEC)

def print_device_list():
    print("-------------\nGetting microphone devices...\n-------------")
    microphones = Microphone.list_microphone_names()

    for index, name in enumerate(microphones):
        print("----> Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    
    print("-------------")


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
    while True:

        print('Initialization')

        if r is None:
            print("Use device_index=%s and sample_rate=%s" % (MICROPHONE_DEVICE_INDEX, SAMPLE_RATE))

        r = Recognizer()

        with Microphone(device_index=MICROPHONE_DEVICE_INDEX, sample_rate=SAMPLE_RATE) as source:
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
