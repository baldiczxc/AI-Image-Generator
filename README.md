# AI-Image-Generator

## Описание

Этот проект предоставляет функции для генерации изображений и видео, распознавания текста на изображениях и аудио, а также для удаления фона с изображений с помощью различных AI-сервисов (OpenAI, HuggingFace и др.). Для удаления фона используется бесплатный сервис HuggingFace Space (akhaliq/remove-bg), не требующий ключа.

## Возможности

- Генерация изображений по текстовому описанию (DALL-E, Flux)
- Генерация видео по тексту (HuggingFace Lightricks/LTX-Video)
- Распознавание текста на изображениях (OpenAI Vision, g4f)
- Распознавание речи с аудиофайлов (OpenAI Whisper)
- Удаление фона с изображений 

## Установка

Установите зависимости:
    Минимальные зависимости:
    - openai
    - requests
    - huggingface_hub
    - aiogram
    - g4f

## Получение API-ключей

- **HuggingFace:** https://huggingface.co/settings/tokens  
  Создайте токен и используйте его как `hf_api_key`.
- **OpenAI:** https://platform.openai.com/api-keys  
  Создайте токен и используйте его как `openai.api_key`.


## Примеры использования

### Генерация изображения

```python
await generate_image(message, "A cat in a space suit")
```

### Генерация видео по тексту

```python
video_bytes = await generate_video_from_text("A young man walking on the street", hf_api_key="ВАШ_HF_API_KEY")
with open("result.mp4", "wb") as f:
    f.write(video_bytes)
```

### Распознавание текста на изображении

```python
text = await recognize_text_from_image_openai("path/to/image.png")
print(text)
```

### Распознавание речи с аудио

```python
text = await recognize_text_from_voice("path/to/audio.mp3")
print(text)
```

### Удаление фона с изображения

```python
result_bytes = await remove_background_from_image("path/to/image.png")
with open("no_bg.png", "wb") as f:
    f.write(result_bytes)
```

## Важно

- Для работы с HuggingFace InferenceClient и некоторыми моделями может потребоваться платная подписка или специальные права доступа.
- Для OpenAI также необходим действующий API-ключ.
- Для удаления фона с изображений ключ не требуется, используется бесплатный сервис HuggingFace Space.
-ссылка на репозиторий g4f: [text](https://github.com/xtekky/gpt4free)
