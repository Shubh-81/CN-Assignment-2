import argparse
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import os
import threading


# Custom topology class
class MyNetworkTopo(Topo):
    def build(self, **_opts):
        # Add switches and hosts
        s1, s2 = [self.addSwitch(s) for s in ['s1', 's2']]
        h1, h2, h3, h4 = [self.addHost(h, ip='10.0.0.%d/24' % i) for i, h in
                          enumerate(['h1', 'h2', 'h3', 'h4'], start=1)]
        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(s1, s2)


# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Mininet TCP client-server using iPerf3")
    parser.add_argument('--config', choices=['b', 'c'], required=True, help='Configuration type')
    parser.add_argument('--congestion', default='reno', help='Congestion control scheme')
    parser.add_argument('--loss', type=float, default=0, help='Link loss rate')
    return parser.parse_args()


def start_iperf_servers(net, server, ports):
    for port in ports:
        server.cmd('iperf3 -s -p ' + str(port) + ' &')


def run_iperf_client(net, host_name, server_ip, port, output_file):
    host = net.get(host_name)
    host.cmd('iperf3 -c ' + server_ip + ' -p ' + str(port) + ' -t 60 > ' + output_file + ' 2>&1')


def run_iperf_test(net, congestion, config):
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

    for h in [h1, h2, h3]:
        h.cmd('sysctl -w net.ipv4.tcp_congestion_control=' + congestion)

    if config == 'b':
        h4.cmd('iperf3 -s &')
        result = h1.cmd('iperf3 -c 10.0.0.4 -t 60')

    elif config == 'c':
        # Start multiple server instances on different ports
        start_iperf_servers(net, h4, [5201, 5202, 5203])

        # Run iPerf3 clients on h1, h2, and h3 in separate threads
        threads = []
        ports = [5201, 5202, 5203]
        for i, host in enumerate(['h1', 'h2', 'h3']):
            output_file = '/tmp/iperf3_' + host + '.log'
            thread = threading.Thread(target=run_iperf_client, args=(net, host, '10.0.0.4', ports[i], output_file))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        result = ""
        for host in ['h1', 'h2', 'h3']:
            output_file = '/tmp/iperf3_' + host + '.log'
            with open(output_file, 'r') as file:
                result += host + " output:\n" + file.read() + "\n"

    return result


def run():
    args = parse_args()

    topo = MyNetworkTopo()
    net = Mininet(topo=topo, switch=OVSSwitch, link=TCLink, waitConnected=True)

    if args.loss:
        for link in net.links:
            link.intf1.config(loss=args.loss)
            link.intf2.config(loss=args.loss)

    try:
        net.start()
        output = run_iperf_test(net, args.congestion, args.config)
        print(output)
    finally:
        # Ensure clean termination of iPerf processes
        for host in net.hosts:
            host.cmd('killall -9 iperf3')
        net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
