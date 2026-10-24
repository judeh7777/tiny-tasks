"""A dependency-free task tracker for the terminal."""

import argparse
import json
from pathlib import Path


def load_tasks(path):
    """Load tasks, treating a missing file as a new list."""
    if not path.exists():
        return []
    tasks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(tasks, list) or any(
        not isinstance(task, dict)
        or type(task.get("id")) is not int
        or task["id"] < 1
        or not isinstance(task.get("title"), str)
        or not task["title"].strip()
        or type(task.get("done")) is not bool
        for task in tasks
    ):
        raise ValueError("Task file has an invalid format.")
    if len({task["id"] for task in tasks}) != len(tasks):
        raise ValueError("Task file contains duplicate IDs.")
    return tasks


def save_tasks(path, tasks):
    """Replace the data file only after the new content has been written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file", type=Path, default=Path.home() / ".tiny-tasks" / "tasks.json",
        help="data file (default: ~/.tiny-tasks/tasks.json)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a task")
    add.add_argument("title", help="task title, in quotes")
    listing = commands.add_parser("list", help="show tasks")
    listing.add_argument("--pending", action="store_true", help="hide completed tasks")
    done = commands.add_parser("done", help="mark a task complete")
    done.add_argument("id", type=int, help="task ID")
    args = parser.parse_args(argv)

    try:
        tasks = load_tasks(args.file)
        if args.command == "add":
            title = args.title.strip()
            if not title:
                raise ValueError("Task title cannot be empty.")
            task_id = max((task["id"] for task in tasks), default=0) + 1
            tasks.append({"id": task_id, "title": title, "done": False})
            save_tasks(args.file, tasks)
            print(f"Added #{task_id}: {title}")
        elif args.command == "list":
            visible = [task for task in tasks if not args.pending or not task["done"]]
            if not visible:
                print("No pending tasks." if args.pending else "No tasks yet.")
            for task in visible:
                mark = "x" if task["done"] else " "
                print(f"[{mark}] #{task['id']} {task['title']}")
        elif args.command == "done":
            task = next((task for task in tasks if task["id"] == args.id), None)
            if task is None:
                raise ValueError(f"Task #{args.id} was not found.")
            task["done"] = True
            save_tasks(args.file, tasks)
            print(f"Completed #{args.id}: {task['title']}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
