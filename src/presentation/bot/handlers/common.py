from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router(name="common")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Welcome to the AI Task Management Platform!\n"
        "Send me a text or voice message in Persian, and I will extract the task details and create a ticket directly in Plane."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Commands:\n"
        "/new - Start a new task manually\n\n"
        "You can also just send a voice or text message in Persian to create a task!"
    )
