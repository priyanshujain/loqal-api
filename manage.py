#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

    import django
    from django.core.management import execute_from_command_line

    sys.stdout.write("Django VERSION " + str(django.VERSION) + "\n")

    execute_from_command_line(sys.argv)
