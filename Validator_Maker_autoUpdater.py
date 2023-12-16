#!/usr/bin/env python3

import subprocess
import time
import os


def Git_Repo():
	os.system("git clone https://github.com/Fair-Exchange/Safecoin.git")


def Get_User_Input(question):
        return input(question)

def New_install():
	os.system("sudo apt-get update")
	os.system("sudo apt-get install curl libssl-dev libudev-dev pkg-config zlib1g-dev llvm clang make git screen -y")
	
def Install_Cargo():
        os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
        os.system("source '$HOME/.cargo/env'")


def build_safecoin():
        os.system("cargo build --release --manifest-path Safecoin/Cargo.toml")


def Key_create():
	os.system("mkdir ~/home/$USER/ledger")
	print("")
	print("Creating validator identity keypair")
	time.sleep(2)
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ~/home/$USER/ledger/validator-identity.json")
        print("")
	print("Creating vote account keypair")
	time.sleep(2)
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ~/home/$USER/ledger/validator-vote-account.json")
	print("")
	print("Creating  authorized withdrawer keypair")
	time.sleep(2)
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ~/home/$USER/ledger/authorized-withdrawer.json")
	
	os.system("Safecoin/target/release/safecoin config set --keypair ~/home/$USER/ledger/validator-identity.json")
	
	
	os.system("Safecoin/target/release/safecoin address")
	res = Get_User_Input("Please add some safe to this address, this is for your validator to vote, would recomend 50 safe, please type anything, once safe has been sent, or press n to force build with out safe : ")

	if(res == "N" or res == "n"):
                HasDeposit = False
        else:
                time.sleep(10)
                HasDeposit = False
	
	while(HasDeposit == False):
                try:
                        proc = subprocess.Popen(["Safecoin/target/release/safecoin balance"], stdout=subprocess.PIPE, shell=True)
                        (out, err) = proc.communicate()
                        print("balance : ", out)
                        if(int(out).decode() > 1):
                                HasDeposit = True
                        else:
                                time.sleep(10)
                except:
                        time.sleep(10)
                        print("safecoin chain connection issue") 
                        res = Get_User_Input("do you want to force setup with no connection to chain (y or n) : ")
                        if(res == "y" or res == "Y"):
                                HasDeposit = True
                                
        os.system("Safecoin/target/release/safecoin create-vote-account ~/home/$USER/ledger/validator-vote-account.json ~/home/$USER/ledger/validator-identity.json ~/home/$USER/ledger/authorized-withdrawer.json")              
        res = Get_User_Input("Setup full history  (y or n) : ")
                if(res == "y" or res == "Y"):
                        print("adding auto start service for Full history Validator")
                        os.system("sudo cp start.sh ~/start.sh")
                        os.system("sudo chmod +x ~/start.sh")
                        os.system("sudo cp validator.service /etc/systemd/system/validator.service")
                        os.system("sudo systemctl enable --now validator")
                        os.system("sudo systemctl start validator")
                        sleep(60)
                        os.system("sudo systemctl stop validator")
                        os.system("sudo cp fullstart.sh ~/start.sh")
                        os.system("sudo chmod +x ~/start.sh")
                        os.system("sudo systemctl start validator")
                        
                else:
                        print("adding auto start service for pruned Validator")
                        os.system("sudo cp start.sh ~/start.sh")
                        os.system("sudo chmod +x ~/start.sh")
                        os.system("sudo cp validator.service /etc/systemd/system/validator.service")
                        os.system("sudo systemctl enable --now validator")
                        os.system("sudo systemctl start validator")

                print("auto start validator set and working, Please check https://onestopshop.ledamint.io/ or https://metrics.safegw.net:3000/ to make sure your validator is running corectly, can take 5 min to show")

                        
                        
	
res = Get_User_Input("New Validator (y or n) : ")

if(res == "y" or res == "Y"):
        #Setup new validator
        print("setting up New Validator, installing programs we uses")
        New_install()
        print("Getting safecoin repo")
        Git_Repo()
        print("installing safecoin")
        Install_Cargo()
        build_safecoin()
        print("repo built, build your validator keys")
        Key_create()


elif(res == "n" or res == "N"):
        res = Get_User_Input("Update Validator (y or n) : ")
        if(res == "y" or res == "Y"):
                #Update validator
                Git_Repo()
                print("New safecoin update downloaded, starting the build")
                time.sleep(2)
                build_safecoin()
                print("restarting your Validator please wait")
                os.system("sudo systemctl restart validator")
                time.sleep(5)
                os.system("~/Safecoin/target/release/safecoin validators")
                print("please check in above that you validator is running") 
                
        elif(res == "n" or res == "N"):
                print("Nothing left to do ending")
