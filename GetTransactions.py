from fints.client import FinTS3PinTanClient
from time import strftime
from datetime import datetime, timedelta
from lxml import etree as ET
import getpass
import uuid
import yaml
import os

with open('settings.yml') as f:
    dataMap = yaml.safe_load(f)
blz = str(dataMap['account']['blz'])
acc = str(dataMap['account']['acc'])
username = dataMap['account']['username']
password = getpass.getpass("Password:")
api = dataMap['account']['api']
endDate = datetime.now()
delta = input("Transactions for the last x Days:")
deltaint = int(delta)
startDate = endDate - timedelta(days=deltaint)

def GetTransactions(blz, username, password, api, acc):
    # Init fints Class
    fints = FinTS3PinTanClient(
        blz,
        username,
        password,
        api
    )
    accounts = fints.get_sepa_accounts()
    account = next(account for account in accounts if account.accountnumber == acc)
    transactions = fints.get_transactions(account, startDate, endDate)
    return transactions

#Create XML
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
timestamp2 = datetime.now().strftime("%Y%m%d000000")
root = ET.Element("OFX")
SIGNONMSGSRSV1 = ET.SubElement(root, "SIGNONMSGSRSV1")
SONRS = ET.SubElement(SIGNONMSGSRSV1, "SONRS")
STATUS = ET.SubElement(SONRS, "STATUS")
ET.SubElement(STATUS, "CODE").text = "0"
ET.SubElement(STATUS, "SEVERITY").text = "INFO"
ET.SubElement(SONRS, "DTSERVER").text = str(timestamp)
ET.SubElement(SONRS, "LANGUAGE").text = "GER"
BANKMSGSRSV1 = ET.SubElement(root, "BANKMSGSRSV1")
STMTTRNRS = ET.SubElement(BANKMSGSRSV1, "STMTTRNRS")
ET.SubElement(STMTTRNRS, "TRNUID").text = "0"
STMTTRNRSSTATUS = ET.SubElement(STMTTRNRS, "STATUS")
ET.SubElement(STMTTRNRSSTATUS, "CODE").text = "0"
ET.SubElement(STMTTRNRSSTATUS, "SEVERITY").text = "INFO"
STMTRS = ET.SubElement(STMTTRNRS, "STMTRS")
ET.SubElement(STMTRS, "CURDEF").text = "EUR"
BANKACCTFROM = ET.SubElement(STMTRS, "BANKACCTFROM")
ET.SubElement(BANKACCTFROM, "BANKID").text = str(blz)
ET.SubElement(BANKACCTFROM, "ACCTID").text = str(acc)
ET.SubElement(BANKACCTFROM, "ACCTTYPE").text = "CHECKING"
BANKTRANLIST = ET.SubElement(STMTRS, "BANKTRANLIST")
ET.SubElement(BANKTRANLIST, "DTSTART").text = str(timestamp2)
ET.SubElement(BANKTRANLIST, "DTEND").text = str(timestamp2)


#Get Transactions
transactions = GetTransactions(blz, username, password, api, acc)
for transaction in transactions:
    payee = transaction.data.get('applicant_name')
    amount = str(transaction.data.get('amount'))
    amountshort = amount[:-5][1:]
    amountfloat = float(amountshort)
    purpose = transaction.data.get('purpose')
    date = transaction.data.get('date')
    dateformated = date.strftime("%Y%m%d000000")
    uid = uuid.uuid4().hex
    STMTTRN = ET.SubElement(BANKTRANLIST, "STMTTRN")
    if amountfloat > 0:
        ET.SubElement(STMTTRN, "TRNTYPE").text = "CREDIT"
    else:
        ET.SubElement(STMTTRN, "TRNTYPE").text = "DEBIT"
    ET.SubElement(STMTTRN, "DTPOSTED").text = str(dateformated)
    ET.SubElement(STMTTRN, "TRNAMT").text = str(amountfloat)
    ET.SubElement(STMTTRN, "FITID").text = uid
    ET.SubElement(STMTTRN, "MEMO").text = purpose
    ET.SubElement(STMTTRN, "NAME").text = payee


xmlfile = root
tree = ET.ElementTree(xmlfile)
homedir = os.path.expanduser('~')
desktop = os.path.join(homedir, "Desktop")
path = os.path.join(desktop, "transactions.ofx")
tree.write(path, pretty_print=True, xml_declaration = True, encoding='UTF-8')