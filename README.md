# Prophecy DeFi
Install python https://www.python.org/downloads/

## Install GIT
If you are a mac user, download GIT from [this](https://git-scm.com/download/mac) link.

```
git clone https://github.com/vittoriopippi/prophecy_defi.git
cd prophecy_defi
python -m ensurepip
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python setup_webflow.py webflow_prophecy_defi.zip
python app.py
```
