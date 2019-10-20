# -*- coding: UTF-8 -*-
from typing import Dict

import pydivert
from pydivert import Packet

import datetime
import time

import atexit

import psutil


class ProcessConnection:
    """the process and one of its connections as extracted from psutils"""

    def __init__(self, process: str = "", pid: int = -1, local_address: str = ""):
        self.process = process
        self.pid = pid
        self.local_address = local_address


class ProcessConnections:
    """contains a dictionary of all ProcessConnection objects, and the logic to create that dictionary"""

    none_found: ProcessConnection = ProcessConnection("no process found", -1, "")

    def __init__(self):
        self.__inner_process_connections: Dict[str, ProcessConnection] = {}

        self.__checked: Dict[str, int] = {}
        self.__processes: Dict[int, str] = {}

        self.pc_ns: int = time.time_ns()

    def clear(self) -> None:
        self.__inner_process_connections = {}

        self.__checked = {}
        self.__processes = {}

        self.pc_ns = time.time_ns()

    def assemble_process_connections(self) -> None:
        """assembles all ProcessConnections possible into"""

        self.__update_processes_cache()

        for connection in psutil.net_connections():
            # [sconn(fd=115, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            # ip='10.0.0.1', port=48776), raddr = addr(ip='93.186.135.91', port=80), status ='ESTABLISHED', pid = 1254),
            # sconn(fd=117, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            #  ip='10.0.0.1', port=43761), raddr = addr(ip='72.14.234.100', port=80), status = 'CLOSING', pid = 2987),
            # ...]

            process_string = self.__processes.get(connection.pid, connection.pid)

            left_address = NetworkPacket.concat_address(connection.laddr.ip, connection.laddr.port)

            self.__inner_process_connections[left_address] = \
                ProcessConnection(
                    process_string,
                    connection.pid,
                    left_address
                )

    def __update_processes_cache(self) -> None:
        """updates the process cache (id + name)"""

        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                key3 = f"{pid}/{process.create_time()}"
                if self.__checked.get(key3, None) is None:
                    self.__checked[key3] = 1
                    if process.name():
                        if process.name() == "svchost.exe":
                            service_names = [process.name()]
                            for service in psutil.win_service_iter():
                                if service.pid() == pid:
                                    service_names.append(service.name())
                            self.__processes[pid] = "/".join(service_names)
                        else:
                            self.__processes[pid] = process.name()
                    else:
                        self.__processes[pid] = pid
            except psutil.NoSuchProcess:
                pass

    def read_process_connections(self) -> Dict[str, ProcessConnection]:
        return self.__inner_process_connections.copy()


class NetworkPacket:
    """the network packet received or sent"""

    def __init__(self, timestamp: datetime, packet_input: Packet = None):
        self.direction = "OUT" if packet_input.is_outbound else "IN"
        self.type = "TCP" if packet_input.tcp else ("UDP" if packet_input.udp else "UNKNOWN")
        src_address = NetworkPacket.concat_address(packet_input.src_addr, packet_input.src_port)
        dst_address = NetworkPacket.concat_address(packet_input.dst_addr, packet_input.dst_port)
        # "we" aka my ip is always the local address, as being always left in comodo
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
        # self.discriminator = self.type + self.direction + self.local_address + self.remote_address
        self.discriminator = f"{self.type}{self.direction}{self.local_address}{self.remote_address}"

    @staticmethod
    def concat_address(adr, port):
        if port is None:
            return adr
        else:
            return f"{adr}:{port}"


class NetworkLine:
    """one network line contains one NetworkPacket information, combined with its the corresponding process and
       occurrence count """

    def __init__(self, process_connections2: Dict[str, ProcessConnection], packet_input: NetworkPacket = None,
                 count: int = 0):
        self.packet = packet_input
        if packet_input is None:
            self.process = ProcessConnection()
            self.timestamp_first_occurrence = None
            self.timestamp_first_occurrence_text = None
        else:
            self.process = ProcessConnections.none_found
            self.renew_process(process_connections2)
            self.timestamp_first_occurrence = packet_input.timestamp
            self.timestamp_first_occurrence_text = packet_input.timestamp_text
        self.count = count

    def update(self, network_packet: NetworkPacket, process_connections2: Dict[str, ProcessConnection]):
        self.packet = network_packet
        self.renew_process(process_connections2)
        self.count += 1

    def renew_process(self, process_connections2: Dict[str, ProcessConnection]):
        new_process = self.process
        if new_process is ProcessConnections.none_found:
            new_process = process_connections2.get(self.packet.local_address,
                                                   ProcessConnections.none_found)
            if new_process is ProcessConnections.none_found:
                tmp_port = str(self.packet.local_port)
                new_process = process_connections2.get("0.0.0.0:" + tmp_port,
                                                       ProcessConnections.none_found)
                if new_process is ProcessConnections.none_found:
                    new_process = process_connections2.get(":::" + tmp_port,
                                                           ProcessConnections.none_found)
            self.process = new_process

    def print(self):
        """prints to console"""

        print(
            "{:15s} {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s} // {:10d} times".format(
                self.packet.timestamp_text, self.timestamp_first_occurrence_text, self.packet.type,
                self.packet.direction, self.packet.local_address, self.packet.remote_address,
                self.process.process, self.count
            )
        )


