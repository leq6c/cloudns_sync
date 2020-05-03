import os
import time
import fcntl
import cloudns_api as capi
from utils_sync import GetDiffs, Copy
from utils_bind import bind_path, GetBINDRecordsAndCheck
from utils_cloudns import CloudnsUpdateRecordsBindFormat
from utils_debugging import Echo, Log, SetPrintConsole, EchoTraceback

# PATH
base_dir = "/etc/cloudns_sync/"
bind_path = os.environ['BIND_NAMED_PATH']
local_repo = base_dir + "repo/"
normal_log = base_dir + "main.log"
error_log = base_dir + "error.log"
lock_file = base_dir + "lf.lock"

# Debug
debugging = os.environ['CLOUDNS_API_DEBUG'] == "True"
SetPrintConsole(debugging)
call_api = True

def Main():
	# CREATE DIR
	os.makedirs(base_dir, exist_ok=True)

	try:
		dels, creates, updates = GetDiffs(bind_path, local_repo)
	except:
		Log("init: error while getting diffs", error_log)
		EchoTraceback()
		exit()

	for zone in dels:
		# call delete zone API
		try:
			if call_api:
				capi.zone.delete(domain_name=zone)
		except:
			continue
		# remove file
		Log("zone deleted => " + zone, normal_log)
		try:
			os.remove(os.path.join(local_repo, zone))
		except:
			Log("delete: error while removing local file", error_log)
			EchoTraceback()
			continue

	for zone in creates:
		# call create zone API
		try:
			if call_api:
				capi.zone.create(domain_name=zone, zone_type="master")
		except:
			continue
		Log("zone created => " + zone, normal_log)

	for zone in updates:
		# get bind
		try:
			bind = GetBINDRecordsAndCheck(zone)
		except:
			Log("update: error while getting bind " + zone, error_log)
			EchoTraceback()
			continue
		# call update zone API
		try:
			if call_api:
				CloudnsUpdateRecordsBindFormat(zone, bind)
		except:
			Log("create: error while calling api " + zone, error_log)
			EchoTraceback()
			continue
		Log("zone updated => " + zone, normal_log)
		# copy file
		try:
			Copy(zone, bind_path, local_repo)
		except:
			Log("update: error while copying file " + zone, error_log)
			EchoTraceback()
			continue

if not os.path.exists(lock_file):
	with open(lock_file, "w+") as lf:
		pass

with open(lock_file, "w") as lockFile:
	try:
		fcntl.flock(lockFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
		Main()
	except IOError:
		print("already running")
		pass
