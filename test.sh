THRESHOLD=500000 # Đặt ngưỡng ổ cứng ở đây (tính theo MB)
TARGET_DIRECTORY="/" # Thay thế bằng thư mục bạn muốn kiểm tra

 available_space=$(df -m $TARGET_DIRECTORY | awk 'NR==2{print $4}')

    if [ $available_space -lt $THRESHOLD ]; then
        # Thực hiện hành động khi dung lượng ổ cứng giảm xuống ngưỡng đã đặt
        # Ví dụ: gửi thông báo, thực hiện một lệnh cụ thể

        # Ví dụ: hiển thị thông báo
    #   curl -X POST -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}' https://pushmore.io/webhook/r6Uybjxdr7HKXg7H7dXfaqEW
        
        curl -X POST -H "Content-Type: application/json" -d "{\"DISK\": \"$available_space\"}" https://pushmore.io/webhook/r6Uybjxdr7HKXg7H7dXfaqEW

        echo "Low disk space alert"
    fi