import ipaddress
import re
import subprocess


def masscan_execution(ip, ports="0-1023", rate=50):  # TODO:change the name

    try:
        ipaddress.ip_network(ip)
    except ValueError:
        return "Is not a valid ip range or ip"
    cmd = [
        "masscan",
        "-p",
        str(ports),
        str(ip),
        "--rate",
        str(rate),
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.stdout.decode()


def parse_masscan_output(raw_output):
    open_ports = []
    for line in raw_output.splitlines():
        match = re.search(r"Discovered open port (\d+/[a-z]+) on ([\d.]+)", line)
        if match:
            port, ip = match.groups()
            open_ports.append({"ip": ip, "port": port})
    return open_ports


