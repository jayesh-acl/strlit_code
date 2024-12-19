import requests,json,os
class Login:
    def login(self,userid,password,tpin):
        loginData = {
            "user_id":userid,
            "password" :password
        }
        response =  requests.post(url="https://kite.zerodha.com/api/login",data=loginData)
        login_response = json.loads(response.text)
        request_id = ""
        if login_response.get("status") == 'success' :
            print(f"You are Authenticated with {loginData['user_id']} UserID.")
            request_id = login_response.get("data",{}).get("request_id")
            twoFa_url = "https://kite.zerodha.com/api/twofa"
            msg = {
                "user_id":loginData.get('user_id'),
                "request_id":request_id,
                "twofa_value" : tpin,
                "twofa_type":"app_code"
            }
            response = requests.post(url=twoFa_url,data=msg)

            if response.status_code==200:
                print(f"2FA Authenticated with {loginData['user_id']} UserID.")
                enctoken=response.cookies.get("enctoken")
                return enctoken
            else:
                print("Error on 2FA",response.text)
        else:
                print("Error on Authentication",response.text)


    def generateContractFile(self,enctoken):
        try:
            url = f"https://api.kite.trade/instruments"
            headers = {
            'Authorization': "enctoken "+enctoken,
            'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("GET", url, headers=headers)
            if response.status_code==200:
                with open('zerodha_contractfile.csv','w') as file :
                    file.write(response.text)
        except Exception as e:
            print(e)
