import os
import sys
import threading
import errno
import glob
import argparse
import time
import shutil

if __name__ == "__main__":
    from getEndpoints import endpointSearch
    from colors import *
    from getVariables import variableSearch
    from extractSocialmedia import extract
else:
    from helpers.getEndpoints import endpointSearch
    from helpers.colors import *
    from helpers.getVariables import variableSearch
    from helpers.extractSocialmedia import extract


class crawlThreads(threading.Thread):
    def __init__(self, file, output_file, verbose):
        threading.Thread.__init__(self)
        self.file = file
        self.output_file = output_file
        self.verbose = verbose

    def run(self):
        threadLimiter.acquire()

        try:
            endpointSearch(self.file, self.output_file, self.verbose)
        finally:
            threadLimiter.release()


class getVarNamesThreads(threading.Thread):
    def __init__(self, file, output_file, verbose):
        threading.Thread.__init__(self)
        self.file = file
        self.output_file = output_file
        self.verbose = verbose

    def run(self):
        threadLimiter.acquire()

        try:
            variableSearch(self.file, self.output_file, self.verbose)
        finally:
            threadLimiter.release()


class getSocialMediaThreads(threading.Thread):
    def __init__(self, file, output_file, verbose):
        threading.Thread.__init__(self)
        self.file = file
        self.output_file = output_file
        self.verbose = verbose

    def run(self):
        threadLimiter.acquire()

        try:
            extract(self.file, self.output_file, self.verbose)
        finally:
            threadLimiter.release()


def crawlOutput(output_dir, crawl_output, verbose):

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

    files = []

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
        print(Colors.YELLOW +
              "\n[+] Starting to crawl through the response files to find hidden endpoints\n" + Colors.RESET)
        time.sleep(2)

        file_threads = []

        for file in files:
            file_threads.append(crawlThreads(file, endpoint_file, verbose))

        for file_thread in file_threads:
            file_thread.start()

        for file_thread in file_threads:
            file_thread.join()

    if crawl_output == None:
        crawl = input(
            Colors.YELLOW + "[!] Do you want to crawl through the response files obtained to find javascript variables? [y/n]: ")
    else:
        crawl = 'y'

    if crawl.lower() == 'y':
        file_threads = []

        var_file = None
        if crawl_output != None:
            var_file = os.path.join(crawl_output, "jsvars")

        time.sleep(1.5)
        print(Colors.YELLOW +
              "\n[+] Starting to crawl through the response files to find javascript variables\n" + Colors.RESET)
        time.sleep(2)

        for file in files:
            file_threads.append(getVarNamesThreads(file, var_file, verbose))

        for file_thread in file_threads:
            file_thread.start()

        for file_thread in file_threads:
            file_thread.join()

    if crawl_output == None:
        crawl = input(
            Colors.YELLOW + "[!] Do you want to crawl through the response files obtained to extract social media links? [y/n]: ")

    if crawl.lower() == 'y':
        file_threads = []

        social_media_file = None
        if crawl_output != None:
            social_media_file = os.path.join(
                crawl_output, "social-media")

        time.sleep(1.5)
        print(Colors.YELLOW +
              "\n[+] Starting to crawl through the response files to extract social media\n" + Colors.RESET)
        time.sleep(2)

        for file in files:
            file_threads.append(getSocialMediaThreads(
                file, social_media_file, verbose))

        for file_thread in file_threads:
            file_thread.start()

        for file_thread in file_threads:
            file_thread.join()


threads = 150
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
