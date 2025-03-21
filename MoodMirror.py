# █████   █████                   █████      ██████████                                                                █████     
#░░███   ░░███                   ░░███      ░░███░░░░███                                                              ░░███      
# ░███    ░███   ██████   ██████  ░███ █████ ░███   ░░███  ██████  █████ █████             ██████   ████████   ██████  ░███████  
# ░███████████  ███░░███ ███░░███ ░███░░███  ░███    ░███ ███░░███░░███ ░░███  ██████████ ░░░░░███ ░░███░░███ ███░░███ ░███░░███ 
# ░███░░░░░███ ░███ ░███░███ ░███ ░██████░   ░███    ░███░███████  ░███  ░███ ░░░░░░░░░░   ███████  ░███ ░░░ ░███ ░░░  ░███ ░███ 
# ░███    ░███ ░███ ░███░███ ░███ ░███░░███  ░███    ███ ░███░░░   ░░███ ███              ███░░███  ░███     ░███  ███ ░███ ░███ 
# █████   █████░░██████ ░░██████  ████ █████ ██████████  ░░██████   ░░█████              ░░████████ █████    ░░██████  ████ █████
#░░░░░   ░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░ ░░░░░░░░░░    ░░░░░░     ░░░░░                ░░░░░░░░ ░░░░░      ░░░░░░  ░░░░ ░░░░░                                                                                                                                 
# meta developer: @wiley_station
# meta icon: https://example.com/moodmirror_icon.png
# meta banner: https://example.com/moodmirror_banner.png

import logging
import random
from .. import loader, utils

__version__ = (0, 0, 1)

logger = logging.getLogger(__name__)

@loader.tds
class MoodMirror(loader.Module):
    """Отражает твое настроение через эмодзи и цитаты"""

    strings = {
        "name": "MoodMirror",
        "mood_detected": "🌟 Твое настроение: {mood}\n{emoji} {quote}",
        "no_mood": "🤔 Я пока не понял твоего настроения. Напиши что-нибудь!",
        "mood_reset": "🧹 Анализ настроения сброшен.",
    }

    strings_ru = {
        "name": "MoodMirror",
        "mood_detected": "🌟 Твое настроение: {mood}\n{emoji} {quote}",
        "no_mood": "🤔 Я пока не понял твоего настроения. Напиши что-нибудь!",
        "mood_reset": "🧹 Анализ настроения сброшен.",
    }

    def __init__(self):
        self.mood_history = []
        self.moods = {
            "радость": {
                "words": ["круто", "класс", "здорово", "супер", "рад", "весело", "ура", "отлично", "праздник", "счастье", "позитив", "восторг"],
                "emojis": ["😊", "🎉", "🌞", "✨", "🥳"],
                "quotes": [
                    "Счастье — это когда душа танцует!",
                    "Улыбка — твой лучший аксессуар.",
                    "Жизнь прекрасна, когда ты в деле!",
                    "Свети ярче солнца!"
                ]
            },
            "грусть": {
                "words": ["грустно", "плохо", "жаль", "тоска", "печаль", "слезы", "одиноко", "хреново", "упал", "разбит"],
                "emojis": ["😔", "🌧️", "💧", "🥀", "😢"],
                "quotes": [
                    "Дождь пройдет, и солнце выглянет снова.",
                    "Иногда тишина говорит громче слов.",
                    "Все проходит, и это тоже пройдет.",
                    "Грусть — это тень перед светом."
                ]
            },
            "усталость": {
                "words": ["устал", "выдохся", "спать", "надоело", "лень", "нет сил", "утомился", "выжат", "сонный", "капец"],
                "emojis": ["😴", "🥱", "🛌", "😩", "💤"],
                "quotes": [
                    "Отдых — это тоже искусство.",
                    "Сон — лучший лекарь.",
                    "Пора дать себе передышку.",
                    "Тишина лечит усталость."
                ]
            },
            "злость": {
                "words": ["бесит", "злюсь", "раздражает", "фу", "достали", "нервы", "беда", "злой", "гнев", "взрыв"],
                "emojis": ["😡", "🔥", "💢", "👿", "😤"],
                "quotes": [
                    "Гнев — это ветер, который гасит свечи разума.",
                    "Выдохни и отпусти.",
                    "Ты сильнее своего раздражения.",
                    "Спокойствие — твой щит."
                ]
            },
            "спокойствие": {
                "words": ["спокойно", "тихо", "мир", "релакс", "хорошо", "уют", "гармония", "баланс"],
                "emojis": ["🧘", "🌙", "🌿", "☕", "🌊"],
                "quotes": [
                    "Тишина — это музыка души.",
                    "Спокойствие — сила внутри.",
                    "Мир начинается с тебя.",
                    "Дыши глубже, все в порядке."
                ]
            }
        }

    def analyze_mood(self, text):
        """Анализирует текст и возвращает настроение"""
        text = text.lower()
        for mood, data in self.moods.items():
            if any(word in text for word in data["words"]):
                return mood
        return None

    def get_mood_response(self, mood):
        """Генерирует ответ с эмодзи и цитатой"""
        if mood not in self.moods:
            return None
        data = self.moods[mood]
        emoji = random.choice(data["emojis"])
        quote = random.choice(data["quotes"])
        return {"mood": mood, "emoji": emoji, "quote": quote}

    @loader.watcher("out", only_messages=True)
    async def watcher(self, message):
        """Следит за твоими сообщениями и анализирует настроение"""
        if message.sender_id != (await self._client.get_me()).id:
            return
        mood = self.analyze_mood(message.text)
        if mood:
            self.mood_history.append(mood)
            if len(self.mood_history) > 10:  # Ограничиваем историю
                self.mood_history.pop(0)

    @loader.command(ru_doc="Показать текущее настроение")
    async def mood(self, message):
        """Показывает текущее настроение"""
        if not self.mood_history:
            await utils.answer(message, self.strings["no_mood"])
            return

        # Берем последнее настроение
        latest_mood = self.mood_history[-1]
        response = self.get_mood_response(latest_mood)
        if response:
            await utils.answer(message, self.strings["mood_detected"].format(**response))

    @loader.command(ru_doc="Сбросить анализ настроения")
    async def moodreset(self, message):
        """Сбрасывает историю настроения"""
        self.mood_history = []
        await utils.answer(message, self.strings["mood_reset"])