import jsbeautifier
import sys
import os


def getEndpointFromFile(file):
    endpoint = file.split('/')[2]
    endpoint = endpoint[:-4]
    endpoint = endpoint.replace("@", "/")
    endpoint = "http://" + endpoint

    return endpoint


def variableSearch(file, output_file, verbose):

    code = jsbeautifier.beautify_file(file)

    i = 0

    res = []

    while i < len(code):
        # this is done to avoid redunduncy while comparing let and var
        name = code[i:i+3]

        if name == "var" or name == "let" or code[i:i+5] == "const":
            if name == "var":
                i += 3
            else:
                i += 5
            if code[i] != "=" and code[i] != " " and code[i] != ";":
                continue
            var_name = ""
            while 1:
                if code[i] == " ":
                    i += 1
                    continue
                if code[i] == "=" or code[i] == ";":
                    break
                var_name += code[i]
                i += 1
            if "," in var_name:
                for name in var_name.split(","):
                    res.append(name)
                    # print(name)
            else:
                res.append(var_name)
                # print(var_name)
        else:
            i += 1

    # removes duplicates
    res = list(dict.fromkeys(res))
    if verbose == True and res != []:
        verbose_message = "URL " + \
            getEndpointFromFile(file) + " contains the variables: "
        print(verbose_message)
    for word in res:
        print(word)

    if output_file != None:
        out = open(output_file, "a")
        if verbose != None:
            out.write(verbose_message + "\n")
        for word in res:
            out.write(word + "\n")
        out.write("\n")
        out.close()


if __name__ == "__main__":
    getVarNames(sys.argv[1], sys.argv[2])
