(optional) use a venv:

```
python3 -m venv venv
. venv/bin/activate
```

install the deps:

```
pip3 install -r requirements.txt
```

fill in info:

```
python3 prompt.py in.json out.json
```

> note: please share `out.json` with cnemo

gen out the secondary artifacts:

```
python3 report.py out.json report.txt
python3 credits.py out.json credits.csv
python3 master.py out.json master.csv
```
