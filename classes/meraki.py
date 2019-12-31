from .api import Api
import json


class Meraki:

    def __init__(self, apiKey):
        self.baseURL = 'https://api.meraki.com/api/v0/'
        self.apiKey = apiKey

    def getHeaders(self):
        return {
            'X-Cisco-Meraki-API-Key': '{}'.format(self.apiKey),
            "Accept": '*/*'
        }
    
    def getOrganisations(self):
        organisations = Api.getRequest(self.baseURL + 'organizations', self.getHeaders())
        if (organisations["success"]):
            return {"success": True, "data": json.loads(organisations["body"])}
        else:
            return {"success": False, "data": []}


    def getNetworks(self, organisation):
        networks = Api.getRequest(self.baseURL + 'organizations/{}/networks'.format(organisation["id"]), self.getHeaders())
        if (networks["success"]):
            return {"success": True, "data": json.loads(networks["body"])}
        else:
            return {"success": False, "data": []}
    

    def getNetworkEvents(self, network):
        events = Api.getRequest(self.baseURL + 'networks/{}/events?productType=wireless&perPage=1000'.format(network["id"]), self.getHeaders())
        if (events["success"]):
            return {"success": True, "data": events["events"]}
        else:
            return {"success": False, "data": []}
    

    def getNetworkClients(self, network):
        clients = Api.getRequest(self.baseURL + 'networks/{}/clients?timespan=2678400'.format(network["id"]), self.getHeaders())
        if (clients["success"]):
            return {"success": True, "data": json.loads(clients["body"])}
        else:
            return {"success": False, "data": []}

    def getDeviceClients(self, device):
        clients = Api.getRequest(self.baseURL + 'devices/{}/clients?&timespan=2678400'.format(device["serial"]), self.getHeaders())
        if (clients["success"]):
            return {"success": True, "data": json.loads(clients["body"])}
        else:
            return {"success": False, "data": []}

    def getDevices(self, network):
        devices = Api.getRequest(self.baseURL + 'networks/{}/devices'.format(network["id"]), self.getHeaders())
        if (devices["success"]):
            devices = json.loads(devices["body"])
            for device in devices:
                if device["model"][:2] == 'MX':
                    device["pxType"] = 'firewall'
                elif device["model"][:2] == 'MR':
                    device["pxType"] = 'access-point'
                elif device["model"][:2] == 'MS':
                    device["pxType"] = 'switch'
                elif device["model"][:2] == 'MV':
                    device["pxType"] = 'security-camera'
                elif device["model"][:2] == 'MG':
                    device["pxType"] = 'wireless-wan'
                elif device["model"][:2] == 'MC':
                    device["pxType"] = 'voip-phone'
                else:
                    device["pxType"] = 'unidentified'
            return {"success": True, "data": devices}
        else:
            return {"success": False, "data": []}