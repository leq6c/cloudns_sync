import os
import time
from dnslib import RR, QTYPE, SOA, DNSLabel, CLASS
from utils_debugging import Echo

bind_path = os.environ['BIND_NAMED_PATH']
retry_sleep = 0.5
retry_times = 5

def HostConvert(r, domain):
	label = DNSLabel(r.get_rname()).label
	ret = ".".join([ s.decode("idna") for s in label ]) + "$"
	idx = ret.rfind(domain + "$")
	if idx != -1:
		ret = ret[0:idx] + "$"
	ret = ret[0:-1]
	if len(ret) > 0 and ret[-1] == ".":
		ret = ret[0:-1]
	if ret == "":
		return "@"
	else:
		return ret

def BINDPath(domain):
	global bind_path
	return bind_path + domain

def BINDZoneExists(domain):
	return os.path.exists(BINDPath(domain))

def WaitForZoneChanges(domain):
	"""
	Returns
	=======
	0: NOT CHANGED
	1: CHANGED
	2: DELETED
	"""
	global retry_sleep
	global retry_times
	fileName = BINDPath(domain)
	last_mtime = os.stat(fileName).st_mtime
	current_time = time.time()
	elapsed = current_time - last_mtime
	if elapsed <= 1:
		# under a second
		return 2
	for i in range(retry_times):
		time.sleep(retry_sleep)
		if not os.path.exists(fileName):
			return 3
		cur_mtime = os.stat(fileName).st_mtime
		if cur_mtime != last_mtime:
			return 1
	return 0

def WaitForZoneCreated(domain):
	global retry_sleep
	global retry_times
	file = BINDPath(domain)
	for i in range(retry_times):
		time.sleep(retry_sleep)
		if os.path.exists(file):
			return True
	return False

def GetBINDRecords(domain):
	file = BINDPath(domain)
	f = open(file, "r")
	body = f.read()
	f.close()

	records = RR.fromZone(body)
	ss = ""
	for r in records:
		host = HostConvert(r, domain)
		ttl = r.ttl
		cl = CLASS.get(r.rclass)
		qt = QTYPE.get(r.rtype)
		record = r.rdata.toZone()
		line = '%-23s %-7s %-7s %-7s %s' % (host, ttl, cl, qt, record)
		ss += line + "\n"
	return ss

def GetBINDRecordsAndCheck(domain):
	bind = GetBINDRecords(domain)
	if bind == "":
		bind = GetBINDRecords(domain)
	return bind

def GetBINDRecordsUntil(domain):
	for i in range(retry_times):
		try:
			rs = GetBINDRecords(domain)
			if rs == "":
				pass
			else:
				return rs
		except:
			pass
		time.sleep(retry_sleep)
	return None
