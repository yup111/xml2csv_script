# !/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import csv
import os
import pandas as pd 

def find_duplicate(directory):
    df_= pd.DataFrame()
    list_=[]

    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for f in files:
            df_dummy = pd.read_csv(os.path.join(root, f), index_col=None, header=0)
            list_.append(df_dummy)
    
    df_ = pd.concat(list_)
    projects = df_.groupby("ProjectID")

    df_duplicate = pd.DataFrame()
    list_duplicate = []

    for id_, project in projects:
        print(len(project))
        if(len(project) > 1):
            list_duplicate.append(project)

    df_duplicate = pd.concat(list_duplicate)
    df_duplicate.to_csv("duplicate.csv")

def merge_files(directory):
    df_= pd.DataFrame()
    list_=[]
    record_set = set()

    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for f in files:
            df_dummy = pd.read_csv(os.path.join(root, f), index_col=None, header=0)
            list_.append(df_dummy)
    
    df_ = pd.concat(list_)
    no_duplicates = df_.drop_duplicates(subset='ProjectID', keep="last")
    no_duplicates.to_csv("no_duplicate.csv")

def xml2csv(inputfile, outputfile):
    projects_list = []
    file_name = inputfile
    #get xml tree root
    tree = ET.parse(file_name)
    root = tree.getroot()
    #slice xml tree by projects
    projects = root.findall(".//Hsrproj")
    #iterate project
    for project in projects:
        #attach Fund year and Fund mount value
        FundMount = ""
        FundYear = ""
        if len(project.findall(".//YearFundingAmount")) > 0:
            for x in project.findall(".//YearFundingAmount"):
                year = x.findall(".//Year")[0]
                amount = x.findall(".//Amount")[0]
                
                if year.text is None:
                    continue
                if amount.text is None:
                    continue

                FundYear += year.text + "|"
                FundMount += amount.text + '|'
       #build attribute dictionary
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
            "FundYear": FundYear,
            "FundMount": FundMount,
            "NumberOfSubjects": project.findall(".//NumberOfSubjects")[0].text if len(project.findall(".//NumberOfSubjects")) > 0 else "",
            "PopulationBase": project.findall(".//PopulationBase")[0].text if len(project.findall(".//PopulationBase")) > 0 else "",
            "StudyDesign": project.findall(".//StudyDesign")[0].text if len(project.findall(".//StudyDesign")) > 0 else "",

        }
        #append to project list
        projects_list.append(projects_dict)
    #build header name
    header = []
    for key, value in projects_list[0].items():
        header.append(key)
    #write to csv file
    with open(outputfile, 'a+', newline = '', encoding = 'utf-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=header, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for project in projects_list:
            writer.writerow(project)

if __name__ == "__main__":
    merge_files("../csv")

    # xml2csv('16_9.xml', '16_9.csv')