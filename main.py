from g4f.client import Client
from aiogram.types import Message
import openai

g4f_client = Client()
openai.api_key = "YOUR_OPENAI_API_KEY"  # Замените на ваш ключ

async def generate_image(message: Message, prompt: str):
    """
    Генерация изображения: сначала через DALL-E, при ошибке — через Flux (flux-def).
    """
    generating_message = None

    try:
        # Пробуем сгенерировать через DALL-E
        response = g4f_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            response_format="url",
        )
        image_url = response.data[0].url
        if generating_message:
            await generating_message.delete()
        await message.answer_photo(image_url)
    except Exception as e:
        response = g4f_client.images.generate(
            model="flux-def",
            prompt=prompt,
            response_format="url"
        )
        image_url = response.data[0].url
        if generating_message:
            await generating_message.delete()
        await message.answer_photo(image_url)

async def recognize_text_from_image(image_url: str) -> str:
    """
    Распознаёт текст на изображении через OpenAI (g4f).
    """
    try:
        response = g4f_client.images.ocr(
            model="openai-ocr",  
            image=image_url,
        )
        # Предполагается, что результат содержит поле 'text'
        return response.text
    except Exception as e:
        return f"Ошибка распознавания текста: {e}"

async def recognize_text_from_voice(audio_path: str) -> str:
    """
    Распознаёт текст из голосового сообщения (аудио) через OpenAI API (Whisper).
    """
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript
    except Exception as e:
        return f"Ошибка распознавания речи: {e}"

async def recognize_text_from_image_openai(image_path: str) -> str:
    """
    Распознаёт текст на изображении через OpenAI Vision API.
    """
    try:
        with open(image_path, "rb") as image_file:
            response = openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Извлеки весь текст с этого изображения."},
                            {"type": "image_url", "image_url": {"url": "attachment://image.png"}}
                        ]
                    }
                ],
                files=[{"name": "image.png", "file": image_file}],
                max_tokens=300
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка распознавания текста с фото: {e}"

