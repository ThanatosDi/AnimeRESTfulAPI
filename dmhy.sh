cd /home/dmhy
if [ ! -d ".env" ]; then
        virtualenv .env --no-site-packages
        source .env/bin/activate
        python3 -m pip install -r requirements.txt
fi

source .env/bin/activate
python3 app.py