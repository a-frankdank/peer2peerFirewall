# -*- coding: UTF-8 -*-

import pydivert
from pydivert import Packet

import datetime
import time

import atexit

import psutil

from appJar import gui


class ProcessConnections:
    """the process and its connections as extracted from psutils"""

    inner_process_connections = {}
    checked = {}
    processes = {}

    def __init__(self, process: str = "", local_address: str = ""):  # , right_address: str = ""):
        self.process = process
        self.local_address = local_address
        # self.right_address = right_address

    @staticmethod
    def read_process_connections():

        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                key3 = str(pid) + "/" + str(process.create_time())
                if ProcessConnections.checked.get(key3, None) is None:
                    ProcessConnections.checked[key3] = 1
                    if process.name():
                        ProcessConnections.processes[pid] = process.name()
            except psutil.NoSuchProcess:
                pass

        for connection in psutil.net_connections():
            # [sconn(fd=115, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            #     ip='10.0.0.1', port=48776), raddr = addr(ip='93.186.135.91', port=80), status = 'ESTABLISHED', pid = 1254),
            # sconn(fd=117, family= < AddressFamily.AF_INET: 2 >, type = < SocketType.SOCK_STREAM: 1 >, laddr = addr(
            #     ip='10.0.0.1', port=43761), raddr = addr(ip='72.14.234.100', port=80), status = 'CLOSING', pid = 2987),
            # ...]

            process_string = ProcessConnections.processes.get(connection.pid, connection.pid)
            left_address = NetworkPacket.concat_address(str(connection.laddr.ip), str(connection.laddr.port))
            # do i really need the r address
            # right_address = ""
            # if connection.raddr:
            #     right_address = NetworkPacket.concat_address(str(connection.raddr.ip), str(connection.raddr.port))
            ProcessConnections.inner_process_connections[left_address] = \
                ProcessConnections(process_string, left_address)  # , right_address)

            # print("paused till you type")
            # input()

            # for key2 in ProcessConnections.inner_process_connections.keys():
            #     print(
            #         "process conn: " + ProcessConnections.inner_process_connections[key2].process
            #         + "//" + ProcessConnections.inner_process_connections[key2].local_address
            #         + "//" + ProcessConnections.inner_process_connections[key2].right_address
            #           )

        return ProcessConnections.inner_process_connections


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


def unregister(to_close):
    try:
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


def renew_process(process: ProcessConnections, packet2: NetworkPacket, process_connections2):
    new_process = process
    if new_process is none_found:  # and network_line['count'] % 20 == 0:
        new_process = process_connections2.get(
            packet2.local_address, none_found
        )
        if new_process is none_found:
            new_process = process_connections2.get(
                "0.0.0.0:" + str(packet2.local_port), none_found
            )
            if new_process is none_found:
                new_process = process_connections2.get(
                    ":::" + str(packet2.local_port), none_found
                )
    return new_process


