import os
import sys
import glob

# files = glob.glob(sys.argv[1] + '/**/*.txt', recursive=True)


ending_chars = ['"', "'", '/', ' ', ';', ]


def condition_does_not_fail(text, social_media):
    if social_media == "instagram.com/":
        if "instagram.com/p" == text:
            return False
    elif social_media == "twitter.com/":
        twitter_exclude = ["intent", "share",
                           "widgets.js", "hashtag", "search", "?"]
        length = len(social_media)
        for exclude in twitter_exclude:
            if exclude in text:
                return False
    elif social_media == "facebook.com/":
        exclude = ["?", "sharer", "search"]
        for ex in exclude:
            if ex in text:
                return False

    return True


def check(f, social_media, output_file, verbose):
    file = open(f, "r")

    social_media += "/"
    length = len(social_media)

    if output_file != None:
        output = open(output_file, "a")

    for line in file:
        for i in range(len(line)-length):
            to_be_printed = ""
            if line[i:i+length] == social_media:
                to_be_printed += social_media
                i += length
                while i != len(line)-1 and line[i] not in ending_chars:
                    to_be_printed += line[i]
                    i += 1
                if condition_does_not_fail(to_be_printed, social_media):
                    if output_file != None:
                        output.write(to_be_printed + "\n")
                    print(to_be_printed)


def extract(file, output_file, verbose):

    check(file, "twitter.com", output_file, verbose)
    check(file, "instagram.com", output_file, verbose)
    check(file, "facebook.com", output_file, verbose)
