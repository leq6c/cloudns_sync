import os
import filecmp
import shutil

def Filter(path, files):
	ret = []
	for f in files:
		cur_path = os.path.join(path, f)
		if not os.path.isfile(cur_path):
			continue
		if f == None or f == "named.root" or f == "PROTO.localhost.rev" or f == "localhost.rev" or f == "make-localhost":
			continue
		if "." not in f:
			continue
		ret.append(f)
	return ret

def GetDiffs(src, dst):
	os.makedirs(dst, exist_ok=True)
	src_files = Filter(src, os.listdir(src))
	dst_files = Filter(dst, os.listdir(dst))
	# vars
	need_delete_zone = []
	need_create_zone = []
	need_update_zone = []
	#1. need to be deleted.
	for f in dst_files:
		if f not in src_files:
			need_delete_zone.append(f)
	#2. need to be created and updated.
	for f in src_files:
		if f not in dst_files:
			need_create_zone.append(f)
			need_update_zone.append(f)
		else:
			# update or stay
			s_f = os.path.join(src, f)
			d_f = os.path.join(dst, f)
			if filecmp.cmp(s_f, d_f):
				pass #stay
			else:
				need_update_zone.append(f)
	return need_delete_zone, need_create_zone, need_update_zone

def Copy(f, src, dst):
	src = os.path.join(src, f)
	dst = os.path.join(dst, f)
	shutil.copyfile(src, dst)
