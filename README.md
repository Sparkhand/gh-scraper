# GitHub file scraper by language

This Python command line tool follows a filter based on a programming language and its relative file extension to fetch and download files from a pool of GitHub repositories found by GitHub API (virtually every existing public and not-a-fork GitHub repository)

## Usage

```bash
python3 fetchgithubfiles.py language file-extension api-key [OPTIONS]...
```

### Positional arguments

- `language` is the programming language to search for
- `file-extension` is the file extension (without .) of the chosen programming language
- `api-key` is a GitHub Personal Access Token that you can [generate here](https://github.com/settings/tokens)

### Options

- `-mp maxpages`, `--MaxPages=maxpages` is the maximum number of pages you want to fetch (each page contains 100 fetched repositories). Set as 100 by default

- `-d dir`, `--Directory=dir` is the directory where fetched files will be saved. Set as `./fetchedfiles` by default

- `-t topic`, `--Topic=topic` is the topic for which repositories will be additionally filtered for. By default it has no value, meaning this filter won't be applied

- `-k keywords`, `--Keywords=keywords` are blank separated keywords for which repositories will be additionally filtered for. By default it has no value, meaning this filter won't be applied 

## Example

```bash
python3 fetchgithubfiles.py rust rs 123123123 -mp 20
```
