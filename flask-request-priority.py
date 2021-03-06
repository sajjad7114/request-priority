from flask import Flask, render_template, request, redirect, url_for
from random import random, randint
import threading
import time


# environment variables
BASE = 100
SPEED = 10
#######################

app = Flask(__name__)


def limited_f(work):
    global current_work
    current_work = work.rank
    r = random() * ord(work.job.title[0]) * 3
    print("from limited", r)
    if SPEED > 0:
        time.sleep(r/SPEED)
    return r


def assign():
    while True:
        if number_of_done_works < number_of_works:
            dic = dict()
            for user in users:
                if user.first_pending_work != -1:
                    user.credit += user.weight * BASE
                    dic[user.first_pending_work] = user
            lis = [dic[i] for i in sorted(dic)]
            if len(lis):
                print([(user.name, user.queue[0].job.title) for user in lis])
            for user in lis:
                if user.credit >= user.queue[0].job.average_time():
                    print(user.queue[0].job.title + " is getting done for " + user.name)
                    t = limited_f(user.queue[0])
                    print(t, "seconds passed")
                    print()
                    user.work_done(t)


class Job:
    def __init__(self, title):
        self.title = title
        self.total_time = 0
        self.count_done = 0

    def done(self, t):
        self.count_done += 1
        self.total_time += t

    def average_time(self):
        if self.count_done == 0:
            return 0
        return self.total_time / self.count_done


class Work:
    def __init__(self, job):
        global number_of_works
        self.rank = number_of_works
        number_of_works += 1
        self.job = job
        self.result = -1
        self.duration = -1

    def done(self, t, res):
        global number_of_done_works
        number_of_done_works += 1
        self.result = res
        self.duration = t
        self.job.done(t)


class User:
    def __init__(self, name, weight):
        global number_of_users
        self.id = number_of_users
        number_of_users += 1
        self.name = name
        self.weight = weight
        self.credit = 0
        self.queue = list()
        self.done = list()
        self.first_pending_work = -1

    def add_work(self, work):
        self.queue.append(work)
        if self.first_pending_work == -1:
            self.first_pending_work = work.rank

    def work_done(self, t):
        work = self.queue[0]
        del self.queue[0]
        self.done.append(work)
        work.done(t, int(t))
        self.credit -= t
        if len(self.queue) == 0:
            self.first_pending_work = -1
        else:
            self.first_pending_work = self.queue[0].rank


@app.route("/")
def home():
    return render_template("index.html", users=users)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_name = request.form["nm"]
        usr = User(user_name, randint(1, 10))
        users.append(usr)
        return redirect(url_for("user_page", Id=usr.id))
    else:
        return render_template("register.html")


@app.route("/users/<Id>", methods=["POST", "GET"])
def user_page(Id):
    usr = None
    for user in users:
        if user.id == int(Id):
            usr = user
    if usr:
        if request.method == "POST":
            job_title = request.form["job_title"]
            job = [job for job in jobs if job.title == job_title][0]
            usr.add_work(Work(job))
        return render_template("user.html", user=usr, jobs=jobs, current=current_work)

    return redirect(url_for("home"))


@app.route("/works/<uid>/<rank>")
def works(uid, rank):
    try:
        user = [user for user in users if user.id == int(uid)][0]
        work = [work for work in user.done if work.rank == int(rank)][0]
        if work:
            return render_template("work.html", work=work, uname=user.name)
        return f"""<h1>Not Found</h1>
                <p>The {user.name} is not own {work.job.title} work with rank {rank} or it has not finished yet</p>"""
    except:
        return f"""<h1>Not Found</h1>
                <p>A user with id {uid} or a work with rank {rank} is not own found</p>"""


if __name__ == "__main__":
    number_of_works = 0
    number_of_done_works = 0
    number_of_users = 0
    current_work = -1
    jobs = [Job("x"), Job("y"), Job("z")]
    users = list()
    thread = threading.Thread(target=assign)
    thread.start()
    app.run(debug=True)
