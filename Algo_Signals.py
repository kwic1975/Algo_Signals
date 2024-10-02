import os
import urllib.request
from cryptography.fernet import Fernet
import pandas
# Clients get this, they have to configure the path
json_file_pathname='<enter your filepath to json files here>'
jsonkey_file_pathname='<enter your filepath to encryption key here>'

# This is IC's settings, not to be shared
# json_file_pathname="C:\\Users\\...\\Testing\\"
# jsonkey_file_pathname="C:\\Users\\...\\Testing\\"

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
jsonlist=['cme_trident_daily_signal_menu.json','etf_trident_daily_signal_menu.json','TRIDENT_TLTD_NEW_SIGNALS.json','TRIDENT_TLTD_DAILY_DECISIONS.json','TRIDENT_TLTD_RGL.json','TRIDENT_TLTD_URGL.json']
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

api_trident_signal_menu=pandas.DataFrame()
for fn in ['cme_trident_daily_signal_menu.json','etf_trident_daily_signal_menu.json',]:
    api_trident_signal_menu=pandas.concat([api_trident_signal_menu,pandas.read_json(json_file_pathname+fn,orient='table')])

api_trident_tltd_new_signals=pandas.read_json(json_file_pathname+'TRIDENT_TLTD_NEW_SIGNALS'+'.json',orient='table')
api_trident_tltd_daily_decisions=pandas.read_json(json_file_pathname+'TRIDENT_TLTD_DAILY_DECISIONS'+'.json',orient='table')
api_trident_tltd_rgl=pandas.read_json(json_file_pathname+'TRIDENT_TLTD_RGL'+'.json',orient='table')
api_trident_tltd_urgl=pandas.read_json(json_file_pathname+'TRIDENT_TLTD_URGL'+'.json',orient='table')

print(api_trident_signal_menu.shape,api_trident_tltd_new_signals.shape,api_trident_tltd_daily_decisions.shape,api_trident_tltd_rgl.shape,api_trident_tltd_urgl.shape,)


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
for fn in jsonlist:
    try:
        os.remove(json_file_pathname+fn,)
    except:
        pass