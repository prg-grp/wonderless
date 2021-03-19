import subprocess
import os
import csv
import datetime
import sys
import shutil


# get the git commit history of each repository
def get_git_commits():
    parent_dir = '/storage/nfs/nafise/filtered_repos/'
    for x in os.listdir(parent_dir):
        repo_path = parent_dir + x
        if os.path.isdir(repo_path):
            os.chdir(repo_path)
            command = 'git log --date=short --pretty=format:"%h%x09%an%x09%cd%x09%s">/storage/nfs/nafise/git_commits/' \
                      + x + '_git_commits.csv'
            subprocess.call(command, shell=True)


# get the lifetime of each project(difference between last commit and first commit)
def get_lifetime(result):
    csv.field_size_limit(sys.maxsize)
    parent_dir = '/storage/nfs/nafise/git_commits/'
    for x in os.listdir(parent_dir):
        # skip hidden files
        if x.startswith('.'):
            print(x)
            continue
        file_path = parent_dir + x
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    commits = csv.reader(f, delimiter='\t')
                    dates = []
                    for commit in commits:
                        dates.append(commit)
                    last_commit = datetime.datetime.strptime(dates[0][2], '%Y-%m-%d').date()
                    first_commit = datetime.datetime.strptime(dates[-1][2], '%Y-%m-%d').date()
                    lifetime = (last_commit.year - first_commit.year) * 12 + last_commit.month - first_commit.month
            except UnicodeDecodeError as ude:
                print(ude)
                print(x)

        with open(result, 'a+') as result:
            wtr = csv.writer(result)
            project_id = x.split('_git_commits.csv')[0]
            url = 'https://github.com/' + project_id.split('_', 1)[0] + '/' + project_id.split('_', 1)[1]
            wtr.writerow([url, last_commit, first_commit, lifetime, project_id])


# get the id of projects with a lifetime of less than a year
def get_immature_projects(git_commits, remove_ids):
    with open(git_commits, 'r') as f:
        rows = csv.reader(f)
        with open(remove_ids, 'w') as removed:
            wtr = csv.writer(removed)
            wtr.writerow(['Project_id'])
            for row in rows:
                if int(row[3]) < 12:
                    wtr.writerow([row[4]])


# remove projects by id
def remove_immature_projects(project_ids):
    parent_dir = '/storage/nfs/nafise/filtered_repos/'
    with open(project_ids, 'r') as file:
        rows = csv.reader(file)
        next(rows, None)
        for row in rows:
            repo_dir = parent_dir + row[0]
            print(repo_dir)
            if os.path.isdir(repo_dir):
                shutil.rmtree(repo_dir, ignore_errors=True)


# ----------------------------- MAIN --------------------------------------


get_git_commits()
get_lifetime('git_commits.csv')
get_immature_projects('git_commits.csv', 'remove_ids.csv')
remove_immature_projects('remove_ids.csv')
