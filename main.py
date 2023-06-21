import os, pkg_resources, json, subprocess as sp, zipfile

home_dir_path = os.path.expanduser ("~")
mainDir = os.path.abspath (os.path.dirname (__file__))

backup_dir_path = os.path.join (home_dir_path, ".backup")
cfg_bak_dir_path = os.path.join (backup_dir_path, "cfg")


def print_error (error: str):
    print (F"\033[1;31m[-] {error}\033[0m")


def print_success (succ: str):
    print (f"\033[1;32m[+] {succ}\033[0m")


def pkgs_backup ():
    pkgs_bak_file_path = os.path.join (backup_dir_path, "pkgs.json")
    installed_packages = {}

    for pkg in pkg_resources.working_set:
        pkg_name = str (pkg).split (" ")[0]
        pkg_version = str (pkg).split (" ")[1]
        installed_packages [pkg_name] = pkg_version

    if not os.path.exists (backup_dir_path):
        os.makedirs (backup_dir_path)

    with open (pkgs_bak_file_path, "w") as f:
        json.dump (installed_packages, f, indent = 4)


def cfg_backup ():
    info = {}
    ls_command = sp.Popen (['ls', '-al', home_dir_path], stdout = sp.PIPE)
    grep_command = sp.Popen (['grep', '.cfg'], stdin = ls_command.stdout, stdout = sp.PIPE)
    cfg_files = grep_command.communicate ()[0].decode ().strip ().split ("\n")
    cfg_info_file = os.path.join (cfg_bak_dir_path, "info.json")

    for i in range (len (cfg_files)):
        cfg_files [i] = cfg_files [i].split (" ")[-1]

    if not os.path.exists (cfg_bak_dir_path):
        os.makedirs (cfg_bak_dir_path)

    for file in cfg_files:
        cfg_file_path = os.path.join (home_dir_path, file)
        cmd = f"cp -r {cfg_file_path} {cfg_bak_dir_path}"

        info [cfg_file_path] = os.path.split (file)[1]
        os.system (cmd)

    with open (cfg_info_file, "w") as f:
        json.dump (info, f, indent = 4)


def zipper (dir_path: os.path, zip_file_path: os.path):
    with zipfile.ZipFile (zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk (dir_path):
            for file in files:
                file_path = os.path.join (root, file)
                zipf.write (file_path, os.path.relpath (file_path, dir_path))


def rm_bak_dir ():
    print (f"removing the backup dir [{backup_dir_path}].")
    os.system (f"rm -r {backup_dir_path}")
    print_success (f"Successfully removed the backup dir [{backup_dir_path}].")


def main (rm_bak: bool = True):
    try: pkgs_backup (); print_success ("Successfully creted the backup file for all the installed pkgs.")
    except Exception as e: print_error (e)

    try: cfg_backup (); print_success ("Successfully creted the backup dir for all the custom configs.")
    except Exception as e: print_error (e)

    try: zipper (backup_dir_path, f"{backup_dir_path}.zip"); print_success (f"Successfully compressed the backup dir as '{backup_dir_path}.zip'.")
    except Exception as e: print_error (e)

    if rm_bak:
        try: rm_bak_dir ()
        except Exception as e: print_error (e)


if __name__ == "__main__":
    main ()
