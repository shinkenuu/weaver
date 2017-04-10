

class Credential:
    def __init__(self, of, ipAddress, port, username, pwd):
        self.of = of
        self.ipAddress = ipAddress
        self.port = port
        self.username = username
        self.pwd = pwd


credentials_dict = {
    'gmail': Credential('gmail', 'smtp.gmail.com', 465, 'weavers.pigeon@gmail.com', 'Wre8t5naWe=#'),
    'mongodb': Credential('mongodb', '192.168.1.251', 27017, 'weaver', 'dreamer')
}
