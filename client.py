import base64

class Client:

    def __init__(self, screen):
        self.screen = screen
        self.client = None
        self.assign = None
        self.wait1 = False
        self.wait2 = False
        self.dec = None

    def heading(self):			#Generating heading
        font = self.pygame.font.SysFont("arial", 72)
        head = font.render("Waiting for Game to start...", True, (255, 255, 255))
        self.screen.blit(head, (30, 30))

    def background(self):
        self.screen.fill((0, 0, 0))

    def conClient(self, host, username):			#Function to connect to the host server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#Creating a network stream with IPv4 and TCP protocol
        print(host)
        self.client.connect((host, 8080))		#Connect to host server at port 8080
        self.client.send(bytes(username, 'utf-8'))

    def decrypt(self, ip):		#Function to decrypt the invite code that we generated through server module
        self.dec = ""
        for i in ip:
            if i == "@":
                ch = "."		#Here we are reversing the procedure and covering the @ symbol back to . for IP address
            else:
                ch = str(ord(i) - 98)	#Converting the letters back to their respective ASCII numbers
            self.dec += ch	#Appending the converted digits of IP back to decrypted code

    def run(self, username, ip, first):
        self.background()
        self.heading()
        self.decrypt(ip=ip)
        if self.dec and first:
            self.conClient(self.dec, username=username)
            self.wait1 = True
        pygame.display.update()
        if self.wait2:
            message = self.client.recv(1024)
            if message.decode("utf-8") == "Place Ships":
                print(message)
                self.assign = True
                return self.assign
        if self.wait1:
            self.wait2 = True
        print(self.wait2)
        return False
