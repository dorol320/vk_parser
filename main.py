import vk_api
import os
from collections import Counter

#Чтение логина и пароля для авторизации
opened_file = open("auth_vk.txt", "r")
AUTH_LOG_PASS = str(opened_file.readline())
opened_file.close()
AUTH_LOG_PASS= AUTH_LOG_PASS.split(":"),
#Авторизация
try:
	vk_session = vk_api.VkApi(AUTH_LOG_PASS[0][0], AUTH_LOG_PASS[0][1])
	vk_session.auth()
	vk = vk_session.get_api()
except:
	print("Неверный логин и/или пароль. Возможно вы используете 2ФА, она не поддреживается. Запишите данные для входа в файл auth_vk.txt")

def GetMainUserInfo(user_id): #main function
	global person_info_by_user_ids
	global CURRENT_ID
	person_info_by_user_ids = vk.users.get(user_ids=user_id,fields='sex, bdate, city, country, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_see_all_posts, can_see_audio, career, military, ')
	person_info_by_user_ids = dict(person_info_by_user_ids[0])
	CURRENT_ID = person_info_by_user_ids['id']
	try:
		print("Создание папки юзера")
		os.mkdir(str(person_info_by_user_ids['first_name'])+ " " + str(person_info_by_user_ids['last_name']))
		os.chdir(str(person_info_by_user_ids['first_name'])+ " " + str(person_info_by_user_ids['last_name']))
		print("Папка успешно создана")
	except FileExistsError:
		print("Папка уже существует, все файлы будут заменены")
		os.chdir(str(person_info_by_user_ids['first_name'])+ " " + str(person_info_by_user_ids['last_name']))
	#создание main data файла
	opened_file = open(str(CURRENT_ID) + "_main_data.txt", "w")
	opened_file.write("Данные из users.get:" + "\n")
	try:
		for each in person_info_by_user_ids:
			if (person_info_by_user_ids[each] != ''):
				opened_file.write('\t' + str(each) + ' : ' + str(person_info_by_user_ids[each]) + "\n")
	except:
		print("smt happened")
	opened_file.close()

def GetFriendsInfo(user_id):
	#создание файла с id друзей
	person_friend_list = vk.friends.get(user_id=user_id)
	opened_file = open(str(user_id) + "_friend_list.txt", "w")
	opened_file.write(str("Количество: ") + str(person_friend_list['count']))
	opened_file.write(str("\n") + str("ID каждого в порядке возрастания: " + str("\n\t")))
	for each in person_friend_list['items']: # в этом цикле должна быть обработка друзей или не в этом :D
		opened_file.write(str(each) + str("\n\t"))
	opened_file.close()
	if (person_info_by_user_ids.get('city', None) == None):
		most_popular_cities = []
		i = 1 # otladka
		for each in person_friend_list['items']:
			current_friend_info = vk.users.get(user_ids=each,fields='city')
			try:
				i = i+1 # otladka
				most_popular_cities.append(current_friend_info[0]['city']['title'])
				if (i == 6):# otladka
					break;
			except:
				continue
			#most_popular_cities.append(current_friend_info['city'])
		most_popular_city = Counter(most_popular_cities)
		opened_file = open(str(user_id) + "_main_data.txt", "a")
		opened_file.write("Большинство друзей из города: " + str(most_popular_city.most_common(1)[0][0]) + ". " + str(most_popular_city.most_common(1)[0][1]) + " человек.")	
		opened_file.write("\n")
	opened_file.close()

def SearchOfLocationOnPhotos(user_id):
	all_photos = vk.photos.getAll(owner_id=user_id)
	opened_file = open(str(user_id) + "_main_data.txt", "a")
	opened_file.write("Геолокация на фото:")
	geo_counter = 0
	for each in all_photos['items']:
		try:
			opened_file.write(str("\n\t") + "ID of photo : " + str(each['id']) + " Latitude is: " + str(each['lat']) + " Longitude is: " + str(each['long']))
			geo_counter += 1
		except KeyError:
			continue
	if (geo_counter == 0):
		opened_file.write("Геолокация не найдена")
	opened_file.close()

def GetCommentsOnProfile(user_id):
	all_photos = vk.photos.getAll(owner_id=user_id)
	most_common_commentators = []
	for each in all_photos['items']:
		current_photo_comments = vk.photos.getComments(owner_id=user_id, photo_id=int(each['id']))
		current_photo_comments  = current_photo_comments['items']
		for each1 in current_photo_comments:
			 most_common_commentators.append(each1['from_id'])
	most_common_commentators = Counter(most_common_commentators)
	opened_file = open(str(user_id) + "_main_data.txt", "a")
	opened_file.write("\nБольше всего комментариев оставили пользователи:")
	for each in most_common_commentators.most_common(3):
		opened_file.write("\n\t" + " vk.com/id" + str(each[0]))
	opened_file.close()

CURRENT_USER = None
while (CURRENT_USER == None):
	CURRENT_USER = str(input("Введите ID либо короткую ссылку: "))
GetMainUserInfo(CURRENT_USER)
ask_for_friends_info = None
while ((ask_for_friends_info != str("y")) and (ask_for_friends_info != ("n"))):
	ask_for_friends_info = input("Создать файл с ID всех друзей и найти самый популярный город среди них? y/n: ")
ask_for_geo_metki =	None
while ((ask_for_geo_metki != str("y")) and (ask_for_geo_metki != ("n"))):
	ask_for_geo_metki = str(input("Искать геометки на фото? y/n: " ))
ask_for_get_comments = None
while ((ask_for_get_comments != str("y")) and (ask_for_get_comments != ("n"))):
	ask_for_get_comments = str(input("Найти человека, оставившего большинство комментариев? y/n: "))
if (ask_for_friends_info == "y"):
	GetFriendsInfo(CURRENT_ID)
if (ask_for_geo_metki == "y"):
	SearchOfLocationOnPhotos(CURRENT_ID)
if (ask_for_get_comments == "y"):
	GetCommentsOnProfile(CURRENT_ID)
print("Done!")