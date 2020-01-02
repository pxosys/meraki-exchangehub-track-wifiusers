from classes import Api, Meraki
import json, time, argparse, pprint


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--apiKey', required=False)
    parser.add_argument('--credentialsFile', required=False)
    parser.add_argument('--reportMode', required=False, default='clients')

    args = parser.parse_args()

    apiKey = None

    if args.credentialsFile:
        with open(args.credentialsFile) as json_file:
            parsed = json.load(json_file)
            if "apiKey" in parsed:
                apiKey = parsed["apiKey"]

    if args.apiKey:
        apiKey = args.apiKey

    if apiKey == None:
        print('Please include a Cisco Meraki Dashboard API Key!')
        exit()


    meraki = Meraki(apiKey)

    orgs = meraki.getOrganisations()
    resultDevices = {}
    clients = {}
    if len(orgs["data"]):
        for org in orgs["data"]:
            networks = meraki.getNetworks(org)
            if len(networks["data"]):
                for network in networks["data"]:
                    devices = meraki.getDevices(network)
                    for device in devices["data"]:
                        resultDevices[device["mac"]] = device
                        deviceClients = meraki.getDeviceClients(device)
                        for client in deviceClients["data"]:
                            client["events"] = []
                            clients[client["id"]] = client
                    networkClients = meraki.getNetworkClients(network)
                    for client in networkClients["data"]:
                        client["events"] = []
                        clients[client["id"]] = client

                    events = meraki.getNetworkEvents(network)
                    for event in events["data"]:
                        if event["type"] == 'disassociation' or event["type"] == 'association':
                            if event["clientId"] in clients:
                                if args.reportMode == 'ping':
                                    print('got one')
                                clients[event["clientId"]]["events"].append(event)
    if args.reportMode == 'devices':
        pprint.pprint(devices)
    elif args.reportMode == 'clients':
        pprint.pprint(clients)

    
if __name__ == '__main__':
    main()