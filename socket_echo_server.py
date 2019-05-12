import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('210.213.231.10', 14355)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        connection.sendall('OK Welcome to the CSc 113 Arithmetic Server!\n')
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print >>sys.stderr, 'Data received {}'.format(data)
            #slice data into 3 parts
            data = data.split(' ')
            print >>sys.stderr, 'len: {}'.format(len(data))
            if data:
                if len(data) == 3:
                    operation = str(data[0].decode('UTF-8').strip())
                    n1 = str(data[1].decode('UTF-8').strip())
                    n2 = str(data[2].decode('UTF-8').strip())
                    print >>sys.stderr, 'is expr {} {} {}'.format(operation, n1, n2)
                    if operation in ['ADD', 'SUB', 'MUL', 'DIV']:
                        if (n1.isdigit() == True) and (n2.isdigit() == True):
                            if operation == 'ADD':
                                result = int(n1) + int(n2)
                                message = 'OK {}\n'.format(result)
                                connection.sendall(message)
                            elif operation == 'SUB\n':
                                result = int(n1) - int(n2)
                                message = 'OK {}\n'.format(result)
                                connection.sendall(message)
                            elif operation == 'MUL':
                                result = int(n1) * int(n2)
                                message = 'OK {}\n'.format(result)
                                connection.sendall(message)
                            elif operation == 'DIV':
                                if int(n2) == 0:
                                    message = 'ERR Diviosion by {}\n'.format(int(n2))
                                    connection.sendall(message)
                                else:
                                    result = int(n1) / int(n2)
                                    message = 'OK {}\n'.format(result)
                                    connection.sendall(message)
                        else:
                            message = 'ERR Invalid argument type\n'
                            connection.sendall(message)
                    else:
                        message = 'ERR Unknown operation {}\n'.format(operation)
                        connection.sendall(message)
                elif len(data) == 2:
                    operation = str(data[0].decode('UTF-8').strip())
                    command = str(data[1].decode('UTF-8').strip())
                    print >>sys.stderr, 'is op {} command {}'.format(operation, command)
                    if operation == 'HELP':
                        if command == 'HELP':
                            message = 'OK HELP [command] - to display the syntax and semantics of a specific command. If no command is specified, it will display all the available commands and their meanings\n'
                            connection.sendall(message)
                        elif command == 'ADD':
                            message = 'ADD <N1> <N2> - to add N1 and N2.\n'
                            connection.sendall(message)
                        elif command == 'SUB':
                            message = 'SUB <N1> <N2> - to subtract N2 from N1.\n'
                            connection.sendall(message)
                        elif command == 'MUL':
                            message = 'MUL <N1> <N2> - to multiply N1 by N2.\n'
                            connection.sendall(message)
                        elif command == 'DIV':
                            message = 'MUL <N1> <N2> - to multiply N1 by N2.\n'
                            connection.sendall(message)
                        elif command == 'QUIT':
                            message = 'QUIT - to end the current session of the arithmetic server.\n'
                            connection.sendall(message)
                        else:
                            message = 'ERR unknown command HELP {}\n'.format(command)
                            connection.sendall(message)  
                    else:
                        print >>sys.stderr, 'ERR unknown command {}\n'.format(operation)
                        message = 'ERR unknown command {}'.format(operation)
                        connection.sendall(message)
                elif len(data) == 1:
                    operation = str(data[0].decode('UTF-8').strip())
                    print >>sys.stderr, 'is op {}'.format(operation)
                    if operation == 'HELP':
                        message = 'OK The following commands are available:\n\
                                    \tADD <N1> <N2> - to add N1 and N2\n\
                                    \tSUB <N1> <N2> - to subtract N2 from N1\n\
                                    \tMUL <N1> <N2> - to multiply N1 by N2\n\
                                    \tDIV <N1> <N2> - to divide N1 by N2\n\
                                    \tHELP [command] - to display the syntax and semantics of a specific command. If no command is specified, it will display all the available commands and their meanings\n\
                                    \tQUIT - to end the current session of the arithmetic server\n'
                        connection.sendall(message)
                    elif operation == 'QUIT':
                        message = 'OK Bye.\n'
                        connection.sendall(message)
                        connection.close()
                    else:
                        message = 'ERR unknown command {}\n'.format(operation)
                        connection.sendall(message)
            else:
                print >>sys.stderr, 'no more data from\n', client_address
                break        
    finally:
        # Clean up the connection
        connection.close()
