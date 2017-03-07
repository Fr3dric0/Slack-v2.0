# Slack v2.0
Slack v2.0 aims to provide slack features in a Command Line Interface (_CLI_), and through local/personal servers.

Our first aim is to provide what one can consider the bare minimum of a chatting application, login with a username, and one common chatting group. When this is completed we move on to adding features like database storage, group chatting and authentication, described in the sections bellow.

## Structure

### 1. Server
We will firstly aim to implement the minimum requirements, but structure the implementation to better support additional features.

#### Requests

- `login <username>` - Follows the requirements provided in the task. Initial plan is to map `username` and `ip`, for session storage
- `logout` - As required. Will pop the _user-object_ from the _active-users storage_
- `help` - Nothing more planed here
- `history` - Follows initial requirements. Store data as a `history.json` in the following format `List<Message>`, where `Message` firstly contains the fields `user` (_username_) and `message`. This implementation would easier let us scale and evolve.
- `msg <message>` - As Required.
- `names` - As required.

### 2. Client
Much like our server, the client handles the same requests, but nothing specially more. 
We will store our user, and print chat reasonable formatted (including errors). If time, we might implement simplified markdown support (bold, italics, and code (colored purple)).

#### Chat format

```
======================================
             Slack v2.0
======================================

--------------------------------------
 Server: R1c0 joined chat!
--------------------------------------

--------------------------------------
 R1c0: Yo!
--------------------------------------

--------------------------------------
 P3taH: Hey, sup?
--------------------------------------

--------------------------------------
 R1c0: Nothin, much
--------------------------------------

--------------------------------------
 P4m.4nD3rS: Hey guys, whats going on?
			 I've been lorem lipsum
			 dolor sit amed.
--------------------------------------

--------------------------------------
 Server: R1c0 left chat
--------------------------------------

```

### 3. Models
To ensure better scalability, we create models for `User`, `History` (chat log, List<Message>), `Message` and `ActiveUsers` (List<User>). These models will also be responsible for _finding_ and _storing_ data to each models. Details on the database is provided in section 4.

### 4. Datastorage
Our first plan is to take it simple by storing chat history in `history.json`, active users in `active_user.json` and so on. However, an unverified issue might be access collision when two or more _models_ tries to access the same file. Therefore, we will (if time) implement mongodb for data-handling.
This will ofcourse be modularized through our models, making the transition to `mongodb` abstract


## Plan Ahead
If we find out, we get enough time, we will aim to implement features such as Database storage (_most likely MongoDB_), group chatting, and eventually group-chat **athentication**.

- [ ] `login <username> <group_id?>` - Login to a specific group
- [ ] `group <group_id>` - Switch group
- [ ] `login <username> <group_id?> <group_pwd>` - Authentication to a group
