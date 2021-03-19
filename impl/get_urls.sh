#!/usr/bin/env bash
#

url="https://api.github.com"

# set token to your GitHub access token (public access)
token="4140e8459f083a8c580031c53241713b36b81668"

today=$(date +"%Y-%m-%d")

keyword="serverless"

interval=20

dependency_test()
{
  for dep in curl jq ; do
    command -v $dep &>/dev/null || { echo -e "\n${_error}Error:${_reset} I require the ${_command}$dep${_reset} command but it's not installed.\n"; exit 1; }
  done
}

token_test()
{
  if [ -n "$token" ]; then
    token_cmd="Authorization: token $token"
  else
    echo "You must set a Personal Access Token to the GITHUB_TOKEN environment variable"
    exit 1
  fi
}


# Progress indicator
working() {
   echo -n "."
}

work_done() {
  echo -n "done!"
  echo -e "\n"
}

output_list()
{
    printf '%s\n' "${all_repos[@]}" | sort --ignore-case >> result-$today.txt
}

get_repos()
{
  for (( i=500; i<=10000; i+=$interval ))
  do
    j=$((i+interval-1))
    last_repo_page=$( curl -s --head -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100" | sed -nE 's/^Link:.*per_page=100.page=([0-9]+)>; rel="last".*/\1/p' )

    if [[ "$last_repo_page" == "" ]]; then
      echo "Fetching repository list for $keyword filename"
      all_repos=($( curl -s -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100" | jq --raw-output '.items[].html_url' | tr '\n' ' ' ))
      output_list
      total_repos=$( echo "${all_repos[@]}" | wc -w | tr -d "[:space:]" )
      echo
      echo "Total # of repositories for size:$i..$j: $total_repos"
      echo "List saved to result-$today.txt"
    else
      echo "Fetching repository list for $keyword filename"
      all_repos=()
      for (( k=1; k<=$last_repo_page; k++ ))
      do
        working
        paginated_repos=$( curl -s -H "$token_cmd" "$url/search/code?q=filename:$keyword+size:$i..$j+extension:yml&per_page=100&page=$k" | jq --raw-output '.items[].html_url' | tr '\n' ' ' )
        all_repos=(${all_repos[@]} $paginated_repos)
      done
      work_done
      output_list
      total_repos=$( echo "${all_repos[@]}" | wc -w | tr -d "[:space:]" )
      echo "Total # of repositories for size:$i..$j: $total_repos"
      echo "List saved to result-$today.txt"
    fi
  done
}

#### MAIN

dependency_test

token_test

get_repos


exit 0