def infinite_loop():
    print("start")
    first_time = True
    number = 0
    process_connections = ProcessConnections.read_process_connections()
    network_lines = {}
    ns = time.time_ns()
    ns2 = ns
    delay = 5000000000
    delay_p_c = 20000000
    to_refresh = None
    total_lines = 0
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
                # if number < 1:
                if time.time_ns() - ns2 > delay_p_c:
                    ns2 = time.time_ns()
                    # print("loaded")
                    process_connections = ProcessConnections.read_process_connections()
                    # number = 1000
                # number -= 1
                # print(packet)
                network_packet = NetworkPacket(datetime.datetime.now(), packet)
                network_line = network_lines.get(network_packet.discriminator, None)
                if network_line is None:
                    process_connection = process_connections.get(
                        network_packet.local_address, none_found
                    )
                    network_lines[network_packet.discriminator] = \
                        {
                            'packet': network_packet,
                            'process': process_connection,
                            'count': 1
                        }
                else:
                    network_line['process'] = renew_process(network_line['process'], network_packet, process_connections)
                    network_line['packet'] = network_packet
                    network_line['count'] += 1
                if to_refresh is not None:
                    network_line = network_lines[to_refresh]
                    network_line['process'] = renew_process(network_line['process'], network_line['packet'],
                                                            process_connections)
                    to_refresh = None
                # print("NEW ONE")
                if time.time_ns() - ns > delay:
                    ns = time.time_ns()
                    print("")
                    if total_lines == 0:
                        app.queueFunction(app.removeAllWidgets)
                        app.queueFunction(app.startScrollPane, "PANE")
                    else:
                        app.queueFunction(app.openScrollPane, "PANE")
                    keys = list(network_lines.keys())
                    line_nr = 0
                    for key in keys:
                        line = network_lines[key]
                        tmp_packet = line['packet']
                        # time since tmp_packet was added until now, in minutes
                        minutes_diff = (network_packet.timestamp - tmp_packet.timestamp).total_seconds() / 60.0
                        # delete after 3 minutes since the packet discriminator has been last seen
                        if minutes_diff > 2:
                            # print("one less now")
                            del network_lines[key]
                        else:
                            if line['process'] is none_found:
                                to_refresh = key
                            tmp_process = line['process'].process
                            tmp_count = line['count']

                            tmp_function = app.addLabel
                            if line_nr < total_lines:
                                tmp_function = app.setLabel
                                app.queueFunction(tmp_function,
                                                  "column0"+str(line_nr),
                                                  "{:16s}  {:3s}/{:3s}".format(
                                                      tmp_packet.timestamp_text,
                                                      tmp_packet.type,
                                                      tmp_packet.direction)
                                                  )
                                app.queueFunction(tmp_function, "column3"+str(line_nr), tmp_packet.local_address)
                                app.queueFunction(tmp_function, "column4"+str(line_nr), tmp_packet.remote_address)
                                app.queueFunction(tmp_function, "column5"+str(line_nr), tmp_process)
                                app.queueFunction(tmp_function, "column6"+str(line_nr), tmp_count)
                            else:
                                app.queueFunction(tmp_function,
                                                  "column0" + str(line_nr),
                                                  "{:16s}  {:3s}/{:3s}".format(
                                                      tmp_packet.timestamp_text,
                                                      tmp_packet.type,
                                                      tmp_packet.direction),
                                                  line_nr, 0)
                                app.queueFunction(tmp_function, "column3" + str(line_nr), tmp_packet.local_address,
                                                  line_nr, 1)
                                app.queueFunction(tmp_function, "column4" + str(line_nr), tmp_packet.remote_address,
                                                  line_nr, 2)
                                app.queueFunction(tmp_function, "column5" + str(line_nr), tmp_process, line_nr, 3)
                                app.queueFunction(tmp_function, "column6" + str(line_nr), tmp_count, line_nr, 4)

                            # app.queueFunction(
                            #     app.addLabel,
                            #     key,
                            #     "{:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s} // {:10d} times".format(
                            #                       tmp_packet.timestamp_text, tmp_packet.type, tmp_packet.direction,
                            #                       tmp_packet.local_address, tmp_packet.remote_address, tmp_process,
                            #                       tmp_count
                            #                   )
                            #                  )
                            print(
                                "{:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s} // {:10d} times".format(
                                    tmp_packet.timestamp_text, tmp_packet.type, tmp_packet.direction,
                                    tmp_packet.local_address, tmp_packet.remote_address, tmp_process, tmp_count
                                )
                            )
                        line_nr += 1
                    app.queueFunction(app.stopScrollPane)
                    total_lines = line_nr
                # print(
                #     "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                #         network_packet.timestamp, network_packet.type, network_packet.direction,
                #         network_packet.local_address,
                #         network_packet.remote_address, process_connection.process)
                # )
    except KeyboardInterrupt:
        print("shutting down")


none_found = ProcessConnections("no process found", "")

app = gui("peer2peerFirewall", "1000x500")

app.setStretch("column")
app.addLabel("l1", "starting up...")
app.thread(infinite_loop)

app.go()
