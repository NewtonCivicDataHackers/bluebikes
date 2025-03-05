#!/usr/bin/env python3
"""
BlueBikes Newton Station Filter

This script filters BlueBikes trip data to only include trips involving Newton stations.
Newton stations are identified by station IDs starting with 'N'.
The script processes input data from standard input (stdin) and outputs filtered
results to standard output (stdout).

Usage:
    cat data/trip_data.csv | python scripts/filter_newton.py > data/newton_trips.csv
    
Features:
    - Filters for any trip that either starts or ends at a Newton station
    - Preserves all original columns from input data
    - Handles potential missing station ID values gracefully
"""

# /// script
# requires-python = ">=3.6"
# dependencies = []
# ///

import csv
import sys

def filter_n_stations():
    """
    Filter trip data to only include trips involving Newton stations.
    
    Reads trip data from stdin and writes filtered data to stdout.
    A trip is included if either the start or end station ID starts with 'N'.
    """
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    
    for row in reader:
        # Get station IDs, handling potential missing values
        start_id = row.get('start_station_id', '')
        end_id = row.get('end_station_id', '')
        
        # Check if either station ID starts with 'N' (case-sensitive)
        if (start_id.startswith('N') or end_id.startswith('N')):
            writer.writerow(row)

if __name__ == "__main__":
    filter_n_stations()
