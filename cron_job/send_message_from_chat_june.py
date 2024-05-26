
import os

from aiogram.types import InputFile, FSInputFile


class MessageScheduler:
    def __init__(self, bot, texts, images_dir, chat_id):
        self.bot = bot
        self.texts = texts
        self.images_dir = images_dir
        self.chat_id = chat_id
        self.index = 0

    async def send_message_with_image(self):
        text = self.texts[self.index]
        image_path = os.path.join(self.images_dir, f"text_{self.index + 1}.jpg")

        photo = FSInputFile(image_path)
        await self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=text)

        # Update message index
        self.index = (self.index + 1) % len(self.texts)
