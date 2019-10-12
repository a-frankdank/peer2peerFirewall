# -*- coding: UTF-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict

import pydivert
from pydivert import Packet

import datetime
import time

import atexit

import psutil

import threading
import concurrent.futures
import copy


class ProcessConnection:
    """the process and one of its connections as extracted from psutils"""

    inner_process_connections = {}
    inner_process_connections_lock = threading.Lock()

    checked = {}
    processes = {}

    ns2 = None

    def __init__(self, process: str = "", local_address: str = ""):
        self.process = process
        self.local_address = local_address

    @staticmethod
    def assemble_process_connections():
        """assembles all ProcessConnections possible into inner_process_connections"""

        ProcessConnection.update_processes_cache()

        for connection in psutil.net_connections():
            # [sconn(fd=115, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            # ip='10.0.0.1', port=48776), raddr = addr(ip='93.186.135.91', port=80), status ='ESTABLISHED', pid = 1254),
            # sconn(fd=117, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            #  ip='10.0.0.1', port=43761), raddr = addr(ip='72.14.234.100', port=80), status = 'CLOSING', pid = 2987),
            # ...]

            process_string = ProcessConnection.processes.get(connection.pid, connection.pid)
            # process_string = psutil.Process(connection.pid).name()
            # if process_string is None:
            #     process_string = connection.pid

            left_address = NetworkPacket.concat_address(connection.laddr.ip, connection.laddr.port)

            with ProcessConnection.inner_process_connections_lock:
                ProcessConnection.inner_process_connections[left_address] = \
                    ProcessConnection(
                        process_string,
                        left_address
                    )

    @staticmethod
    def update_processes_cache():
        """updates the process cache (id + name)"""

        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                key3 = str(pid) + "/" + str(process.create_time())
                if ProcessConnection.checked.get(key3, None) is None:
                    ProcessConnection.checked[key3] = 1
                    if process.name():
                        ProcessConnection.processes[pid] = process.name()
            except psutil.NoSuchProcess:
                pass

    @staticmethod
    def read_process_connections():
        """returns a Dict[str, ProcessConnection]"""
        with ProcessConnection.inner_process_connections_lock:
            tmp_copy = copy.copy(ProcessConnection.inner_process_connections)
        return tmp_copy

    @staticmethod
    def loop_assembly():
        ns2 = time.time_ns()
        delay_p_c = 20000000
        # print("in loop_assembly")
        try:
            while True:
                if time.time_ns() - ns2 > delay_p_c:
                    ns2 = time.time_ns()
                    # print("loaded")
                    ProcessConnection.assemble_process_connections()
        except KeyboardInterrupt:
            print("shutting down")


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
            self.local_port = packet_input.src_port
            self.remote_address = dst_address
        else:
            self.local_address = dst_address
            self.local_port = packet_input.dst_port
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


class NetworkLine:
    """one network line contains one NetworkPacket information, combined with its the corresponding process and
       occurrence count """

    process_connections = None

    network_lines = {}
    network_lines_lock = threading.Lock()

    ns = None

    def __init__(self, packet_input: NetworkPacket = None, count: int = 0):
        self.packet = packet_input
        if NetworkLine.process_connections is None:
            NetworkLine.process_connections = ProcessConnection.read_process_connections()
        self.process = NetworkLine.process_connections.get(packet_input.local_address, none_found)
        self.count = count

    def update(self, network_packet: NetworkPacket):
        self.packet = network_packet
        self.renew_process()
        self.count += 1

    def renew_process(self):
        new_process = self.process
        if new_process is none_found:
            new_process = NetworkLine.process_connections.get(self.packet.local_address, none_found)
            if new_process is none_found:
                tmp_port = str(self.packet.local_port)
                new_process = NetworkLine.process_connections.get("0.0.0.0:" + tmp_port, none_found)
                if new_process is none_found:
                    new_process = NetworkLine.process_connections.get(":::" + tmp_port, none_found)
                    if new_process is none_found:
                        # print("re-read process_connections")
                        NetworkLine.process_connections = ProcessConnection.read_process_connections()
            self.process = new_process

    def print(self):
        """prints to console"""

        print(
            "{:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s} // {:10d} times".format(
                self.packet.timestamp_text, self.packet.type, self.packet.direction,
                self.packet.local_address, self.packet.remote_address,
                self.process.process, self.count
            )
        )

    @staticmethod
    def print_all_lines():
        print("")
        for key in list(NetworkLine.network_lines.keys()):
            line = NetworkLine.network_lines[key]
            # time since line.packet was added until now, in minutes
            minutes_diff = (datetime.datetime.now() - line.packet.timestamp).total_seconds() / 60.0
            # delete after 3 minutes since the packet discriminator has been last seen
            if minutes_diff > 2:
                # print("one less now")
                with NetworkLine.network_lines_lock:
                    del NetworkLine.network_lines[key]
            else:
                if line.process is none_found:
                    line.renew_process()
                line.print()

    @staticmethod
    def add_line(network_packet):
        network_line = NetworkLine.network_lines.get(network_packet.discriminator, None)
        if network_line is None:
            with NetworkLine.network_lines_lock:
                NetworkLine.network_lines[network_packet.discriminator] = NetworkLine(network_packet, 1)
        else:
            network_line.update(network_packet)

    @staticmethod
    def print_loop():
        ns = time.time_ns()
        delay = 5000000000
        # print("in print loop")
        try:
            while True:
                if time.time_ns() - ns > delay:
                    ns = time.time_ns()
                    NetworkLine.print_all_lines()
        except KeyboardInterrupt:
            print("shutting down")


def unregister(to_close):
    try:
        print("unregistering")
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


def add_packet(packet: Packet):
    network_packet = NetworkPacket(datetime.datetime.now(), packet)
    NetworkLine.add_line(network_packet)


def main_loop():
    first_time = True
    ProcessConnection.ns2 = time.time_ns()
    NetworkLine.ns = time.time_ns()
    # print("in main_loop")
    try:
        # would send other packets too: we don't care for those
        with pydivert.WinDivert("tcp or udp") as w:
            for packet in w:
                try:
                    w.send(packet)
                except OSError:
                    pass
                if first_time:
                    atexit.register(unregister, w)
                    first_time = False
                # print(packet)
                if time.time_ns() - ProcessConnection.ns2 > 20000000:
                    ProcessConnection.ns2 = time.time_ns()
                    ProcessConnection.assemble_process_connections()
                if time.time_ns() - NetworkLine.ns > 5000000000:
                    NetworkLine.ns = time.time_ns()
                    NetworkLine.print_all_lines()
                add_packet(packet)
                # print(
                #     "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                #         network_packet.timestamp, network_packet.type, network_packet.direction,
                #         network_packet.local_address,
                #         network_packet.remote_address, process_connection.process)
                # )
    except KeyboardInterrupt:
        print("shutting down")


print("start")
none_found = ProcessConnection("no process found", "")
main_loop()
# with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#    executor.submit(ProcessConnection.loop_assembly)
#    executor.submit(main_loop, executor)
#    executor.submit(NetworkLine.print_loop)
