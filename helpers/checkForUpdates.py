import requests
import os
import sys
import yaml
import shutil
import time

if __name__ != "__main__":
    from helpers.colors import *
else:
    from colors import Colors


def checkUpdates():
    new_features, bug_fixes, info = [], [], ""
    disableColorsForWindows()
    if os.name == "nt":
        source_dir = sys.argv[0].split('\\')
    else:
        source_dir = sys.argv[0].split('/')
    if len(source_dir) != 1:
        source_dir = source_dir[:-1]
        if os.name == "nt":
            source_dir = '\\'.join(source_dir) + '\\'
        else:
            source_dir = '/'.join(source_dir) + '/'
    else:
        source_dir = "."
    latest_version = requests.get(
        "https://raw.githubusercontent.com/micha3lb3n/SourceWolf/master/helpers/sourcewolf-version.yaml")
    if str(latest_version) != "<Response [200]>":
        print(Colors.RED + "Error while fetching the version file! SourceWolf requires an internet connection to check for updates.")
        print("If you are connected to the internet and you are seeing this, please open an issue on github!" + Colors.RESET)
        sys.exit(1)

    try:
        with open("helpers/sourcewolf-version.yaml") as file:
            version_info = yaml.full_load(file)

            for attribute, value in version_info.items():
                if attribute == "version":
                    local_version = value
                    break
    except FileNotFoundError:
        print("The sourcewolf-version.yaml file must be located under the 'helpers' directory, which was not found!")
        sys.exit(1)

    temp_file = open(os.path.join(source_dir, "temp_file"), "w")
    temp_file.write(latest_version.text)
    temp_file.close()

    with open(os.path.join(source_dir, "temp_file")) as file:
        version_info = yaml.full_load(file)
        # attributes are version and features
        for attribute, value in version_info.items():
            if attribute == "version":
                latest_version = value
            elif attribute == "new-features":
                new_features += value
            elif attribute == "bug-fixes":
                bug_fixes += value
            elif attribute == "info":
                info = str(value)

    if os.path.exists(os.path.join(source_dir, "temp_file")):
        os.remove(os.path.join(source_dir, "temp_file"))

    return local_version, latest_version, new_features, bug_fixes, info


def printResults():
    local_version, latest_version, new_features, bug_fixes, info = checkUpdates()
    local_version, latest_version = str(local_version), str(latest_version)
    if local_version == latest_version:
        print(Colors.GREEN + "SourceWolf up to date! v" +
              local_version + Colors.RESET)
    else:
        print(Colors.CYAN + "Yaay!\n")
        print("An upgrade from version " + local_version +
              " to " + latest_version + " is available" + Colors.RESET)
        time.sleep(2)
        if info != "":
            print(Colors.YELLOW +
                  "\nInformation about the update: " + info[2:-2])
        print(Colors.GREEN)
        if new_features != []:
            print("The new features added are:")
            for feature in new_features:
                print(" - " + feature)
            print()
        if bug_fixes != []:
            print("The fixed bugs are:")
            for fix in bug_fixes:
                print(" - " + fix)
            print()
        print(Colors.YELLOW + "You can update SourceWolf by placing update.py (present in the root of SourceWolf) outside the SourceWolf directory, and use it as")
        print("python3 update.py /path/to/SourceWolf")
        print(Colors.RESET)


if __name__ == "__main__":
    update()
