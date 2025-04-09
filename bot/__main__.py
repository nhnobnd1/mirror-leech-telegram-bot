from aiofiles import open as aiopen
from aiofiles.os import path as aiopath, remove
from asyncio import gather, create_subprocess_exec
from os import execl as osexecl
from psutil import (
    disk_usage,
    cpu_percent,
    swap_memory,
    cpu_count,
    virtual_memory,
    net_io_counters,
    boot_time,
)
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from signal import signal, SIGINT
from sys import executable
from time import time

from bot import (
    bot,
    botStartTime,
    LOGGER,
    intervals,
    config_dict,
    scheduler,
    sabnzbd_client,
)
from .helper.ext_utils.telegraph_helper import telegraph
from .helper.ext_utils.bot_utils import (
    cmd_exec,
    sync_to_async,
    create_help_buttons,
    new_task,
)
from .helper.ext_utils.db_handler import database
from .helper.ext_utils.files_utils import clean_all, exit_clean_up
from .helper.ext_utils.jdownloader_booter import jdownloader
from .helper.ext_utils.status_utils import get_readable_file_size, get_readable_time
from .helper.listeners.aria2_listener import start_aria2_listener
from .helper.mirror_leech_utils.rclone_utils.serve import rclone_serve_booter
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.button_build import ButtonMaker
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.message_utils import send_message, edit_message, send_file
from .modules import (
    authorize,
    cancel_task,
    clone,
    exec,
    file_selector,
    gd_count,
    gd_delete,
    gd_search,
    mirror_leech,
    status,
    ytdlp,
    shell,
    users_settings,
    bot_settings,
    help,
    force_start,
)


@new_task
async def stats(_, message):
    if await aiopath.exists(".git"):
        last_commit = await cmd_exec(
            "git log -1 --date=short --pretty=format:'%cd <b>From</b> %cr'", True
        )
        last_commit = last_commit[0]
    else:
        last_commit = "No UPSTREAM_REPO"
    total, used, free, disk = disk_usage("/")
    swap = swap_memory()
    memory = virtual_memory()
    stats = (
        f"<b>Ngày Commit:</b> {last_commit}\n\n"
        f"<b>Thời gian hoạt động của Bot:</b> {get_readable_time(time() - botStartTime)}\n"
        f"<b>Thời gian hoạt động của hệ điều hành:</b> {get_readable_time(time() - boot_time())}\n\n"
        f"<b>Tổng dung lượng ổ đĩa:</b> {get_readable_file_size(total)}\n"
        f"<b>Đã sử dụng:</b> {get_readable_file_size(used)} | <b>Còn trống:</b> {get_readable_file_size(free)}\n\n"
        f"<b>Tải lên:</b> {get_readable_file_size(net_io_counters().bytes_sent)}\n"
        f"<b>Tải xuống:</b> {get_readable_file_size(net_io_counters().bytes_recv)}\n\n"
        f"<b>CPU:</b> {cpu_percent(interval=0.5)}%\n"
        f"<b>RAM:</b> {memory.percent}%\n"
        f"<b>DISK:</b> {disk}%\n\n"
        f"<b>Nhân vật lý:</b> {cpu_count(logical=False)}\n"
        f"<b>Tổng số nhân:</b> {cpu_count(logical=True)}\n\n"
        f"<b>SWAP:</b> {get_readable_file_size(swap.total)} | <b>Đã sử dụng:</b> {swap.percent}%\n"
        f"<b>Tổng bộ nhớ:</b> {get_readable_file_size(memory.total)}\n"
        f"<b>Bộ nhớ còn trống:</b> {get_readable_file_size(memory.available)}\n"
        f"<b>Bộ nhớ đã sử dụng:</b> {get_readable_file_size(memory.used)}\n"
    )
    await send_message(message, stats)


@new_task
async def start(client, message):
    buttons = ButtonMaker()
    buttons.url_button(
        "Mã nguồn", "https://www.github.com/anasty17/mirror-leech-telegram-bot"
    )
    buttons.url_button("Tác giả mã", "https://t.me/anas_tayyar")
    reply_markup = buttons.build_menu(2)
    if await CustomFilters.authorized(client, message):
        start_string = f"""
Bot này có thể phản chiếu tất cả các liên kết|tệp|torrents của bạn lên Google Drive hoặc bất kỳ đám mây rclone nào hoặc lên telegram.
Nhập /{BotCommands.HelpCommand} để nhận danh sách các lệnh có sẵn
"""
        await send_message(message, start_string, reply_markup)
    else:
        await send_message(
            message,
            "Bạn không phải là người dùng được ủy quyền! Hãy triển khai bot mirror-leech của riêng bạn",
            reply_markup,
        )


