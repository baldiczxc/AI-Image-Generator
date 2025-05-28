from g4f.client import Client
g4f_client = Client()
from aiogram.types import Message


async def generate_image_with_flux_and_send(message: Message, prompt: str):
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
            response_format="url"
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