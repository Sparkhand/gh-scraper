# GitHub file fetcher by language

This simple Python script serves as a tool to download files of a specific programming language from every existing GitHub repository (public and not-a-fork repos)

## Usage

```bash
python3 language api-key [OPTIONS]...
```

### Positional arguments

- `language` is the programming language to search for
- `api-key` is a GitHub Personal Access Token that you can [generate here](https://github.com/settings/tokens)

### Options

- `-mp maxpages`, `--MaxPages=maxpages` is the maximum number of pages you want to fetch (each page contains 100 fetched repositories). Set as 100 by default

- `-d dir`, `--Directory=dir` is the directory where fetched files will be saved. Set as `./fetchedfiles` by default