import pandas as pd
import csv


# change the format of the file to csv
def txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as in_file:
        with open('help.txt', 'w') as text_file:
            for line in in_file:
                if ' ' in line:
                    line = line.replace(' ', '\n')
                text_file.write(line)

    df = pd.read_fwf('help.txt')
    df.to_csv(csv_file)


# remove projects developed by the Serverless framework community
# remove projects that their config file is in a template, example, demo, or test directory
def filter_urls(file_urls, filtered_file_urls):
    wtr = csv.writer(open(filtered_file_urls, 'w'), lineterminator='\n')
    wtr.writerow(['File_URL'])

    remove = ['/templates/', '/template/', '/examples/', '/example/', '/demos/', '/demo/',
              '/test/', '/tests/', '/github.com/serverless/', '/github.com/serverless-components/']

    with open(file_urls, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if any(c in row[1].lower() for c in remove):
                continue
            elif not row[1].rstrip().endswith('serverless.yml'):
                continue
            else:
                wtr.writerow([row[1]])

# ----------------------------- MAIN --------------------------------------


txt_to_csv('result-2020-07-29.txt', 'file_url.csv')
filter_urls('file_url.csv', 'file_urls.csv')
