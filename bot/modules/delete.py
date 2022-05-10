from threading import Thread
from telegram import Update
from telegram.ext import CommandHandler

from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils import gdriveTools
from bot.helper.ext_utils.bot_utils import is_gdrive_link


def deletefile(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
    elif reply_to is not None:
        link = reply_to.text
    else:
        link = ''
    if is_gdrive_link(link):
        LOGGER.info(link)
        drive = gdriveTools.GoogleDriveHelper()
        msg = drive.deletefile(link)
    else:
        msg = '𝐒𝐞𝐧𝐝 𝐆𝐝𝐫𝐢𝐯𝐞 𝐥𝐢𝐧𝐤 𝐚𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐨𝐫 𝐛𝐲 𝐫𝐞𝐩𝐥𝐲𝐢𝐧𝐠 𝐭𝐨 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐛𝐲 𝐜𝐨𝐦𝐦𝐚𝐧𝐝'
    reply_message = sendMessage(msg, context.bot, update.message)
    Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()

delete_handler = CommandHandler(command=BotCommands.DeleteCommand, callback=deletefile, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
dispatcher.add_handler(delete_handler)
