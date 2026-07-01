import pathlib
import xml.etree.ElementTree as ET
import re
import json
from collections import defaultdict


def format_time(seconds):
    if seconds >= 60:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes} m. {secs} s."
    else:
        return f"{seconds:.1f} s."


def get_os_from_hostname(hostname):
    """Extract OS from hostname pattern tm-mt-X where X is m/w/u."""
    if not hostname:
        return "Unknown"
    match = re.search(r'tm-mt-([mwu])', hostname)
    if match:
        os_letter = match.group(1)
        if os_letter == 'm':
            return "macOS"
        elif os_letter == 'w':
            return "Windows"
        elif os_letter == 'u':
            return "Ubuntu"
    return "Unknown"


folder = pathlib.Path(".")

# Structure: suite -> test -> OS -> list of times
results = defaultdict(lambda: defaultdict(lambda: {"macOS": [], "Windows": [], "Ubuntu": []}))

for file_path in folder.glob("*.xml"):
    root = ET.parse(file_path).getroot()
    suite_name = root.attrib.get("name")
    hostname = root.attrib.get("hostname")
    os_name = get_os_from_hostname(hostname)
    
    if not suite_name:
        continue
    
    # Parse each testcase
    for testcase in root.findall("testcase"):
        classname = testcase.attrib.get("classname", "")
        time_str = testcase.attrib.get("time", "0")
        
        # Extract test name from classname (format: suite_name.test_name)
        if "." in classname:
            test_name = classname.split(".")[-1]
        else:
            test_name = classname
        
        if test_name:
            results[suite_name][test_name][os_name].append(float(time_str))

# Build JSON tree structure: suite -> {time, tests: {test -> {average, OS: time}}}
json_tree = {}
for suite_name in sorted(results.keys()):
    tests = results[suite_name]
    
    # First pass: calculate all test averages to get suite total
    test_entries = []
    suite_total_avg = 0
    
    for test_name in sorted(tests.keys()):
        os_data = tests[test_name]
        
        # Calculate totals first to get average
        os_totals = {}
        for os_name in ["macOS", "Windows", "Ubuntu"]:
            times = os_data[os_name]
            if times:
                os_totals[os_name] = sum(times)
        
        # Calculate average
        if os_totals:
            avg_time = sum(os_totals.values()) / len(os_totals)
            avg_str = format_time(avg_time)
            suite_total_avg += avg_time
        else:
            avg_time = 0
            avg_str = "N/A"
        
        test_entries.append((test_name, avg_str, os_totals))
    
    # Build suite entry with time field
    json_tree[suite_name] = {"time": format_time(suite_total_avg)}
    
    # Add test entries
    for test_name, avg_str, os_totals in test_entries:
        json_tree[suite_name][test_name] = {"average": avg_str}
        for os_name in ["macOS", "Windows", "Ubuntu"]:
            if os_name in os_totals:
                json_tree[suite_name][test_name][os_name] = format_time(os_totals[os_name])

# Write JSON
with open("results.json", "w") as f:
    json.dump(json_tree, f, indent=2)