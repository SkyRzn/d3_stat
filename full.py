#!/usr/bin/python


import lxml.html as html
import time, json, urllib2, urllib
import glob
from users import load_users


def load_html(username):
	print 'LOAD HTML FOR %s' % username
	r = urllib2.urlopen('http://dirty.ru/user/%s/posts/' % username)
	page = r.read()

	f = open('html/%s.htm' % username, 'w')
	f.write(page)
	f.close()

def load_page(username):
	try:
		page = html.parse('html/%s.htm' % username)
	except:
		load_html(username)
		page = html.parse('html/%s.htm' % username)
	return page.getroot()

def children(page):
	div = page.find_class('b-invited_users')

	if not div:
		return []

	inv_users = div[0].find_class('c_user')
	res = []
	for u in inv_users:
		res.append(u.text.strip())
	return res

def groups(page):
	div = page.find_class('b_users_table_holder')
	grs = div[0].find_class('link')
	for gr in grs:
		name = gr.text.strip()
		weight = int(gr.attrib.get('data-weight', 0))
		print name, weight

def date_from(page):
	span = page.find_class('js-date js-date-regular')
	if len(span) != 1:
		print 'date error'
	span = span[0]

	stamp = int(span.attrib.get('data-epoch_date', 0))
	return time.localtime(stamp)

def work(username):
	page = load_page(username)
	childs = children(page)
	gr = groups(page)
	df = date_from(page)
	print df


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



#users = load_users()
work('Mitrophan')
#work('Jovan')
#ids = get_ids()
#for i, id in enumerate(ids):
	#user = load_user(id)
	#print i, len(user['cons'])
	#break



