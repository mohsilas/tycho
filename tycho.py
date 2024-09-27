import os
import sys
import json
import shutil
import readline
from pathlib import Path
from datetime import datetime
pjoin = os.path.join



main_log_dir = pjoin('.tyc', 'log.json')
comment_text_padding = 50
log_data = {}
cwd = os.getcwd()
repo_name = os.path.basename(cwd)
arg = "help" if len(sys.argv) < 2 else sys.argv
ingore_alrt_flag = True

def repo_init():
    main_log = {
        "project_name": repo_name,
        "latest": 1,
        "ignore": [""],
    }

    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    init_version_log = {
        'push#': 1,
        "pdate": time_stamp,
        "comment": "First Commit / Init Commit",
    }

    init_version_dir = pjoin(cwd, ".tyc", "1")
    copy_tree(init_version_dir)
    json_dump(main_log_dir, main_log)
    json_dump(pjoin(init_version_dir, "vlog.json"), init_version_log)

    print("Repo \x1b[38;5;50m", repo_name ,"\x1b[0m Initalized Successfully")

def repo_update_push():
    comment = input("comment: ").strip()
    comment = comment if comment != "" else "No Comment"

    main_log = json_load(main_log_dir)
    main_log["latest"] += 1
    this_version = main_log["latest"]
    this_version_dir = pjoin(cwd, ".tyc", str(this_version))
    copy_tree(this_version_dir,ignore_patterns)
    json_dump(main_log_dir, main_log)

    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version_log = {
        'push#': this_version,
        "pdate": time_stamp,
        "comment": comment
    }
    json_dump(pjoin(this_version_dir, "vlog.json"), version_log)

    print("Update Pushed \x1b[38;5;50mSuccessfully\x1b[0m")

def commit_log_show():
    main_log = json_load(main_log_dir)
    print(f"\x1b[38;5;249m repository name:\x1b[0m {main_log['project_name']}\x1b[38;5;249m | Total commits:\x1b[0m {main_log['latest']}\x1b[38;5;249m | main file(s) :\x1b[0m {files_number()}\x1b[38;5;249m | backup-size:\x1b[0m {backup_size():.1f} KB")
    print("=" * win_size())
    print(f"  #  | {str('COMMENT'):<{comment_text_padding}} | TIME")
    print("=" * win_size())
    for v in range(1, main_log["latest"] + 1):
        vdata = json_load(pjoin(".tyc", str(v), "vlog.json"), False)
        i = ((v%2) * 3) + 249
        print(f"\x1b[38;5;{i}m", end="")
        if vdata == None:
           print(f"\x1b[38;5;125m {v:<3} | COMMIT IS MISSING!\x1b[0m")
        else:
            print(f" {vdata['push#']:<3} | {vdata['comment']:<{comment_text_padding}} | {vdata['pdate']}")
        print("\x1b[0m", end="")

def ignore_update():
    user_ignore_pattern = input("Add Ignore Pattern: ").strip().split(" ")
    main_log = json_load(main_log_dir)
    if user_ignore_pattern == "" or main_log == None:
        exit()
    main_log["ignore"] += user_ignore_pattern
    json_dump(main_log_dir, main_log)
    print("Ignore Pattern Updated \x1b[38;5;50mSuccessfully\x1b[0m")
    print("Updated Ignore Pattern: ", " | ".join(main_log["ignore"]))

def help_show():
    msg = """
    _____           _
   |_   _|   _  ___| |__   ___
     | || | | |/ __| '_ \ / _ \  \t
     | || |_| | (__| | | | (_) | \t
     |_| \__, |\___|_| |_|\___/ \t
         |___/ \t
    A tiny version backup script
    commands: init, push, log, help
    """
    print(msg)
    exit()

# ___________________ lvl2 functions _____________________________
def json_dump(path, data):
    try:
        with open(path, "w") as fo:
            json.dump(data, fo, indent=4)
    except Exception as e:
        print(e)
        exit()

def json_load(path, exit_when_error = True):
    try:
        with open(path, "r") as fo:
            return json.load(fo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if exit_when_error:
            print(f"Error: {str(e)}. Please Initialize First.")
            exit()
    except Exception as e:
        if exit_when_error:
            print(f'An error occurred: {e}')
            exit()

def copy_tree(target_dir, ig_patterns=None):
    try:
        shutil.copytree(cwd, target_dir, ignore=ig_patterns)
    except Exception as e:
        print(e)
        exit()

def win_size():
    try:
        s = os.get_terminal_size().columns
    except:
        s = 80
    return s

def ignore_patterns(path, names):
    global ingore_alrt_flag
    user_ignore = json_load(main_log_dir)
    try:
        ui = user_ignore["ignore"] + ['.tyc', '__pycache__'] if (user_ignore["ignore"] != [""]) or (user_ignore["ignore"] != None) else ['.tyc', '__pycache__']
    except:
        ui = ['.tyc', '__pycache__']

    if ingore_alrt_flag:
        print("Ignored Dirs/Files: ", " | ".join(ui))
        ingore_alrt_flag = False
    return [name for name in names if name in ui]


def files_number():
    # List all entries in the directory and filter them
    files = [
        f for f in os.listdir(cwd)
        if os.path.isfile(os.path.join(cwd, f)) and not f.startswith('.')
    ]
    return len(files)

def backup_size():
    root_directory = Path(pjoin(cwd, '.tyc'))
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) * 0.001
# ____________________________________________________________________
#                           MAIN
# ____________________________________________________________________
def main():
    args_list = {
        'init': repo_init,
        'push': repo_update_push,
        'log': commit_log_show,
        'ignore': ignore_update,
        'help': help_show
    }

    _ = args_list['help']() if not (arg[1] in args_list) else args_list[arg[1]]()

main()
