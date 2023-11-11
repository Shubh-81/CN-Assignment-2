## Computer Networks Assignment - 2

## Question 1
### Overview q1.py

This Python script, `q1.py`, utilizes the Mininet network emulator to create a simulated network environment. The script defines a custom network topology with three routers configured to route traffic between three different IP subnets, each subnet connected to two hosts. This setup demonstrates the basics of IP routing and network topology design.

### Prerequisites

- **Python 3:** The script is written in Python 3.
- **Mininet:** An environment for network emulation using Linux.
- **Root Privileges:** Required for network manipulation.

### Components

#### 1. **LinuxRouter Class**
   - **Purpose:** Acts as a router with IP forwarding enabled.
   - **Methods:**
     - `config()`: Enables IP forwarding.
     - `terminate()`: Disables IP forwarding and cleans up.

#### 2. **NetworkTopo Class**
   - **Purpose:** Defines the network topology.
   - **Topology:**
     - **Routers (`ra`, `rb`, `rc`):** Three routers connected in a triangle.
     - **Hosts (`h1` to `h6`):** Six hosts divided into three subnets, each connected to a router.
     - **Switches (`sa`, `sb`, `sc`):** Connects hosts to routers.
   - **Build Method:** Sets up the routers, switches, and hosts, along with their connections.

#### 3. **run() Function**
   - **Purpose:** Initializes and starts the network simulation.
   - **Steps:**
     - Constructs the network with `NetworkTopo`.
     - Assigns IP addresses to router interfaces.
     - Configures static routes for inter-router communication.
     - Displays routing tables of routers.
     - Opens Mininet CLI for user interaction.
     - Stops the network on exit.

### Execution

1. **Run the Script:**
   - Command: `sudo python3 q1.py`
   - This must be executed with root privileges due to the requirement of network manipulation.

2. **Interact with the Network:**
   - Once the script is running, the Mininet CLI is accessible.
   - Use Mininet commands to interact with the network, test connectivity, etc.

3. **Exit Simulation:**
   - Use the `exit` command in Mininet CLI.
   - The script will clean up and terminate the network.
  
## Question 2

### Overview of `q2.py`

This Python script, `q2.py`, is designed to demonstrate TCP performance in a network using Mininet and iPerf3. It creates a custom network topology and allows users to test TCP throughput under different congestion control algorithms and link conditions. 

### Prerequisites

- **Python 3:** The script is written in Python 3.
- **Mininet:** A network emulation environment using Linux.
- **iPerf3:** A tool for active measurements of the maximum achievable bandwidth on IP networks.
- **Root Privileges:** Necessary for network operations.

### Components

#### 1. **MyNetworkTopo Class**
   - **Purpose:** Defines the network topology for the experiment.
   - **Topology:**
     - **Switches (`s1`, `s2`):** Two switches.
     - **Hosts (`h1` to `h4`):** Four hosts with IP addresses in the `10.0.0.0/24` subnet.
   - **Build Method:** Sets up the switches and hosts, and links them together.

#### 2. **Argument Parsing Function**
   - **Purpose:** Parses command-line arguments for various configurations.
   - **Parameters:**
     - `--config`: Chooses between different test configurations.
     - `--congestion`: Specifies the TCP congestion control algorithm.
     - `--loss`: Sets the link loss rate.

#### 3. **iPerf3 Test Functions**
   - **start_iperf_servers()**: Starts iPerf3 servers on specified ports.
   - **run_iperf_client()**: Executes iPerf3 client operations.
   - **run_iperf_test()**: Orchestrates the iPerf3 testing process, including starting server and client instances and collecting results.

#### 4. **run() Function**
   - **Purpose:** Initializes and executes the network test.
   - **Steps:**
     - Parses command-line arguments.
     - Creates the network topology with `MyNetworkTopo`.
     - Configures link loss if specified.
     - Starts the network and runs the iPerf3 test.
     - Prints test results and ensures clean shutdown of the network and processes.

### Execution

1. **Run the Script:**
   - Command: `sudo python3 q2.py --config [b/c] --congestion [algorithm] --loss [rate]`
   - Requires root privileges for network configuration.

2. **Conduct Network Tests:**
   - The script will automatically start the iPerf3 servers and clients based on provided arguments, conducting the TCP performance tests.

3. **Review Test Results:**
   - Test results are printed to the console for analysis.

4. **Exit and Clean Up:**
   - The script ensures a clean termination of iPerf3 processes and stops the network.


