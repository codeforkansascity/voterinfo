import json
#Create the headers and POST body
url = "https://api.securevan.com/v4/people/find"
get_url = "https://api.securevan.com/v4/people/"
get_expand_url = "?&$expand=phones,emails,addresses"

headers = {
    'Content-Type' : 'application/json',
    'Authorization' : 'Basic ZG5jLmtlc3NsZXIuYXBpIDo1YTc3OTk3OS0wY2MzLTcxYTQtYzAyMi1jOTNjNTM4MDk5YTN8MQ=='
}
#demo_API_key = '0614e2a3-dba0-eacf-a715-b50175b1dbd5'
auth = ('dnc.kessler.api', '5a779979-0cc3-71a4-c022-c93c538099a3|0')
returnAddress = None

#Split on contact full name - its the only value that persists between 
#textit triggers, as far as i could tell
name = input_data.get('fullName')
splitNames = name.split()
print(splitNames)

#Split phone number into format expected by NGP VAN
streetAddress = input_data.get('streetAddress')
if streetAddress is None:
    phone = input_data.get('urn')
    phone = phone.split('+')
    phone = phone[1]
    #phone = phone[0] + '-' + phone[1] + phone[2] + phone[3] + '-' + phone[4] + phone[5] + phone[6] + '-' + phone[7] + phone[8] + phone[9] + phone[10]  
else:
    phone = input_data.get('urn')
    
print(phone)

payload = {
    'firstName': splitNames[0],
    'lastName': splitNames[1],
    'dateOfBirth': input_data.get('dob'),
    'addresses': [
        {
            'addressLine1': input_data.get('streetAddress'),
            'zipOrPostalCode': input_data.get('zip5'),
        }
    ],
    'phones': [
        {
            'phoneNumber': phone,
        },
    ]
}
if input_data.get('email') != None:
    payload['emails'] = [ {'email': input_data.get('email'),} ]

#print(payload)

#Make the API request
r = requests.post( url, headers=headers, auth=auth, data=json.dumps(payload) )

#Extract the response as a JSON object
returnValue = r.json()

if returnValue.get('vanId') != None:  
    r = requests.get( get_url + str(returnValue.get('vanId')) + get_expand_url,          headers=headers, auth=auth)
    getReturnValue = r.json()
    address = getReturnValue.get('addresses')
    mainAddress = address[1]
    addressLine1 = mainAddress.get('addressLine1')
    addressLine2 = mainAddress.get('addressLine2')
    city = mainAddress.get('city')
    state = mainAddress.get('stateOrProvince')
    zipOrPostalCode = mainAddress.get('zipOrPostalCode')
    returnAddress = addressLine1
    if addressLine2 != None:
        returnAddress = returnAddress + '\n' + addressLine2
    returnAddress = returnAddress + '\n' + city + ', ' + state + ' ' +  zipOrPostalCode
    #Crawford is going to replace these two lines below
    #vote411Address = addressLine1+addressLine2+city+state+zipOrPostalCode
    #vote411Address =vote411Address.replace(" ","% 20")
    #print(returnAddress)
    

#Set the data we return to textit
#Crawford is going to replace #'s
output = {
    'vanId': returnValue.get('vanId'),
    'address': returnAddress,
    'status': returnValue.get('status')
    #'addressLine1': addressLine1,
    #'addressLine2': addressLine2,
    #'city' : city,
    #'state' : state,
    #'zipOrPostalCode' :zipOrPostalCode
    #'vote411Address' : vote411Address
}