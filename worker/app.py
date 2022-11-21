import pika
print("Connecting to server...")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    pass

channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True, durable=True)#Exclusive queues are deleted when their declaring connection is closed or gone
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)

print("Waiting for message...")

def callback(channel, method, properties, body):
    print(" Received %s" % body.decode())
    print(" Done")

channel.basic_qos(prefetch_count=1)#don't dispatch a new message to a worker until it has processed and acknowledged the previous one. 
                                    #Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()