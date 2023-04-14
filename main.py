from telegram import __version__ as TG_VER
import re
from santa import Santa
import secret


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

def santa_egg(sentence) -> bool:
    return re.search("s.*a.*n.*t.*a", sentence)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text.lower()

    for trigger in Santa.GREATINGS:
        if trigger in msg:
            await update.message.reply_text(f"{update.message.text} {santa.get_rand_name()}!")
            return
        
    if "non mi chiamo" in msg:
        names = santa.game_name()
        res = await update.message.reply_text(f"{names[0]}?")

        for name in names[1:-2]:
            res = await res.reply_text(f"{name}?")

        await res.reply_text(f"Sarai {names[-1]}")

        return

    for trigger in Santa.TRIGGERS:
        if trigger in msg:
            await update.message.reply_text(santa.prep_reply())
            return 

    nominated = santa_egg(msg)

    if nominated: 
        await update.message.reply_text(f"Non lo sapevi ma mi hai nominato `{nominated.group()}`, eccoti una citazione `{santa.get_citation()}`")


def main() -> None:
    application = Application.builder().token(secret.TOKEN).build()

    # on different commands - answer in Telegram
    #application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("quit", stop_toggle))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()