mirror = """<b>Gửi link cùng với dòng lệnh hoặc </b>

/cmd link

<b>Bằng cách trả lời link/file</b>:

/cmd -n tên mới -e -up nơi tải lên

<b>LƯU Ý:</b>
1. Các lệnh bắt đầu bằng <b>qb</b> CHỈ dành cho torrent."""

yt = """<b>Gửi link cùng với dòng lệnh</b>:

/cmd link
<b>Bằng cách trả lời link</b>:
/cmd -n tên mới -z mật khẩu -opt x:y|x1:y1

Xem tất cả các trang được hỗ trợ tại <a href='https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md'>TRANG WEB</a>
Xem tất cả các tùy chọn yt-dlp api từ <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a> hoặc sử dụng <a href='https://t.me/mltb_official_channel/177'>script này</a> để chuyển đổi tham số dòng lệnh sang tùy chọn api."""

clone = """Gửi link Gdrive|Gdot|Filepress|Filebee|Appdrive|Gdflix hoặc đường dẫn rclone cùng với lệnh hoặc bằng cách trả lời link/rc_path bằng lệnh.
Sử dụng -sync để sử dụng phương thức đồng bộ trong rclone. Ví dụ: /cmd rcl/rclone_path -up rcl/rclone_path/rc -sync"""

new_name = """<b>Tên mới</b>: -n

/cmd link -n tên mới
Lưu ý: Không hoạt động với torrent"""

multi_link = """<b>Nhiều link chỉ bằng cách trả lời link/file đầu tiên</b>: -i

/cmd -i 10(số lượng link/file)"""

same_dir = """<b>Di chuyển file/thư mục vào thư mục mới</b>: -m

Bạn cũng có thể sử dụng tham số này để di chuyển nhiều link/nội dung torrent vào cùng một thư mục, vì vậy tất cả các link sẽ được tải lên cùng nhau như một tác vụ

/cmd link -m thư mục mới (chỉ một link trong thư mục mới)
/cmd -i 10(số lượng link/file) -m tên thư mục (tất cả nội dung link trong một thư mục)
/cmd -b -m tên thư mục (trả lời hàng loạt tin nhắn/file(mỗi link trên một dòng mới))

Khi sử dụng số lượng lớn, bạn cũng có thể sử dụng tham số này với tên thư mục khác nhau cùng với các link trong tin nhắn hoặc lô file
Ví dụ:
link1 -m folder1
link2 -m folder1
link3 -m folder2
link4 -m folder2
link5 -m folder3
link6
vì vậy nội dung link1 và link2 sẽ được tải lên từ cùng một thư mục là folder1
nội dung link3 và link4 sẽ được tải lên từ cùng một thư mục là folder2
link5 sẽ được tải lên riêng lẻ trong thư mục mới có tên folder3
link6 sẽ được tải lên bình thường một mình
"""

thumb = """<b>Hình thu nhỏ cho tác vụ hiện tại</b>: -t

/cmd link -t tg-message-link(doc hoặc photo)"""

split_size = """<b>Kích thước phân chia cho tác vụ hiện tại</b>: -sp

/cmd link -sp (500mb hoặc 2gb hoặc 4000000000)
Lưu ý: Chỉ hỗ trợ mb và gb hoặc viết bằng byte không có đơn vị!"""

