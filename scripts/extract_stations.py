#!/usr/bin/env python3
"""
BlueBikes Station Extractor

This script extracts station information from BlueBikes trip data.
It processes input data from standard input (stdin) and outputs a CSV of
unique stations with their IDs, names, and coordinates to standard output (stdout).

Usage:
    cat data/trip_data.csv | python scripts/extract_stations.py > data/stations.csv
    
Features:
    - Automatically detects and extracts all station-related fields 
    - Consolidates data from start and end points of trips
    - Outputs a unique list of stations with all associated information
"""

# /// script
# requires-python = ">=3.6"
# dependencies = []
# ///

import csv
import sys
from collections import defaultdict

def extract_stations():
    """
    Extract station information from trip data.
    
    Reads trip data from stdin, extracts all station information, and
    writes consolidated station data to stdout as CSV.
    """
    # Dict to store station information
    stations = defaultdict(dict)
    
    reader = csv.DictReader(sys.stdin)
    
    # Identify station-related fields in the header
    station_fields = {
        'start': set(),
        'end': set()
    }
    
    for field in reader.fieldnames:
        if field.startswith('start_station_'):
            if field != 'start_station_id':
                station_fields['start'].add(field)
        elif field.startswith('end_station_'):
            if field != 'end_station_id':
                station_fields['end'].add(field)
    
    # Process each row
    for row in reader:
        # Process start station
        if 'start_station_id' in row and row['start_station_id']:
            station_id = row['start_station_id']
            
            # Update station info if any field is non-empty
            for field in station_fields['start']:
                if row.get(field) and not stations[station_id].get(field.replace('start_', '')):
                    stations[station_id][field.replace('start_', '')] = row[field]
            
            # Add coordinates if available
            if row.get('start_lat') and not stations[station_id].get('latitude'):
                stations[station_id]['latitude'] = row['start_lat']
            if row.get('start_lng') and not stations[station_id].get('longitude'):
                stations[station_id]['longitude'] = row['start_lng']
        
        # Process end station
        if 'end_station_id' in row and row['end_station_id']:
            station_id = row['end_station_id']
            
            # Update station info if any field is non-empty
            for field in station_fields['end']:
                if row.get(field) and not stations[station_id].get(field.replace('end_', '')):
                    stations[station_id][field.replace('end_', '')] = row[field]
            
            # Add coordinates if available
            if row.get('end_lat') and not stations[station_id].get('latitude'):
                stations[station_id]['latitude'] = row['end_lat']
            if row.get('end_lng') and not stations[station_id].get('longitude'):
                stations[station_id]['longitude'] = row['end_lng']
    
    # Write output CSV
    if stations:
        # Get all possible fields from the collected data
        fieldnames = ['station_id'] + sorted(set().union(*(d.keys() for d in stations.values())))
        
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write each station's data
        for station_id, station_data in sorted(stations.items()):
            row = {'station_id': station_id}
            row.update(station_data)
            writer.writerow(row)

if __name__ == "__main__":
    extract_stations()
    