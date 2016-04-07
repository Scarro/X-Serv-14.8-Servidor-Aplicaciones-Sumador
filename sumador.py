#!/usr/bin/python
# -*- coding: utf-8 -*-
# Sergio Carro Albarran

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket

class webApp():
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def close(self):
        self.mySocket.close()
        print "Desconecto mySocket"

    def __init__(self, hostname, port):
        """Initialize the web application."""
        recvSocket = None
        
        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        try:
            while True:
                print 'Waiting for connections'
                (recvSocket, address) = mySocket.accept()
                request = recvSocket.recv(2048)
                if request:
                    print 'HTTP request received (going to parse and process):'
                    parsedRequest = self.parse(request)
                    print parsedRequest
                    (returnCode, htmlAnswer) = self.process(parsedRequest)
                    print 'Answering back...'
                    recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                    + htmlAnswer + "\r\n")
                recvSocket.close()
        except KeyboardInterrupt:
            if recvSocket:
                recvSocket.close()
            mySocket.close()
            print "Servidor cerrado"

class sumaApp(webApp):
    def parse(self, request):
        introducido = request.split()[1][1:]
        return introducido
    def process(self,parsedRequest):
        html = '<html><body><h1>'
        htmlend = '</h1></body></html>'
        try:
            numero = int(parsedRequest)
            if self.numero1 is None:
                self.numero1 = numero
                html += 'Primer numero: '
                html += str(self.numero1)
                html += '<p>Introduce el segundo</p>'
                html += htmlend
            else:
                self.numero2 = numero
                suma = self.numero1 + self.numero2
                html += 'Primero numero: ' + str(self.numero1)
                html += '<br/>Segundo numero: ' + str(self.numero2)
                html += '<br/><em>Suma:</em> ' + str(suma)
                html += htmlend
                self.numero1 = None
                self.numero2 = None
        except:
            html += 'Introduce un numero correcto'
            html += htmlend
        return ("200 OK", html)

    def __init__(self, hostname, port):
        self.numero1 = None
        self.numero2 = None
        webApp.__init__(self,hostname,port)

if __name__ == "__main__":
    testWebApp = sumaApp("localhost", 1234)
