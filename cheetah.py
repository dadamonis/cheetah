import sys
import time
import argparse
from sys import argv
from collections import OrderedDict


def summary():
    match_strings = ["NuoAgent version", "ASSERT", "error", "failed", "INFO", "WARN", "SEVERE", "Local node", "Remote Node",
                     "minorty partition", "heartbeat expired", "evict", "DIED", "exit code", "Database is inactive",
                     "Node joined", "Node left", "deleting database", "stopping database", "Environment.logEnv",
                     "LocalServer.convertTo"]

    print "Summarized Totals"

    summarize = ["error", "INFO", "WARN", "failed", "Database is inactive"]
    summarize_length = 5

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
    print "== Total Message Counts =="
    print "======================================"
    for string in matches:
        if " (last %d lines)" % summarize_length not in string:
            print "Total entires matching \"%s\": %d" % (string, len(matches[string]))
    select()


def assertion():
    # search for:
    # Assertion, exit code only if assert is found and get line numbers
    print "\nDESCRIPTION:\nThe presence of one or more 'Assertion' messages in the agent.log",\
          "file indicates runtime failures of TEs and\or SMs.\nIf 'Assertion' messages are",\
          "present execute a 'nuodb [domain] > diagnose domain' command to collect debug information.\n"
    match_strings = ["ASSERT"]
    # Create data structure to handle results
    matches = OrderedDict()
    for string in match_strings:
        matches[string] = []

    for i, s in enumerate(data, 1):
        for string in match_strings:
            if string in s:
                matches[string].append('Line %03d: %s' % (i, s,))
    for string in matches:
        print "%s:" % string.upper()
        if len(matches[string]) > 0:
            print '\n'.join([str(myelement) for myelement in matches[string]])
        else:
            # print "No %s entries in the log" % string.upper()
            print "0 entries in the log."
    select()


def env():
    # search for:
    # Environment.logEnv, LocalServer.convertTo
    print "\nDESCRIPTION:\nThe following contains important envrionmental and configuration",\
          "details about the host that is running NuoDB.\nUse this information to verify things",\
          "such as NuoDB and Java version, domain and RAFT configuration.\n"
    match_strings = [
        "Environment.logEnv", "LocalServer.convertTo", "PropertiesContainerImpl"]
    print "env data"
    # Create data structure to handle results
    matches = OrderedDict()
    for string in match_strings:
        matches[string] = []

    for i, s in enumerate(data, 1):
        for string in match_strings:
            if string in s:
                matches[string].append('Line %03d: %s' % (i, s,))
    for string in matches:
        print "%s:" % string.upper()
        if len(matches[string]) > 0:
            print '\n'.join([str(myelement) for myelement in matches[string]])
        else:
            # print "No %s entries in the log" % string.upper()
            print "0 entries in the log."
    select()


def nodes():
    # print TE/SM info and split output by local
    # search for:
    # "exit code", "Database is inactive",
    # "Node joined", "Node left", "deleting database", "stopping database"
    match_strings = ["Node joined", "Node left", "Local node", "Remote Node"]
    print "env data"
    # Create data structure to handle results
    matches = OrderedDict()
    for string in match_strings:
        matches[string] = []

    for i, s in enumerate(data, 1):
        for string in match_strings:
            if string in s:
                matches[string].append({'Line': i, 'String': s})
    nodemerge = matches['Node joined'] + matches['Node left']
    matches['Node'] = sorted(nodemerge, key=lambda x: x['Line'])
    del matches['Node joined']
    del matches['Node left']

    for string in matches:
        print "%s:" % string.upper()
        if len(matches[string]) > 0:
            print '\n'.join(['Line {0}, {1}'.format(x['Line'], x['String']) for x in matches[string]])
        else:
            # print "No %s entries in the log" % string.upper()
            print "0 entries in the log."
    select()


def search():
    print "DESCRIPTION:\nInteractive search prompt.\n\n",\
          "ATTN: Search is case sensative.\n",\
        "'\q' to quit."

    while True:
        answer = raw_input("\nEnter Search Value : ")
        if answer == "\q":
            print "\nReturning to options...(\q)"
            select()
        else:
            for i, line in enumerate(data):
                if answer in line:
                    for l in data[i:i + 1]:
                        print "\n", l,


def select():

    while True:
        print "\n Select one: \n a (Assertion Messages)\n e (Environment Details)\n n (List TEs and SMs)\n s (Search Prompt)\n sum (Summarized Informaton)\n q (Quit)"
        answer = raw_input("> ")
        if answer == "a":
            assertion()
        elif answer == "e":
            env()
        elif answer == "n":
            nodes()
        elif answer == "q":
            print "\nexiting...\n"
            exit()
        elif answer == "s":
            search()
        elif answer == "sum":
            summary()
        else:
            print "Invalid selection...try again:"

parser = argparse.ArgumentParser(
    description="This utility is meant to help interactively parse an agent log file.")
# the followign is a positional argument note the lack of --
parser.add_argument(
    "logFile", nargs='?', help="the agent.log file(s) to parse.")
# parser.add_argument(
#   'files', metavar='N', type=str, nargs='+', help="files to be processed")
parser.add_argument(
    "-a", "--assertion", help="pull all assertion messages; local messages only", action="store_true")
parser.add_argument(
    "-e", "--environment", help="pull the environment details", action="store_true")
parser.add_argument(
    "-n", "--nodelist", help="pull all TE / SM process info; remote and local", action="store_true")
parser.add_argument(
    "-s", "--search", help="search prompt", action="store_true")
args = parser.parse_args()
with open(args.logFile) as f:
    data = f.read().splitlines()
    if args.assertion:
        assertion()
    elif args.environment:
        env()
    elif args.nodelist:
        nodes()
    elif args.search:
        search()
    else:
        summary()
