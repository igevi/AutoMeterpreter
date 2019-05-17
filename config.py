# Directory in which the payload files will be stored
PAYLOAD_DIR = './payloads'

# Ports on which unique payloads will be served
# e.g.
# PAYLOADS = {
#   {   
#       'payload': 'filename1.ext', 
#       'port': 3001 
#   },
#   {   
#       'payload': 'filename2.ext',
#       'port': 3002 
#   }
# }
PAYLOADS = [
    {
        'payload': 'default.txt',
        'port': 8080
    }
]

# file containing newline separated meterpreter commands to run on the remote machine
METERPRETER_COMMAND_SCRIPT = './scripts/default.txt'

# metasploit msfrpcd port
MSFRPCD_PORT = 55553

# metasploit LPORT
METSPLOIT_LPORT = 4444

# metasploit payload
METASPLOIT_PAYLOAD = 'linux/x86/meterpreter/reverse_tcp'

# length of msfrpcd password
MSFRPCD_PASSLENGTH = 10