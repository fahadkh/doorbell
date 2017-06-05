# coding=utf-8

from pymongo import MongoClient
from twilio.rest import Client
client = MongoClient('localhost', 27017)
db = client.test_db
people = db.people_collection

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACfd96d05b41ec687155b7f07983276713", "9cc72a6347ca17b0583e9edcd9b98c65")

# this is the URL to an image file we're going to send in the MMS
photo = "http://13.58.38.35/images/logo.png"

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send MMS to any phone number that MMS is available


def contact(numbers,photo):
	if not numbers is None:
		for number in numbers:
			strNum = "+1" + str(number)
			print "sending text to: " + strNum
			client.api.account.messages.create(to=strNum,from_="+13345390920",body="Someone\'s at your door!",media_url=photo)


def getContacts(name):
	doc = people.find_one({"name": name})
	if doc is None:
		return None
	return doc['group_contacts']


#contact(getContacts('Charlie'),photo)


#person1 = {
#	"name": 'Greg',
#	"group_members": ['Shlok Amin'],
#	"group_contacts": ['5309023614'],
#}

#person2 = {
# 	"name": 'Nikhil',
# 	"group_members": ['Armaan Shah'],
# 	"group_contacts": ['9144717671'],
#}

#person3 = {
# 	"name": 'Shlok',
# 	"group_members": ['Greg', 'Fahad'],
# 	"group_contacts": ['3347280151', '6304147003'],
#}

#people.insert_one(person1).inserted_id
#people.insert_one(person3).inserted_id
#print getContacts('Bob')






