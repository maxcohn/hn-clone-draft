# hn-clone

#### THIS REPO IS A ROUGH DRAFT FOR A FUTURE PROJECT

This is a rough implementation of a [HackerNews](https://news.ycombinator.com)
clone.

Right now, this is a basic Flask application that can be run like any other
standard Flask application. There are no users, so everything is anonymous, similar
to 4chan. The main reason for this is because I just wanted to through together
a basic draft one night as an experiment for dealing with nested comments.

This is not an end result, I plan to flesh out this application with a more
efficient and type safe language like Rust, create easy deployment option using
Docker, and adding the ability to plugin in custom CSS files for easy customization.

In the end, I want this to be a simple self-hosted implementation of HackerNews
(essentially a single subreddit) that users can deploy themselves as a more modern
forum. Nested comments enhance readability of any thread, and I think I am spoiled
by them now, as apposed to the traditional linear forum. The reason for writing
in Rust would be to get optimal performance out of any given hardware, making it
cheaper to deploy, with a cheap VPS being fine for the majority of cases.

## Pretty lousy eh?

This is mostly an archival effort for myself so that when I get the time to flesh
this out in the previously mentioned finished version, I can base my SQL schema
and queries on this rough draft.

## Why are you using SQLite?

SQLite is awesome, especially for tossing something together quickly. Python has
SQLite built into the standard library, and this would make testing way faster.
Not to mention that
[SQLite is a fine database for small websites](https://www.sqlite.org/whentouse.html).

## Future plans for this project

* Rewrite in Rust
* Package as `Dockerfile`
* Add `docker-compose.yml` with PostgresDB for quick and easy deployment
* Add users
* Add custom CSS options