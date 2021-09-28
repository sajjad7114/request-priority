# request priority
request_priority.py is just a trial without using flask
# flask request priority
flask_request_priority.py is giving credit to users according to their weights. <br /><br />
Every user has a queue of works.
Every time a work finishes, we take the first works of every user's queue of works, then sorting them by the time they have submitted (their rank). Also, every user with work in their queue, gets some credit according to their weight.
Then we go through the sorted list and if the users have more credit than the average time of their first work in queue, their work will get proccessed.
When we get to the last of the list, we start the proccess of assigning works again. <br /><br />
You can register, go to evety user's page and add work for them. You can see the user's last proccessed work in green and you can click on them and see the result and duration of the proccessing. The result is simply the integer part of the duration time. Also, the user's pending works are shown in yellow and if one of them is under proccess, it will tell you.
## Run
You just need to install flask on your system by
```
python -m pip install flask
```
And then run the code!
