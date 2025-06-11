import ipaddress

import pika


def generate_public_ipv4_ranges_stream(cidr_prefix=24):
    all_space = ipaddress.IPv4Network("0.0.0.0/0")
    for subnet in all_space.subnets(new_prefix=cidr_prefix):
        if subnet.is_global and not (
            subnet.is_private
            or subnet.is_loopback
            or subnet.is_link_local
            or subnet.is_multicast
            or subnet.is_reserved
        ):
            yield str(subnet)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="public_ip_ranges", durable=True)

    for ip_range in generate_public_ipv4_ranges_stream(24):
        channel.basic_publish(
            exchange="",
            routing_key="public_ip_ranges",
            body=ip_range.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"Sent: {ip_range}")

    connection.close()
