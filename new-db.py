import sqlite3
import os


CREATE_POSTS = """
create table posts (
	post_id integer primary key autoincrement,
	title varchar(140) not null,
	is_link bool not null,
    --poster_id int not null, --TODO new for adding users
	body text not null,
	timestamp text default CURRENT_TIMESTAMP
    --foreign key (poster_id) references users(user_id), -- TODO foreign key for users
)
"""

CREATE_COMMENTS = """
create table comments (
	comment_id integer primary key autoincrement,
	post_id int not null,
	parent_id int not null,
    --poster_id int not null, --TODO new for adding users
	body text not null,
	timestamp text default CURRENT_TIMESTAMP,
	foreign key (post_id) references posts(post_id),
    --foreign key (poster_id) references users(user_id) --TODO foreign key for users
	foreign key (parent_id) references comments(comment_id)
)
"""

CREATE_USERS = """
create table users (
    user_id interger primary key autoincrement,
    username varchar(20) not null
)

"""

# create new db file
os.remove('_test.db')
conn = sqlite3.connect('_test.db')
cur = conn.cursor()

# run DDL queries
cur.execute(CREATE_POSTS)
conn.commit()
cur.execute(CREATE_COMMENTS)
conn.commit()

#cur.execute('insert into ')




cur.close()
conn.close()
