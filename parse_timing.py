#!/usr/bin/env python3
"""
Parse timing data from syslog and extract execution trace for Cheddar verification.

Usage:
    python3 parse_timing.py <syslog_file> > timing_trace.txt
"""

import sys
import re
from collections import defaultdict

def parse_syslog(filename):
    """Parse syslog file and extract timing information."""

    thread_data = defaultdict(list)

    with open(filename, 'r') as f:
        for line in f:
            # Look for timing lines with format:
            # [COURSE:X][ASSIGNMENT:Y] Thread Z start X @time on core C
            # [COURSE:X][ASSIGNMENT:Y] Thread Z end value @time on core C

            start_match = re.search(r'\[COURSE:\d+\]\[ASSIGNMENT:\d+\] Thread (\d+) start .* @([\d.]+) on core', line)
            end_match = re.search(r'\[COURSE:\d+\]\[ASSIGNMENT:\d+\] Thread (\d+) end .* @([\d.]+) on core', line)

            if start_match:
                thread_num = int(start_match.group(1))
                timestamp = float(start_match.group(2))
                thread_data[thread_num].append({
                    'type': 'start',
                    'time': timestamp
                })

            elif end_match:
                thread_num = int(end_match.group(1))
                timestamp = float(end_match.group(2))
                thread_data[thread_num].append({
                    'type': 'end',
                    'time': timestamp
                })

    return thread_data

def generate_timing_report(thread_data):
    """Generate timing report suitable for Cheddar analysis."""

    print("=" * 80)
    print("TIMING EXECUTION TRACE")
    print("=" * 80)
    print()

    # Analyze each thread
    for thread_num in sorted(thread_data.keys()):
        events = thread_data[thread_num]
        print(f"Thread {thread_num} Execution Analysis:")
        print("-" * 60)

        # Pair start/end events
        i = 0
        execution_num = 0
        while i < len(events) - 1:
            if events[i]['type'] == 'start' and events[i+1]['type'] == 'end':
                execution_num += 1
                start_time = events[i]['time']
                end_time = events[i+1]['time']
                duration = end_time - start_time

                print(f"  Execution #{execution_num}:")
                print(f"    Start Time: {start_time:.6f} ms")
                print(f"    End Time:   {end_time:.6f} ms")
                print(f"    Duration:   {duration:.6f} ms")

                i += 2
            else:
                i += 1

        print()

    # Generate summary statistics
    print("=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)

    for thread_num in sorted(thread_data.keys()):
        events = thread_data[thread_num]
        durations = []

        i = 0
        while i < len(events) - 1:
            if events[i]['type'] == 'start' and events[i+1]['type'] == 'end':
                duration = events[i+1]['time'] - events[i]['time']
                durations.append(duration)
                i += 2
            else:
                i += 1

        if durations:
            print(f"Thread {thread_num}:")
            print(f"  Total Executions: {len(durations)}")
            print(f"  Min Duration:     {min(durations):.6f} ms")
            print(f"  Max Duration:     {max(durations):.6f} ms")
            print(f"  Avg Duration:     {sum(durations)/len(durations):.6f} ms")
            print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_timing.py <syslog_file>")
        sys.exit(1)

    syslog_file = sys.argv[1]

    try:
        thread_data = parse_syslog(syslog_file)
        generate_timing_report(thread_data)
    except FileNotFoundError:
        print(f"Error: File '{syslog_file}' not found")
        sys.exit(1)

if __name__ == '__main__':
    main()
