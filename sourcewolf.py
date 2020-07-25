import threading
import time
import argparse
import sys
import requests
import os
import shutil

from helpers.crawlResponses import crawlOutput
from helpers.checkForUpdates import printResults, checkUpdates

# Establishing a keep-alive TCP connection for ultra fast connection
session = requests.Session()

file_names = {'2': '2XX', '3': '3XX', '4': '4XX', '5': '5XX'}


class colors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = "\033[1;36m"


color_dictionary = {"2": colors.GREEN,
                    "3": colors.YELLOW, "4": colors.RED, "5": colors.CYAN}


def removeColors():
    colors.MAGENTA = colors.BLUE = colors.GREEN = colors.YELLOW = colors.RED = colors.RESET = colors.BOLD = colors.UNDERLINE = colors.CYAN = ''


class getResponseThread(threading.Thread):
    def __init__(self, url, delay):
        threading.Thread.__init__(self)
        self.url = url
        self.delay = delay

    def run(self):
        # limits the number of threads to whatever is mentioned below (other threads wait)
        threadLimiter.acquire()

        try:
            # my code to be executed here
            getResponse(self.url, self.delay)
        finally:
            # releases the thread so that the waiting thread can start
            threadLimiter.release()


def removeProtocol(url):
    if url[:5] == "https":
        return url[8:]
    return url[7:]


def getResponse(url, delay):

    if os.name == "nt" or args.no_colors == True:
        removeColors()

    if url[-1] == '\n' or url[-1] == ' ':
        url = url[:-1]
    try:
        if args.timeout != None:
            response = session.get(url, headers=args.headers,
                                   cookies=args.cookies, timeout=(float(args.timeout), 30))
        else:
            response = session.get(url, headers=args.headers,
                                   cookies=args.cookies)
        if os.name == "nt" or args.no_colors == True:
            pass
        else:
            print(color_dictionary[str(response)[11]], end="")
        if (brute_urls == None or str(response) != "<Response [404]>" or args.verbose == True):
            if args.only_success == True:
                if str(response)[11] == "2":
                    print(url + " --> ", end="")
                    print(str(response)[11:14])
                    print(colors.RESET, end="")
            else:
                print(url + " --> ", end="")
                print(str(response)[11:14])
                print(colors.RESET, end="")
        print(colors.RESET, end="")
        if status_code_file != None and (brute_urls == None or str(response) != "<Response [404]>" or args.verbose == True):
            status_code_file.write(url + " --> " + str(response)[11:14] + "\n")
        if output_dir != None:
            file_name = removeProtocol(url) + ".txt"
            # replacing the '/' in the paths with '@', so that they can be file names
            file_name = file_name.replace('/', '@')
            status_directory = file_names[str(response)[11]]
            location = os.path.join(output_dir, status_directory)
            location = os.path.join(location, file_name)
            file = open(location, "w")
            file.write(response.text)
            file.close()
    except Exception as e:
        if args.verbose == True:
            print(colors.MAGENTA, end="")
            print(url + " --> ", end="")
            print("Error!" + colors.RESET)
            if status_code_file != None:
                status_code_file.write(url + " --> Error" + "\n")
        else:
            pass
    finally:
        time.sleep(delay)


def createOutputFolders():
    two_xx_path, three_xx_path, four_xx_path, five_xx_path = "2XX", "3XX", "4XX", "5XX"
    os.mkdir(output_dir)
    os.mkdir(os.path.join(output_dir, two_xx_path))
    os.mkdir(os.path.join(output_dir, three_xx_path))
    os.mkdir(os.path.join(output_dir, four_xx_path))
    os.mkdir(os.path.join(output_dir, five_xx_path))


