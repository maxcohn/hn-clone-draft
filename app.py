from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import sys
import logging


app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
	conn = sqlite3.connect('_test.db')
	posts = None
	with conn:
		cur = conn.cursor()
		cur.execute('select post_id, title, is_link, body from posts order by timestamp asc')

		posts = list(map(lambda x: {'post_id': x[0], 'title': x[1], 'is_link': x[2], 'body': x[3]} , cur.fetchall()))
		cur.close()

	return render_template('index.html', posts=posts)


@app.route('/comments')
def comments():
	post_id = request.args.get('pid')

	conn = sqlite3.connect('_test.db')
	comments = None
	with conn:
		cur = conn.cursor()
		# query all comments associated with the post and order by their parent IDs
		# this ensures that there are no comments deeper in the thread appearing
		# later in the query results, allowing us to build the tree in a single loop
		
		#TODO build flattened tree structure, ordered by parent id's
		#https://stackoverflow.com/questions/32022273/render-threaded-comment-tree-in-jinja-template
		#TODO or use recursive loop
		#https://jinja.palletsprojects.com/en/2.10.x/templates/#for
		#TODO or use a macro
		#https://jinja.palletsprojects.com/en/2.10.x/templates/#macros
		
		# for getting an entire thread, we don't need to call an expensive recurisve
		# call. We can get away with just querying every comment with a given post_id
		cur.execute('select comment_id, parent_id, body, timestamp from comments where post_id=? order by parent_id asc', (post_id,))
		
		# create tree about thread
		comments = {0: {'body':'', 'children':[]}} # comment id -> parent id
		PARENT_ID = 1
		COMMENT_ID = 0
		BODY = 2
		for c in cur.fetchall():
			if c[PARENT_ID] in comments:
				comments[c[PARENT_ID]]['children'].append(c[COMMENT_ID])
				comments[c[COMMENT_ID]] = {'body': c[BODY], 'children': []}

		cur.close()
	#print(comments, file=sys.stderr, flush=True)
	traverse(comments)
	
	return render_template('comments.html', comments=comments, pid=post_id)

def traverse(comments, cur_node=0, depth=0):
	if cur_node != 0:
		print('--'*depth, end='', file=sys.stderr)
		print(cur_node, file=sys.stderr, flush=True)
	for n in comments[cur_node]['children']:
		traverse(comments, n, depth + 1)

@app.route('/newcomment', methods=['POST'])
def new_comment():
	post_id = request.json['post_id'] # parses json if set as content-type in request headers
	parent_id = request.json['parent_id']
	body = request.json['body']
	
	conn = sqlite3.connect('_test.db')
	with conn:
		cur = conn.cursor()
		cur.execute('insert into comments (body, post_id, parent_id) values (?, ?, ?)', (body, post_id, parent_id))
		cur.close()

	return redirect(f'/comments?pid={post_id}')

@app.route('/newpost', methods=['POST'])
def new_post():
	title = request.json['title']
	is_link = request.json['is_link']
	body = request.json['body']

	print(f'{title}, {is_link}, {body}', file=sys.stderr)

	if len(title) > 140:
		return 'bad' #TODO make this not awful

	conn = sqlite3.connect('_test.db')
	with conn:
		cur = conn.cursor()
		cur.execute('insert into posts (title, is_link, body) values (?, ?, ?)', (title, is_link, body))
		cur.close()

	return redirect('/')