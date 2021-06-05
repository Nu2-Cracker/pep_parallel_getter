
import subprocess
from multiprocessing import Pool
import time
import re
import argparse


def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    args = parser.parse_args()
    return args.arg1


def patternCheck(ftp):
    pattern = re.compile(r"pep\.all\.fa\.gz")
    s = pattern.search(ftp)
    return s != None


def createFastaUrl(text):
    header = "ftp://ftp.ensembl.org/pub/current_fasta/"

    with open(text, mode="r", encoding="utf-8") as fr:
        global url
        url = fr.read()

    urls = list(map(lambda x: x.replace("./", ""), url.split("\n")))
    urls = list(filter(patternCheck, urls))
    urls = list(filter(lambda y: y != "", urls))
    urls = list(map(lambda z: header + z, urls))

    return urls


def getFasta(ftp):
    subprocess.run(["aria2c", "-x16", "-s16", "-k20M", ftp])


def worker(text):
    p = Pool(6)
    urls = createFastaUrl(text)
    for ftp in urls:
        p.apply_async(getFasta, args=(ftp,))

    print("waiting for all subprocesses done....")
    p.close()
    p.join()
    print('All subprocesses done.')


if __name__ == "__main__":
    start = time.perf_counter()
    text = argParser()
    worker(text)
    end = time.perf_counter() - start

    print("Time: {}".format(end))