@new_task
async def restart(_, message):
    intervals["stopAll"] = True
    restart_message = await send_message(message, "Đang khởi động lại...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    if qb := intervals["qb"]:
        qb.cancel()
    if jd := intervals["jd"]:
        jd.cancel()
    if nzb := intervals["nzb"]:
        nzb.cancel()
    if st := intervals["status"]:
        for intvl in list(st.values()):
            intvl.cancel()
    await sync_to_async(clean_all)
    if sabnzbd_client.LOGGED_IN:
        await gather(
            sabnzbd_client.pause_all(),
            sabnzbd_client.purge_all(True),
            sabnzbd_client.delete_history("all", delete_files=True),
        )
    proc1 = await create_subprocess_exec(
        "pkill",
        "-9",
        "-f",
        "gunicorn|aria2c|qbittorrent-nox|ffmpeg|rclone|java|sabnzbdplus",
    )
    proc2 = await create_subprocess_exec("python3", "update.py")
    await gather(proc1.wait(), proc2.wait())
    async with aiopen(".restartmsg", "w") as f:
        await f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    osexecl(executable, executable, "-m", "bot")


@new_task
async def ping(_, message):
    start_time = int(round(time() * 1000))
    reply = await send_message(message, "Đang bắt đầu Ping")
    end_time = int(round(time() * 1000))
    await edit_message(reply, f"{end_time - start_time} ms")


@new_task
async def log(_, message):
    await send_file(message, "log.txt")


help_string = f"""
LƯU Ý: Thử mỗi lệnh mà không có đối số để xem thêm chi tiết.
/{BotCommands.MirrorCommand[0]} hoặc /{BotCommands.MirrorCommand[1]}: Bắt đầu phản chiếu lên đám mây.
/{BotCommands.QbMirrorCommand[0]} hoặc /{BotCommands.QbMirrorCommand[1]}: Bắt đầu phản chiếu lên đám mây sử dụng qBittorrent.
/{BotCommands.JdMirrorCommand[0]} hoặc /{BotCommands.JdMirrorCommand[1]}: Bắt đầu phản chiếu lên đám mây sử dụng JDownloader.
/{BotCommands.NzbMirrorCommand[0]} hoặc /{BotCommands.NzbMirrorCommand[1]}: Bắt đầu phản chiếu lên đám mây sử dụng Sabnzbd.
/{BotCommands.YtdlCommand[0]} hoặc /{BotCommands.YtdlCommand[1]}: Phản chiếu link hỗ trợ yt-dlp.
/{BotCommands.LeechCommand[0]} hoặc /{BotCommands.LeechCommand[1]}: Bắt đầu leech lên Telegram.
/{BotCommands.QbLeechCommand[0]} hoặc /{BotCommands.QbLeechCommand[1]}: Bắt đầu leech sử dụng qBittorrent.
/{BotCommands.JdLeechCommand[0]} hoặc /{BotCommands.JdLeechCommand[1]}: Bắt đầu leech sử dụng JDownloader.
/{BotCommands.NzbLeechCommand[0]} hoặc /{BotCommands.NzbLeechCommand[1]}: Bắt đầu leech sử dụng Sabnzbd.
/{BotCommands.YtdlLeechCommand[0]} hoặc /{BotCommands.YtdlLeechCommand[1]}: Leech link hỗ trợ yt-dlp.
/{BotCommands.CloneCommand} [drive_url]: Sao chép tệp/thư mục vào Google Drive.
/{BotCommands.CountCommand} [drive_url]: Đếm tệp/thư mục của Google Drive.
/{BotCommands.DeleteCommand} [drive_url]: Xóa tệp/thư mục khỏi Google Drive (Chỉ Owner & Sudo).
/{BotCommands.UserSetCommand[0]} hoặc /{BotCommands.UserSetCommand[1]} [query]: Cài đặt người dùng.
/{BotCommands.BotSetCommand[0]} hoặc /{BotCommands.BotSetCommand[1]} [query]: Cài đặt bot.
/{BotCommands.SelectCommand}: Chọn tệp từ torrents hoặc nzb theo gid hoặc trả lời.
/{BotCommands.CancelTaskCommand[0]} hoặc /{BotCommands.CancelTaskCommand[1]} [gid]: Hủy tác vụ theo gid hoặc trả lời.
/{BotCommands.ForceStartCommand[0]} hoặc /{BotCommands.ForceStartCommand[1]} [gid]: Buộc bắt đầu tác vụ theo gid hoặc trả lời.
/{BotCommands.CancelAllCommand} [query]: Hủy tất cả các tác vụ [trạng thái].
/{BotCommands.ListCommand} [query]: Tìm kiếm trong Google Drive(s).
/{BotCommands.SearchCommand} [query]: Tìm kiếm torrents với API.
/{BotCommands.StatusCommand}: Hiển thị trạng thái của tất cả các lượt tải xuống.
/{BotCommands.StatsCommand}: Hiển thị thống kê của máy nơi bot được lưu trữ.
/{BotCommands.PingCommand}: Kiểm tra thời gian Ping đến Bot (Chỉ Owner & Sudo).
/{BotCommands.AuthorizeCommand}: Ủy quyền một chat hoặc người dùng để sử dụng bot (Chỉ Owner & Sudo).
/{BotCommands.UnAuthorizeCommand}: Hủy ủy quyền một chat hoặc người dùng để sử dụng bot (Chỉ Owner & Sudo).
/{BotCommands.UsersCommand}: Hiển thị cài đặt người dùng (Chỉ Owner & Sudo).
/{BotCommands.AddSudoCommand}: Thêm người dùng sudo (Chỉ Owner).
/{BotCommands.RmSudoCommand}: Xóa người dùng sudo (Chỉ Owner).
/{BotCommands.RestartCommand}: Khởi động lại và cập nhật bot (Chỉ Owner & Sudo).
/{BotCommands.LogCommand}: Lấy tệp nhật ký của bot. Hữu ích để nhận báo cáo sự cố (Chỉ Owner & Sudo).
/{BotCommands.ShellCommand}: Chạy lệnh shell (Chỉ Owner).
/{BotCommands.AExecCommand}: Thực thi hàm bất đồng bộ (Chỉ Owner).
/{BotCommands.ExecCommand}: Thực thi hàm đồng bộ (Chỉ Owner).
/{BotCommands.ClearLocalsCommand}: Xóa {BotCommands.AExecCommand} hoặc {BotCommands.ExecCommand} locals (Chỉ Owner).
/{BotCommands.RssCommand}: Menu RSS.
"""


@new_task
async def bot_help(_, message):
    await send_message(message, help_string)


async def restart_notification():
    if await aiopath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
    else:
        chat_id, msg_id = 0, 0

    async def send_incomplete_task_message(cid, msg):
        try:
            if msg.startswith("Khởi động lại thành công!"):
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=msg_id, text=msg
                )
                await remove(".restartmsg")
            else:
                await bot.send_message(
                    chat_id=cid,
                    text=msg,
                    disable_web_page_preview=True,
                    disable_notification=True,
                )
        except Exception as e:
            LOGGER.error(e)

    if config_dict["INCOMPLETE_TASK_NOTIFIER"] and config_dict["DATABASE_URL"]:
        if notifier_dict := await database.get_incomplete_tasks():
            for cid, data in notifier_dict.items():
                msg = "Khởi động lại thành công!" if cid == chat_id else "Bot đã khởi động lại!"
                for tag, links in data.items():
                    msg += f"\n\n{tag}: "
                    for index, link in enumerate(links, start=1):
                        msg += f" <a href='{link}'>{index}</a> |"
                        if len(msg.encode()) > 4000:
                            await send_incomplete_task_message(cid, msg)
                            msg = ""
                if msg:
                    await send_incomplete_task_message(cid, msg)

    if await aiopath.isfile(".restartmsg"):
        try:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id, text="Khởi động lại thành công!"
            )
        except:
            pass
        await remove(".restartmsg")


