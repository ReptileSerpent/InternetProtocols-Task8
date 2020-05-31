import argparse
import requests
import json

token = ""

def inquire(method_name, parameters, access_token, api_version):
	url = "https://api.vk.com/method/" + method_name + "?" + parameters + "&access_token=" + access_token + "&v=" + api_version
	response = requests.get(url)
	json_data = response.json()
	return json_data

def print_friends_list(user_id):
	print("Friends list:")
	friends_list = inquire("friends.get", "user_id=" + str(user_id), token, "5.107")

	try:
		for friend_id in friends_list["response"]["items"]:
			friend_info = inquire("users.get", "user_id=" + str(friend_id), token, "5.107")
			print(friend_info["response"][0]["first_name"] + " " + friend_info["response"][0]["last_name"] + " (id: " + str(friend_id) + ")")
	except Exception:
		print("An error occurred while processing your request. Make sure your token is correct.")

def print_albums_list(user_id):
	print("Albums list:")
	albums_list = inquire("photos.getAlbums", "owner_id=" + str(user_id), token, "5.107")

	try:
		for album_info in albums_list["response"]["items"]:
			album_name = album_info["title"] + " (id: " + str(album_info["id"]) + ")"
			print(album_name)
	except Exception:
		print("An error occurred while processing your request. Make sure your token is correct.")

def print_groups_list(user_id):
	print("Groups list:")
	groups_list = inquire("users.getSubscriptions", "user_id=" + str(user_id), token, "5.107")

	try:
		for group_id in groups_list["response"]["groups"]["items"]:
			group_info = inquire("groups.getById", "group_id=" + str(group_id), token, "5.107")
			print(group_info["response"][0]["name"] + " (" + str(group_id) + ")")
	except Exception:
		print("An error occurred while processing your request. Make sure your token is correct.")

parser = argparse.ArgumentParser()
parser.add_argument("user_id", type=int)
parser.add_argument("request_type", type=str)
args = parser.parse_args()

user_id = args.user_id
request_type = args.request_type

if (token == ""):
	print("No token provided")
else:
	if (request_type == "friends"):
		print_friends_list(user_id)
	elif (request_type == "albums"):
		print_albums_list(user_id)
	elif (request_type == "groups"):
		print_groups_list(user_id)
	else:
		print("Invalid request type")
