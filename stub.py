#!/usr/bin/env python

import os
import subprocess
import sys
import traceback

# ink/stitch
#
# stub.py: pyinstaller execution stub
#
# pyinstaller packages the inkstitch extensions into nice tidy executables.
# That's great, but Inkscape can't execute a plain binary as an extension(!).
#
# This Python script exists only to execute the actual extension binary.  It
# can be copied to, e.g., "embroider_params.py", in which case it will look
# for a binary at inkstitch/bin/embroider_params.
script_name = os.path.basename(__file__)

if script_name.endswith('.py'):
    binary_name = script_name[:-3]
else:
    # Probably not right, but we can at least try.
    binary_name = script_name

binary_path = os.path.join("inkstitch", "bin", binary_name)

args = sys.argv[:]
args[0] = binary_path

# os.execve works here for Linux, but only this seems to get the
# extension output to Inkscape on Windows
try:
    extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = extension.communicate()
except BaseException:
    print >> sys.stderr, "Unexpected error launching Ink/Stitch."
    print >> sys.stderr, "If you're having trouble, please file an issue here, including the text below:"
    print >> sys.stderr, "  https://github.com/inkstitch/inkstitch/issues\n"
    print >> sys.stderr, "Tried to launch:", binary_path
    print >> sys.stderr, "Arguments:", args
    print >> sys.stderr, "Debugging information:\n"
    print >> sys.stderr, traceback.format_exc()
    sys.exit(1)

if sys.platform == "win32":
    import msvcrt

    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

try:
    # In Python 3, we need to use sys.stdout.buffer to write binary data to stdout.
    sys.stdout.buffer.write(stdout)
    sys.stdout.buffer.flush()
except AttributeError:
    # Python 2 doesn't have sys.stdout.buffer but we can write binary data to stdout by default.
    sys.stdout.write(stdout)
    sys.stdout.flush()

stderr = stderr.strip()
if stderr:
    try:
        sys.stderr.buffer.write(stderr)
        sys.stderr.buffer.flush()
    except AttributeError:
        sys.stderr.write(stderr)
        sys.stderr.flush()

sys.exit(extension.returncode)
