from telegram import __version__ as TG_VER
from santa import Santa
import secret
from status import Status
import time
from random import randint


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# class with the stuff
santa = Santa()
status = Status()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def stop_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if status.running:
        status.stop()

        await update.message.reply_text("Pausa, se avete bisogno chiedete a Matteo")
    else:
        await update.message.reply_text("Ragazzi sto facendo pausa, avete Matteo a cui chiedere")

async def start_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not status.running:
        status.restart()

        await update.message.reply_text("Sono tornato! Dove sono gli HPPS?")
    else:
        await update.message.reply_text("Sto parlando, non interrompere")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = status.get_status()

    text = f"Santa in questo momento e' {'in ascolto' if res[0] else 'in pausa'}\n"
    text += f"Santa è arrivato alle {time.ctime(res[1])}\n"

    if res[2]:
        text += f"E ha fatto pausa alle {time.ctime(res[2])}\n"

    if res[3]:
        text += f"E' tornato alle {time.ctime(res[3])}"

    await update.message.reply_text(text)

async def probability_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) >= 1:
        try:
            probability = int(context.args[0])

            if probability >= 0 and probability <= 100:
                santa.set_probability(probability)
                await update.message.reply_text(f"Probabilita' impostata a {probability}")
            else:  
                await update.message.reply_text("La probabilita' deve essere un numero tra 0 e 100")
            
        except ValueError:
            await update.message.reply_text("Non mi sembra un numero")
    else:  
        await update.message.reply_text("Mi serve un numero")

    return

async def text_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    for trigger in Santa.TRIGGERS:
        if trigger in msg:
            await update.message.reply_text(santa.prep_reply())
            return 

    found = santa.santa_egg(msg, bold=True)

    if found: 
        await update.message.reply_text(f"`{found}`, eccoti una citazione `{santa.get_citation()}`", parse_mode='HTML')

async def image_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    await update.message.reply_photo(photo=open('meme/meme_001.jpeg', 'rb'))

    return

async def audio_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    # await update.message.reply_audio(document=open('audio/1.wav', 'rb'))
    await update.message.reply_text("A breve questo messaggio sara' un audio")
    return

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not status.running:
        return 
    
    msg = update.message.text.lower()

    # since santa_bot is a good guy  he always replies to greetings
    for trigger in Santa.GREATINGS:
        if trigger in msg:
            await update.message.reply_text(f"{trigger} {santa.get_rand_name()}!")
            return
    
    # the same goes when addressed directly
    if "non mi chiamo" in msg:
        names = santa.game_name()
        await update.message.reply_text(f"{names[0]}?")

        for name in names[1:-2]:
            await update.message.reply_text(f"{name}?")

        await update.message.reply_text(f"Sarai {names[-1]}")

        return

    # probabilistic reply from here
    if randint(0, 100) > santa.response_probability:
        return
    reply_mode = randint(0, 2)

    if reply_mode == 0:
        await text_reply(update, context, msg)
    elif reply_mode == 1:
        await image_reply(update, context, msg)
    else:
        await audio_reply(update, context, msg)


def main() -> None:
    application = Application.builder().token(secret.TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("stop", stop_toggle))
    application.add_handler(CommandHandler("start", start_toggle))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("probability", probability_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()