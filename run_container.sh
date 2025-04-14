#!/bin/bash

# Thông số cấu hình
IMAGE_NAME="nhnobnd/obnd:latest"
CONTAINER_NAME="obnd-77"
PORT="2222"

# Thông báo bắt đầu
echo "Bắt đầu triển khai container $CONTAINER_NAME từ image $IMAGE_NAME..."

# Đăng nhập vào Docker Hub
echo "Đăng nhập vào Docker Hub..."
echo "Dunghoi131290" | docker login -u nhnobnd --password-stdin

# Kiểm tra và dừng/xóa container hiện có nếu tồn tại
if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
    echo "Dừng và xóa container $CONTAINER_NAME hiện có..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Pull image mới nhất từ Docker Hub
echo "Pull image mới nhất từ Docker Hub..."
docker pull $IMAGE_NAME

# Chạy container mới
echo "Chạy container mới..."
docker run -d --name $CONTAINER_NAME -p $PORT:$PORT $IMAGE_NAME

# Kiểm tra container đã chạy thành công chưa
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Container $CONTAINER_NAME đã được triển khai thành công và đang chạy!"
    echo "Ứng dụng đang chạy ở cổng: $PORT"
else
    echo "Lỗi: Container không khởi động được. Vui lòng kiểm tra logs."
    docker logs $CONTAINER_NAME
fi 