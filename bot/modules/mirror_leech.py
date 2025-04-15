from aiofiles.os import path as aiopath
from base64 import b64encode
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from re import match as re_match
from os import environ
from requests import get as rget
import json
from motor.motor_asyncio import AsyncIOMotorClient

from bot import bot, DOWNLOAD_DIR, LOGGER, bot_loop, task_dict_lock
from ..helper.ext_utils.bot_utils import (
    get_content_type,
    sync_to_async,
    arg_parser,
    COMMAND_USAGE,
)
from ..helper.ext_utils.exceptions import DirectDownloadLinkException
from ..helper.ext_utils.links_utils import (
    is_url,
    is_magnet,
    is_gdrive_link,
    is_rclone_path,
    is_telegram_link,
    is_gdrive_id,
)
from ..helper.listeners.task_listener import TaskListener
from ..helper.mirror_leech_utils.download_utils.aria2_download import (
    add_aria2c_download,
)
from ..helper.mirror_leech_utils.download_utils.direct_downloader import (
    add_direct_download,
)
from ..helper.mirror_leech_utils.download_utils.direct_link_generator import (
    direct_link_generator,
)
from ..helper.mirror_leech_utils.download_utils.gd_download import add_gd_download
from ..helper.mirror_leech_utils.download_utils.jd_download import add_jd_download
from ..helper.mirror_leech_utils.download_utils.qbit_download import add_qb_torrent
from ..helper.mirror_leech_utils.download_utils.nzb_downloader import add_nzb
from ..helper.mirror_leech_utils.download_utils.rclone_download import (
    add_rclone_download,
)
from ..helper.mirror_leech_utils.download_utils.telegram_download import (
    TelegramDownloadHelper,
)
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.message_utils import send_message, get_tg_link_message

# MongoDB constants
MONGO_URI = 'mongodb+srv://nhnobnd:Dunghoi1@cluster0.uha2oe3.mongodb.net/'
DB_NAME = 'magnet-db'
COLLECTION_NAME = 'magnets'

