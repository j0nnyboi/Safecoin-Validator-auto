#!/usr/bin/env python3

from git import Repo
import subprocess
import time


def Git_Repo():
        Repo.clone_from('https://github.com/Fair-Exchange/Safecoin', "~/Desktop")

def Get_User_Input(question):
        return input(question)


def Install_Cargo():
        subprocess.run(["curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"])


def build_safecoin():
        subprocess.run(["cargo build --release --target-dir ~/Desktop/Safecoin"])







res = Get_User_Input("New Validator (y or n) : ")

if(res == "y" or res == "Y"):
        #Setup new validator
        print("setting up New Validator")
        print("Getting safecoin repo")
        Git_Repo()
        Install_Cargo()


elif(res == "n" or res == "N"):
        res = Get_User_Input("Update Validator (y or n) : ")
        if(res == "y" or res == "Y"):
                #Update validator
                Git_Repo()
                print("New safecoin update downloaded, starting the build")
                time.sleep(2)
                build_safecoin()
                print("restarting your Validator please wait")
                subprocess.run(["sudo systemctl restart validator"])
                time.sleep(5)
                subprocess.run(["sudo systemctl restart validator"])
                print("please check in above you validator is running") 
        elif(res == "n" or res == "N"):
                print("Nothing left to do ending")
