import os
import sys

import pika
import masscan_worker

def callback(ch, method, properties, body):
    ip_range = body.decode('utf-8')
    print(f" ip Received {ip_range}")
    result = masscan_worker.masscan_execution(ip_range)
    parsed_result = masscan_worker.parse_masscan_output(result)
    print(parsed_result)



def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="public_ip_ranges", durable=True)

    def callback(ch, method, properties, body):
        print(f" ip Received {body}")

    channel.basic_consume(
        queue="public_ip_ranges", on_message_callback=callback, auto_ack=True
    )

    print(" Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
