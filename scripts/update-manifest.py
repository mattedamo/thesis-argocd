import yaml, os


def main():
    
    with open("./input.yaml") as file:
        input = yaml.load(file, Loader=yaml.FullLoader)
    
    tier = os.environ["TIER"]
    code_branch = os.environ["CODE_BRANCH"]
    source_repo_url = os.environ["SOURCE_REPO_URL"] 
    app_name = os.environ["APP_NAME"]

    os.makedirs("manifests/"+app_name+"/", exist_ok=True)
    if "anchor" not in os.listdir("manifests/"+app_name+"/"):
        open("manifests/"+app_name+"/anchor", "x")
    code_branch_list = code_branch.split("/")
    
    working_dir = "manifests/"+app_name+"/"
    
    clusters = input["clusters"]
    list_manifests_to_delete = []
    for c in clusters:
        #build metatata name
        if code_branch == "master":
            manifest_name = "prod" + "-" + c + ".yaml"
        else:
            manifest_name = tier+"-"+code_branch_list[0]+"-"+code_branch_list[1] +"-" + c + ".yaml"
        if manifest_name in os.listdir(working_dir):
            list_manifests_to_delete.append(manifest_name)

    for man in list_manifests_to_delete:
        os.remove(working_dir+man)
    
    list_manifests = os.listdir(working_dir)
    for c in clusters:
        if code_branch == "master":
            manifest_name = "prod-" + c + ".yaml" 
        else:
            manifest_name = tier+"-"+code_branch_list[0]+"-"+code_branch_list[1] +"-" + c + ".yaml"
        
        if manifest_name not in list_manifests:
            if code_branch == "master":
                path = "kustomize/overlays/prod/"
                metadata_name = "prod-" + c
                namespace = app_name+"-prod"

            else:
                path = "kustomize/overlays/"+tier+"/"+code_branch+"/"
                metadata_name = tier+"-"+code_branch_list[0]+"-"+code_branch_list[1] + "-" + c
                namespace = app_name+"-"+tier+"-"+code_branch_list[0]+"-"+code_branch_list[1]
            
            #creo il file dentro a manifests/ con come name il manifest_name
            open(working_dir+manifest_name, "x")

            #lo fillo
            manifest = {}
            manifest["apiVersion"] = "argoproj.io/v1alpha1"
            manifest["kind"] = "Application"
            finalizers = ["resources-finalizer.argocd.argoproj.io"]
            manifest["metadata"] = { "name" : metadata_name, "namespace" : "argocd", "finalizers": finalizers }
            source = { "repoURL" : source_repo_url, "path" : path, "targetRevision" : "HEAD"}
            destination = { "name" : c, "namespace" : namespace}
            automated = { "prune" : True, "selfHeal" : True, "allowEmpty" : True }
            syncOptions = ["CreateNamespace=true"]
            syncPolicy = {"automated" : automated, "syncOptions" : syncOptions}
            manifest["spec"] = {"project" : "default", "source" : source,  "destination" : destination, "syncPolicy" : syncPolicy}

            #lo salvo
            with open(working_dir+manifest_name, "w") as file:
                yaml.dump(manifest, file)
    
if __name__ == '__main__':
    main()