upload = """<b>Điểm đến tải lên</b>: -up

/cmd link -up rcl/gdl (rcl: để chọn cấu hình rclone, remote & path | gdl: Để chọn token.pickle, gdrive id) sử dụng nút
Bạn có thể trực tiếp thêm đường dẫn tải lên: -up remote:dir/subdir hoặc -up Gdrive_id hoặc -up id/username (telegram) hoặc -up id/username|topic_id (telegram)
Nếu DEFAULT_UPLOAD là `rc` thì bạn có thể truyền up: `gd` để tải lên bằng công cụ gdrive đến GDRIVE_ID.
Nếu DEFAULT_UPLOAD là `gd` thì bạn có thể truyền up: `rc` để tải lên đến RCLONE_PATH.

Nếu bạn muốn thêm path hoặc gdrive thủ công từ config/token của bạn (TẢI LÊN TỪ USETTING) thêm mrcc: cho rclone và mtp: trước path/gdrive_id không có khoảng trắng.
/cmd link -up mrcc:main:dump hoặc -up mtp:gdrive_id

Để thêm điểm đến leech:
-up id
-up @username
-up b:id/@username/pm (b: nghĩa là leech bởi bot) (id hoặc username của cuộc trò chuyện hoặc viết pm có nghĩa là tin nhắn riêng để bot sẽ gửi các tệp riêng tư cho bạn)
khi nào bạn nên sử dụng b:(leech bởi bot)? Khi cài đặt mặc định của bạn là leech bởi người dùng và bạn muốn leech bởi bot cho một tác vụ cụ thể.
-up u:id/@username(u: nghĩa là leech bởi người dùng) Điều này trong trường hợp OWNER đã thêm USER_STRING_SESSION.
-up m:id/@username(leech hỗn hợp) m: để tải lên các tệp bởi bot và người dùng dựa trên kích thước tệp.
-up id/@username|topic_id(leech trong cuộc trò chuyện và chủ đề cụ thể) thêm | không có khoảng trắng và viết topic id sau chat id hoặc username.

Trong trường hợp bạn muốn chỉ định sử dụng token.pickle hoặc tài khoản dịch vụ, bạn có thể thêm tp:gdrive_id (sử dụng token.pickle) hoặc sa:gdrive_id (sử dụng tài khoản dịch vụ) hoặc mtp:gdrive_id (sử dụng token.pickle được tải lên từ usetting).
DEFAULT_UPLOAD không ảnh hưởng đến các lệnh leech.
"""

user_download = """<b>Tải xuống của người dùng</b>: link

/cmd tp:link để tải xuống bằng token.pickle của chủ sở hữu trong trường hợp tài khoản dịch vụ được bật.
/cmd sa:link để tải xuống bằng tài khoản dịch vụ trong trường hợp tài khoản dịch vụ bị vô hiệu hóa.
/cmd tp:gdrive_id để tải xuống bằng token.pickle và file_id trong trường hợp tài khoản dịch vụ được bật.
/cmd sa:gdrive_id để tải xuống bằng tài khoản dịch vụ và file_id trong trường hợp tài khoản dịch vụ bị vô hiệu hóa.
/cmd mtp:gdrive_id hoặc mtp:link để tải xuống bằng token.pickle của người dùng được tải lên từ usetting
/cmd mrcc:remote:path để tải xuống bằng cấu hình rclone của người dùng được tải lên từ usetting"""

rcf = """<b>Cờ Rclone</b>: -rcf

/cmd link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value
Điều này sẽ ghi đè tất cả các cờ khác ngoại trừ --exclude
Kiểm tra tất cả <a href='https://rclone.org/flags/'>CờRclone</a> tại đây."""

bulk = """<b>Tải xuống hàng loạt</b>: -b

Số lượng lớn chỉ có thể được sử dụng bằng cách trả lời tin nhắn văn bản hoặc tệp văn bản chứa các liên kết được phân tách bằng dòng mới.
Ví dụ:
link1 -n tên mới -up remote1:path1 -rcf |key:value|key:value
link2 -z -n tên mới -up remote2:path2
link3 -e -n tên mới -up remote2:path2
Trả lời ví dụ này bằng lệnh này -> /cmd -b(bulk)

Lưu ý: Bất kỳ đối số nào cùng với cmd sẽ được đặt cho tất cả các liên kết
/cmd -b -up remote: -z -m tên thư mục (tất cả nội dung liên kết trong một thư mục nén được tải lên đến một điểm đến)
vì vậy bạn không thể đặt các điểm đến tải lên khác nhau cùng với liên kết trong trường hợp bạn đã thêm -m cùng với cmd
Bạn có thể đặt bắt đầu và kết thúc của các liên kết từ số lượng lớn như hạt giống, với -b start:end hoặc chỉ kết thúc bằng -b :end hoặc chỉ bắt đầu bằng -b start.
Điểm bắt đầu mặc định là từ không (liên kết đầu tiên) đến vô cùng."""

rlone_dl = """<b>Tải xuống Rclone</b>:

Đối xử với đường dẫn rclone giống như các liên kết
/cmd main:dump/ubuntu.iso hoặc rcl(Để chọn cấu hình, remote và path)
Người dùng có thể thêm rclone của riêng họ từ cài đặt người dùng
Nếu bạn muốn thêm đường dẫn thủ công từ cấu hình của mình, hãy thêm mrcc: trước đường dẫn không có khoảng trắng
/cmd mrcc:main:dump/ubuntu.iso"""

