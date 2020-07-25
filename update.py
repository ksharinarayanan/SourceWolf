import os
import sys
import shutil

print("WARNING: UPDATING ERASES ALL THE DATA INSIDE THE DIRECTORY! (It removes the entire directory, and clones the repo again)")

update = input("Do you want to update? [y/n]: ")

if update.lower() == 'y':
    try:
        shutil.rmtree(str(sys.argv[1]))
    except IndexError:
        print("\nError: Move this update.py file outside the SourceWolf directory, and run it as")
        print("python3 update.py /path/to/SourceWolf/\n")
        sys.exit(2)
    os.system("git clone https://github.com/micha3lb3n/SourceWolf --quiet")
    print("\n\nSuccessfully clone into SourceWolf.")
    print("You are on the latest version now!\n")
