from dataclasses import dataclass
from typing import List, TypedDict


@dataclass
class Notification(TypedDict):
    """Class to hold notification details - what to say and when."""
    time: str
    texts: List[str]
    lang: str


@dataclass
class Configuration(TypedDict):
    notifications: List[Notification]


config_default: Configuration = {
    'notifications': [
        Notification(
            time='07:00', lang='uk',
            texts=[
                'Доброго ранку. Уже шоста година. Пора прокидатися.',
                'Шоста година ранку. Прокидайтесь і радійте новому дню',
            ],
        ),
        Notification(
            time='12:00', lang='uk',
            texts=['Дванадцять годин дня. Полудень', 'Уже дванадцята година. Пів дня позаду.'],
        ),
        Notification(
            time='14:00', lang='uk',
            texts=['Чотирнадцята година. Пора обідати'],
        ),
        Notification(
            time='22:00', lang='uk',
            texts=['Вже пізно. Готуємось лягати спати.', "Двадцять друга година. Відбій!"],
        ),
    ]
}
