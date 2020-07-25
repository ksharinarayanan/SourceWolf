import os
import sys
import threading
import errno
import glob
import argparse
import time
import shutil

# from search import endpointSearch
if __name__ == "__main__":
    from search import endpointSearch
    from colors import *
else:
    from helpers.search import endpointSearch
    from helpers.colors import *


class crawlThreads(threading.Thread):
    def __init__(self, file, output_file):
        threading.Thread.__init__(self)
        self.file = file
        self.output_file = output_file

    def run(self):
        threadLimiter.acquire()

        try:
            endpointSearch(self.file, self.output_file)
        finally:
            threadLimiter.release()


def crawlOutput(output_dir, crawl_output):

    if os.path.isdir(output_dir) == False:
        print(Colors.RED + "'" + output_dir + "' directory does not exist!")
        sys.exit(1)

    if crawl_output != None:
        if os.path.isdir(crawl_output):
            remove = input(Colors.YELLOW + "\n[!] '" + crawl_output +
                           "' directory already exists. Do you want to remove it?[y/n] " + Colors.RESET)
            if remove.lower() != 'y':
                sys.exit(0)
            shutil.rmtree(crawl_output)
        os.mkdir(crawl_output)

    temp_directory = []

    files = glob.glob(output_dir + '/**/*.txt', recursive=True)

    if files == []:
        print(Colors.RED + "No *.txt files found in the specified directory! \nAll your response text files must be txt files with SourceWolf compatible file names." + Colors.RESET)
        sys.exit(0)

    print(Colors.GREEN + "\n[+] Found " +
          str(len(files)) + " response files\n")
    time.sleep(1)

    if crawl_output == None:
        crawl = input(
            Colors.YELLOW + "[!] Do you want to crawl through the response files obtained to find endpoints? [y/n]: ")
    else:
        crawl = 'y'
    if crawl.lower() == 'y':
        endpoint_file = None
        if crawl_output != None:
            endpoint_file = os.path.join(crawl_output, "endpoints")
        time.sleep(1.5)
        print(
            "\n[+] Starting to crawl through the response files to find hidden endpoints\n" + Colors.RESET)
        time.sleep(2)

        file_threads = []

        for file in files:
            file_threads.append(crawlThreads(file, endpoint_file))

        for file_thread in file_threads:
            file_thread.start()

        for file_thread in file_threads:
            file_thread.join()


threads = 100
threadLimiter = threading.BoundedSemaphore(threads)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory",
                        help="Directory where the response files are present")
    parser.add_argument("-o", "--output",
                        help="Directory to store the output")

    disableColorsForWindows()

    args = parser.parse_args()

    if args.directory == None:
        print("Error: Required argument -d/--directory")
        parser.print_help()
        sys.exit(2)

    crawlOutput(args.directory, args.output)
