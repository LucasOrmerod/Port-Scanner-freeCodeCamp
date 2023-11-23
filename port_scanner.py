import socket
import ipaddress
import re
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    # Determine whether the input is an IP or domain
    isDomain = False
    
    try:
      ip_obj = ipaddress.ip_address(target)
      isDomain = False
    except ValueError:
      try:
        socket.gethostbyname(target)
        isDomain = True
      except socket.error:
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
          return "Error: Invalid IP address"
        else:
          return "Error: Invalid hostname"
  
    open_ports = []
    return_string = ""
    domain = ""
    ip = ""
    if isDomain:
      domain = target
      ip = socket.gethostbyname(target)
    else:
      ip = target
      domain = ""
      try:
        domain = socket.gethostbyaddr(ip)[0]
      except socket.error:
        domain = ""
  
    for port in range(port_range[0], port_range[1] + 1):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      result = sock.connect_ex((ip, port))
      if result == 0:
        open_ports.append(port)
      sock.close()

    if verbose is True:
      if domain == "":
        return_string += "Open ports for " + str(ip) + "\n"
      else:
        return_string += "Open ports for " + str(domain) + " (" + str(ip) + ")\n"
      return_string += "PORT     SERVICE\n" # 5 spaces between
      for index, value in enumerate(open_ports):
        if value in ports_and_services:
          return_string += str(value) + " " * (4 - len(str(value))) + "     " + ports_and_services[value] + "\n"
      return return_string.rstrip("\n")
    else:
      return open_ports