#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ghpytracker.settings")
	os.environ.setdefault("DJANGO_PROJECT_DIR", os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(os.environ['DJANGO_PROJECT_DIR'] + '/irc')

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)