extract_zip = """<b>Giải nén/Nén</b>: -e -z

/cmd link -e mật khẩu (giải nén được bảo vệ bằng mật khẩu)
/cmd link -z mật khẩu (nén được bảo vệ bằng mật khẩu)
/cmd link -z mật khẩu -e (giải nén và nén được bảo vệ bằng mật khẩu)
Lưu ý: Khi cả giải nén và nén được thêm vào với cmd, nó sẽ giải nén trước và sau đó nén, vì vậy luôn giải nén trước"""

join = """<b>Nối các tệp đã phân chia</b>: -j

Tùy chọn này sẽ chỉ hoạt động trước khi giải nén và nén, vì vậy hầu hết nó sẽ được sử dụng với đối số -m (samedir)
Bằng cách trả lời:
/cmd -i 3 -j -m tên thư mục
/cmd -b -j -m tên thư mục
nếu bạn có liên kết (thư mục) có các tệp đã phân chia:
/cmd link -j"""

tg_links = """<b>Liên kết TG</b>:

Đối xử với các liên kết giống như bất kỳ liên kết trực tiếp nào
Một số liên kết cần quyền truy cập của người dùng vì vậy bạn phải thêm USER_SESSION_STRING cho nó.
Ba loại liên kết:
Công khai: https://t.me/channel_name/message_id
Riêng tư: tg://openmessage?user_id=xxxxxx&message_id=xxxxx
Super: https://t.me/c/channel_id/message_id
Phạm vi: https://t.me/channel_name/first_message_id-last_message_id
Ví dụ phạm vi: tg://openmessage?user_id=xxxxxx&message_id=555-560 hoặc https://t.me/channel_name/100-150
Lưu ý: Liên kết phạm vi sẽ chỉ hoạt động bằng cách trả lời cmd cho nó"""

sample_video = """<b>Video mẫu</b>: -sv

Tạo video mẫu cho một video hoặc thư mục video.
/cmd -sv (nó sẽ lấy các giá trị mặc định là thời lượng mẫu 60 giây và thời lượng phần là 4 giây).
Bạn có thể kiểm soát các giá trị đó. Ví dụ: /cmd -sv 70:5(thời lượng mẫu:thời lượng phần) hoặc /cmd -sv :5 hoặc /cmd -sv 70."""

screenshot = """<b>Ảnh chụp màn hình</b>: -ss

Tạo ảnh chụp màn hình cho một video hoặc thư mục video.
/cmd -ss (nó sẽ lấy giá trị mặc định là 10 ảnh).
Bạn có thể kiểm soát giá trị này. Ví dụ: /cmd -ss 6."""

seed = """<b>Seed Bittorrent</b>: -d

/cmd link -d ratio:seed_time hoặc bằng cách trả lời file/link
Để chỉ định tỷ lệ và thời gian seed, thêm -d ratio:time.
Ví dụ: -d 0.7:10 (tỷ lệ và thời gian) hoặc -d 0.7 (chỉ tỷ lệ) hoặc -d :10 (chỉ thời gian) trong đó thời gian tính bằng phút"""

zip_arg = """<b>Nén</b>: -z mật khẩu

/cmd link -z (nén)
/cmd link -z mật khẩu (nén được bảo vệ bằng mật khẩu)"""

qual = """<b>Nút chất lượng</b>: -s

Trong trường hợp chất lượng mặc định được thêm từ tùy chọn yt-dlp sử dụng tùy chọn định dạng và bạn cần chọn chất lượng cho liên kết cụ thể hoặc liên kết với tính năng nhiều liên kết.
/cmd link -s"""

yt_opt = """<b>Tùy chọn</b>: -opt

/cmd link -opt playliststart:^10|fragment_retries:^inf|matchtitle:S13|writesubtitles:true|live_from_start:true|postprocessor_args:{"ffmpeg": ["-threads", "4"]}|wait_for_video:(5, 100)|download_ranges:[{"start_time": 0, "end_time": 10}]
Lưu ý: Thêm `^` trước số nguyên hoặc số thực, một số giá trị phải là số và một số là chuỗi.
Ví dụ: playlist_items:10 hoạt động với chuỗi, vì vậy không cần thêm `^` trước số nhưng playlistend chỉ hoạt động với số nguyên nên bạn phải thêm `^` trước số như ví dụ trên.
Bạn cũng có thể thêm tuple và dict. Sử dụng dấu ngoặc kép bên trong dict."""

