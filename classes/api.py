import json, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Api:
    def getRequest(url, headers={}):
        try:
            r = requests.get(url, headers=headers, verify=False)
            status = r.status_code
            resp = r.text
            if status == 200:
                try:
                    result = json.loads(resp)
                    result["success"] = True
                except:
                    result = {"success": True, "body": resp}
                return result
            else:
                # r.raise_for_status()
                r.close()
                return {"success": False, "error": resp, "code": status}
        except requests.exceptions.HTTPError as err:
            return {"success": False, "error": "Error in connection --> " + str(err), "code": status    }


    def deleteRequest(url, headers={}):
        try:
            r = requests.delete(url, headers=headers, verify=False)

            status = r.status_code
            resp = r.text
            
            if status == 200:
                result = json.loads(resp)
                result["success"] = True
                return result
            else:
                r.raise_for_status()
                r.close()
                return {"success": False, error: resp}
        except requests.exceptions.HTTPError as err:
            return {"success": False, "error": "Error in connection --> " + str(err)}


    def postRequest(url, headers={}, data={}):
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        data["grant_type"] = "client_credentials"
        try:
            r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
            status_code = r.status_code
            resp = r.text
            if status_code == 201 or status_code == 202 or status_code == 200:
                try:
                    response = json.loads(resp)
                except:
                    response = {}
                response["success"] = True
                return response
            else:
                return {"success": False, "response": resp, "status": status_code, "data": json.dumps(data), "url": url}
        except requests.exceptions.HTTPError as err:
            return {"success": False, "error": "Error in connection --> " + str(err)}


    def putRequest(url, headers={}, data={}):
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"

        try:
            r = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
            status_code = r.status_code
            resp = r.text
            if (status_code == 200 or status_code == 201 or status_code == 202):
                result = json.loads(resp)
                result["success"] = True
                return result
            else:
                return {"response": resp, "status": status_code}
        except requests.exceptions.HTTPError as err:
            return {"success": False, "error": "Error in connection --> " + str(err)}
