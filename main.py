from telegram import Bot, File, __version__ as TG_VER
from santa import Santa
import secret
from status import Status
import time
from random import randint
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message)

async def download_image(file: File) -> None:
    await file.download_to_drive(f"meme/{file.file_path.split('/')[-1]}")

    santa.insert_photo(file.file_path.split('/')[-1], file.file_id)

async def download_audio(file: File) -> None:
    await file.download_to_drive(f"audio/{file.file_path.split('/')[-1]}")

    santa.insert_audio(file.file_path.split('/')[-1], file.file_id)

async def insert_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await download_image(await update.message.effective_attachment[-1].get_file())

        await update.message.reply_text("Immagine salvata")
    except:
        await update.message.reply_text("Ho avuto problemi a salvare l'immagine")

async def insert_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:   
        await download_audio( await update.message.effective_attachment.get_file())

        await update.message.reply_text("Audio salvato")
    except:
        await update.message.reply_text("Ho avuto problemi a salvare l'audio")

async def save_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    type = None

    if isinstance(update.message.reply_to_message.effective_attachment, tuple):
        type = "image"
    else :
        type = update.message.reply_to_message.effective_attachment.mime_type.split('/')[0]

    try:
        if type == "image":
            await download_image(await update.message.reply_to_message.effective_attachment[-1].get_file())

            await update.message.reply_text("Immagine salvata")
        elif type == "audio":
            await download_audio(await update.message.reply_to_message.effective_attachment.get_file())

            await update.message.reply_text("Audio salvato")
        else:
            await update.message.reply_text("Non mi sembra un audio o un'immagine")
    except Exception as e:
        print(e)
        await update.message.reply_text("Non mi sembra un audio o un'immagine")

# text replies
async def text_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    await update.message.reply_text(santa.prep_reply())
    
    return

# photo replies
async def image_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    index, photo = santa.get_photo()

    if photo["id"]:
        await update.message.reply_photo(photo=photo["id"])
    else:
        res = await update.message.reply_photo(photo=open(f"meme/{photo['name']}", 'rb'))

        santa.update_photo(index, photo["name"], res.photo[-1].file_id)

    return

# audio replies
async def audio_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str) -> None:
    index, audio = santa.get_audio()

    # with the reply_voice everything is treated as an audio message instead of an audio file
    if audio["id"]:
        await update.message.reply_voice(voice=audio["id"])
    else:
        res = await update.message.reply_voice(voice=open(f"audio/{audio['name']}", 'rb'))

        santa.update_audio(index, audio["name"], res.voice.file_id)
    
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
    
    for trigger in Santa.TRIGGERS:
        if trigger in msg:
            reply_mode = randint(0, 2)

            if reply_mode == 0:
                await text_reply(update, context, msg)
            elif reply_mode == 1:
                await image_reply(update, context, msg)
            else:
                await audio_reply(update, context, msg)

            return

    found = santa.santa_egg(msg, bold=True)

    if found: 
        await update.message.reply_text(f"`{found}`, eccoti una citazione `{santa.get_citation()}`", parse_mode='HTML')


def main() -> None:
    application = Application.builder().token(secret.TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("stop", stop_toggle))
    application.add_handler(CommandHandler("start", start_toggle))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("probability", probability_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, echo))
    application.add_handler(MessageHandler(filters.PHOTO & filters.Caption("/save"), insert_image))
    application.add_handler(MessageHandler(filters.AUDIO & filters.Caption("/save"), insert_audio))
    application.add_handler(MessageHandler(filters.REPLY & filters.Text("/save"), save_reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()