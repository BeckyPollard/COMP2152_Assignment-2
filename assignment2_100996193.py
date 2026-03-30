"""
Author: Becky Pollard
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

# Import the required modules (Step ii) ✓
import socket, threading, sqlite3, os, platform, datetime



# Print Python version and OS name (Step iii) ✓
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("┃ WELCOME TO THE PORT SCANNER TOOL ┃")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
print(f"Python Version: {platform.python_version()}")
print(f"Operating System: {os.name}\n")

# Create the common_ports dictionary (Step iv) ✓
# Add a 1-line comment above it explaining what it stores ✓
# This dictionary maps common network port numbers to their human-readable service names label determined by IANA.
common_ports = {
  21: "FTP",
  22: "SSH",
  23: "Telnet",
  25: "SMTP",
  53: "DNS",
  80: "HTTP",
  110: "POP3",
  143: "IMAP",
  443: "HTTPS",
  3306: "MySQL",
  3389: "RDP",
  8080: "HTTP-Alt"
}



# Create the NetworkTool parent class (Step v) ✓
#     - Constructor: takes target, stores as private self.__target
#     - @property getter for target ✓
#     - @target.setter with empty string validation ✓
#     - Destructor: prints "NetworkTool instance destroyed" ✓
class NetworkTool:
  def __init__(self, target: str):
    self.target = target

  @property
  def target(self):
    return self.__target

  @target.setter
  def target(self, value):
    if value != "":
      self.__target = value
    else:
      print("ERROR: Invalid target, cannot be empty string!")

  def __del__(self):
    print("NetworkTool instance destroyed!")
# Q3: What is the benefit of using @property and @target.setter?
# Your 2-4 sentence answer here... (Part 2, Q3)
"""
Q3 /
The @property and @target.setter decorator allows us to easily create get/set methods by transforming them
into properties. We can access target as if it were a normal property. These private attributes can be accessed
in a controlled method. Using this way also makes validation of the method data easier, like how we reject an
empty target. 
"""
# Q1: How does PortScanner reuse code from NetworkTool?
# Your 2-4 sentence answer here... (Part 2, Q1)
"""
Q1 /
PortScanner inherits from NetworkTool by calling super method super().__init__(target) in the constructor.
PortScanner can thus reuse the target attribute without programming again the handling of target.
"""


# Create the PortScanner child class that inherits from NetworkTool (Step vi) and has the fllowing:
# + Constructor: call super().__init__(target), initialize self.scan_results = [], self.lock = threading.Lock() ✓
# + Destructor: print "PortScanner instance destroyed", call super().__del__() ✓
# + scan_port(self, port): ✓
# Q4: What would happen without try-except here?
# Your 2-4 sentence answer here... (Part 2, Q4)
"""
Q4 /
Any error while scanning would cause this program to crash without this try-except. The try-except block 
allows us to account for anticipated errors and handle them gracefully, in this case with an error message. 
The exception handling allows for the program to continue. Connection issues could be one error to catch.
"""
#     - try-except with socket operations ✓
#     - Create socket, set timeout, connect_ex ✓
#     - Determine Open/Closed status (0 = "Open") ✓
#     - Look up service name from common_ports (use "Unknown" if not found) ✓
#     - Acquire lock, append (port, status, service_name) tuple, release lock ✓
#     - Close socket in finally block ✓
#     - Catch socket.error, print error message ✓
# + get_open_ports(self): ✓
#     - Use list comprehension to return only "Open" results ✓
# Q2: Why do we use threading instead of scanning one port at a time?
# Your 2-4 sentence answer here... (Part 2, Q2)
"""
Q2 /
Threading allows the scanner to run different processes at the same time, like how we scan multiple ports 
at the same time. We're scanning a lot of ports, I even tested it with 7000 looking for an open one. If we
scanned each port one at a time, it'd take longer than the instant it does cirrently. Without threading, 
each process would have to finish before the next began.
"""
# + scan_range(self, start_port, end_port):
#     - Create threads list ✓
#     - Create Thread for each port targeting scan_port ✓
#     - Start all threads (one loop) ✓
#     - Join all threads (separate loop) ✓
class PortScanner(NetworkTool):
  def __init__(self, target):
    super().__init__(target)
    self.scan_results = []
    self.lock = threading.Lock()

  def __del__(self):
    print("PortScanner instance destroyed!")
    super().__del__()

  def scan_port(self, port):
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      result = sock.connect_ex((self.target, port))
      if result == 0:
        status = "Open"
      else:
        status = "Closed"
      service_name = common_ports.get(port, "Unknown")
      self.lock.acquire()
      self.scan_results.append((port, status, service_name))
      self.lock.release()
    except socket.error:
      print(f"ERROR: something went wrong while scanning port {port}: {socket.error}")
    finally:
      if sock:
        sock.close()

  def get_open_ports(self):
    return [result for result in self.scan_results if result[1] == "Open"]

  def scan_range(self, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
      thread = threading.Thread(target = self.scan_port, args = (port,))
      threads.append(thread)
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()


# Create save_results(target, results) function (Step vii) ✓
# - Connect to scan_history.db ✓
# - CREATE TABLE IF NOT EXISTS scans (id✓, target✓, port✓, status✓, service✓, scan_date✓) ✓
# - INSERT each result with datetime.datetime.now() ✓
# - Commit, close ✓
# - Wrap in try-except for sqlite3.Error ✓
def save_results(target, results):
  try:
    connection = sqlite3.connect("scan_history.db")
    cursor = connection.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        port INTEGER,
        status TEXT,
        service TEXT,
        scan_date TEXT
      )
    """)
    for port, status, service in results:
      cursor.execute(
        """INSERT INTO scans (target, port, status, service, scan_date) VALUES (?, ?, ?, ?, ?)""",
        (target, port, status, service, str(datetime.datetime.now()))
      )
    connection.commit()
  except sqlite3.Error:
    print(f"ERROR: SQL database error: {sqlite3.Error}")
  finally:
    connection.close()

