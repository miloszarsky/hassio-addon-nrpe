#!/usr/bin/env python3
## Author: RocknRollGlue
## License MIT
## Tested on Ubuntu, should be compatible with debian as well, but not tested
## For Icinga2 to load the plugin, place in the plugin folder, default directory is /usr/lib/nagios/plugins

__version__ = 0.5

import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-w', '--warning_level', type=str, required=False, help='Threshold %% of warning levels of memory available. Defaults to 70', default=70)
parser.add_argument('-c', '--critical_level', type=str, required=False, help='Threshold %% of critical levels of memory available. Defaults to 90', default=90)
params = parser.parse_args()

def AttemptParseArguments():
    #Attempt to parse arguments
    try:
        params.warning_level = int(params.warning_level)
        params.critical_level = int(params.critical_level)
        return True
    except ValueError:
        print('MEMORY UNKNOWN: INCORRECT PARAMETERS PARSED')
        sys.exit(3)

def getMemoryUsage():
    total_mem = 0
    avail_mem = 0
    # Get the total system memory in KB via /proc/ data
    with open('/proc/meminfo', 'r') as meminfo:
        for line in meminfo:
            # Get the total system memory in KB
            if line.startswith('MemTotal:'):
                total_mem = int(line.split()[1])
                # Get the free system memory in KB
            if line.startswith('MemAvailable:'):
                avail_mem = int(line.split()[1])

    #return percentage of available memory
    return 100-(avail_mem / total_mem)*100

def getStatus(memory_usage):
    # we default to unknown state
    # Look at https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/#status
    status_dict = {
        "code": 3,
        "string": "UNKOWN"
    }
    if memory_usage >= int(params.critical_level):
        status_dict = {
            "code": 2,
            "string": "CRITICAL"
        }
    elif memory_usage >= int(params.warning_level):
        status_dict = {
            "code": 1,
            "string": "WARNING"
        }
    elif memory_usage > 0 and memory_usage < int(params.warning_level):
        status_dict = {
            "code": 0,
            "string": "OK"
        }
    return status_dict
        

def generateOutputString(displayString, _label, _value, _warn_value, _crit_value):
    # creating output as according to https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/#performance-data-metrics
    rtaString = "'{label}'={value};{warn_value};{crit_value};0;100".format(
        label = _label, 
        value = _value, 
        warn_value = _warn_value, 
        crit_value = _crit_value 
    )
    return f"{displayString} |{rtaString}"

AttemptParseArguments()
_memoryUsage = round(getMemoryUsage(),2 )
_status=getStatus(_memoryUsage)
_displayString = "STATUS {status} - Memory Usage: {memory}%".format(status=_status['string'], memory=_memoryUsage)
print(generateOutputString(_displayString, "Memory", _memoryUsage, int(params.warning_level), int(params.critical_level)))
sys.exit(_status["code"])

