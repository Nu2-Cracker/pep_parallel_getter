import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ensembl_list")
args = parser.parse_args()
print(args.ensembl_list)
