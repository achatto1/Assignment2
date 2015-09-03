from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

#code has been zero indexed

class CustomTopo(Topo):
	"Single switch connected to n hosts."
	def build(self, num_hosts=4, num_switches=2):
		switches = []
		hosts = []
		for s in range(num_switches):
			switch = self.addSwitch('s%s' % (s))
			switches.append(switch)
			
			host = self.addHost('h%s' % (2*(s)), bw=2)
			self.addLink(host, switch)
			hosts.append(host)			

			host = self.addHost('h%s' % (2*(s) + 1), bw=1)
			self.addLink(host, switch)
			hosts.append(host)	

		
		for s in range(num_switches - 1):
			self.addLink(switches[s], switches[(s+1)])		


def simpleTest(num_hosts, num_switches):
	"Create and test a simple network"
	topo = CustomTopo(num_hosts, num_switches)
	net = Mininet(topo)
	net.start()
	#net.addController('c0', controller=RemoteController,ip="127.0.0.1",port=6633)
	for i in range(num_hosts):
        	for j in range(num_hosts):
            		if (i-j)%2 == 1:
                		h1 = net.get("h"+str(i))
				h2 = net.get("h"+str(j))
				h1.cmd("iptables -A OUTPUT -o h"+str(i)+"-eth0 -d 10.0.0."+ str(j+1)+" -j DROP")
				
				
	print "Dumping host connections"
	#dumpNodeConnections(net.hosts)
	dumpNodeConnections(net.switches)
	print "Testing network connectivity"
	net.pingAll()
	net.stop()

if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	x = input("Number of hosts: ")
	y = input("Number of switches: ")
	simpleTest(x, y)
