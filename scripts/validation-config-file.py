import yaml, os, sys

def main():
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    #check if mandatory key-values are present in config.yaml and in general, if keys have allowed values
    mandatory_elements = ["source-repo-url"]
    for e in mandatory_elements:
        if e not in config.keys():
            sys.exit(e + " not present in config file. It is a mandatory value.")
    
if __name__ == '__main__':
    main()
