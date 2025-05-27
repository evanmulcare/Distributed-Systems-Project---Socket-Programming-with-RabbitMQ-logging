import pika

# Connect to RabbitMQ from localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='activity_log')

#callback that is called when a message is received
def callback(ch, method, properties, body):
    print(f"MESSAGE: {body.decode()}") #print the message received
#listen to the activity log queue
channel.basic_consume(queue='activity_log', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