# Create load_past_scans() function (Step viii) ✓
# - Connect to scan_history.db ✓
# - SELECT all from scans ✓
# - Print each row in readable format ✓
# - Handle missing table/db: print "No past scans found." ✓
# - Close connection ✓
def load_past_scans():
  print("┏━━ Scan History ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  try:
    connection = sqlite3.connect("scan_history.db")
    cursor = connection.cursor()
    # cursor.execute("""SELECT * FROM scans""") i want to keep track of what i'm querying
    cursor.execute("""SELECT target, port, status, service, scan_date FROM scans""")
    rows = cursor.fetchall()
    if rows:
      for row in rows:
        print(f"┣━ [{row[4]}] {row[0]} || Scanned port {row[1]} ({row[3]}) - status {row[2]}")
    else:
      print("┣━ No past scans found.")
  except sqlite3.Error:
    print(f"┣━ ERROR: No past scans found because SQL database error: {sqlite3.Error}")
  finally:
    connection.close()
  print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
  # Get user input with try-except (Step ix) ✓
  # - Target IP (default "127.0.0.1" if empty) ✓
  # - Start port (1-1024) ✓
  # - End port (1-1024, >= start port) ✓
  # - Catch ValueError: "Invalid input. Please enter a valid integer." ✓
  # - Range check: "Port must be between 1 and 1024." ✓
  try:
    target = input("Please enter the target IP address (default 127.0.0.1): ").strip()
    if target == "":
      target = "127.0.0.1"
    start_port = int(input("Enter start port (between 1-1024): ").strip())
    while start_port < 1 or start_port > 1024:
      print(f"ERROR for {start_port}: Port must be between 1 and 1024.")
      start_port = int(input("Enter start port (1-1024): ").strip())
    end_port = int(input(f"Enter end port (between {start_port}-1024): ").strip())
    while end_port < start_port or end_port > 1024:
      print(f"End port must be between start port ({start_port}) and 1024.")
      end_port = int(input(f"Enter end port (between {start_port}-1024): ").strip())
  except ValueError:
    print("ERROR: Invalid input. Please enter a valid integer.")

  # After valid input (Step x)
  # - Create PortScanner object ✓
  # - Print "Scanning {target} from port {start} to {end}..." ✓
  # - Call scan_range() ✓
  # - Call get_open_ports() and print results ✓
  # - Print total open ports found ✓
  # - Call save_results() ✓
  # - Ask "Would you like to see past scan history? (yes/no): "
  # - If "yes", call load_past_scans()
  scan = PortScanner(target)
  print(f"\nScanning {target} from port {start_port} to {end_port}...\n")
  scan.scan_range(start_port, end_port)
  open_ports = scan.get_open_ports()
  print(f"┏━━ Scan Results for {target} ━━━━━━━━━━┓")
  for port, status, service in open_ports:
    print(f"┣━ Port {port}: {status} ({service})")
  print("┃")
  print(f"┃ Total open ports found: {len(open_ports)}")
  print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
  save_results(target, scan.scan_results)
  showHistoryChoice = input("\nWould you like to see past scan history? (yes/no): ").strip().lower()
  if showHistoryChoice == "yes":
    load_past_scans()


# Q5: New Feature Proposal
# Your 2-3 sentence description here... (Part 2, Q5)
# Diagram: See diagram_100996193.png in the repository root
"""
Q5 /
New feature proposal: exportable summary/report of scanned ports.
This new feature would create a method to export the results of the scan in either a txt or csv document.
It could use some nested if statments to control what kind of report document is generated.
A promt will ask the user what kind of report they need, 0 for .txt and 1 for .csv.
The method would then generate/print the row(s) of the scan to a file named like "scan-{target}-{timestamp}{format}"
"""
