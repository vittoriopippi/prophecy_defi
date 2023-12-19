# Prophecy DeFi

## Installation
Install python https://www.python.org/downloads/
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo "export PATH=/opt/homebrew/bin:$PATH" >> ~/.zshrc
```
Close the terminal and reopen it.
```
brew doctor
brew install git
```
With the terminal open the desired location where you want to create the project. (E.g., `cd ~/Desktop` if you want to create it on the Desktop)
```
git clone https://github.com/vittoriopippi/prophecy_defi.git
cd prophecy_defi
python3 -m ensurepip
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Import new version of webflow
```
python3 setup_webflow.py webflow_prophecy_defi.zip
python3 app.py
```
