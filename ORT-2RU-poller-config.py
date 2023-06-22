import json
from insite_plugin import InsitePlugin
from ORT_2RU import MediatorCollector


class Plugin(InsitePlugin):
    def can_group(self):
        return True

# Hosts are passed in via hosts field in poller.
# Arguments to be manually filled: username, password

    def fetch(self, hosts):
      
        documents = []

        #host = hosts[-1]
        for host in hosts:

            # Defines the params to pass into the class constructor
            params = {
                "address": host,
                "username": "evertz",
                "password": "evertz"
                }


            # Instantiates the MediatorCollector class passing in params
            self.mediatorCollector = MediatorCollector(**params)
            document = self.mediatorCollector.collect
            documents.extend(document)



        return json.dumps(documents)
