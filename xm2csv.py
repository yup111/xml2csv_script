import xml.etree.ElementTree as ET
import csv

projects_list = []
# project_dict = {}
file_name = '16_9.xml'
tree = ET.parse(file_name)
root = tree.getroot()

projects = root.findall(".//Hsrproj")

Investigator_list = root.findall(".//Investigator")
total_len = len(Investigator_list)

for project in projects:
    FundMount = ""
    if len(project.findall(".//YearFundingAmount/Amount")) > 0:
        for x in project.findall(".//YearFundingAmount/Amount"):
            if x.text is None:
                continue
            FundMount = x.text + ','

    project_dict = {}
    projects_dict= {
        "ProjectID": project.findall(".//ProjectID")[0].text,
        "DateCreated": "/".join([item.text for item in project.findall(".//DateCreated/*")]),
        "ProjectTitle": project.findall(".//ProjectTitle")[0].text,
        "Investigator": "",
        "LastName": project.findall(".//Investigator/LastName")[0].text if len(project.findall(".//Investigator/LastName")) > 0 else "",
        "ForeName": project.findall(".//Investigator/ForeName")[0].text if len(project.findall(".//Investigator/ForeName")) > 0 else "",
        "Initials": project.findall(".//Investigator/Initials")[0].text if len(project.findall(".//Investigator/Initials")) > 0 else "",
        "Email": project.findall(".//Investigator/Email")[0].text if len(project.findall(".//Investigator/Email")) > 0 else "",
        "PerformingOrganization": project.findall(".//PerformingOrganization/Name")[0].text if len(project.findall(".//PerformingOrganization/Name")) > 0 else "",
        "URLlink": project.findall(".//PerformingOrganization/URLlink")[0].text if len(project.findall(".//PerformingOrganization/URLlink")) > 0 else "",
        "State": project.findall(".//PerformingOrganization/State")[0].text if len(project.findall(".//PerformingOrganization/State")) > 0 else "",
        "Country": project.findall(".//PerformingOrganization/Country")[0].text if len(project.findall(".//PerformingOrganization/Country")) > 0 else "",
        "ZipCode": project.findall(".//PerformingOrganization/ZipCode")[0].text if len(project.findall(".//PerformingOrganization/ZipCode")) > 0 else "",
        "AwardID": project.findall(".//Award/AwardID")[0].text if len(project.findall(".//Award/AwardID")) > 0 else "",
        "AgencyName": project.findall(".//Agency/Name")[0].text,
        "AgencyLink": project.findall(".//Agency/URLlink")[0].text if len(project.findall(".//Agency/URLlink")) > 0 else "",
        "InitialYear": "/".join([x.text for x in project.findall(".//InitialYear/*")]),
        "FinalYear": "/".join([x.text for x in project.findall(".//FinalYear/*")]),
        "AwardType": project.findall(".//AwardType")[0].text if len(project.findall(".//AwardType")) > 0 else "",
        "ProjectStatus": project.findall(".//ProjectStatus")[0].text,
        "Abstract": project.findall(".//Abstract/AbstractText")[0].text if len(project.findall(".//Abstract/AbstractText")) > 0 else "",
        "MeshList": ",".join([x.text for x in project.findall(".//MeshHeading/*")]),
        "MajorTopic": ",".join([x.text for x in project.findall(".//MeshHeading/QualifierName")]),
        "Keywords": ",".join([x.text for x in project.findall(".//Keyword")]),
        "FundYear": ",".join([x.text for x in project.findall(".//YearFundingAmount/Year")]) if len(project.findall(".//YearFundingAmount/Year")) > 0 else "",
        "FundMount": FundMount,
        "NumberOfSubjects": project.findall(".//NumberOfSubjects")[0].text if len(project.findall(".//NumberOfSubjects")) > 0 else "",
        "PopulationBase": project.findall(".//PopulationBase")[0].text if len(project.findall(".//PopulationBase")) > 0 else "",
        "StudyDesign": project.findall(".//StudyDesign")[0].text if len(project.findall(".//StudyDesign")) > 0 else "",

    }
    projects_list.append(projects_dict)

header = []
for key, value in projects_list[0].items():
    header.append(key)

with open('16_9.csv', 'a+', newline = '', encoding = 'utf-8') as csv_f:
    writer = csv.DictWriter(csv_f, fieldnames=header, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for project in projects_list:
        writer.writerow(project)