async def main():
    if config_dict["DATABASE_URL"]:
        await database.db_load()
    await gather(
        jdownloader.boot(),
        sync_to_async(clean_all),
        bot_settings.initiate_search_tools(),
        restart_notification(),
        telegraph.create_account(),
        rclone_serve_booter(),
        sync_to_async(start_aria2_listener, wait=False),
    )
    create_help_buttons()

    bot.add_handler(
        MessageHandler(
            start, filters=command(BotCommands.StartCommand, case_sensitive=True)
        )
    )
    bot.add_handler(
        MessageHandler(
            log,
            filters=command(BotCommands.LogCommand, case_sensitive=True)
            & CustomFilters.sudo,
        )
    )
    bot.add_handler(
        MessageHandler(
            restart,
            filters=command(BotCommands.RestartCommand, case_sensitive=True)
            & CustomFilters.sudo,
        )
    )
    bot.add_handler(
        MessageHandler(
            ping,
            filters=command(BotCommands.PingCommand, case_sensitive=True)
            & CustomFilters.authorized,
        )
    )
    bot.add_handler(
        MessageHandler(
            bot_help,
            filters=command(BotCommands.HelpCommand, case_sensitive=True)
            & CustomFilters.authorized,
        )
    )
    bot.add_handler(
        MessageHandler(
            stats,
            filters=command(BotCommands.StatsCommand, case_sensitive=True)
            & CustomFilters.authorized,
        )
    )
    LOGGER.info("Bot Started!")
    signal(SIGINT, exit_clean_up)


bot.loop.run_until_complete(main())
bot.loop.run_forever()
