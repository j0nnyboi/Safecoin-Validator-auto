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
        #os.system("source '$HOME/.cargo/env'")


def build_safecoin():
        os.system("cargo build --release --manifest-path Safecoin/Cargo.toml")


def Key_create():
	os.system("mkdir ledger")
	print("Creating validator identity keypair")
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ledger/validator-identity.json")

	print("Creating vote account keypair")
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ledger/validator-vote-account.json")
	
	print("Creating  authorized withdrawer keypair")
	os.system("Safecoin/target/release/safecoin-keygen new --word-count 24 -o ledger/authorized-withdrawer.json")
	
	os.system("Safecoin/target/release/safecoin config set --keypair ledger/validator-identity.json")
	
	
	os.system("Safecoin/target/release/safecoin address")
	res = Get_User_Input("Please add some safe to this address, this is for your validator to vote, would recomend 50 safe, please type y once safe has been sent : ")
	
	time.sleep(5)
	
	proc = subprocess.Popen(["Safecoin/target/release/safecoin balance"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	print("balance : ", out)
	if(int(out).decode() > 1):
		os.system("Safecoin/target/release/safecoin create-vote-account ledger/validator-vote-account.json ledger/validator-identity.json ledger/authorized-withdrawer.json")
		
		print("adding auto start service")
		os.system("sudo chmod +x ~/start.sh")
		os.system("sudo cp validator.service /etc/systemd/system/validator.service")
		os.system("sudo systemctl enable --now validator")
		os.system("sudo systemctl start validator")
		print("auto start validator set and working")


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
                print("please check in above you validator is running") 
                
        elif(res == "n" or res == "N"):
                print("Nothing left to do ending")
