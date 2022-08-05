import json
import requests

def createAPIData(url):
    response = requests.get(url)
    data = response.json()
    return data

def getShort(d):
    return d['shortDescription'] if 'shortDescription' in d else "We don't seem to know a lot about this one…"

def filterCollegeData(d):
    data = d["colleges"]
    schools = []
    for school in data:
            schools.append(
                {
                    "Name": school["name"],
                    "City": school["city"],
                    "State": school["stateAbbr"],
                    "ShortDescription": getShort(school),
                    "Website": school["website"],
                    "Acceptance": school["acceptanceRate"]*100,
                    "Enrolled Students": school["enrolledStudents"],
                    "Average Cost of Attendance": school["avgCostOfAttendance"],
                    "Average Financial Aid Award": school["averageFinancialAid"],
                    "Logo Image": school["logoImage"],
                    "Campus Image": school["campusImage"]
                }
            )
    return schools
