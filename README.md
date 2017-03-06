# Slack v2.0

## Setup

1. Server


2. Client


3. Models


4. Datastorage
Our first plan is to take it simple by storing chat history in `history.json`, active users in `active_user.json` and so on. However, an unverified issue might be access collision when two or more _models_ tries to access the same file. Therefore, we will (if time) implement mongodb for data-handling.
This will ofcourse be modularized through our models. Making the change from `.json` to `mongodb` abstract

5. Run client, bla bla bla


6. Done


## Plan
Our initial plan is to build the basic functionality of our chatting application (_login with username_, _chatting as one open group_, _etc._). However, given enough time, we plan to implement group-chatting through commands

- [ ] - `login <username> <group_id>`
- [ ] - `group <group_id>` (_assumes user is already authenticated_)

Given even more time, we might plan to implement **Authorization** of our groups, firstly through simple commands any _group-user_ can apply, and later might implement _admin-roles_ for specific users.
