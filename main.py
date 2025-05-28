from g4f.client import Client
from aiogram.types import Message
g4f_client = Client()

async def generate_image(message: Message, prompt: str):
    """
    Генерация изображения: сначала через DALL-E, при ошибке — через Flux (flux-def).
    """
    generating_message = None

    try:
        generating_message = await message.answer("⏳ Создание изображения (DALL-E)...")
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
        try:
            generating_message = await message.answer("⏳ Создание изображения (Flux)...")
            response = g4f_client.images.generate(
                model="flux-def",
                prompt=prompt,
                response_format="url"
            )
            image_url = response.data[0].url
            if generating_message:
                await generating_message.delete()
            await message.answer_photo(image_url)
        except Exception as e2:
            await message.answer("⚠️ Произошла ошибка при генерации изображения. Попробуйте снова.")

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

async def recognize_text_from_voice(audio_url: str) -> str:
    """
    Распознаёт текст из голосового сообщения (аудио) через OpenAI (g4f).
    """
    try:
        response = g4f_client.audio.transcribe(
            model="whisper-1",
            audio=audio_url,
        )
        return response.text
    except Exception as e:
        return f"Ошибка распознавания речи: {e}"

