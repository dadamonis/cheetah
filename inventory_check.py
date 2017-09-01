import pandas as pd
import re


def padlines(text, padding):
	return "\n".join(padding + l for l in text.splitlines())
	#comment


def format_chk(a):
	if file.endswith('.csv'):
		print('\nReading file...', file)
	else:
		print("Incorrect file format. Exiting.")
		exit()


def missing_data():
	x = inventory_df[inventory_df.isnull().any(axis=1)]
	# print(x)  # debug
	if x.empty:
		print(five,'INFO: No Missing Data Found')
	else:
		# print(x)  # debug
		print(five, 'WARN: MISSING DATA FOUND'.replace('\t',''))
		print(padlines(x.to_string(index=False), six))


def additional_data():
	add_data = inventory_df[['STORE_NO', 'SKU']].copy()
	cols = ['STORE_NO', 'SKU']
	for name in cols:
		add_data[name] = add_data[name].astype(str)
		#print(name)
		
	for name in add_data.columns:
		long = add_data[name].astype(str).map(len).max()
		small = add_data[name].astype(str).map(len).min()
		# print(long, small)
		if long == small:
			print(five, 'INFO: %s Values appear correct' % name)
		else:
			print(five, 'WARN: %s VALUES MAY BE IN ERROR FOR:' % name)
			if name == 'STORE_NO':
				x = add_data[add_data.STORE_NO.str.len() == max(add_data.STORE_NO.str.len())]
				print(padlines(x.to_string(index=False), six))
			elif name == 'SKU':
				x = add_data[add_data.STORE_NO.str.len() == max(add_data.STORE_NO.str.len())]
				print(padlines(x.to_string(index=False), six))
	# Check for > 3 columns for one or any row


def duplicate_data():
	dup_df = inventory_df[inventory_df.duplicated(['STORE_NO','SKU'],keep=False)]
	if dup_df.empty:
		print(five, 'INFO: No Duplicate Entries Found')
	else:
		#print('\n')
		print(five, 'WARN: DUPLICAE DATA FOUND!')
		print(padlines(dup_df.to_string(index=False), six))


file = input('Enter inventory file name and path if applicaple: ').lower()
format_chk(file)
inventory_df = pd.read_csv(file, delimiter=' *, *', engine='python')
# print(inventory_df.tail(2),'\n')  # debug
five = '     '
six = '      '
print()

missing_data()
additional_data()
duplicate_data()
print('\n')
