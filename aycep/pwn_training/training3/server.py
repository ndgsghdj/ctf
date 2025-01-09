import winreg
import socketserver

host = "127.0.0.1"
port = 1337

class SocketHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b"Welcome to the ROP LLC. Employee Database\n")
        self.wfile.write(b"Username: ")
        username = self.rfile.readline().strip(b"\n")
        self.wfile.write(b"Password: ")
        password = self.rfile.readline().strip(b"\n")
        print(password)
        reghandle = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"employee_database\\")
        key = winreg.CreateKey(reghandle, str(username))

        stored_pwd = b"\x00"
        try: 
            stored_pwd = winreg.QueryValueEx(key, "password")[0]
            print("Password found")
        except: 
            print("Password not found")

        if (stored_pwd == b"\x00"): 
            winreg.SetValueEx(key, "password", 0, winreg.REG_BINARY, password)
            self.wfile.write(b"Account created\n")
        else: 
            if (stored_pwd != password):
                self.wfile.write(b"Wrong password!")
                return
            else: 
                self.wfile.write(b"Login successful\n")

        run_continue = 1
        option = 0
        while (run_continue == 1): 
            menu = b"""--------------\nCOMMAND LIST: \n1. Store data\n2. Change user\n3. Read data\n4. Exit\nCommand >> """
            self.wfile.write(menu)
            option = self.rfile.readline().strip(b"\n")
            if (option == b"1"):
                self.wfile.write(b"Enter data: ")
                data = self.rfile.readline().strip(b"\n")
                try: 
                    winreg.SetValueEx(key, "data", 0, winreg.REG_BINARY, data)
                    self.wfile.write(b"Data successfully stored.\n")
                except: 
                    self.wfile.write(b"Access is denied.\n")
            elif (option == b"2"): 
                self.wfile.write(b"Enter username: ")
                username = self.rfile.readline().strip(b"\n")
                try:
                    key = winreg.OpenKeyEx(reghandle, str(username)) 
                    self.wfile.write(b"User switch success\n")
                except:
                    self.wfile.write(b"User switch failed\n")
            elif (option == b"3"): 
                try:
                    dataread = winreg.QueryValueEx(key, "data")[0]
                    self.wfile.write(b"Data: \n")
                    self.wfile.write(dataread)
                    self.wfile.write(b"\n")
                except: 
                    self.wfile.write(b"Data does not exist\n")
            elif (option == b"4"): 
                self.wfile.write(b"Exiting...\n")
                run_continue = 0
            else: 
                self.wfile.write(b"Invalid command!\n")

if __name__ == "__main__":
    print("ROP LLC Employee Database is listening on port 1337")
    server = socketserver.ThreadingTCPServer(("", port), SocketHandler)
    server.serve_forever()