convert_media = """<b>Chuyển đổi phương tiện</b>: -ca -cv
/cmd link -ca mp3 -cv mp4 (chuyển đổi tất cả âm thanh sang mp3 và tất cả video sang mp4)
/cmd link -ca mp3 (chuyển đổi tất cả âm thanh sang mp3)
/cmd link -cv mp4 (chuyển đổi tất cả video sang mp4)
/cmd link -ca mp3 + flac ogg (chỉ chuyển đổi âm thanh flac và ogg sang mp3)
/cmd link -cv mkv - webm flv (chuyển đổi tất cả video sang mp4 ngoại trừ webm và flv)"""

force_start = """<b>Bắt đầu cưỡng chế</b>: -f -fd -fu
/cmd link -f (bắt buộc tải xuống và tải lên)
/cmd link -fd (chỉ bắt buộc tải xuống)
/cmd link -fu (buộc tải lên trực tiếp sau khi tải xuống hoàn tất)"""

gdrive = """<b>Gdrive</b>: link
Nếu DEFAULT_UPLOAD là `rc` thì bạn có thể truyền up: `gd` để tải lên bằng công cụ gdrive đến GDRIVE_ID.
/cmd gdriveLink hoặc gdl hoặc gdriveId -up gdl hoặc gdriveId hoặc gd
/cmd tp:gdriveLink hoặc tp:gdriveId -up tp:gdriveId hoặc gdl hoặc gd (để sử dụng token.pickle nếu tài khoản dịch vụ được bật)
/cmd sa:gdriveLink hoặc sa:gdriveId -p sa:gdriveId hoặc gdl hoặc gd (để sử dụng tài khoản dịch vụ nếu tài khoản dịch vụ bị vô hiệu hóa)
/cmd mtp:gdriveLink hoặc mtp:gdriveId -up mtp:gdriveId hoặc gdl hoặc gd(nếu bạn đã thêm gdriveId tải lên từ usetting) (để sử dụng token.pickle của người dùng được tải lên bởi usetting)"""

rclone_cl = """<b>Rclone</b>: path
Nếu DEFAULT_UPLOAD là `gd` thì bạn có thể truyền up: `rc` để tải lên đến RCLONE_PATH.
/cmd rcl/rclone_path -up rcl/rclone_path/rc -rcf flagkey:flagvalue|flagkey|flagkey:flagvalue
/cmd rcl hoặc rclonePath -up rclonePath hoặc rc hoặc rcl
/cmd mrcc:rclonePath -up rcl hoặc rc(nếu bạn đã thêm đường dẫn rclone từ usetting) (để sử dụng cấu hình người dùng)"""

name_sub = r"""<b>Thay thế tên</b>: -ns
/cmd link -ns script/code/s | mirror/leech | tea/ /s | clone | cpu/ | \[mltb\]/mltb | \\text\\/text/s
Điều này sẽ ảnh hưởng đến tất cả các tệp. Định dạng: wordToReplace/wordToReplaceWith/sensitiveCase
Thay thế từ. Bạn có thể thêm mẫu thay vì văn bản thông thường. Thời gian chờ: 60 giây
LƯU Ý: Bạn phải thêm \ trước bất kỳ ký tự nào, đó là các ký tự: \^$.|?*+()[]{}-
1. script sẽ được thay thế bằng code với trường hợp nhạy cảm
2. mirror sẽ được thay thế bằng leech
4. tea sẽ được thay thế bằng khoảng trắng với trường hợp nhạy cảm
5. clone sẽ bị xóa
6. cpu sẽ được thay thế bằng khoảng trắng
7. [mltb] sẽ được thay thế bằng mltb
8. \text\ sẽ được thay thế bằng text với trường hợp nhạy cảm
"""

mixed_leech = """Leech hỗn hợp: -ml
/cmd link -ml (leech bởi phiên người dùng và bot với tôn trọng kích thước)"""

thumbnail_layout = """Bố cục hình thu nhỏ: -tl
/cmd link -tl 3x3 (widthxheight) 3 ảnh trong hàng và 3 ảnh trong cột"""

leech_as = """<b>Leech dưới dạng</b>: -doc -med
/cmd link -doc (Leech dưới dạng tài liệu)
/cmd link -med (Leech dưới dạng phương tiện)"""

