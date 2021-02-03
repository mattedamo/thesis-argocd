import os, yaml, sys

def main():
    args = sys.argv
    k = args[-1]
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    if k in ["source-repo-url"]:
        if k not in config.keys():
            sys.exit(k + " not present in config file, add it")
        else:
            print(config[k])
if __name__ == "__main__":
    main()
