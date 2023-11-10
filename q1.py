from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    """A network topology with three routers connected in a triangle and six hosts in three subnets."""

    def build(self, **_opts):
        # Add routers
        ra = self.addNode('ra', cls=LinuxRouter, ip='192.168.1.1/24')
        rb = self.addNode('rb', cls=LinuxRouter, ip='172.16.0.1/12')
        rc = self.addNode('rc', cls=LinuxRouter, ip='10.0.0.1/8')

        # Add switches for connecting hosts to routers
        sa, sb, sc = [self.addSwitch('s' + r) for r in ['1', '2', '3']]

        # Add links between routers
        self.addLink(ra, rb, intfName1='ra-eth2', intfName2='rb-eth2')
        self.addLink(rb, rc, intfName1='rb-eth3', intfName2='rc-eth2')
        self.addLink(rc, ra, intfName1='rc-eth3', intfName2='ra-eth3')

        # Add links between routers and switches
        self.addLink(sa, ra, intfName2='ra-eth1', params2={'ip': '192.168.1.1/24'})
        self.addLink(sb, rb, intfName2='rb-eth1', params2={'ip': '172.16.0.1/12'})
        self.addLink(sc, rc, intfName2='rc-eth1', params2={'ip': '10.0.0.1/8'})

        # Add hosts and connect them to their respective switches
        h1 = self.addHost('h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.1.101/24', defaultRoute='via 192.168.1.1')
        self.addLink(h1, sa)
        self.addLink(h2, sa)

        h3 = self.addHost('h3', ip='172.16.0.100/12', defaultRoute='via 172.16.0.1')
        h4 = self.addHost('h4', ip='172.16.0.101/12', defaultRoute='via 172.16.0.1')
        self.addLink(h3, sb)
        self.addLink(h4, sb)

        h5 = self.addHost('h5', ip='10.0.0.100/8', defaultRoute='via 10.0.0.1')
        h6 = self.addHost('h6', ip='10.0.0.101/8', defaultRoute='via 10.0.0.1')
        self.addLink(h5, sc)
        self.addLink(h6, sc)


def run():
    """Test the network"""
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    # Assigning IP addresses for inter-router links
    net['ra'].cmd('ifconfig ra-eth2 192.168.12.1/30')
    net['rb'].cmd('ifconfig rb-eth2 192.168.12.2/30')
    net['rb'].cmd('ifconfig rb-eth3 192.168.23.1/30')
    net['rc'].cmd('ifconfig rc-eth2 192.168.23.2/30')
    net['rc'].cmd('ifconfig rc-eth3 192.168.13.1/30')
    net['ra'].cmd('ifconfig ra-eth3 192.168.13.2/30')

    # Static routes for ra
    net['ra'].cmd('ip route add 172.16.0.0/12 via 192.168.12.2')
    net['ra'].cmd('ip route add 10.0.0.0/8 via 192.168.13.1')

    # Static routes for rb
    net['rb'].cmd('ip route add 192.168.1.0/24 via 192.168.12.1')
    net['rb'].cmd('ip route add 10.0.0.0/8 via 192.168.23.2')

    # Static routes for rc
    net['rc'].cmd('ip route add 192.168.1.0/24 via 192.168.13.2')
    net['rc'].cmd('ip route add 172.16.0.0/12 via 192.168.23.1')

    info('*** Routing Table on Router ra:\n')
    info(net['ra'].cmd('route'))
    info('*** Routing Table on Router rb:\n')
    info(net['rb'].cmd('route'))
    info('*** Routing Table on Router rc:\n')
    info(net['rc'].cmd('route'))

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
