import sys
import os


def removeQuotes(endpoint):
    try:
        if endpoint[0] == '"':
            endpoint = endpoint[1:]
    except:
        pass
    try:
        if endpoint[-1] == '"':
            endpoint = endpoint[:-1]
    except:
        pass
    return endpoint


def getAttributeValues(file):
    links = []
    if "src" in file:
        for i in range(len(file)-3):
            if file[i:i+3] == "src":
                endpoint = file[i+4:].split('>')[0].split(' ')[0]
                if '=' in endpoint:
                    endpoint = endpoint.split('=')[1].strip()
                endpoint = removeQuotes(endpoint)
                try:
                    # if endpoint[0] != '/':
                    links.append(endpoint)
                except:
                    pass
    elif "href" in file:
        for i in range(len(file)-4):
            if file[i:i+4] == "href":
                endpoint = file[i+5:].split('>')[0].split(' ')[0]
                endpoint = removeQuotes(endpoint)
                if '=' in endpoint:
                    endpoint = endpoint.split('=')[1].strip()
                try:
                    # if endpoint[0] != '/':
                    links.append(endpoint)
                except:
                    pass
    return links


def getHostFromFilename(file_path):
    if os.name == "nt":
        host = file_path.split('\\')[-1]
    else:
        host = file_path.split('/')[-1]
    host = "http://" + host[:-4]
    if host[:-1] != '/':
        host += '/'
    host = host.replace('@', '/')
    return host


def getDomainFromEndpoint(endpoint):
    if endpoint[:8] == "https://":
        endpoint = endpoint[8:]
    elif endpoint[:7] == "http://":
        endpoint = endpoint[7:]
    return "http://" + endpoint.split('/')[0] + '/'


def endpointSearch(file, output_file):
    f = open(file, "r")
    terminating_chars = ['"', "'", ')', '(', ';', ':', ' ', '<', '>', ',']
    endpoints = []

    # endpoints.append(getAttributeValues(file))
    # print(file)
    for line in f:
        values = getAttributeValues(line)
        host = getHostFromFilename(file)
        if values != []:
            for v in values:
                res = ""
                try:
                    if v[:8] == "https://" or v[:7] == "http://":
                        res = v
                    elif v[:2] == "//":
                        res = "http:" + v
                    elif v[0] == "/":
                        v = v[1:]
                        res = getDomainFromEndpoint(
                            getHostFromFilename(file)) + v
                    else:
                        res = host + v
                    endpoints.append(res)
                    print(res)
                except:
                    pass
        flag = 0
        endpoint = ""
        prev = ''
        for char in line:
            if char in terminating_chars and flag == 1:
                flag = 0
                if '>' not in endpoint:
                    if endpoint[:2] == "//":
                        endpoint = "http:" + endpoint
                    else:
                        # file is /path/to/url, host is url
                        host = getHostFromFilename(file)
                        if endpoint[0] == '/':
                            endpoint = endpoint[1:]
                            host = getDomainFromEndpoint(host)
                        endpoint = host + endpoint
                        endpoint = endpoint.replace('@', '/')
                    print(endpoint)
                    endpoints.append(endpoint)
                endpoint = ""
            elif prev == '<':
                prev = char
                continue
            elif (char == '/' or flag == 1) and char not in terminating_chars:
                endpoint += char
                flag = 1
            prev = char

    # removes duplicates
    endpoints = list(dict.fromkeys(endpoints))

    if output_file != None:
        # if os.path.isfile(output_file) == True:
        #     os.remove(output_file)
        out = open(output_file, "a")
        for endpoint in endpoints:
            out.write(endpoint + "\n")
