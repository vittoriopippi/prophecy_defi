# Prophecy DeFi

## Installation
Install python https://www.python.org/downloads/
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
git clone https://github.com/vittoriopippi/prophecy_defi.git
cd prophecy_defi
python -m ensurepip
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Import new version of webflow
```
python setup_webflow.py webflow_prophecy_defi.zip
python app.py
```
