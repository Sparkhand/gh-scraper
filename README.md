# GitHub file scraper by language

This Python command line tool follows a filter based on a programming language and its relative file extension to fetch and download files from a pool of GitHub repositories found by GitHub API (virtually every existing public and not-a-fork GitHub repository)

## Usage

```bash
python3 fetchgithubfiles.py language file-extension api-key [OPTIONS]...
```

## IMPORTANT NOTE

In order for the script to work you'll have to provide a GitHub Personal Access Token of yours that you can [generate here](https://github.com/settings/tokens). Once you have your Access Token at hand, you can set an environment variable named exactly `GHScraperAPIToken` OR you can use the specific command line option given below. Note that setting the Access Token via command line option discards the value of `GHScraperAPIToken` environment variable

### Positional arguments

- `language` is the programming language to search for
- `file-extension` is the file extension (without `.`) of the chosen programming language

### Options

- `-apitoken apitoken`, `--ApiToken=apitoken` is a GitHub Personal Access Token of yours. [Don't have it? Generate it here](https://github.com/settings/tokens)

- `-mr maxrepos`, `--MaxRepos=maxrepos` is the maximum number of repos you want to fetch. Set as 100 by default

- `-d dir`, `--Directory=dir` is the directory where fetched files will be saved. Set as `./fetchedfiles` by default

- `-t topic`, `--Topic=topic` is the single topic for which repositories will be additionally filtered for. By default it has no value, meaning this filter won't be applied

- `-k keywords`, `--Keywords=keywords` are one or more blank separated keywords for which repositories will be additionally filtered for. By default it has no value, meaning this filter won't be applied 

## Example

```bash
python3 fetchgithubfiles.py rust rs -apitoken 123123123 -mp 20
```
