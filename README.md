# FinTS (HBCI) to OFX export, for using with YNAB
Get Transactions via fints (HBCI) and safe them in a OFX File

## Dependencies
Please use pip to install these Python-modules first:
pip install fints lxml

## Parameters
The scripts config File (settings.yml) is in yaml Syntax. This parameters must be defined:

```yaml
account:
  blz: 76010085
  acc: 12345678
  username: 'xxxxxx'
  api: 'https://hbci.postbank.de/banking/hbci.do'
```

* blz: bank code
* acc: bank account number
* username: bank login Name or Number
* api: FinTS (HBCI) API URL

## Run the Script

```bash
fintsToOFX git:(master) ✗ python3 GetTransactions.py
Password:
Transactions for the last x Days:2
```

The script first asks you for your banking password or PIN. The second input is how many days in the past you will request.
The script will save the OFX file on your Desktop. Maybe it's necessary that you edit the Path on Lines 88-90.