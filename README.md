# Tiny Tasks

A small Python command-line task tracker by [judeh7777](https://github.com/judeh7777).
Built as a demo project for learning Python, Git, and GitHub.

## Features

- Add tasks, list them, and mark them complete.
- Filter the list to show only pending tasks.
- Save tasks locally in a JSON file between runs.
- Use Python's standard library with no packages to install.

## Quick start

Requires Python 3.10 or newer. After uploading this project to your GitHub account:

```sh
git clone https://github.com/judeh7777/tiny-tasks.git
cd tiny-tasks
python tiny_tasks.py add "Create my first GitHub project"
python tiny_tasks.py add "Write a useful README"
python tiny_tasks.py list
python tiny_tasks.py done 1
python tiny_tasks.py list --pending
```

On Windows, `py` can be used in place of `python`.

Example list output before marking a task complete:

```text
[ ] #1 Create my first GitHub project
[ ] #2 Write a useful README
```

Tasks are stored in `~/.tiny-tasks/tasks.json`, outside this repository.
To choose another file, put `--file` before the command:

```sh
python tiny_tasks.py --file ./my-tasks.json add "Try a separate list"
python tiny_tasks.py --file ./my-tasks.json list
```

Run one command at a time against a given data file. This demo does not support
concurrent writers or syncing between devices.

## Tests

```sh
python -m unittest discover -v
```

Tests use temporary data files. GitHub Actions runs them on Linux and Windows
with Python 3.10 and 3.13.

## Publish on GitHub

Create an **empty** repository named `tiny-tasks` under `judeh7777`.
Do not initialize it with a README, license, or .gitignore; those are included here.
From this project's folder, run:

```sh
git add .
git commit -m "Initial commit: Tiny Tasks demo"
git branch -M main
git remote add origin https://github.com/judeh7777/tiny-tasks.git
git push -u origin main
```

Git must have your name and email configured, and GitHub will require authentication
when pushing. The local repository is already initialized.

## Project files

```text
tiny_tasks.py               CLI and JSON storage
test_tiny_tasks.py          Automated tests
.github/workflows/tests.yml GitHub Actions test workflow
LICENSE                    MIT license
```

## License

MIT. See [LICENSE](LICENSE).
