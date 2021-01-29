import os


def main():
    #get env var
    tier = os.environ["TIER"]
    code_branch = os.environ["CODE_BRANCH"]
    app_name = os.environ["APP_NAME"]
    code_branch_list = code_branch.split("/")

    if code_branch == "master":
        manifest_name_pattern = "prod-" 
    else:
        manifest_name_pattern = tier+"-"+code_branch_list[0]+"-"+code_branch_list[1]
    
    toRemove = []
    for f in os.listdir("manifests/"+app_name+"/"):
        if manifest_name_pattern in f:
            toRemove.append(f)

    for ele in toRemove:
        os.remove("manifests/"+app_name+"/"+ele)

        
    
if __name__ == '__main__':
    main()
