import pika


def create_connection():

    return connection


def send_message(cmd):
    '''Hàm gửi tin nhắn các worker

    Args:
        data: Thông tin message
    Returns:
        Thành công
            {
                'status': True,
                'status_code': 'S001',
                'message': 'Thành công',
                'data': {},
            }

        Thất bại
            {
                'status': False,
                'status_code': 'E001',
                'message': 'Có lỗi xảy ra khi gửi message',
                'data': {},
            }

        Danh sách status code
            S001: Thành công
            E001: Có lỗi trong khi gửi message

    Raises:
    '''
    # KHỞI TẠO RESPONSE

    response = {
        'status': False,
        'status_code': None,
        'message': None,
    }

    # Tạo connection đến rabbitmq

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
    except pika.exceptions.AMQPConnectionError as exc:
        response['status'] = False
        response['status_code'] = 'E001'
        response['message'] = 'Có lỗi xảy ra khi gửi message'
        return response

    # Tạo channel để gửi tin nhắn

    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=cmd
    )

    # Đóng connection

    connection.close()

    # Trả True nếu hợp lệ

    response['status'] = True
    response['status_code'] = 'S001'
    response['message'] = 'Thành công'
    return response
