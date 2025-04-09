from psutil import cpu_percent, virtual_memory, disk_usage
from pyrogram.filters import command, regex
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from time import time

from bot import (
    task_dict_lock,
    status_dict,
    task_dict,
    botStartTime,
    DOWNLOAD_DIR,
    intervals,
    bot,
)
from ..helper.ext_utils.bot_utils import sync_to_async, new_task
from ..helper.ext_utils.status_utils import (
    MirrorStatus,
    get_readable_file_size,
    get_readable_time,
    speed_string_to_bytes,
)
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.filters import CustomFilters
from ..helper.telegram_helper.message_utils import (
    send_message,
    delete_message,
    auto_delete_message,
    send_status_message,
    update_status_message,
    edit_message,
)
from ..helper.telegram_helper.button_build import ButtonMaker


@new_task
async def mirror_status(_, message):
    async with task_dict_lock:
        count = len(task_dict)
    if count == 0:
        currentTime = get_readable_time(time() - botStartTime)
        free = get_readable_file_size(disk_usage(DOWNLOAD_DIR).free)
        msg = f"Không có tác vụ đang hoạt động!\nMỗi người dùng có thể nhận trạng thái cho các tác vụ của mình bằng cách thêm tôi hoặc user_id sau lệnh: /{BotCommands.StatusCommand} me"
        msg += (
            f"\n<b>CPU:</b> {cpu_percent()}% | <b>TRỐNG:</b> {free}"
            f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>THỜI GIAN HOẠT ĐỘNG:</b> {currentTime}"
        )
        reply_message = await send_message(message, msg)
        await auto_delete_message(message, reply_message)
    else:
        text = message.text.split()
        if len(text) > 1:
            user_id = message.from_user.id if text[1] == "me" else int(text[1])
        else:
            user_id = 0
            sid = message.chat.id
            if obj := intervals["status"].get(sid):
                obj.cancel()
                del intervals["status"][sid]
        await send_status_message(message, user_id)
        await delete_message(message)


@new_task
async def status_pages(_, query):
    data = query.data.split()
    key = int(data[1])
    if data[2] == "ref":
        await query.answer()
        await update_status_message(key, force=True)
    elif data[2] in ["nex", "pre"]:
        await query.answer()
        async with task_dict_lock:
            if data[2] == "nex":
                status_dict[key]["page_no"] += status_dict[key]["page_step"]
            else:
                status_dict[key]["page_no"] -= status_dict[key]["page_step"]
    elif data[2] == "ps":
        await query.answer()
        async with task_dict_lock:
            status_dict[key]["page_step"] = int(data[3])
    elif data[2] == "st":
        await query.answer()
        async with task_dict_lock:
            status_dict[key]["status"] = data[3]
        await update_status_message(key, force=True)
    elif data[2] == "ov":
        message = query.message
        tasks = {
            "Tải xuống": 0,
            "Tải lên": 0,
            "Chia sẻ": 0,
            "Lưu trữ": 0,
            "Giải nén": 0,
            "Chia nhỏ": 0,
            "Hàng đợi TLXuống": 0,
            "Hàng đợi TLLên": 0,
            "Nhân bản": 0,
            "Kiểm tra": 0,
            "Tạm dừng": 0,
            "Video mẫu": 0,
            "Chuyển đổi": 0,
        }
        dl_speed = 0
        up_speed = 0
        seed_speed = 0
        async with task_dict_lock:
            for download in task_dict.values():
                match await sync_to_async(download.status):
                    case MirrorStatus.STATUS_DOWNLOADING:
                        tasks["Tải xuống"] += 1
                        dl_speed += speed_string_to_bytes(download.speed())
                    case MirrorStatus.STATUS_UPLOADING:
                        tasks["Tải lên"] += 1
                        up_speed += speed_string_to_bytes(download.speed())
                    case MirrorStatus.STATUS_SEEDING:
                        tasks["Chia sẻ"] += 1
                        seed_speed += speed_string_to_bytes(download.seed_speed())
                    case MirrorStatus.STATUS_ARCHIVING:
                        tasks["Lưu trữ"] += 1
                    case MirrorStatus.STATUS_EXTRACTING:
                        tasks["Giải nén"] += 1
                    case MirrorStatus.STATUS_SPLITTING:
                        tasks["Chia nhỏ"] += 1
                    case MirrorStatus.STATUS_QUEUEDL:
                        tasks["Hàng đợi TLXuống"] += 1
                    case MirrorStatus.STATUS_QUEUEUP:
                        tasks["Hàng đợi TLLên"] += 1
                    case MirrorStatus.STATUS_CLONING:
                        tasks["Nhân bản"] += 1
                    case MirrorStatus.STATUS_CHECKING:
                        tasks["Kiểm tra"] += 1
                    case MirrorStatus.STATUS_PAUSED:
                        tasks["Tạm dừng"] += 1
                    case MirrorStatus.STATUS_SAMVID:
                        tasks["Video mẫu"] += 1
                    case MirrorStatus.STATUS_CONVERTING:
                        tasks["Chuyển đổi"] += 1
                    case _:
                        tasks["Tải xuống"] += 1
                        dl_speed += speed_string_to_bytes(download.speed())

        msg = f"""<b>TẢI XUỐNG:</b> {tasks['Tải xuống']} | <b>TẢI LÊN:</b> {tasks['Tải lên']} | <b>CHIA SẺ:</b> {tasks['Chia sẻ']} | <b>LƯU TRỮ:</b> {tasks['Lưu trữ']}
<b>GIẢI NÉN:</b> {tasks['Giải nén']} | <b>CHIA NHỎ:</b> {tasks['Chia nhỏ']} | <b>HÀNG ĐỢI TẢI XUỐNG:</b> {tasks['Hàng đợi TLXuống']} | <b>HÀNG ĐỢI TẢI LÊN:</b> {tasks['Hàng đợi TLLên']}
<b>NHÂN BẢN:</b> {tasks['Nhân bản']} | <b>KIỂM TRA:</b> {tasks['Kiểm tra']} | <b>TẠM DỪNG:</b> {tasks['Tạm dừng']} | <b>VIDEO MẪU:</b> {tasks['Video mẫu']}
<b>CHUYỂN ĐỔI:</b> {tasks['Chuyển đổi']}

<b>TỐC ĐỘ TẢI XUỐNG TỔNG:</b> {get_readable_file_size(dl_speed)}/s
<b>TỐC ĐỘ TẢI LÊN TỔNG:</b> {get_readable_file_size(up_speed)}/s
<b>TỐC ĐỘ CHIA SẺ TỔNG:</b> {get_readable_file_size(seed_speed)}/s
"""
        button = ButtonMaker()
        button.data_button("Quay lại", f"status {data[1]} ref")
        await edit_message(message, msg, button.build_menu())


bot.add_handler(
    MessageHandler(
        mirror_status,
        filters=command(BotCommands.StatusCommand, case_sensitive=True)
        & CustomFilters.authorized,
    )
)
bot.add_handler(CallbackQueryHandler(status_pages, filters=regex("^status")))
