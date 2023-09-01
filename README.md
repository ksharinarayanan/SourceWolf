<p align="center">
  <img src="https://github.com/ksharinarayanan/SourceWolf/blob/master/images/logo.png" width="130px" height="130px">
  <br>
  <br>
  <h1 align="center">SourceWolf</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.7-brightgreen">
  <img src="https://img.shields.io/github/issues-closed/ksharinarayanan/SourceWolf">
  <img src="https://img.shields.io/github/issues-pr-closed/ksharinarayanan/SourceWolf">
  <img src="https://img.shields.io/github/contributors/ksharinarayanan/SourceWolf">
</p>

​

**Tested environments:** Windows, MAC, linux, and windows subsystem for linux (WSL)

## Sponsors

Support this project by <a href="mailto:ksharinarayanan36@gmail.com">becoming</a> a sponsor. Checkout these awesome sponsors:

<a href="https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=997&url_id=120">
<img src="https://raw.githubusercontent.com/ksharinarayanan/SourceWolf/master/images/oxylabs.jpeg" width="400" height="200" />
</a>


## Sections

-   <a href="#features">Features</a>
-   <a href="#installation">Installation</a>
-   <a href="#usage">Usage</a>
-   <a href="#workflow">How can this be integrated into your workflow?</a>
-   <a href="#todo">To do</a>
-   <a href="#update">Updating SourceWolf</a>
-   <a href="#contributions">Contributions</a>
-   <a href="#issues">Issues</a>
-   <a href="#naming">File naming conventions</a>

<div id="features">
<h3> What can SourceWolf do?</h3>

-   Crawl through responses to find hidden endpoints, either by sending requests, or from the local response files (if any).

-   Create a list of javascript variables found in the source

-   Extract all the social media links from the websites to identify potentially broken links

-   Brute forcing host using a wordlist.

-   Get the status codes for a list of URLs / Filtering out the live domains from a list of hosts.

All the features mentioned above execute with great speed.

-   SourceWolf uses the **Session** module from the requests library, which means, it reuses the TCP connection, making it really fast.

-   SourceWolf provides you with an option to crawl the responses files **locally** so that you aren't sending requests again to an endpoint, whose response you already have a copy of.

-   The final endpoints are in a complete form with a host like `https://example.com/api/admin` are not as `/api/admin`. This can come useful, when you are scanning a list of hosts.

</div>
<hr>

### Installation

-   git clone https://github.com/ksharinarayanan/SourceWolf (or) Download the latest <a href="https://github.com/ksharinarayanan/SourceWolf/releases">release</a>!
-   cd SourceWolf/
-   pip3 install -r requirements.txt

<hr>

### Usage

```
> python3 sourcewolf.py -h

-l LIST, --list LIST  List of javascript URLs
-u URL, --url URL     Single URL
-t THREADS, --threads THREADS
                      Number of concurrent threads to use (default 5)
-o OUTPUT_DIR, --output directory-name OUTPUT_DIR
                      Store URL response text in a directory for further analysis
-s STATUS_CODE_FILE, --store-status-code STATUS_CODE_FILE
                      Store the status code in a file
-b BRUTE, --brute BRUTE
                      Brute force URL with FUZZ keyword (--wordlist must also be used along with this)
-w WORDLIST, --wordlist WORDLIST
                      Wordlist for brute forcing URL
-v, --verbose         Verbose mode (displays all the requests that are being sent)
-c CRAWL_OUTPUT, --crawl-output CRAWL_OUTPUT
                      Output directory to store the crawled output
-d DELAY, --delay DELAY
                      Delay in the requests (in seconds)
--timeout TIMEOUT     Maximum time to wait for connection timing out (in seconds)
--headers HEADERS     Add custom headers (Must be passed in as {'Token': 'YOUR-TOKEN-HERE'}) --> Dictionary format
--cookies COOKIES     Add cookies (Must be passed in as {'Cookie': 'YOUR-COOKIE-HERE'}) --> Dictionary format
--only-success        Only print 2XX responses
--local LOCAL         Directory with local response files to crawl for
--no-colors           Remove colors from the output
--update-info         Check for the latest version, and update if required
```

<div id="test">SourceWolf has <b>3 modes</b>, which corresponds to it's <b>3 core features</b>.</div>

-   #### Crawl response mode:

