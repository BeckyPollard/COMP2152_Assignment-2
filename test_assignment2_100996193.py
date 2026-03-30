"""
Unit Tests for Assignment 2 — Port Scanner
"""

import unittest 

# Import your classes and common_ports from assignment2_studentID ✓
# from assignment2_studentID import PortScanner, common_ports ✓
from assignment2_100996193 import PortScanner, common_ports

class TestPortScanner(unittest.TestCase):
  def test_scanner_initialization(self):
    """Test that PortScanner initializes with correct target and empty results list."""
    scanner = PortScanner("127.0.0.1")
    self.assertEqual(scanner.target, "127.0.0.1")
    self.assertEqual(scanner.scan_results, [])

  def test_get_open_ports_filters_correctly(self):
    """Test that get_open_ports returns only Open ports."""
    # Create a PortScanner object ✓
    # Manually add these tuples to scanner.scan_results: ✓
    #   (22, "Open", "SSH"), (23, "Closed", "Telnet"), (80, "Open", "HTTP") ✓
    # Call get_open_ports() and assert the returned list has exactly 2 items ✓
    scanner = PortScanner("127.0.0.1")
    scanner.scan_results = [
      (22, "Open", "SSH"),
      (23, "Closed", "Telnet"),
      (80, "Open", "HTTP")
    ]
    open_ports = scanner.get_open_ports()
    self.assertIn((22, "Open", "SSH"), open_ports)
    self.assertNotIn((23, "Closed", "Telnet"), open_ports)
    self.assertIn((80, "Open", "HTTP"), open_ports)
    self.assertEqual(len(open_ports), 2)

  def test_common_ports_dict(self):
    """Test that common_ports dictionary has correct entries."""
    # Assert common_ports[80] equals "HTTP" ✓
    # Assert common_ports[22] equals "SSH" ✓
    self.assertEqual(common_ports[80], "HTTP")
    self.assertEqual(common_ports[22], "SSH")

  def test_invalid_target(self):
    """Test that setter rejects empty string target."""
    # Create a PortScanner with target "127.0.0.1" ✓
    # Try setting scanner.target = "" (empty string) ✓
    # Assert scanner.target is still "127.0.0.1" ✓
    scanner = PortScanner("127.0.0.1")
    scanner.target = ""
    self.assertEqual(scanner.target, "127.0.0.1")


if __name__ == "__main__":
  unittest.main()