class Mirror(TaskListener):
    def __init__(
        self,
        client,
        message,
        is_qbit=False,
        is_leech=False,
        is_jd=False,
        is_nzb=False,
        same_dir=None,
        bulk=None,
        multi_tag=None,
        options="",
    ):
        if same_dir is None:
            same_dir = {}
        if bulk is None:
            bulk = []
        self.message = message
        self.client = client
        self.multi_tag = multi_tag
        self.options = options
        self.same_dir = same_dir
        self.bulk = bulk
        super().__init__()
        self.is_qbit = is_qbit
        self.is_leech = is_leech
        self.is_jd = is_jd
        self.is_nzb = is_nzb
        
    async def check_magnet_in_db(self, magnet_link):
        try:
            mongo_client = AsyncIOMotorClient(MONGO_URI)
            db = mongo_client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            # Check if magnet link exists in database
            result = await collection.find_one({"url": magnet_link})
            return result is not None
        except Exception as e:
            LOGGER.error(f"Error checking magnet in database: {e}")
            return False
        finally:
            if 'mongo_client' in locals():
                mongo_client.close()
                
    async def save_magnet_to_db(self, magnet_link):
        try:
            mongo_client = AsyncIOMotorClient(MONGO_URI)
            db = mongo_client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            # Get current date
            from datetime import datetime
            current_date = datetime.now()
            
            # Create document to save
            document = {
                "url": magnet_link,
                "code": magnet_link,
                "source": "mirror_leech",
                "date": current_date.strftime("%Y-%m-%d"),
                "created_at": current_date
            }
            
            # Insert document into collection
            await collection.insert_one(document)
            LOGGER.info(f"Saved magnet to database: {magnet_link}")
            
        except Exception as e:
            LOGGER.error(f"Error saving magnet to database: {e}")
        finally:
            if 'mongo_client' in locals():
                mongo_client.close()

    async def new_event(self):
        text = self.message.text.split("\n")
        input_list = text[0].split(" ")

        args = {
            "-doc": False,
            "-med": False,
            "-d": False,
            "-j": False,
            "-s": False,
            "-b": False,
            "-e": False,
            "-z": False,
            "-sv": False,
            "-ss": False,
            "-f": False,
            "-fd": False,
            "-fu": False,
            "-ml": False,
            "-i": 0,
            "-sp": 0,
            "link": "",
            "-n": "",
            "-m": "",
            "-up": "",
            "-rcf": "",
            "-au": "",
            "-ap": "",
            "-h": "",
            "-t": "",
            "-ca": "",
            "-cv": "",
            "-ns": "",
            "-tl": "",
        }

        arg_parser(input_list[1:], args)

        self.select = args["-s"]
        self.seed = args["-d"]
        self.name = args["-n"]
        self.up_dest = args["-up"]
        self.rc_flags = args["-rcf"]
        self.link = args["link"]
        self.compress = args["-z"]
        self.extract = args["-e"]
        self.join = args["-j"]
        self.thumb = args["-t"]
        self.split_size = args["-sp"]
        self.screen_shots = args["-ss"]
        self.force_run = args["-f"]
        self.force_download = args["-fd"]
        self.force_upload = args["-fu"]
        self.convert_audio = args["-ca"]
        self.convert_video = args["-cv"]
        self.name_sub = args["-ns"]
        self.mixed_leech = args["-ml"]
        self.thumbnail_layout = args["-tl"]
        self.as_doc = args["-doc"]
        self.as_med = args["-med"]
        self.folder_name = f"/{args["-m"]}" if len(args["-m"]) > 0 else ""

        headers = args["-h"]
        is_bulk = args["-b"]

        bulk_start = 0
        bulk_end = 0
        ratio = None
        seed_time = None
        reply_to = None
        file_ = None
        session = ""
        arrayLink = []
        URL_MAGNET = environ.get('URL_MAGNET', '')

        if ",j" in self.link:
            dataTorrent = rget(f'{URL_MAGNET}special/?date={self.link}')
            arrayLink = json.loads(dataTorrent.content)
        
        if ",f" in self.link:
            dataTorrent = rget(f'{URL_MAGNET}special/?date={self.link}')
            arrayLink = json.loads(dataTorrent.content)

        if ",t" in self.link:
            dataTorrent = rget(f'{URL_MAGNET}special/?date={self.link}')
            arrayLink = json.loads(dataTorrent.content)

        LOGGER.info(f'zoday 2 {arrayLink}')
        
        for currentLink in arrayLink:
            await send_message(self.message, currentLink)

        try:
            self.multi = int(args["-i"])
        except:
            self.multi = 0

        if not isinstance(self.seed, bool):
            dargs = self.seed.split(":")
            ratio = dargs[0] or None
            if len(dargs) == 2:
                seed_time = dargs[1] or None
            self.seed = True

        if not isinstance(is_bulk, bool):
            dargs = is_bulk.split(":")
            bulk_start = dargs[0] or 0
            if len(dargs) == 2:
                bulk_end = dargs[1] or 0
            is_bulk = True

        if not is_bulk:
            if self.multi > 0:
                if self.folder_name:
                    self.seed = False
                    ratio = None
                    seed_time = None
                    async with task_dict_lock:
                        if self.folder_name in self.same_dir:
                            self.same_dir[self.folder_name]["tasks"].add(self.mid)
                            for fd_name in self.same_dir:
                                if fd_name != self.folder_name:
                                    self.same_dir[fd_name]["total"] -= 1
                        elif self.same_dir:
                            self.same_dir[self.folder_name] = {"total": self.multi, "tasks": {self.mid}}
                            for fd_name in self.same_dir:
                                if fd_name != self.folder_name:
                                    self.same_dir[fd_name]["total"] -= 1
                        else:
                            self.same_dir = {self.folder_name: {"total": self.multi, "tasks": {self.mid}}}
                elif self.same_dir:
                    async with task_dict_lock:
                        for fd_name in self.same_dir:
                            self.same_dir[fd_name]["total"] -= 1
        else:
            await self.init_bulk(input_list, bulk_start, bulk_end, Mirror)
            return

        if len(self.bulk) != 0:
            del self.bulk[0]

        await self.run_multi(input_list, Mirror)

        await self.get_tag(text)

        path = f"{DOWNLOAD_DIR}{self.mid}{self.folder_name}"

        if not self.link and (reply_to := self.message.reply_to_message):
            if reply_to.text:
                self.link = reply_to.text.split("\n", 1)[0].strip()
        if is_telegram_link(self.link):
            try:
                reply_to, session = await get_tg_link_message(self.link)
            except Exception as e:
                await send_message(self.message, f"ERROR: {e}")
                await self.remove_from_same_dir()
                return

        if isinstance(reply_to, list):
            self.bulk = reply_to
            b_msg = input_list[:1]
            self.options = " ".join(input_list[1:])
            b_msg.append(f"{self.bulk[0]} -i {len(self.bulk)} {self.options}")
            nextmsg = await send_message(self.message, " ".join(b_msg))
            nextmsg = await self.client.get_messages(
                chat_id=self.message.chat.id, message_ids=nextmsg.id
            )
            if self.message.from_user:
                nextmsg.from_user = self.user
            else:
                nextmsg.sender_chat = self.user
            await Mirror(
                self.client,
                nextmsg,
                self.is_qbit,
                self.is_leech,
                self.is_jd,
                self.is_nzb,
                self.same_dir,
                self.bulk,
                self.multi_tag,
                self.options,
            ).new_event()
            return

        if reply_to:
            file_ = (
                reply_to.document
                or reply_to.photo
                or reply_to.video
                or reply_to.audio
                or reply_to.voice
                or reply_to.video_note
                or reply_to.sticker
                or reply_to.animation
                or None
            )

            if file_ is None:
                if reply_text := reply_to.text:
                    self.link = reply_text.split("\n", 1)[0].strip()
                else:
                    reply_to = None
            elif reply_to.document and (
                file_.mime_type == "application/x-bittorrent"
                or file_.file_name.endswith((".torrent", ".dlc", ".nzb"))
            ):
                self.link = await reply_to.download()
                file_ = None

        if (
            not self.link
            and file_ is None
            or is_telegram_link(self.link)
            and reply_to is None
            or file_ is None
            and not is_url(self.link)
            and not is_magnet(self.link)
            and not await aiopath.exists(self.link)
            and not is_rclone_path(self.link)
            and not is_gdrive_id(self.link)
            and not is_gdrive_link(self.link)
        ):
            await send_message(
                self.message, COMMAND_USAGE["mirror"][0], COMMAND_USAGE["mirror"][1]
            )
            await self.remove_from_same_dir()
            return

        if len(self.link) > 0:
            LOGGER.info(self.link)

        # Check if link is a magnet link and exists in database
        if is_magnet(self.link) and await self.check_magnet_in_db(self.link):
            await send_message(self.message, "Magnet link đã tồn tại trong database. Không cần mirror/leech lại.")
            await self.remove_from_same_dir()
            return

        try:
            await self.before_start()
        except Exception as e:
            await send_message(self.message, e)
            await self.remove_from_same_dir()
            return

        if (
            not self.is_jd
            and not self.is_nzb
            and not self.is_qbit
            and not is_magnet(self.link)
            and not is_rclone_path(self.link)
            and not is_gdrive_link(self.link)
            and not self.link.endswith(".torrent")
            and file_ is None
            and not is_gdrive_id(self.link)
        ):
            content_type = await get_content_type(self.link)
            if content_type is None or re_match(r"text/html|text/plain", content_type):
                try:
                    self.link = await sync_to_async(direct_link_generator, self.link)
                    if isinstance(self.link, tuple):
                        self.link, headers = self.link
                    elif isinstance(self.link, str):
                        LOGGER.info(f"Generated link: {self.link}")
                except DirectDownloadLinkException as e:
                    e = str(e)
                    if "This link requires a password!" not in e:
                        LOGGER.info(e)
                    if e.startswith("ERROR:"):
                        await send_message(self.message, e)
                        await self.remove_from_same_dir()
                        return

        if self.is_jd:
            await add_jd_download(self, path, headers)
        elif self.is_nzb:
            await add_nzb(self)
        elif self.is_qbit and (
            is_magnet(self.link) or self.link.endswith(".torrent")
        ):
            await add_qb_torrent(self, path, ratio, seed_time)
        elif is_magnet(self.link) or self.link.endswith(".torrent"):
            await add_aria2c_download(self, path, headers, ratio, seed_time)
        elif is_rclone_path(self.link):
            await add_rclone_download(self, path)
        elif is_gdrive_link(self.link) or is_gdrive_id(self.link):
            await add_gd_download(self, path)
        elif file_:
            await TelegramDownloadHelper(self).download(reply_to, path)
        else:
            await add_direct_download(self, path, headers)
            
        # Save magnet to database if task was successful
        if is_magnet(self.link) and self.mid in task_dict:
            await self.save_magnet_to_db(self.link)


