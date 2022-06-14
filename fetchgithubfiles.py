from ast import keyword
from httplib2 import Authentication
import requests
import sys
import base64
import json
import os
import argparse

# GLOBAL VARIABLES

language = ""
fileExtension = ""
apiToken = ""
maxRepos = 100
directory = "./fetchedfiles"
topic = None
keywords = None

#####################################################################

# COMMAND LINE ARGUMENTS AND OPTIONS PARSING

parser = argparse.ArgumentParser()

# Positional arguments
parser.add_argument(
    "Language", help="Set the programming language you want to search for")
parser.add_argument(
    "FileExtension", help="Set the extension (without .) you want to search for")
parser.add_argument("ApiToken", help="Set your GitHub API token")

# Options
parser.add_argument("-mr", "--MaxRepos",
                    help="Set max number of repos pages to be fetched")
parser.add_argument("-d", "--Directory",
                    help="Set the directory where downloaded files will be stored")
parser.add_argument("-t", "--Topic", help="Filter repositories by topic")
parser.add_argument("-k", "--Keywords", nargs='+',
                    help="Filter repositories by keywords")

args = parser.parse_args()

if args.ApiToken != None:
    apiToken = args.ApiToken

if args.MaxRepos != None:
    maxRepos = abs(int(args.MaxRepos))

if args.Language != None:
    language = (args.Language).lower()

if args.FileExtension != None:
    fileExtension = (args.FileExtension).lower()

if args.Directory != None:
    directory = args.Directory

if args.Topic != None:
    topic = (args.Topic).lower()

if args.Keywords != None:
    keywords = args.Keywords
    keywords = '+'.join(keywords)

#####################################################################

# FUNCTIONS

def checkAPIRateExceeded(JSONresponse):
    if "message" in JSONresponse:
        return "API rate limit exceeded" in JSONresponse["message"]
    return False


def printJSONLog(log):
    with open("log.json", "w") as o:
        o.write(json.dumps(log))
        o.close()


def fetchRepos(page, reposPerPage, headers):
    queryString = "https://api.github.com/search/repositories?q="

    if keywords != None:
        queryString = queryString + keywords

    if topic != None:
        queryString = queryString + "+topic:" + str(topic)

    queryString = queryString + "+language:" + str(language)

    queryString = queryString + "&order=desc&page=" + \
        str(page) + "&per_page=" + str(reposPerPage)

    response = requests.get(queryString, headers=headers)
    JSONresponse = response.json()

    if not ("items" in JSONresponse):
        if checkAPIRateExceeded(JSONresponse):
            print("API Rate Exceeded")
            sys.exit()
        printJSONLog(JSONresponse)
        return None

    print("Fetched " + str(len(JSONresponse["items"])) + " " + str(
        language) + " language repos (page " + str(page) + ")")
    return JSONresponse["items"]


def fetchRepoFiles(repoFullName, headers):
    request = requests.get("https://api.github.com/search/code?q=extension:" +
                           str(fileExtension) + "+repo:" + str(repoFullName) + "&per_page=100", headers=headers)
    JSONresponse = request.json()

    if not ("items" in JSONresponse):
        if checkAPIRateExceeded(JSONresponse):
            print("API Rate Exceeded")
            sys.exit()
        printJSONLog(JSONresponse)
        return None

    print("\tFetched " + str(len(JSONresponse["items"])
                             ) + " files for " + str(repoFullName) + " repo")
    return JSONresponse["items"]


def fetchSingleFile(repoFullName, fileName, filePath, headers):
    request = requests.get("https://api.github.com/repos/" +
                           str(repoFullName) + "/contents/" + str(filePath), headers=headers)
    JSONresponse = request.json()

    if not ("content" in JSONresponse):
        if checkAPIRateExceeded(JSONresponse):
            print("API Rate Exceeded")
            sys.exit()
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

# MAIN


headers = {
    'Accept': 'application/vnd.github.preview.text-match+json',
    'Authorization': "token " + str(apiToken)
}

# Create directory where files will be downloaded
os.makedirs(directory, exist_ok=True)

page = 1
countFetchedRepos = 0
reposPerPage = maxRepos % 100

while countFetchedRepos <= maxRepos:

    fetchedRepos = fetchRepos(page, reposPerPage, headers)

    if fetchedRepos == None:
        break

    for repo in fetchedRepos:   # For each repo, fetch files in that repo

        if repo["fork"] == True:
            continue

        repoName = repo["name"]
        repoFullName = repo["full_name"]

        fetchedFilesList = fetchRepoFiles(repoFullName, headers)

        if fetchedFilesList == None:
            break

        for file in fetchedFilesList:   # Download each file in fetchedFiles

            fileName = file["name"]
            filePath = file["path"]

            fetchedFile = fetchSingleFile(
                repoFullName, fileName, filePath, headers)

            if fetchedFile == None:
                break

            fileContent = decodeFileContent(fetchedFile)

            downloadSingleFile(repoName, fileName, fileContent)

    page = page + 1    # Next page

print("############## END OF FETCHED FILES ##############")

#####################################################################
