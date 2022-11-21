import pika

def create_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        return
    
    return connection
     
def send_message(cmd):
    connection = create_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=cmd
    )

    connection.close()
    return " ___ Sent: %s" % cmd

def send_message_to_worker(cmd):
    connection = create_connection()
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )

    connection.close()
    return " ___ Sent: %s" % cmd