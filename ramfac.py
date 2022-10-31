from os import environ as env
import requests

class customer:
    def __init__(self, tenantId):
        
        self.clientId = env['clientId']
        self.clientSecret = env['clientSecret']
        self.tenantId = tenantId
        
    def getAccessToken(self, scope):
        
        match scope:
            case 'graph':
                self.audience = 'https://graph.microsoft.com/.default'
            case 'keyvault':
                self.audience = 'https://vault.azure.net/.default'
            case 'management':
                self.audience = 'https://management.core.windows.net/.default'
                        
        request_data = {
            "scope": self.audience,
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "grant_type": "client_credentials"
        }
        
        uri = f"https://login.microsoftonline.com/{self.tenantId}/oauth2/v2.0/token"
        
        response = requests.post(uri, request_data)
        
        return response.json()['access_token']
    
    def getApiResponse(self, scope, uri):
        
        self.accessToken = self.getAccessToken(scope)
        listOfObjects = []
        response = requests.get(uri, headers={"Authorization":f"Bearer {self.accessToken}","Content-type":"application/json"})
        
        if response.status_code == 400:
            
            return response.json()
        
        elif response.status_code == 200:
            
            jsonData = response.json()
            for item in jsonData['value']:
                
                listOfObjects.append(item)
                
            while '@odata.nextLink' in jsonData:
                
                uri = jsonData['@odata.nextLink']
                response = requests.get(uri, headers={"Authorization":f"Bearer {self.accessToken}","Content-type":"application/json"})
                jsonData = response.json()
                for item in jsonData['value']:
                    
                    listOfObjects.append(item)
        
        return listOfObjects
    
    def getDevices(self):
        
        return self.getApiResponse('graph', 'https://graph.microsoft.com/v1.0/deviceManagement/managedDevices')
    
    def getLicenses(self):
        
        return self.getApiResponse('graph', 'https://graph.microsoft.com/v1.0/users')
    
    def getEnterpriseApps(self):
        
        return self.getApiResponse('graph', 'https://graph.microsoft.com/beta/applications')
    
    def getIntuneApps(self):
        
        return self.getApiResponse('graph', 'https://graph.microsoft.com/beta/deviceAppManagement/mobileApps')


def uniqueList(list, attribute):
    uniqueList = []
    for i in list:
        if i[attribute] not in uniqueList:
            uniqueList.append(i[attribute])
    return uniqueList