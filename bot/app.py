async def on_startup(dp):
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('Бот запущен')

if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')))

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
