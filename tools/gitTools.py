import os

def pushRepository():

    os.system("git add .")
    os.system("git commit -m 'AI generated project'")
    os.system("git push origin main")

    return "code pushed to github"