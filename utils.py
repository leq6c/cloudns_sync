from os import path
import subprocess
import sys
import os

"""
VALIDATION
"""

def Valid(domain, allowNull=True):
	if ".." in domain or "/" in domain or "%" in domain or "$" in domain or "%" in domain:
		return False
	if len(domain) <= 2 and allowNull:
		return False
	return True

def GetDomains():
	args = sys.argv
	if len(args) < 3:
		Error("args invalid")
		exit()
	old_domain = args[1]
	domain = args[2]
	sub_domain = args[3]

	if not Valid(domain, False):
		exit()
	if not Valid(old_domain, True):
		exit()
	if not Valid(sub_domain, False):
		exit()

	if sub_domain != "":
		domain = sub_domain + "." + domain

	return old_domain, domain, sub_domain
