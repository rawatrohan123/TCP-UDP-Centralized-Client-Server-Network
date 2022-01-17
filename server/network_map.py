from pythonping import ping


class NetworkMap:

    @staticmethod
    def ping_device(ip_address):
        ping(ip_address)
        # divide ping my 2 to get RTT/2
        
