from httplib2 import Authentication
import requests
import sys
import base64
import json
import os
import argparse

########## GLOBAL VARIABLES

language = ""
apiToken = ""
maxPages = 100
directory = "./fetchedfiles"

#####################################################################

########## COMMAND LINE ARGUMENTS AND OPTIONS PARSING

parser = argparse.ArgumentParser()

parser.add_argument("Language", help = "Set the programming language you want to search for")
parser.add_argument("ApiToken", help = "Set your GitHub API token")
parser.add_argument("-mp", "--MaxPages", help = "Set max number of repos pages to be fetched (100 results (repos) per page)")
parser.add_argument("-d", "--Directory", help = "Set the directory where downloaded files will be stored")

args = parser.parse_args()

if args.ApiToken != None:
    apiToken = args.ApiToken

if args.MaxPages != None:
    maxPages = int(args.MaxPages)

if args.Language != None:
    language = (args.Language).lower()

if args.Directory != None:
    directory = args.Directory

#####################################################################

########## FUNCTIONS

def printJSONLog(log):
    with open("log.json", "w") as o:
        o.write(json.dumps(log))
        o.close()

def fetchRepos(page, headers):
    response = requests.get("https://api.github.com/search/repositories?q=language:" + str(language) + "&order=desc&page=" + str(page) + "&per_page=100", headers=headers)
    JSONresponse = response.json()

    if not ("items" in JSONresponse):
        print("ERROR: NO REPOS FETCHED, CHECK JSON LOG")
        printJSONLog(JSONresponse)
        return None
    
    print("Fetched " + str(len(JSONresponse["items"])) + " " + str(language) + " language repos (page " + str(page) + ")")
    return JSONresponse["items"]

def fetchRepoFiles(repoFullName, headers):
    request = requests.get("https://api.github.com/search/code?q=extension:rs+repo:" + str(repoFullName), headers=headers)
    JSONresponse = request.json()

    if not ("items" in JSONresponse):
        print("ERROR: NO FILES FETCHED, CHECK JSON LOG")
        printJSONLog(JSONresponse)
        return None

    print("\tFetched " + str(len(JSONresponse["items"])) + " files for " + str(repoFullName) + " repo")
    return JSONresponse["items"]

def fetchSingleFile(repoFullName, fileName, filePath, headers):
    request = requests.get("https://api.github.com/repos/" + str(repoFullName) + "/contents/" + str(filePath), headers=headers)
    JSONresponse = request.json()

    if not ("content" in JSONresponse):
        print("ERROR: NO FILE CONTENT FETCHED, CHECK JSON LOG")
        printJSONLog(JSONresponse)
        return None

    print("\t\tFetched file " + str(fileName) + " ... ", end="")
    return JSONresponse["content"]

def decodeFileContent(fileContent):
    return base64.b64decode(fileContent).decode()

def downloadSingleFile(repoName, fileName, fileContent):
    print("Downloading ... ", end="")
    with open(str(directory) + "/" + str(repoName) + "_" + str(fileName), "w") as o:
        o.write(fileContent)
        o.close()
    print("Done!")
    return

#####################################################################

########## MAIN

headers = {
    'Accept': 'application/vnd.github.preview.text-match+json',
    'Authorization': "token " + str(apiToken)
}

os.makedirs(directory, exist_ok=True)   # Create directory where files will be downloaded

page = 1
while True and page <= maxPages:

    fetchedRepos = fetchRepos(page, headers)

    if fetchedRepos == None:
        sys.exit()

    for repo in fetchedRepos:   # For each repo, fetch files in that repo

        if repo["fork"] == True:
            continue
        
        repoName = repo["name"]
        repoFullName = repo["full_name"]

        fetchedFilesList = fetchRepoFiles(repoFullName, headers)

        if fetchedFilesList == None:
            sys.exit()

        for file in fetchedFilesList:   # Download each file in fetchedFiles

            fileName = file["name"]
            filePath = file["path"]

            fetchedFile = fetchSingleFile(repoFullName, fileName, filePath, headers)

            if fetchedFile == None:
                sys.exit()

            fileContent = decodeFileContent(fetchedFile)

            downloadSingleFile(repoName, fileName, fileContent)
            
    page = page + 1    # Next page

print("############## END OF FETCHED FILES ##############")

#####################################################################