async def mirror(client, message):
    bot_loop.create_task(Mirror(client, message).new_event())


async def qb_mirror(client, message):
    bot_loop.create_task(Mirror(client, message, is_qbit=True).new_event())


async def jd_mirror(client, message):
    bot_loop.create_task(Mirror(client, message, is_jd=True).new_event())


async def nzb_mirror(client, message):
    bot_loop.create_task(Mirror(client, message, is_nzb=True).new_event())


async def leech(client, message):
    bot_loop.create_task(Mirror(client, message, is_leech=True).new_event())


async def qb_leech(client, message):
    bot_loop.create_task(
        Mirror(client, message, is_qbit=True, is_leech=True).new_event()
    )


async def jd_leech(client, message):
    bot_loop.create_task(Mirror(client, message, is_leech=True, is_jd=True).new_event())


async def nzb_leech(client, message):
    bot_loop.create_task(
        Mirror(client, message, is_leech=True, is_nzb=True).new_event()
    )


bot.add_handler(
    MessageHandler(
        mirror,
        filters=command(BotCommands.MirrorCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        qb_mirror,
        filters=command(BotCommands.QbMirrorCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        jd_mirror,
        filters=command(BotCommands.JdMirrorCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        nzb_mirror,
        filters=command(BotCommands.NzbMirrorCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        leech,
        filters=command(BotCommands.LeechCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        qb_leech,
        filters=command(BotCommands.QbLeechCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        jd_leech,
        filters=command(BotCommands.JdLeechCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(
    MessageHandler(
        nzb_leech,
        filters=command(BotCommands.NzbLeechCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
