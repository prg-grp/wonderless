import csv
import git


# get the url for downloading the projects from Github
def make_project_url(file_urls, project_urls):
    wtr = csv.writer(open(project_urls, 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow(['Project_URLs'])

    with open(file_urls, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            wtr.writerow([row[1].split('/blob')[0]])


# remove the duplications
def remove_duplications(project_urls, no_duplication_urls):
    with open(project_urls, 'r') as in_file, open(no_duplication_urls, 'w') as out_file:
        seen = set()
        for row in in_file:
            if row in seen:
                continue  # skip duplicate

            seen.add(row)
            out_file.write(row)


# clone the tmaster branch of projects
def clone_projects(project_urls):
    # set the directory in which you want to store the projects
    directory = '/storage/nfs/nafise/repositories/'
    with open(project_urls, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            url = row[0].rstrip()
            new_url = url.replace('://', '://:@')
            print(new_url)
            try:
                git.Repo.clone_from(new_url, directory + new_url.split('/')[-2] + "_" +
                                    new_url.split('/')[-1])
            except git.exc.GitCommandError as gce:
                print(gce)


# ----------------------------- MAIN --------------------------------------


make_project_url('file_urls.csv', 'project_url.csv')
remove_duplications('project_url.csv', 'project_urls.csv')
clone_projects('project_urls.csv')
