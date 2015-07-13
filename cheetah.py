import sys
from sys import argv
from collections import OrderedDict

# Prtint to log and to file


class Logger(object):

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("chreetah.out", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger()

# Find and catalog each log line that matches these strings
match_strings = ["NuoAgent version", "Assertion", "error", "failed", "INFO", "WARN", "SEVERE", "Local node", "Remote Node",
                 "minorty partition", "heartbeat expired", "evict", "DIED", "exit code", "Database is inactive",
                 "Node joined", "Node left", "deleting database"]
# Don't print out every line that contains these strings, instead trucnate
# to the last N lines
summarize = ["error", "INFO", "WARN", "failed", "Database is inactive"]
summarize_length = 5

if len(argv) > 1:
    files = argv[1:]
else:
    print "ERROR: You must provide at least one log file to be processed."
    print "Example:"
    print "%s my.log" % argv[0]
    exit(2)

for filename in files:
    with open(filename) as f:
        data = f.read().splitlines()

        # Create data structure to handle results
        matches = OrderedDict()
        for string in match_strings:
            matches[string] = []

        for i, s in enumerate(data, 1):
            for string in match_strings:
                if string in s:
                    matches[string].append('Line %03d: %s' % (i, s,))

        # In some cases there are always more messages than are usable.
        # This returns the  most recent messages for each value in summarize.
        for item in summarize:
            matches["%s (last %d lines)" % (item, summarize_length)] = matches[
                item][(summarize_length * -1):]

        nodemerge = matches['Node joined'] + matches['Node left']
        matches['Node'] = nodemerge
        nodemerge.sort(key=lambda x: x[0])
        del matches['Node joined']
        del matches['Node left']
    print
    print "======================================"
    print "==Printing Analysis..."
    print "======================================"
    print
    print "======================================"
    print "==Total Message Counts"
    print "======================================"
    for string in matches:
        if " (last %d lines)" % summarize_length not in string:
            print "Total entires matching \"%s\": %d" % (string, len(matches[string]))
    print
    print "Continue printing details (y/n)?"
    answer = raw_input("> ")
    if answer == "n":
        print "exiting"
    elif answer == "y":
        print "======================================"
        print "==Message Details"
        print "======================================"
        for string in matches:
            if string not in summarize:
                print "%s:" % string.upper()
                if len(matches[string]) > 0:
                    print '\n'.join([str(myelement) for myelement in matches[string]])
                else:
                    # print "No %s entries in the log" % string.upper()
                    print "0 entries in the log."
                print