def removeEmptyDirectories(output_dir):
    try:
        os.rmdir(os.path.join(output_dir, '2XX'))
    except:
        pass
    try:
        os.rmdir(os.path.join(output_dir, '3XX'))
    except:
        pass
    try:
        os.rmdir(os.path.join(output_dir, '4XX'))
    except:
        pass
    try:
        os.rmdir(os.path.join(output_dir, '5XX'))
    except:
        pass


def banner():

    local_version, latest_version, new_features, bug_fixes, info = checkUpdates()
    update_available = False

    if local_version != latest_version:
        update_available = True

    print(colors.CYAN + " \
        \n\n \
        SourceWolf v" + local_version)

    if update_available == True:
        print(colors.GREEN + colors.UNDERLINE + "\n\nUpdated version v" + latest_version +
              " available", end="")
        print(colors.RESET + colors.RED, end="")
        print(end=" ")
        if new_features != [] and bug_fixes != []:
            print("with " + str(len(new_features)) + " new features " +
                  "and " + str(len(bug_fixes)) + " bug fixes!")
        elif new_features != [] and bug_fixes == []:
            print("with " + str(len(new_features)) + " new features!")
        elif new_features == [] and bug_fixes != []:
            print("with " + str(len(bug_fixes)) + " bug fixes!")
        if info != "":
            print("\n" + info[2:-2] + "\n")
        print(colors.RESET, end="")
        print(colors.BLUE + "Run flag --update-info for more details." + colors.RESET)

    print("\n\n" + colors.RESET)


