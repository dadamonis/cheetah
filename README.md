# Tools
Collection of tools, code snippets, etc that may be useful

#### Cheetah.py - Used for parsing agent.log files

##### Usage
```
usage: cheetah.py [-h] [-a] [-e] [-n] [-s] logFile

This utility is meant to help interactively parse an agent log file.

positional arguments:
  logFile            the agent.log file(s) to parse.

optional arguments:
  -h, --help         show this help message and exit
  -a, --assertion    pull all assertion messages; local messages only
  -e, --environment  pull the environment details
  -n, --nodelist     pull all TE / SM process info; remote and local
  -s, --search       search prompt (phase search)
 ```
##### Default Behavior  
When executed with no optional arguments, cheetah retruns a summarized list of default items as well as some canned options for further investigation.

```
$ python cheetah.py agent.log 

======================================
Parsed on: Fri Aug  7 13:35:39 2015
======================================

======================================
==Total Message Counts
======================================
Total entires matching "NuoAgent version": 2
Total entires matching "Assertion": 0
Total entires matching "error": 0
Total entires matching "failed": 5
Total entires matching "INFO": 133
Total entires matching "WARN": 5
Total entires matching "SEVERE": 0
Total entires matching "Local node": 0
Total entires matching "Remote Node": 0
Total entires matching "minorty partition": 0
Total entires matching "heartbeat expired": 0
Total entires matching "evict": 0
Total entires matching "DIED": 0
Total entires matching "exit code": 2
Total entires matching "Database is inactive": 0
Total entires matching "deleting database": 0
Total entires matching "stopping database": 1
Total entires matching "Environment.logEnv": 20
Total entires matching "LocalServer.convertTo": 4
Total entires matching "Node": 6

 Select one: 
 a (Assertion Messages)
 e (Environment Details)
 n (List TEs and SMs)
 s (Search Prompt)
 q (Quit)
> 

```
