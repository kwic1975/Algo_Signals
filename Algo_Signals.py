import os
import urllib.request
from cryptography.fernet import Fernet
import pandas
json_file_pathname='<enter your filepath to json files here>'
jsonkey_file_pathname='<enter your filepath to encryption key here>'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
jsonlist=['cme_trident_daily_signal_menu.json','etf_trident_daily_signal_menu.json']
# READ Encrypted json
def url_get_contents(url):
    req = urllib.request.Request(url=url, headers=HEADERS)
    f = urllib.request.urlopen(req)
    return f.read()
for fn in jsonlist:
    with open(json_file_pathname+fn, "w") as myfile:
        myfile.write(url_get_contents('https://www.algoreturns.com/'+fn).decode('utf-8'))

# DECIPHER
try:
	with open(jsonkey_file_pathname+'jsonkey.key', 'rb') as filekey:
		key = filekey.read()
	fernet = Fernet(key)
	for fn in jsonlist:
		with open(json_file_pathname+fn,'rb') as enc_file:
			encrypted = enc_file.read()
		decrypted = fernet.decrypt(encrypted)
		with open(json_file_pathname+fn, 'wb') as dec_file:
			dec_file.write(decrypted)
	print('Unlocked')
except:
	print('Files are already unlocked')

# READ into dataframe
df=pandas.DataFrame()
for fn in jsonlist:
    df=pandas.concat([df,pandas.read_json(json_file_pathname+fn,orient='table')])

print(df.shape)

# Optional but recommended
# CIPHER
with open(jsonkey_file_pathname+'jsonkey.key', 'rb') as filekey:
	key = filekey.read()
fernet = Fernet(key)
for fn in jsonlist:
	with open(json_file_pathname+fn,'rb') as file:
		original = file.read()
	encrypted = fernet.encrypt(original)
	with open(json_file_pathname+fn, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
print('Locked')

# REMOVE
for file in jsonlist:
    try:
        os.remove(json_file_pathname+fn,)
    except:
        pass