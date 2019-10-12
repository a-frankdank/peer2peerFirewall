# -*- coding: UTF-8 -*-

import pydivert

import atexit

def unregister(to_close):
    try:
        print("unregistering")
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


def main_loop():
    first_time = True
    # print("in main_loop")
    try:

# that alone slows your available bandwidth to half of its real possibility!
#         Ping
#         ms
#         22
#         Download
#         Mbps
#         10.59
#         Upload
#         Mbps
#         5.18

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

                # print(
                #     "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                #         network_packet.timestamp, network_packet.type, network_packet.direction,
                #         network_packet.local_address,
                #         network_packet.remote_address, process_connection.process)
                # )
    except KeyboardInterrupt:
        print("shutting down")


print("start")
main_loop()
