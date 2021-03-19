import os
import shutil
import yaml
import csv


# walk through the directories to read configuration files and extract the name of provider and number of functions
def read_files(output):
    # set the path to the directory where repositories are saved
    parent_dir = '/storage/nfs/nafise/filtered_repos/'
    provider = []
    functions = []
    for x in os.listdir(parent_dir):
        print(x)
        repo_path = parent_dir + x
        # exclude the configuration files that are placed in a template, demo, or test directory
        exclude = {'template', 'templates', 'example', 'examples', 'demo', 'demos', 'test', 'tests'}
        if os.path.isdir(repo_path):
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [d for d in dirs if d not in exclude]
                for file in files:
                    if file == 'serverless.yml':
                        # check if provider and function properties exist in the file and are readable
                        seen_name = False
                        seen_functions = False
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                with open(file_path, 'r') as f:
                                    docs = yaml.load_all(f, Loader=yaml.BaseLoader)
                                    for doc in docs:
                                        # walk through the properties of the configuration file
                                        for k, v in doc.items():
                                            if k == 'provider':
                                                if not isinstance(v, str):
                                                    for item in v.items():
                                                        if item[0] == 'name':
                                                            provider.append([item[1], x])
                                                            seen_name = True
                                                else:
                                                    provider.append([v, x])
                                                    seen_name = True
                                            if k == 'functions':
                                                functions.append([len(v.items()), x])
                                                seen_functions = True
                                        if not seen_name:
                                            provider.append(['Null', x])
                                            seen_name = True
                                        if not seen_functions:
                                            functions.append([0, x])
                                            seen_functions = True
                        except yaml.YAMLError as exc:
                            print(exc)
                            if not seen_name:
                                provider.append(['exc', x])
                            if not seen_functions:
                                functions.append(['exc', x])
                        except UnicodeDecodeError as ude:
                            print(ude)
                            if not seen_name:
                                provider.append(['ude', x])
                            if not seen_functions:
                                functions.append(['ude', x])
                        except AttributeError as ae:
                            print(ae)
                            if not seen_name:
                                provider.append(['ae', x])
                            if not seen_functions:
                                functions.append(['ae', x])

    print(len(provider), len(functions))
    wtr = csv.writer(open(output, 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow(['project_URL', 'Provider', '#Functions', 'Project_id'])

    for i in range(len(provider)):
        file_id = provider[i][1]
        url = 'https://github.com/' + file_id.split('_', 1)[0] + '/' + file_id.split('_', 1)[1]
        wtr.writerow([url, provider[i][0], functions[i][0], functions[i][1]])


# remove the configuration files that are not executable, have no function or specific provider
def get_empty_projects(projects, filtered_files, filtered_out_files):
    potential_ids = set()
    with open(projects, 'r') as file:
        rows = csv.reader(file)
        with open(filtered_files, 'w') as result:
            wtr = csv.writer(result)
            exclude = {'Null', 'exc', '0'}
            for row in rows:
                # get the id of empty files
                if row[1] in exclude or row[2] in exclude:
                    potential_ids.update([row[3]])
                    continue
                # write filtered results to the csv file
                wtr.writerow(row)

    # check if the empty file is the only configuration file in the project
    with open(filtered_files, 'r') as file:
        rows = csv.reader(file)
        with open(filtered_out_files, 'w') as removed:
            wtr1 = csv.writer(removed)
            wtr1.writerow(['Project_id'])
            # check if the filtered files include the id of the project that has an empty config file
            # if yes, remove the id of project from the set
            for row in rows:
                if row[3] in potential_ids:
                    potential_ids.remove(row[3])
            for project_id in potential_ids:
                wtr1.writerow([project_id])


# remove projects by id
def remove_empty_projects(project_ids):
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


read_files('analysis.csv')
get_empty_projects('analysis.csv', 'non_empty_projects.csv', 'remove_ids.csv')
remove_empty_projects('remove_ids.csv')
