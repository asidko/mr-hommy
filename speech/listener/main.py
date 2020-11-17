import json
from speech_recognition import Microphone, Recognizer
from urllib.request import Request, urlopen

VOSK_API_URL = 'http://127.0.0.1:8086'
MICROPHONE_DEVICE_INDEX = -1
SAMPLE_RATE = 16000
PHRASE_TIME_LIMIT_SEC = 20

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

        if r is not None:
            print('Initialization')

        r = Recognizer()

        with Microphone(MICROPHONE_DEVICE_INDEX, sample_rate=SAMPLE_RATE) as source:
            print('Adjusting for noise')
            r.adjust_for_ambient_noise(source)

            print('Recording')
            audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT_SEC if PHRASE_TIME_LIMIT_SEC else None)

        print('Recognition')
        data = audio.get_raw_data(SAMPLE_RATE, 2)
        print(' {}'.format(pretty_size(len(data))), end='\r', flush=True)
        text = stt(data, VOSK_API_URL)

        print('Result: {}'.format(text))


if __name__ == '__main__':
    try:
        listener()
    except Exception as e:
        print('Error occured.')
        raise
