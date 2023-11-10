## Computer Networks Assignment - 2

### Overview

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
