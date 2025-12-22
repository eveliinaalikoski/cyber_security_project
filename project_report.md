# Project Report

LINK: https://github.com/eveliinaalikoski/cyber_security_project

FLAW 1:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L113

DESCRIPTION:
The flaw is type A01:2021 Broken Access Control and it demonstrates the 'CWE-200: Exposure of Sensitive Information to an Unauthorized Actor'. User's notes are listed in the front page and user can only see their own notes. In the flawed version, a user can access someone else's notes by guessing note ids and changing the URL by hand. There is no checks that one is the owner of the note, so anyone can access any note just by guessing an id number. The note page is loaded only based on the note id and the user is not authorized at any point.

FIX:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L117

This flaw is fixed by checking for ownership before user accessing the page. I did that by searching for notes with the given id number and current user as the owner from the database. Now if a user types someone else's note id in the URL, there is check whether the current user owns that note or not. Unauthorized access to somebody else's note will take the user to an error page. This way even though changing the URL, user can only access the note pages that really are theirs and otherwise will be redirected to an error page.


FLAW 2:
register: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L20

login: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L62

DESCRIPTION:
The flaw is type A02:2021 Cryptographic Failures and it is present in both registration and login. The flaw is storing passwords in database as raw text without hashing of any kind (this can be seen from screenshot flaw-2-before-3.png). In register the password is saved as plain text and in login the password is compared directly to the plain text password from the database. This enables an attacker (maybe an employee) with access to the database to see all the usernames and passwords as plain text, and can use the information to hack into anybody's account.

FIX:
register: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L30

login: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L77

A fix for this kind of flaw is protecting user passwords with some kind of hashing. In this case I used django's method create_user for model User objects in the registration, which hashes the password automatically and does not store raw passwords in the database (this can be seen from screenshot flaw-2-after-3.png). In login I used authenticate and login functions from 'django.contrib.auth', which compares the hashed passwords without comparing plain text passwords.


FLAW 3:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L134

DESCRIPTION:
The flaw is type A03:2021 Injection and it demonstrates the 'CWE-89: SQL-injection'. This occurs in searching the notes in the sql query, where the search input from the user is used as a part of the query without validating or sanitizing it. The flaw enables a user to see everyone's notes. This is possible if a user formats the input in a way that changes the structure of the query. If a user searches for example "' OR 1=1 --", the sql query interprets it as a part of the query so that the WHERE clause is always true (because 1=1 is always true) and the "--" makes it so the rest of the query is commented out. This way the application will list every note in the database regardless of the owner (this is demonstrated in the screenshots).

FIX:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L142

In the fix of the flaw, the search input is added to the query as parameters at execution. This ensures that the user input is interpreted as data in the query and not as a part of the query. With the fix, the application only returns the notes that contain the user input, but it will not interpret the input as part of the query. Even if a user tries to give "' OR 1=1 --" as search input, it will only show notes that actually contains the string "' OR 1=1 --" in the note (this can be seen from the screenshot flaw-3-after-2.png, where the search doesn't return anything since there is no note containing the string "' OR 1=1 --").


FLAW 4:
register: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L25

login: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L69 and #L74

DESCRIPTION:
The flaw is type A04:2021 Insecure Design and it demonstrates the 'CWE-209: Generation of Error Message Containing Sensitive information'. The vulnerability appears on registration and login pages where the error messages give too much information for the user. This falls into the insecure design category since registration and login has been designed to give spesific error messages. In registration and login the error message is generated directly from raised exceptions. In addition in login if the given username is an existing username, but the given password is wrong, error messages will reveal that is was incorrect password for user with the specific username. This enables an attacker to test wich usernames are registered in the app and then try to guess their passwords.

FIX:
register: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L37

login: https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L88

A fix for this flaw is replacing the error messages that reveal too much for the user. In this case I replaced them with generic 'Register unsuccessful, try again' and 'Login unsuccessful, try again'. In this case there is no need for the user to know more about what went wrong. Especially in the login, where only a username and a password is needed, it reveals too much for the user to tell the password wasn't right for the username. Generally it is good practise in login to not tell which username or password was incorrect. Otherwise, it will give an opportunity for an attacker to get hold of somebody's credentials more easily.


FLAW 5:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L62 (doesn't contain code per se, since the flaw is the lack of checks/tracking)

DESCRIPTION:
The flaw is type A07:2021 Identification and Authentication Failures and it demonstrates permitting automated and brute force attacks by not tracking or limiting login attempts. This enables an attacker to try numerous password and username combinations without any restrictions in login. 

Especially, in combination with too spesific error messages, automated attacks are made more possible. An attacker can first try common usernames until they find a username that is registered in the app. Then they can try numerous passwords for the username. 

FIX:
https://github.com/eveliinaalikoski/cyber_security_project/blob/main/cyber_project/notes/views.py#L52 and #L83 and #L87

The flaw can be fixed by keeping track of login attempts and then restricting more attempts after some tries. In this case I have implemented the attempt tracking with session. Every login try increases the counter that is stored in the user's session, and the attempts are limited to five tries. After the limit is reached the user gets error message that there has been too many login attempts. This fix prevents automated attacks since an attacker can only attempt guessing the credentials five times before getting restricted. The counter in session is reset after a successful login.