if __name__ == "__main__":
    Parser = argparse.ArgumentParser()
    Parser.add_argument('-l', '--list', help="List of javascript URLs")
    Parser.add_argument('-t', '--threads',
                        help="Number of concurrent threads to use (default 5)")
    Parser.add_argument('-o', '--output directory-name',
                        help="Store URL response text in a directory for further analysis", dest="output_dir")
    Parser.add_argument('-s', '--store-status-code',
                        help="Store the status code in a file", dest="status_code_file")
    Parser.add_argument('-b', '--brute',
                        help="Brute force URL with FUZZ keyword (--wordlist must also be used along with this)")
    Parser.add_argument('-w', '--wordlist',
                        help="Wordlist for brute forcing URL")
    Parser.add_argument('-v', '--verbose',
                        help="Verbose mode (displays all the requests that are being sent)", action="store_true")
    Parser.add_argument(
        '-c', '--crawl-output', help="Output directory to store the crawled output", dest="crawl_output")
    Parser.add_argument(
        '-d', '--delay', help="Delay in the requests (in seconds)")
    Parser.add_argument('--timeout',
                        help="Maximum time to wait for connection timing out (in seconds)", dest="timeout")
    Parser.add_argument(
        '--headers', help="Add custom headers (Must be passed in as {'Token': 'YOUR-TOKEN-HERE'}) --> Dictionary format")
    Parser.add_argument(
        '--cookies', help="Add cookies (Must be passed in as {'Cookie': 'YOUR-COOKIE-HERE'}) --> Dictionary format")
    Parser.add_argument("--only-success", help="Only print 2XX responses",
                        dest="only_success", action="store_true")
    Parser.add_argument(
        '--local', help="Directory with local response files to crawl for")
    Parser.add_argument(
        "--no-colors", help="Remove colors from the output", dest="no_colors", action="store_true")
    Parser.add_argument(
        "--update-info", help="Check for the latest version, and update if required", action="store_true", dest="update")
    args = Parser.parse_args()

    if args.no_colors == True or os.name == "nt":
        removeColors()

    banner()
    if args.update == True:
        printResults()
        sys.exit(0)

    if args.local != None:
        crawlOutput(args.local, args.crawl_output)
        sys.exit(0)

    list_of_urls = args.list
    threads = args.threads
    delay = args.delay
    status_code_file = args.status_code_file
    output_dir = args.output_dir
    brute_urls = args.brute

    if delay:
        delay = int(delay)
    else:
        delay = 0

    if args.brute != None and args.wordlist == None:
        default = input(
            colors.YELLOW + "No wordlist specified!\nUse the default wordlist? [y/n]: " + colors.RESET)
        if default.lower() == 'y':
            args.wordlist = 'db/default-wordlist.txt'
        else:
            print(
                colors.RED + "Error: Required argument --wordlist for brute force mode" + colors.RESET)
            Parser.print_help()
            sys.exit(2)
    elif args.brute == None and args.wordlist != None:
        print(
            colors.RED + "Error: --wordlist argument specified but --brute not specifed" + colors.RESET)
        Parser.print_help()
        sys.exit(2)

    if args.brute != None and "FUZZ" not in args.brute:
        print(colors.RED + "Error: FUZZ keyword not found in the brute URL" + colors.RESET)
        sys.exit(2)

    if list_of_urls is None and args.brute == None:
        print(
            colors.RED + "Error: Required argument --list" + colors.RESET)
        Parser.print_help()
        sys.exit(2)

    try:
        if args.wordlist != None:
            urls = open(args.wordlist, "r")
    except FileNotFoundError:
        print(colors.RED + "File '" + args.wordlist +
              "' not found!" + colors.RESET)
        sys.exit(1)

    try:
        # getting the list of URLs from a list
        if list_of_urls != None:
            urls = open(list_of_urls, "r")
    except FileNotFoundError:
        print("File '" + list_of_urls + "' not found!")
        sys.exit(1)

    # opening the status code file if any
    if status_code_file != None:
        if os.path.exists(status_code_file) == True:
            os.remove(status_code_file)
        status_code_file = open(status_code_file, "a")

    if output_dir != None:
        # creating the output directory if not present
        if os.path.isdir(output_dir) == False:
            createOutputFolders()
        else:
            print(colors.CYAN + "The directory '" +
                  output_dir + "' already exists")
            print("Do you want to remove it? [y/n]" + colors.RESET, end=" ")
            remove = input()
            if remove.lower() == 'y':
                shutil.rmtree(output_dir)
                createOutputFolders()
            else:
                sys.exit(1)
    threads = None

    if args.threads is None:
        threads = 5
    else:
        threads = int(args.threads)

    # Limiting the number of threads to user input or default
    threadLimiter = threading.BoundedSemaphore(threads)

    # List of threading.Thread objects
    threads_to_be_run = []

    if brute_urls != None:

        if brute_urls[-1] != '/':
            brute_urls += '/'

        if brute_urls[0:8] != "https://" and brute_urls[0:7] != "http://":
            brute_urls = "http://" + brute_urls

    # Appending all the URLs to the threads to get their responses
    for url in urls:
        if args.wordlist != None:
            # brute method
            url = brute_urls.replace("FUZZ", url[:-1])
            url = url[:-1]
        else:
            # Adding the protocol if not specified in the list
            if url[0:8] != "https://" and url[0:7] != "http://":
                url = "http://" + url
        threads_to_be_run.append(getResponseThread(url, delay))

    # total number of requests to be sent
    total_lines = len(threads_to_be_run)
    urls_done = 0

    if args.list:
        print(colors.YELLOW + "\n[+] Loaded file '" + args.list +
              "' with " + str(total_lines) + " URLs\n" + colors.RESET)
    elif args.wordlist:
        print(colors.YELLOW + "\n[+] Loaded file '" + args.wordlist +
              "' with " + str(total_lines) + " words\n" + colors.RESET)

    # Running the threads
    for thread in threads_to_be_run:
        try:
            thread.start()
        except KeyboardInterrupt:
            exit_input = input(
                colors.YELLOW + "\nKeyboard interrupt detected! Exit?[y/n] " + colors.RESET)
            if exit_input.lower() == 'y':
                sys.exit(1)

    for thread in threads_to_be_run:
        thread.join()

    if output_dir != None:
        removeEmptyDirectories(output_dir)

        crawlOutput(output_dir, args.crawl_output)