YT_HELP_DICT = {
    "main": yt,
    "New-Name": f"{new_name}\nLưu ý: Không thêm phần mở rộng tệp",
    "Zip": zip_arg,
    "Quality": qual,
    "Options": yt_opt,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "Name-Substitute": name_sub,
    "Mixed-Leech": mixed_leech,
    "Thumbnail-Layout": thumbnail_layout,
    "Leech-Type": leech_as,
}

MIRROR_HELP_DICT = {
    "main": mirror,
    "New-Name": new_name,
    "DL-Auth": "<b>Ủy quyền liên kết trực tiếp</b>: -au -ap\n\n/cmd link -au tên người dùng -ap mật khẩu",
    "Headers": "<b>Tiêu đề tùy chỉnh liên kết trực tiếp</b>: -h\n\n/cmd link -h key: value key1: value1",
    "Extract/Zip": extract_zip,
    "Select-Files": "<b>Lựa chọn tệp Bittorrent/JDownloader/Sabnzbd</b>: -s\n\n/cmd link -s hoặc bằng cách trả lời file/link",
    "Torrent-Seed": seed,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Join": join,
    "Rclone-DL": rlone_dl,
    "Tg-Links": tg_links,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "User-Download": user_download,
    "Name-Substitute": name_sub,
    "Mixed-Leech": mixed_leech,
    "Thumbnail-Layout": thumbnail_layout,
    "Leech-Type": leech_as,
}

CLONE_HELP_DICT = {
    "main": clone,
    "Multi-Link": multi_link,
    "Bulk": bulk,
    "Gdrive": gdrive,
    "Rclone": rclone_cl,
}

RSS_HELP_MESSAGE = """
Sử dụng định dạng này để thêm url feed:
Tiêu đề1 link (bắt buộc)
Tiêu đề2 link -c cmd -inf xx -exf xx
Tiêu đề3 link -c cmd -d ratio:time -z mật khẩu

-c command -up mrcc:remote:path/subdir -rcf --buffer-size:8M|key|key:value
-inf Cho bộ lọc từ bao gồm.
-exf Cho bộ lọc từ loại trừ.
-stv true hoặc false (bộ lọc nhạy cảm)

Ví dụ: Tiêu đề https://www.rss-url.com -inf 1080 or 720 or 144p|mkv or mp4|hevc -exf flv or web|xxx
Bộ lọc này sẽ phân tích các liên kết mà tiêu đề của nó chứa `(1080 hoặc 720 hoặc 144p) và (mkv hoặc mp4) và hevc` và không chứa (flv or web) và các từ xxx. Bạn có thể thêm bất cứ thứ gì bạn muốn.

Một ví dụ khác: -inf 1080 or 720p|.web. or .webrip.|hvec or x264. Điều này sẽ phân tích các tiêu đề chứa (1080 hoặc 720p) và (.web. hoặc .webrip.) và (hvec hoặc x264). Tôi đã thêm khoảng trắng trước và sau 1080 để tránh khớp sai. Nếu số `10805695` này trong tiêu đề, nó sẽ khớp với 1080 nếu thêm 1080 mà không có khoảng trắng sau nó.

Ghi chú bộ lọc:
1. | có nghĩa là and.
2. Thêm `or` giữa các khóa tương tự, bạn có thể thêm nó giữa các chất lượng hoặc giữa các phần mở rộng, vì vậy đừng thêm bộ lọc như thế này f: 1080|mp4 or 720|web vì điều này sẽ phân tích 1080 và (mp4 hoặc 720) và web ... không phải (1080 và mp4) hoặc (720 và web).
3. Bạn có thể thêm `or` và `|` bao nhiêu tùy thích.
4. Hãy xem xét tiêu đề nếu nó có một ký tự đặc biệt tĩnh sau hoặc trước chất lượng hoặc phần mở rộng hoặc bất kỳ thứ gì và sử dụng chúng trong bộ lọc để tránh khớp sai.
Thời gian chờ: 60 giây.
"""

PASSWORD_ERROR_MESSAGE = """
<b>Liên kết này yêu cầu mật khẩu!</b>
- Chèn <b>::</b> sau liên kết và viết mật khẩu sau ký hiệu.

<b>Ví dụ:</b> link::mật khẩu của tôi
"""
