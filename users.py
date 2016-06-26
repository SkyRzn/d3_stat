#!/usr/bin/python


import lxml.html as html
import time, json, urllib2, urllib


def load_karma(root_id):
	url = 'https://dirty.ru/ajax/user/karma/list/'
	values = { 'user': root_id,'limit': 10000, 'offset':0}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data=data)
	response = urllib2.urlopen(req)
	data = response.read()
	data = json.loads(data)
	cons = data.get('cons') or []
	pros = data.get('pros') or []

	if data['status'] == 'ERR':
		print 'ERR', root_id
		return {'invalid': True}, {}

	res = { 'pros_count': int(data.get('pros_count', 0)),
			'cons_count': int(data.get('cons_count', 0)),
			'karma': int(data['karma']),
			'pros': {},
			'cons': {}}
	children = {}
	for it in pros:
		vote = int(it['vote'])
		user = it['user']
		username = user['login']
		uid = int(user['id'])
		res['pros'][uid] = vote
		children[uid] = username
	for it in cons:
		vote = int(it['vote'])
		user = it['user']
		username = user['login']
		uid = int(user['id'])
		res['cons'][uid] = vote
		children[uid] = username
	return res, children


def load_users():
	try:
		f = open('users.json', 'r')
	except:
		return {}
	data = json.load(f)
	f.close()

	users = {}
	for k, v in data.items():
		users[int(k)] = v
	return users

def save_users(users):
	f = open('users.json', 'w')
	json.dump(users, f)
	f.close()

def load_userdata(id, name, users):
	root, children = load_karma(id)
	root['name'] = name

	f = open('users/%06d.json' % int(id), 'w')
	json.dump(root, f)
	f.close()

	new_user_cnt = 0
	for cid, cname in children.items():
		if cid not in users:
			users[cid] = cname
			new_user_cnt += 1
	print 'New users: %d' % new_user_cnt


def go():
	users = load_users()

	beg = len(users)
	print 'BEGIN USERS: %d' % beg

	#users['23295'] = 'ozpp'
	cnt = 0
	for uid, name in users.items():
		try:
			f = open('users/%06d.json' % int(uid), 'r')
			f.close()
		except:
			cnt += 1
			print '%d) %s' % (cnt, name)
			load_userdata(uid, name, users)

			time.sleep(0.1)
			if cnt > 1000:
				break

	end = len(users)
	print 'END USERS: %d' % end
	print 'BALANCE: %d' % (cnt - (end - beg))

	save_users(users)

if __name__ == "__main__":
	go()

