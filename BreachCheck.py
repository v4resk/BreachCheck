import requests
import json
import argparse

# Creating ArgParse stuffs
parser = argparse.ArgumentParser(description='BreachCheck is a tool designed to help users search for their passwords in known data breaches and leaks. It utilizes the breachdirectory.org API')
parser.add_argument('-t', '--target', metavar='TARGET', required=True, help='Target email or username')
parser.add_argument('-oR', '--output-raw', metavar='FILE', required=False, help='Output the full json API call result to a file')
parser.add_argument('-oN', '--output-normal', metavar='FILE', required=False, help='Output the passwords list to a file')
args = parser.parse_args()
target = args.target
output_raw = args.output_raw
output_normal = args.output_normal

# ANSI escape codes for colors
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# This function get all API Keys conf file
def read_api_keys(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Defining API keys as global var
conf_file = "conf.json"
api_keys = read_api_keys(conf_file)
BreachedDirectory_ApiKey = api_keys["BreachedDirectory"]


# This fuction request BreachedDirectory API
# Return false is API key isn't defined 
# Return json if request is success
def req_breachdirectory(target):
    # Modes: auto --> Returns passwords, SHA-1 hashes, and sources given any username or email.
    #        domain --> Returns passwords, SHA-1 hashes, and sources given any domain (Limited to 1000 results for security).
    if(BreachedDirectory_ApiKey != "API-KEY"):
        url_breachdirectory = "https://breachdirectory.p.rapidapi.com/"
        querystring = {"func":"auto","term":target}
        headers = {
        "X-RapidAPI-Key": BreachedDirectory_ApiKey,
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
        }
    
        response = requests.get(url_breachdirectory, headers=headers, params=querystring)
        return response.json()
    else:
        return False
    
def print_breachdirectory_auto_mode(answer):

    if(output_raw):
        with open(output_raw, "w") as file:
            json.dump(answer,file)
    if(output_normal):
        file_normal = open(output_normal, "w")

    #Check if answer is not set to False
    if(not answer):
        print(f"{colors.RED}[-]{colors.RESET} API call to BreachDirectory fails\n")
        return False
    
    #Check if API Call does not failed
    success = answer["success"]
    if(not success): 
        print(f"{colors.RED}[-]{colors.RESET} API call to BreachDirectory fails\n")
        return False
    
    # API Call is a success
    found = answer["found"]
    print(f"{colors.GREEN}[+]{colors.RESET} Successful API call to BreachDirectory")
    print(f"{colors.GREEN}[+]{colors.RESET} Found target in {colors.GREEN}{found}{colors.RESET} data breaches")

    # Print if result[] is empty
    result = answer["result"]
    if(len(result)==0):
        print(f"{colors.RED}[-]{colors.RESET} Target's password not found in data breaches \n")
        return False
    
    print("")
    plaintext_passwords = []
    sha1_hashes = []
    for entry in answer["result"]:
        if entry["email"]:
            #email = entry.get('email', 'N/A')
            password = entry.get('password', 'N/A')
            sha1 = entry.get('sha1', 'N/A')
            source = entry.get('sources', 'N/A')

            if password != 'N/A':
                plaintext_passwords.append((source, password))
            if sha1 != 'N/A':
                sha1_hashes.append((source, sha1))

    if len(plaintext_passwords) > 0:
        print(f"{colors.GREEN}[+]{colors.RESET} Plaintext Passwords")
        for source, password in plaintext_passwords:
            print(f"{colors.GREEN}[+]{colors.RESET} {source}: {colors.GREEN}{password}{colors.RESET}")
            if(output_normal):
                file_normal.writelines(f"Password: {password}\n")
            
    if len(sha1_hashes) > 0:
        print(f"\n{colors.GREEN}[+]{colors.RESET} SHA1 Passwords")
        for source, hash_value in sha1_hashes:
            print(f"{colors.GREEN}[+]{colors.RESET} {source}: {colors.GREEN}{hash_value}{colors.RESET}")
            if(output_normal):
                file_normal.writelines(f"SH1: {hash_value}\n")
    print("")

# This is main function for BreachDirectory
def breachdirectory(target):
    breachedDirectory_answer = req_breachdirectory(target)
    print_breachdirectory_auto_mode(breachedDirectory_answer)

if __name__ == '__main__':
    breachdirectory(target)