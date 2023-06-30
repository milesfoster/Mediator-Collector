import paramiko
import json
import copy
import time

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
            "nvidiaTemp": "nvidia-smi -q -d temperature|grep 'GPU Current Temp'|awk '{ print $5 $6 }'",
            "upTime": "cat /proc/uptime |awk '{ print $1/3600 }'",
            "memUsed": "test4=$(free -g |grep Mem | awk '{print ($3)}'|grep -v free) &&test=$(free -g |grep Mem | awk '{print ($6)}'|grep -v free) &&  test2=$(free -g |grep Mem | awk '{print ($7)}'|grep -v free) && test3=$(free -g |grep Mem | awk '{print ($4)}'|grep -v free) && test1=$(free -g |grep Mem | awk '{print ($2)}') && echo 'scale=2 ; (($test4 -($test + $test2))) / $test1 *100' | bc"
        }

        sudoCommands = {
            "drive1MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:0] -aALL|grep 'Media Error'",
            "drive2MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:1] -aALL|grep 'Media Error'",
            "drive3MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:2] -aALL|grep 'Media Error'",
            "drive4MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:3] -aALL|grep 'Media Error'",
            "drive5MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:4] -aALL|grep 'Media Error'",
            "drive6MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:5] -aALL|grep 'Media Error'",
            "drive7MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:6] -aALL|grep 'Media Error'",
            "drive8MediaErrors": "sudo megacli -PDInfo -PhysDrv [252:7] -aALL|grep 'Media Error'",
            "drive1PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:0] -aALL|grep 'Predictive Failure'",
            "drive2PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:1] -aALL|grep 'Predictive Failure'",
            "drive3PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:2] -aALL|grep 'Predictive Failure'",
            "drive4PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:3] -aALL|grep 'Predictive Failure'",
            "drive5PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:4] -aALL|grep 'Predictive Failure'",
            "drive6PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:5] -aALL|grep 'Predictive Failure'",
            "drive7PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:6] -aALL|grep 'Predictive Failure'",
            "drive8PredictiveErrors": "sudo megacli -PDInfo -PhysDrv [252:7] -aALL|grep 'Predictive Failure'"
        }

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, username=self.username, password=self.password)

        fields = {}

        for key, value in commands.items():

            _stdin, _stdout,_stderr = client.exec_command(value)
            result = (_stdout.read().decode())

            if "command not found" in result:
                fields[key] = "Command not found"

            elif result == "":
                fields[key] = f"No output from command '{key}'"

            else:
                fields[key] = result.rstrip("\n")



        for key, value in sudoCommands.items():


            _stdin, _stdout,_stderr = client.exec_command(value, get_pty = True, timeout = 2)
            _stdin.write(self.password + '\n')
            _stdin.flush()
            result = (_stdout.read().decode())


            if "command not found" in result:
                fields[key] = "Command not found"

            elif result == "":
                fields[key] = f"No output from command '{key}'"

            else:
                result = result.split(":")
                result = result[1]
                result = result.strip(" \r\n")
                fields[key] = result
            


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

    while input_quit != "q":


        documents = mediator.collect

        print(json.dumps(documents, indent=1))


        input_quit = input("\nType q to quit or hit enter to collect again: ")


if __name__ == "__main__":
    main()
