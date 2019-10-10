# -*- coding: UTF-8 -*-

import pydivert
from pydivert import Packet

import datetime
import time

import atexit

import psutil


class ProcessConnections:
    """the process and its connections as extracted from psutils"""

    def __init__(self, process: str = "", local_address: str = "", right_address: str = ""):
        self.process = process
        self.local_address = local_address
        self.right_address = right_address

    @staticmethod
    def read_process_connections():
        inner_process_connections = {}
        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                process_string = str(process.pid)
                if process.name():
                    process_string = process.name()
                for connection in process.connections():
                    left_address = NetworkPacket.concat_address(str(connection.laddr.ip), str(connection.laddr.port))
                    # do i really need the r address
                    if connection.raddr:
                        right_address = NetworkPacket.concat_address(str(connection.raddr.ip), str(connection.raddr.port))
                    inner_process_connections[left_address] = ProcessConnections(process_string, left_address,
                                                                                 right_address)
            except psutil.NoSuchProcess:
                pass
        # print("paused till you type")
        # input()

        for key in inner_process_connections.keys():
            print("process conn: " + inner_process_connections[key].process + "//"
                  +inner_process_connections[key].local_address+"//"+inner_process_connections[key].right_address)

        return inner_process_connections


class NetworkPacket:
    """the network packet received or sent cross referenced with open sockets"""

    def __init__(self, timestamp: datetime, packet_input: Packet = None):
        self.direction = "OUT" if packet_input.is_outbound else "IN"
        self.type = "TCP" if packet_input.tcp else ("UDP" if packet_input.udp else "UNKNOWN")
        src_address = NetworkPacket.concat_address(packet_input.src_addr, packet_input.src_port)
        dst_address = NetworkPacket.concat_address(packet_input.dst_addr, packet_input.dst_port)
        # 'we' aka my ip is always the local address, as being always left in comodo
        if packet_input.is_outbound:
            self.local_address = src_address
            self.remote_address = dst_address
        else:
            self.local_address = dst_address
            self.remote_address = src_address
        self.timestamp_text = timestamp.strftime("%H:%M:%S.%f")
        self.timestamp = timestamp
        self.discriminator = self.type + self.direction + self.local_address + self.remote_address

    @staticmethod
    def concat_address(adr, port):
        tmp_port = str(port or "")
        if tmp_port == "":
            return adr
        else:
            return adr + ":" + tmp_port


def unregister(to_close):
    try:
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


print("start")

first_time = True
number = 0
none_found = ProcessConnections("no process found", "")
process_connections = ProcessConnections.read_process_connections()
network_lines = {}
ns = time.time_ns()
ns2 = ns
delay = 500000000
try:
    # would send other packets too: we don't care for those
    with pydivert.WinDivert("tcp or udp") as w:
        for packet in w:
            if first_time:
                atexit.register(unregister, w)
                first_time = False
            # if number < 1:
            if time.time_ns() - ns2 > delay * 6:
                ns2 = time.time_ns()
                print("loaded")
                process_connections = ProcessConnections.read_process_connections()
                # number = 1000
            # number -= 1
            # print(packet)
            networkPacket = NetworkPacket(datetime.datetime.now(), packet)
            network_line = network_lines.get(networkPacket.discriminator, None)
            if network_line is None:
                process_connection = process_connections.get(
                    networkPacket.local_address, none_found
                )
                network_lines[networkPacket.discriminator] = \
                    {
                        'packet': networkPacket,
                        'process': none_found,
                        'count': 1
                    }
            else:
                if network_line['process'] is none_found:  # and network_line['count'] % 20 == 0:
                    network_line['process'] = process_connections.get(
                        network_line['packet'].local_address, none_found
                    )
                network_line['packet'] = networkPacket
                network_line['count'] += 1
            # print("NEW ONE")
            if time.time_ns() - ns > delay * 10:
                ns = time.time_ns()
                for key in list(network_lines.keys()):
                    line = network_lines[key]
                    tmp_packet = line['packet']
                    # time since tmp_packet was added until now, in minutes
                    minutes_diff = (networkPacket.timestamp - tmp_packet.timestamp).total_seconds() / 60.0
                    # delete after 3 minutes since the packet discriminator has been last seen
                    if minutes_diff > 2:
                        # print("one less now")
                        del network_lines[key]
                    else:
                        tmp_process = line['process'].process
                        tmp_count = line['count']
                        print(
                            "{:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s} // {:10d} times".format(
                                tmp_packet.timestamp_text, tmp_packet.type, tmp_packet.direction,
                                tmp_packet.local_address, tmp_packet.remote_address, tmp_process, tmp_count
                            )
                        )
            # print(
            #     "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
            #         networkPacket.timestamp, networkPacket.type, networkPacket.direction, networkPacket.local_address,
            #         networkPacket.remote_address, process_connection.process)
            # )
            w.send(packet)
except KeyboardInterrupt:
    print("shutting down")
