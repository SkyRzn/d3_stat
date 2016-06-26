#!/usr/bin/python


import lxml.html as html
import time, json, urllib2, urllib
import glob
from users import load_users


def load_user(id):
	f = open('users/%06d.json' % id, 'r')
	user = json.load(f)
	f.close()
	return user

def save_user(id, user):
	f = open('users/%06d.json' % id, 'w')
	json.dump(user, f)
	f.close()

def get_ids():
	files = glob.glob('users/*.json')
	ids = []
	for fn in files:
		fn = fn.split('/')[1]
		fn = fn.split('.')[0]
		ids.append(int(fn))
	ids.sort()
	return ids


def prepare():
	usernames = load_users()

	ids = get_ids()
	users = {}
	for id in ids:
		user = load_user(id)
		users[id] = user

	res = set()
	i = 0
	for id, user in users.items():
		i += 1
		print i
		for pid in user.get('pros', []):
			pid = int(pid)
			puser = users.get(pid)
			#nms = [usernames.get(id), usernames.get(pid)]
			#if nms[0] and nms[1]:
				#res.add(tuple(nms))
			if puser:
				if unicode(id) in puser.get('pros', []):
					nms = [usernames[id], usernames[pid]]
					nms.sort()
					res.add(tuple(nms))
	res = list(res)
	return res

def save(obj):
	f = open('prom.json', 'w')
	json.dump(obj, f)
	f.close()

def load():
	f = open('prom.json', 'r')
	res = json.load(f)
	f.close()
	return res

def cloud(pairs, name):
	cld = set([name])
	i = 0
	for a, b in pairs:
		i += 1
		print i
		if name == a or name == b:
			cld.add(a)
			cld.add(b)
	return filter(lambda a: a[0] in cld and a[1] in cld, pairs)

#res = prepare()
#save(res)
res = load()

cnts = {}
res = cloud(res, 'pomorin')
#res = cloud(res, 'SkyRzn')

for a, b in res:
	cnt = cnts.get(a, 0)
	cnts[a] = cnt + 1
	cnt = cnts.get(b, 0)
	cnts[b] = cnt + 1

pr = []

for a, b in res:
	#if cnts[a] > 1 and cnts[b] > 1:
	pr.append('"%s" -- "%s";' % (a, b))


pr = '\n'.join(pr)


pr = 'graph G {\n%s\n}' % pr

f = open('test_pomor.dot', 'w')
f.write(pr.encode('utf8'))
f.close()
