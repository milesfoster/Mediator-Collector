import paramiko
import json
import copy

class MediatorCollector:
    def __init__(self, **kwargs):

        self.host = None
        self.username = None
        self.password = None

        for key, value in kwargs.items():

            if "address" in key and value:
                self.host = value
            
            if "username" in key and value:
                self.username = value

            if "password" in key and value:
                self.password = value


        # host = "192.168.1.96"
        # username = "evertz"
        # password = "evertz"

    @property
    def collect(self):

        documents = []

        commands = {
            "rootUsage": "df -h  / | awk '{print $5}' | grep -v 'Use'",
            "optUsage": "df -h  /opt | awk '{print $5}' | grep -v 'Use'",
            "loadAvg": "cat /proc/loadavg | awk '{print $3}'",
            "hostname": "hostname", 
        #    "hostnamectl": "hostnamectl"
        }

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, username=self.username, password=self.password)

        fields = {}

        for key, value in commands.items():

            _stdin, _stdout,_stderr = client.exec_command(value)
            result = (_stdout.read().decode())
            print(result)
            fields[key] = result.rstrip("\n")

        document = {"fields": fields, "host": self.host, "name": "mediatorCollector"}
        documents.append(document)

        client.close()
        return documents

def main():

    params = {
                "address": "192.168.1.96",
                "username": "evertz",
                "password": "evertz"
                }

    input_quit = False

    mediator = MediatorCollector(**params)

    while input_quit is not "q":


        documents = mediator.collect

        print(json.dumps(documents, indent=1))


        input_quit = input("\nType q to quit or hit enter to collect again: ")


if __name__ == "__main__":
    main()
