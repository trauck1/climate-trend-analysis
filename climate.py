import mysql.connector
from bs4 import BeautifulSoup
import requests
import csv
from collections import defaultdict
from datetime import datetime

#counts the amount entries to see the total amount of missing data
def countEntries(data_list, locations):
    counts = defaultdict(lambda: {"max": 0, "min": 0})

    for row in data_list:
        station = row["NAME"]  # whatever the actual column header is
        if station not in locations:
            continue
        if row["TMAX"]:  # or whatever the header for column 6 is
            counts[station]["max"] += 1
        if row["TMIN"]:  # column 7
            counts[station]["min"] += 1
    for station in locations:
        print(station,"| Max: ", counts[station]["max"], "| Min: ", counts[station]["min"])

#finds how much data is missing by year for the given location
def missingDataByYear(data_list,locations, location):
    currentYear = 1976
    currentMaxMissingCounter = 0
    currentMinMissingCounter = 0
    for row in data_list:
        length = len(row["DATE"])
        newYear = row["DATE"][length-4:length]
        if currentYear != newYear:
            if currentMinMissingCounter > 0 or currentMaxMissingCounter > 0:
                print(currentYear, "MAX:", currentMaxMissingCounter, "MIN:", currentMinMissingCounter)
            currentYear = newYear
            currentMaxMissingCounter = 0
            currentMinMissingCounter = 0
        station = row["NAME"]
        if station not in locations:
            continue
        if station != location:
            continue
        if not row["TMAX"]:  # or whatever the header for column 6 is
            currentMaxMissingCounter+=1
        if not row["TMIN"]:  # column 7
            currentMinMissingCounter+=1

#sorts the data by data
def sortByDate(data_list):
    return sorted(
        data_list,
        key=lambda row: datetime.strptime(row["DATE"], "%m/%d/%Y")
    )
#used to check the largest gaps in temperature data for each of the locations
#was able to see which location had useable data
def findLargestGap(data_list, locations, location):
    currentMinGap = 0
    currentMaxGap = 0
    maxGap = 0
    minGap = 0
    for row in data_list:
        station = row["NAME"]
        if station not in locations:
            continue
        if station != location:
            continue
        if not row["TMAX"]:
            currentMaxGap+=1
        else:
            if currentMaxGap > maxGap:
                maxGap = currentMaxGap
                currentMaxGap = 0
        if not row["TMIN"]:
            currentMinGap+=1
        else:
            if currentMinGap > minGap:
                minGap = currentMinGap
                currentMinGap = 0
    print("Largest Max Gap Found:", maxGap)
    print("Largest Min Gap Found:", minGap)
if __name__ == "__main__":
    with open('4336517.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # lets you use column names instead of indices
        data_list = list(reader)
    #sort the csv by date
    data_list = sortByDate(data_list)
    locations = [
        "SHERBURNE, NY US",
        "MECHANICSVILLE 5 NE, MD US",
        "NEW BRUNSWICK 3 SE, NJ US",
        "LAKE CITY 2 E, FL US",
    ]
    #Should have 18426 entries per location
    countEntries(data_list, locations)
    missingDataByYear(data_list,locations,locations[2])
    findLargestGap(data_list,locations,locations[2])
    