![](https://github.com/ksharinarayanan/SourceWolf/blob/master/images/crawl.JPG)

Complete usage:

```
  python3 sourcewolf.py -l domains -o output/ -c crawl_output
```

`domains` is the list of URLs, which you want to crawl in the format:

```
https://example.com/
https://exisiting.example.com/
https://exisiting.example.com/dashboard
https://example.com/hitme
```

`output/` is the directory where the response text files of the input file are stored. <br/>

> They are stored in the format output/2XX, output/3XX, output/4XX, and output/5XX. <br>
> output/2XX stores 2XX status code responses, and so on!

<br>

`crawl_output` specified using the `-c` flag is used to store the output, inside a directory which SourceWolf produces by crawling the HTTP response files, stored inside the `output/` directory (currently only endpoints)

The ```crawl_output/``` directory contains:

endpoints - All the endpoints found
<br>
jsvars - All the javascript variables

> The directory will have more files, as more modules, and features are integrated into SourceWolf.

<br>

<p align="center"><b>(OR)</b></p>

For a single URL, <br>

```
  python3 sourcewolf.py -u example.com/api/endpoint -o output/ -c crawl_output
```

Only the flag `-l` is replaced by `-u`, everything else remains the same.

<br>

-   #### Brute force mode

![](https://github.com/ksharinarayanan/SourceWolf/blob/master/images/brute.JPG)

```
python3 sourcewolf.py -b https://hackerone.com/FUZZ -w /path/to/wordlist -s status
```

`-w` flag is optional. If not specified, it will use a default wordlist with 6124 words

SourceWolf replace the `FUZZ` keyword from the `-b` value with the words from wordlist, and sends the requests. This enables you to brute force get parameter values as well.

`-s` will store the output in a file called `status`

-   #### Probing mode

> Screenshot not included as the output looks similar to `crawl response` mode.

```
python3 sourcewolf -l domains -s live
```

The `domains` file can have anything like subdomains, endpoints, js files.
<br>

The `-s` flag write the response to the `live` file.

> Both the brute force and probing mode prints all the status codes except 404 by default. You can customize this behavior to print only `2XX` responses by using the flag `--only-success`

SourceWolf also makes use of multithreading.
<br>
The default number of threads for all modes is 5. You can increase the number of threads using the `-t` flag.

In addition to the above three modes, there is an option crawl locally, provided you have them locally, and follow <a href="#naming">sourcewolf compatible naming conventions.</a>

Store all the responses in a directory, say `responses/`

```
python3 sourcewolf.py --local responses/
```

This will crawl the local directory, and give you the results.

<hr>

### How can this be integrated into your workflow?

<br>
<p align="center">
  Subdomain enumeration <br>
  <b>| <br>
  | <br></b>
  SourceWolf <br>
  <b>| <br>
  | <br></b>
  Filter out live subdomains <br>
  <b>| <br>
  | <br></b>
  Store responses and find hidden endpoints / Directory brute forcing <br>
</p>

At this point, you will have a lot of endpoints from the target, extracted real time from the web pages at the time of performing the scan.

<hr>

SourceWolf core purpose is made with a broader vision to crawl through responses not just for discovering hidden endpoints, but also for automating all the tasks which are done by manually searching through the response files.

> One such example would be manually searching for any leaked keys in the source.

This core purpose explains the modular way in which the files are written.

<div id="#todo">

## To do

-   Generate a custom wordlist for a target from the words obtained in the source.
-   Automate finding any leaked keys.

</div>

<div id="#update">

### Updates

It is possible to update SourceWolf right from the terminal, without you having to clone the repository again.
<br>
SourceWolf checks for updates everytime it runs, and notifies the user if there are any updates available along with a summary of it.
<br>
![](https://github.com/ksharinarayanan/SourceWolf/blob/master/images/update.JPG)

Running

```
python3 sourcewolf.py --update-info
```

provides more details on the update
<br>
![](https://github.com/ksharinarayanan/SourceWolf/blob/master/images/update-info.JPG)

When there are updates available, you must move the update.py file outside of the SourceWolf directory, and run
<br>
**Warning: This deletes all the files and folders inside your SourceWolf directory**

```
python3 update.py /path/to/SourceWolf
```

This actually removes the directory, and clones back the repo.

</div>

<div id="#contributions">

### Contributions

Currently, sourcewolf supports only finding hidden endpoints from the source, but you can expect other features to be integrated in the future.

</div>

**Where can you contribute?**
<br>
Contributions are mainly required for integrating more modules, with sourcewolf, though feel free to open a PR even if it's a typo.

> Before sending a pull request, ensure that you are on the latest version. <br> > **Open an issue first if you are going to add a new feature to confirm if it's required! You must not be wasting time trying to code a new feature which is not required.**

</div>

<div id="#issues">

### Issues

Feel free to [open](https://github.com/ksharinarayanan/SourceWolf/issues/new) any issues you face. <br>
Ensure that you include your operating system, command which was run, and screenshots if possible while opening an issue, which makes it easier for me to reproduce the issue.
<br>
You can also request new features, or enhance existing features by opening an issue.

</div>

<div id="naming">

### Naming conventions

To crawl the files locally, you must follow some naming conventions. These conventions are in place for SourceWolf to directly identify the host name, and thereby parse all the endpoints, including the relative ones.

Consider an URL `https://example.com/api/`

-   Remove the protocol and the trailing slash (if any) from the URL --> `example.com/api`
-   Replace '/' with '@' --> `example.com@api`
-   Save the response as a txt file with the file name obtained above.

So the file finally looks like `example.com@api.txt`

</div>

### Credits

Logo designed by <a href="https://instagram.com/murugan_artworks">Murugan artworks</a>

### License

SourceWolf uses the <a href="https://github.com/ksharinarayanan/SourceWolf/blob/master/LICENSE">MIT license</a>
