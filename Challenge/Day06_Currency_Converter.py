import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
URL = "https://www.iban.com/currency-codes"
CURRENCY_URL = "https://wise.com/gb/currency-converter"
things = []
country = []
code = []

def find_num(country):
	while True:
		try:
			num = int(input("#: "))
			if num >= 0 and num <= 264:
				break
			else:
				print("Choose a number from the list.")
		except ValueError:
			print("That wasn't a number")
	print(f"{country[num]}\n")
	return (num)


def convert_money(base_num, sub_num, code):
	while True:
		print(f"How many {code[base_num]} do you wnat to convert to {code[sub_num]}?")
		try:
			amount = int(input())
			break
		except ValueError:
			print("That wasn't a number.\n")
	result = requests.get(f"{CURRENCY_URL}/{code[base_num].lower()}-to-{code[sub_num].lower()}-rate?amount=1")
	soup = BeautifulSoup(result.text, "html.parser")
	success = float(soup.find("span", {"class": "text-success"}).string) * amount
	print(format_currency(amount, code[base_num], locale = "ko_KR"),"is",format_currency(success, code[sub_num], locale = "ko_KR"))


result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")
everything = soup.find("tbody").find_all("td")
for i in everything:
	things.append(i.string)
for i in range(len(things)):
	if i % 4 == 0:
		if things[i + 1] == "No universal currency":
			continue
		else:
			country.append(things[i].capitalize())
	if i % 4 == 2:
		if things[i] == None:
			continue
		else:
			code.append(things[i])

print("Welcome to CurrencyConvert PRO 2000\n")
for i in range(len(country)):
	print(f"# {i} {country[i]}")
print("\nWhere are you from? Choose a country by number\n")
base_num = find_num(country)
print("Now choose another counntry.\n")
sub_num = find_num(country)
convert_money(base_num, sub_num, code)
