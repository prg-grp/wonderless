import csv
import os


# get the id of all the repositories
def get_project_ids():
    parent_dir = '/storage/nfs/nafise/filtered_repos'
    wtr = csv.writer(open('project_ids.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in os.listdir(parent_dir):
        if x.startswith('.'):
            print(x)
            continue
        wtr.writerow([x])


# find the projects with the same name and different developers
def get_forked_projects(ids):
    repos = {}
    with open(ids, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if row[0].split('_', 1)[1] in repos:
                repos[row[0].split('_', 1)[1]].append(row[0].split('_', 1)[0])
            else:
                repos[row[0].split('_', 1)[1]] = [row[0].split('_', 1)[0]]

    with open('forked.csv', 'w') as result:
        wtr = csv.writer(result)
        for k, v in repos.items():
            if len(v) > 1:
                for i in v:
                    wtr.writerow([i + '_' + k])


# ----------------------------- MAIN --------------------------------------


get_project_ids()
get_forked_projects('project_ids.csv')
