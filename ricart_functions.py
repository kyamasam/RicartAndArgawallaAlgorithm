import socket
import time
import re
r = re.compile(r"^\d*[.]?\d*$")
class Node:

    def __init__(self, port_number, cs_status):
        self.port_number = port_number
        self.cs_status = cs_status
        self.server = self.start_server(port_number)
        # time.sleep(4)
        self.cs_intention_time = time.time()
        self.server.listen(1)
        self.received_time_data=''

    self_ok_count = 0
    total_okay_count = 0
    def connect_to_port(self, port_number):
        # create a reliable TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # local hostname
        local_hostname = socket.gethostname()
        # full host name
        local_fqdn = socket.getfqdn()

        # get the according IP address
        ip_address = socket.gethostbyname(local_hostname)

        # bind the socket to the port 12345, and connect
        server_address = (ip_address, port_number)
        sock.connect(server_address)
        print("connected to ",server_address)
        return sock

    def send_message(self, port, message):
        sock = self.connect_to_port(port)
        print("sending message to ", port)
        sock.send(bytes(message, 'utf-8'))

    def send_cs_requests(self, connection_ports):
        for port in connection_ports:
            sock = self.connect_to_port(port)
            # send the requests to each port
            sock.settimeout(5.0)
            sock.send(bytes("request", 'utf-8'))
            print("request sent to port", port)
            if port == 12348:
                try:
                    data_from_server = sock.recv(64)
                    if data_from_server.decode() == "OK":
                        self.total_okay_count += 1
                    else:
                        print("No okay message received")

                except socket.timeout:
                    print("Timed Out Before Any message was received. Assume critical section")


            elif port == 12349:
                try:
                    data_from_server = sock.recv(64)
                    if data_from_server.decode() == "OK":
                        self.total_okay_count += 1
                    else:
                        print("No okay message received")

                except socket.timeout:
                    print("Timed Out Before Any message was received. Assume critical section")
            else:
                pass
        print("finished sending all the requests to all ports")
        # time
        for port in connection_ports:
            sock = self.connect_to_port(port)
            # send the requests to each port
            sock.settimeout(5.0)
            sock.send(bytes(str(self.cs_intention_time), 'utf-8'))
            print("time sent to port", port)

        print("finished sending time stamps to all ports")

        return self.port_number


    def check_critical_section(self):
        #check if this port is in cs
        if self.cs_status == 0:
            return False
        else:
            return True

    def listen_for_replies(self):

        while True:
            # wait for a connection
            print('waiting for a connection')
            connection, client_address = self.server.accept()
            try:
                print('connection from', client_address)

                # get the data in bits
                while True:
                    data = connection.recv(64)
                    if data.decode('utf-8') == "request" and self.cs_status == True:
                        print("I have received a request for my status")
                        print("I am in my critical Section" , self.cs_status)
                    elif data.decode('utf-8') == "request" and self.cs_status == False:
                        print("request")
                        print("I am not in my critical section", data.decode())

                    elif data.decode('utf-8') == "OK":
                        print("Ok message received")
                        print(data.decode())
                        ok_messages_list = list(data)
                        ok_messages_list.append(data)
                        self.total_okay_count += 1

                    elif r.match(data.decode('utf-8')):
                        print("time data received")
                        if float(self.cs_intention_time) < float(data.decode('utf-8')) :
                            print('time received is' , data.decode('utf-8'))
                            print("i have a less recent cs_section request")
                            self.more_recent_request = 1
                            self.received_time_data = data.decode('utf-8')

                        else:
                            print("the sender has a more recent request")
                            time.sleep(4)
                            pass

                    else:
                        # print("message received was", data.decode('utf-8'))
                        print("server returned, ", data.decode('utf-8'))


                    if self.cs_status == False and self.port_number == 12345 and self.self_ok_count < 1 :
                        # you cannot send anything to yourself so just increment the okay count
                        print('myself')
                        self.self_ok_count += 1
                        self.total_okay_count += 1
                        break
                    elif self.cs_status == False and self.port_number != 12345 and self.received_time_data !='':
                        print("sending OK message")
                        time.sleep(3)
                        self.send_message(12345, "OK")
                        break
                    else:
                        break

            # let's make sure this code is excecuted even in the case of an exception
            finally:
                print("wait for any other node to connect")
                print("total okay count ", self.total_okay_count)

                if self.total_okay_count == 5:
                    print("entering critical section")
                else:
                    print("cannot enter critical section, yet")

    def start_server(self, my_port):
        # create a reliable TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get  local hostname
        local_hostname = socket.gethostname()

        # get complete domain name for this computer
        local_complete_domain_name = socket.getfqdn()

        # the ip address associated with the fqdn
        ip_address = socket.gethostbyname(local_hostname)

        # display hostname, domain name and IP address
        print("Details are as follows %s (%s) with %s" % (local_hostname, local_complete_domain_name, ip_address))

        # bind the socket to the port, Example : 12345
        server_address = (ip_address, my_port)
        print('Starting the server on %s port %s' % server_address)
        sock.bind(server_address)
        # listen for incoming connections (server mode) with one connection at a time

        return sock