class NetworkLines:
    """contains all NetworkLines there are"""

    def __init__(self, process_connections2: ProcessConnections):
        self.__process_connections_cache: Dict[str, ProcessConnection] = process_connections2.read_process_connections()
        self.__process_connections: ProcessConnections = process_connections2

        self.__network_lines: Dict[str, NetworkLine] = {}

        self.nl_ns = time.time_ns()

    def clear(self):
        self.__process_connections_cache = None

        self.__network_lines = {}

        self.nl_ns = time.time_ns()

    def print_all_lines(self):
        print("")
        for line in list(self.__network_lines.values()):
            line.print()

    def reduce_lines(self):
        now = datetime.datetime.now()
        new_lines = {}
        for line in self.__network_lines.values():
            # time since line.packet was added until now, in minutes
            minutes_diff = (now - line.packet.timestamp).total_seconds() / 60.0
            # delete after 3 minutes since the packet discriminator has been last seen
            if minutes_diff < 2:
                if line.process is ProcessConnections.none_found:
                    self.__process_connections_cache = self.__process_connections.read_process_connections()
                    line.renew_process(self.__process_connections_cache)
                new_lines[line.packet.discriminator] = line
        self.__network_lines = new_lines

    def add_line(self, packet: Packet):
        network_packet = NetworkPacket(datetime.datetime.now(), packet)
        network_line = self.__network_lines.get(network_packet.discriminator, None)
        if network_line is None:
            self.__network_lines[network_packet.discriminator] = \
                NetworkLine(self.__process_connections_cache,
                            network_packet,
                            1)
        else:
            if network_line.process is ProcessConnections.none_found:
                self.__process_connections_cache = self.__process_connections.read_process_connections()
            network_line.update(network_packet, self.__process_connections_cache)

    def read_network_lines(self) -> Dict[str, NetworkLine]:
        """returns a Dict[str, NetworkLine]"""
        return self.__network_lines.copy()


# TODO go on
class ProcessTraffic:
    """contains a process grouped together with all its identified NetworkLines"""

    def __init__(self, process: ProcessConnection = None):
        self.process_connection = process
        self.network_lines = []


# begin of 'main' logic
process_connections: ProcessConnections = ProcessConnections()
network_lines: NetworkLines = NetworkLines(process_connections)
stop_it = False


def read_network_lines() -> Dict[str, NetworkLine]:
    """returns a Dict[str, NetworkLine]"""
    return network_lines.read_network_lines()


def unregister(to_close):
    try:
        print("unregistering")
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e


def stop():
    global stop_it
    stop_it = True


def main_loop(
        win_divert_filter: str = "tcp or udp",
        do_print: bool = False,
):
    print("filter: " + win_divert_filter)
    global stop_it
    stop_it = False
    first_time = True
    # print("in main_loop")
    try:
        # would send other packets too: we don't care for those
        divert = pydivert.WinDivert(win_divert_filter)
        divert.open()
        while stop_it is False:
            packet = divert.recv()
            try:
                divert.send(packet)
            except OSError:
                pass
            if first_time:
                atexit.register(unregister, divert)
                first_time = False
            if stop_it:
                network_lines.clear()
                process_connections.clear()
                break
            else:
                # print(packet)
                if time.time_ns() - process_connections.pc_ns > 19000000:
                    process_connections.pc_ns = time.time_ns()
                    process_connections.assemble_process_connections()
                if time.time_ns() - network_lines.nl_ns > 5000000000:
                    network_lines.nl_ns = time.time_ns()
                    network_lines.reduce_lines()
                    if do_print:
                        network_lines.print_all_lines()
                network_lines.add_line(packet)
                # print(
                #     "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                #         network_packet.timestamp, network_packet.type, network_packet.direction,
                #         network_packet.local_address,
                #         network_packet.remote_address, process_connection.process)
                # )
        divert.close()
        divert.unregister()
    except KeyboardInterrupt:
        print("shutting down")
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e


if __name__ == "__main__":
    print("start")

    print("wanna take input from tcp, or udp, or both? default: both")
    decision = input()
    if decision == "udp":
        main_loop("udp", True)
    else:
        if decision == "tcp":
            main_loop("tcp", True)
        else:
            main_loop(do_print=True)
