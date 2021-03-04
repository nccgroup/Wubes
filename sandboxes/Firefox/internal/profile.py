# Parse a 'profiles.ini' like that:
#
# ```
# [Install308046B0AF4A39CB]
# Default=Profiles/vcgcdfj3.default-release
# Locked=1
#
# [Profile1]
# Name=default
# IsRelative=1
# Path=Profiles/7t6yw3fu.default
# Default=1
#
# [Profile0]
# Name=default-release
# IsRelative=1
# Path=Profiles/vcgcdfj3.default-release
#
# [General]
# StartWithLastProfile=1
# Version=2
# ```
#
# If we install, do the following:
# - Copy everything from our shared folder into the sandbox profile
#
# If we backup, do the following:
# - Copy everything from our sandbox profile into our shared folder, keeping a copy of our previous profile in the shared folder

import configparser
import os
import psutil
import sys
import subprocess
import time
import shutil
import argparse

SHARED_PROFILE = 'abcdefgh.default-release'
FIREFOX_PATH = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
APPDATA_FIREFOX = 'C:\\Users\\WDAGUtilityAccount\\AppData\\Roaming\\Mozilla\\Firefox'
PROFILES_INI = os.path.join(APPDATA_FIREFOX, 'profiles.ini')
SHARED_FIREFOX_PATH = 'C:\\Users\\WDAGUtilityAccount\\Desktop\\Firefox'
SHARED_PROFILE_PATH = os.path.join(SHARED_FIREFOX_PATH, SHARED_PROFILE)
SHARED_BACKUPS_PATH = os.path.join(SHARED_FIREFOX_PATH, 'backups')

def show_last_exception():
    """Taken from gef. Let's us see proper backtraces from python exceptions
    """
    PYTHON_MAJOR = sys.version_info[0]
    horizontal_line = "-"
    right_arrow = "->"
    down_arrow = "\\->"

    print("")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(" Exception raised ".center(80, horizontal_line))
    print("{}: {}".format(exc_type.__name__, exc_value))
    print(" Detailed stacktrace ".center(80, horizontal_line))
    for fs in traceback.extract_tb(exc_traceback)[::-1]:
        if PYTHON_MAJOR==2:
            filename, lineno, method, code = fs
        else:
            try:
                filename, lineno, method, code = fs.filename, fs.lineno, fs.name, fs.line
            except:
                filename, lineno, method, code = fs

        print("""{} File "{}", line {:d}, in {}()""".format(down_arrow, filename,
                                                            lineno, method))
        print("   {}    {}".format(right_arrow, code))

def close_firefox_all():
    """TerminateProcess() all Firefox instances by looking at a snapshot of processes
    """
    for process in psutil.process_iter():
        pname = process.name()
        if not pname or pname not in FIREFOX_PATH:
            continue
        print("Killing Firefox process: %d" % process.pid)
        try:
            process.terminate()
        except:
            print("Killing Firefox process failed with error:")
            show_last_exception()
        time.sleep(2)


# XXX - is it possible to modify profiles.ini to points to the shared folder?
#for k,v in config["Profile0"].items():
#    print("%s -> %s" % (k,v))
#first_section_name = config.sections()[0]
# config[first_section_name]["Default"] = PROFILE_PATH
# config["Profile0"]["IsRelative"] = "0"
# config["Profile0"]["Path"] = PROFILE_PATH
# with open(PROFILES_INI, "w") as configfile:
    # config.write(configfile)

def get_default_profile():
    """Parse '%APPDATA\Mozilla\Firefox\profiles.ini' in order to get the default profile
       that was auto generated. This will be used to get the path we need to replace with
       our previously saved profile.
    """
    config = configparser.ConfigParser()
    config.read(PROFILES_INI)
    profile_path = os.path.join(APPDATA_FIREFOX, config["Profile0"]["Path"].replace("/", "\\"))
    print("Profile path: %s" % profile_path)
    return profile_path

def main():
    """Entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', dest='save', action="store_true", help="Save from sandbox to shared folder (default is to install from shared folder to sandbox)")
    args = parser.parse_args()

    if args.save:
        close_firefox_all()
        try:
            os.mkdir(SHARED_BACKUPS_PATH)
        except FileExistsError:
            pass
        timestr = time.strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(SHARED_BACKUPS_PATH, '%s-%s' % (SHARED_PROFILE, timestr))

        if os.path.isdir(SHARED_PROFILE_PATH):
            print("Backuping old shared profile folder...")
            shutil.move(SHARED_PROFILE_PATH, backup_path)

        profile_path = get_default_profile()
        print("Saving latest profile to shared profile folder...")
        shutil.copytree(profile_path, SHARED_PROFILE_PATH)
    else:
        if os.path.isdir(SHARED_PROFILE_PATH):
            cmd = FIREFOX_PATH
            print("Executing: %s" % cmd)
            proc = subprocess.Popen(cmd, shell=True)
            time.sleep(3)
            print("Firefox PID: %d" % proc.pid)
            close_firefox_all()
            proc.wait()

            profile_path = get_default_profile()
            print("Deleting old profile folder...")
            shutil.rmtree(profile_path)

            print("Copying new profile folder...")
            shutil.copytree(SHARED_PROFILE_PATH, profile_path)
        else:
            print("No shared profile found, will init an empty profile next time Firefox runs")

    print("Done")

if __name__ == "__main__":
    main()