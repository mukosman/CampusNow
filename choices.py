import json
import requests

MALE = "Male"
FEMALE = "Female"
NON_BINARY = "Non-Binary"
GENDER_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (NON_BINARY, "Non-Binary"),
]

BLACK = "Black"
ASIAN = "Asian"
AMERICAN_INDIANS = "American Indian"
HISPANIC = "Hispanic"
PACIFIC = "Pacific Islander"
WHITE = "White"
MIXED = "Mixed"
OTHER = "Other"
RACES_IN_CHOICES = [
    (BLACK, "Black/African American"),
    (ASIAN, "Asian"),
    (AMERICAN_INDIANS, "American Indian/Alaskan Native"),
    (HISPANIC, "Hispanic/Latino"),
    (PACIFIC, "Native Hawaiian/Other Pacific Islander"),
    (WHITE, "White"),
    (MIXED, "Two or more races"),
    (OTHER, "Other"),
]

FRESHMAN = "FR"
SOPHOMORE = "SO"
JUNIOR = "JR"
SENIOR = "SR"
GRADUATE = "GR"
YEAR_IN_SCHOOL_CHOICES = [
    (FRESHMAN, "Freshman"),
    (SOPHOMORE, "Sophomore"),
    (JUNIOR, "Junior"),
    (SENIOR, "Senior"),
    (GRADUATE, "Graduate"),
]

highschools_url = "https://code.org/schools.json"


def createAPIData(url):
    response = requests.get(url)
    data = response.json()
    return data


def getName(d):
    v = d["name"]
    if v is None:
        return
    return v


def getLevels(d):
    v = d["levels"]
    if v is None:
        return
    return v


def getCity(d):
    v = d["city"]
    if v is None:
        return
    return v


def getState(d):
    v = d["state"]
    if v is None:
        return
    return v


def filterHighschoolData(d):
    data = d["schools"]
    schools = []
    for school in data:
        if len(school["levels"]) == 1 and school["levels"][0] == "High School":
            schools.append(
                {
                    "Name": school["name"],
                    "City": school["city"],
                    "State": school["state"],
                }
            )

    return schools


data = createAPIData(highschools_url)
highschools = filterHighschoolData(data)


def getData():
    data = createAPIData(highschools_url)
    return filterHighschoolData(data)


# user_input = 'for'
# filteredList = [i for i, school in enumerate(highschools['Name']) if school.lower().startswith(user_input.lower())]
# toDisplay = [(highschools['Name'][i], highschools['City'][i], highschools['State'][i]) for i in filteredList]

STATE_IN_CHOICES = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA", "California"),("CO", "Colorado"),
("CT","Connecticut"),("DC","Washington DC"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),
("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),
("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),
("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),
("WI","Wisconsin"),("WY","Wyoming")]

christian = "christian"
jewish = "jewish"
muslim = "muslim"
buddhist = "buddhist"
hindu = "hindu"
RELIGONS = [
    (christian,"Christian"),
    (jewish, "Jewish"),
    (muslim, "Mulism"),
    (buddhist, "Buddhist"),
    (hindu, "Hindu"),
]

notSelective = ["notSelective"]
lessSelective = ["lessSelective"]
selective = ["selective"]
verySelective =["verySelective"]
mostSelective = ["mostSelective"]
ACCEPTANCE_IN_CHOICES = [
    (notSelective,"Not Selective"),
    (lessSelective,"Less Selective"),
    (selective,"Selective"),
    (verySelective,"Very Selective"),
    (mostSelective,"Most Selective"), 
]

public = ["public"]
private =["private"]
forProfit = ["forprofit"]
SCHOOL_TYPE_CHOICES = [
    (public,"Public"),
    (private,"Private"),
    (forProfit,"For Profit"),
]

large= ["large"]
medium =["medium"]
small = ["small"]
SIZE_TYPE_CHOICES = [
    (large,"Large"),
    (medium,"Medium"),
    (small,"Small"),
]

four_year = ["4year"]
two_year = ["2year"]
DEGREES =[
    (two_year,"Two Year Degree"),
    (four_year,"Four Year Degree"),
]