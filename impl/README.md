# Wonderless implementation

To replicate Wonderless, do the following steps in order:
1. use `<get_urls.sh>` to query GitHub API for 
  all the serverless.yml configuration files 
  that are larger than 0.5 KB. Please do not forget to add 
  your GitHub token to the script. The result
  will be saved in a file with *txt* extension.
  
2. use `<filter_file_urls.py>` to export the results 
  to a file with *csv* format, remove the files 
  developed by the Serverless Framework community, 
  as well as the files placed in a *template*, 
  *example*, *demo*, or *test* directory.
  
3. use `<clone_projects.py>` to extract the URL of 
  the repositories corresponding to each serverless.yml
  configuration file, remove duplications, and clone the 
  master branch of each repository.

4. use `<filter_empty_projects.py>` to walk through 
   the configuration file of each repository and extract 
   the provider's name and number of functions, get the 
   id of empty(no function, no provider) or projects with 
   not executable configuration file, and remove the 
   repositories related to the mentioned ids.
   
5. use `<remove_immature_projects.py>` to get the commit 
   history of each repository, calculate the lifetime of 
   projects, get the id of projects that have been active 
   for less than a year, and remove those projects.


6. use `<remove_toy_projects.py>` to get the meta-data of
   each repository from GitHub API, find the id of projects
   that contain specific keywords in their labels, topics,
   or descriptions, and remove those projects. Please do not 
   forget to add your GitHub token to the request.
  
7. use `<remove_forked_projects.py>` to get the id of all 
   projects and find the projects with the same label and 
   different developers. You then need to manually go 
   through those projects to check whether they are forked, 
   or the accidentally have the same label.
   

  