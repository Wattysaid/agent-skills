You’re hitting PEP 668 on Ubuntu 24.04 (and newer): the OS marks the system Python as “externally managed”, so pip install ... outside a virtual environment is blocked.

Recommended fix (project virtual environment)

From your repo root:

cd /mnt/d/GitHub/processminingagenttest

# 1) Create a venv in the project
python3 -m venv .venv

# 2) Activate it (bash/zsh)
source .venv/bin/activate

# 3) Confirm you are now using the venv python/pip
which python
which pip
python -m pip -V

# 4) Upgrade packaging tools inside the venv
python -m pip install -U pip setuptools wheel

# 5) Install your skill requirements inside the venv
python -m pip install -r .codex/skills/process-mining-assistant/requirements.txt


Quick sanity check:

python -c "import pandas; print('pandas OK')"


If you want to leave the venv:

deactivate


Common gotcha: if you forget to source .venv/bin/activate, you will keep using the system pip and keep seeing externally-managed-environment.

If python3 -m venv .venv fails

Install the “full” Python bundle (covers venv and common tooling):

sudo apt-get update
sudo apt-get install -y python3-full


Then rerun the venv steps above.

About your apt install python3-pandas error

That failure was simply because you didn’t use sudo:

sudo apt install -y python3-pandas


That said, for libraries like pm4py you will usually want the venv approach, because apt often won’t have the versions you need.