import sys
import traceback
import datetime

"""
FOR DEBUGGING
"""

echo_path = "/etc/cloudns_sync/echo.log"
error_path = "/etc/cloudns_sync/error.log"
print_console = False

def SetEchoPath(ss):
	global echo_path
	echo_path = ss

def SetErrorPath(ss):
	global error_path
	error_path = ss

def SetPrintConsole(is_console):
	global print_console
	print_console = is_console

def Error(ss):
	try:
		global error_path
		global print_console
		if print_console:
			print(ss)
		else:
			writer = open(error_path, "a")
			print(ss, file=writer)
			writer.close()
	except:
		pass

def Echo(ss, path=None):
	try:
		global echo_path
		global print_console
		if print_console:
			print(ss)
		else:
			if path == None:
				writer = open(error_path, "a")
			else:
				writer = open(path, "a")
			print(ss, file=writer)
			writer.close()
	except:
		pass

def Log(ss, path=None):
	s = "[" + str(datetime.datetime.now()) + "]"
	s += "\t"
	s += ss
	Echo(s, path)

def EchoTraceback():
	t, v, tb = sys.exc_info()
	result = traceback.format_exception(t,v,tb)
	Echo(result)
