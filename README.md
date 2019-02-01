# FinTS (HBCI) to OFX export, for using with YNAB
Get Transactions via fints (HBCI) and safe them in a OFX File

## Dependencies
Please use pip to install these Modules first:
pip install fints lxml

## Parameters
The Script is contolled by a config File (settings.yml) in yaml Syntax. This Parameters must be definied:

```yaml
account:
  blz: 76010085
  acc: 12345678
  username: 'xxxxxx'
  api: 'https://hbci.postbank.de/banking/hbci.do'
```

* blz:  Your Bank code
* acc: Your Bank account number
* username: Your Bank login Name or Number
* api: The fints (HBCI) API URL from your Bank

## Run the Script

```bash
fintsToOFX git:(master) ✗ python3 GetTransactions.py
Password:
Transactions for the last x Days:2
```

The Script first asks you for your Banking Passwort or PIN. The second input is the Value, how many days in the past you will request. 
The Script will save the OFX file on your Desktop. Maybe it's necessary that you edit the Path on Lines 88-90.