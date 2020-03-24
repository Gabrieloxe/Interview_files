import requests
#URL used in the first instance
url="http://fasttrack.herokuapp.com"
#ensuring that data return type is json
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
#boolean to check if I need to delete part of the URL
first_time = True

try:
    #run until I hit the endpoint
    while True:
        response = requests.get( url, headers = headers)
        json_response = (response.json())
        #output of each round
        print(json_response)
        add = json_response['next']
        #if its the first time just append the "next"
        if first_time:
            url = url+add  
            first_time = False          
        # remove the end of string and add the new "next"
        else: 
            #reverse split
            splitted_list = url.rsplit("/",1)
            url = splitted_list[0] + add
        #while loop end condition
        if response == None:
            break
        #endo of while loop 
          
 # exception handling    
except Exception:
    ("hit the endpoint")
finally:
    #script end
    print("done")

