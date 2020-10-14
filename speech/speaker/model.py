from typing import TypedDict, Dict


class Configuration(TypedDict):
    # voice to speak if not set
    default_voice_name: str
    # lang to voice name map
    voices: Dict[str, str]


config_default: Configuration = {
    'default_voice_name': 'aleksandr',
    'voices': {
        'en': 'alan',
        'ru': 'aleksandr',
        'uk': 'anatol'
    }
}