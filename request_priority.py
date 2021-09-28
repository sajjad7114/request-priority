from random import random
import threading
import time


# environment variables
BASE = 100
SPEED = 10
#######################


def limited_f(work):
    r = random() * ord(work.job.title[0]) * 3
    print("from limited", r)
    if SPEED > 0:
        time.sleep(r/SPEED)
    return r


def scenario0(user):
    user.add_work(Work(jobs[1]))
    time.sleep(3/SPEED)
    user.add_work(Work(jobs[0]))
    time.sleep(40/SPEED)
    user.add_work(Work(jobs[1]))


def scenario1(user):
    time.sleep(4/SPEED)
    user.add_work(Work(jobs[2]))
    time.sleep(5/SPEED)
    user.add_work(Work(jobs[0]))
    time.sleep(30/SPEED)
    user.add_work(Work(jobs[2]))


def scenario2(user):
    time.sleep(2/SPEED)
    user.add_work(Work(jobs[1]))
    time.sleep(10/SPEED)
    user.add_work(Work(jobs[2]))
    time.sleep(20/SPEED)
    user.add_work(Work(jobs[1]))


def assign():
    while True:
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

    def done(self, time):
        self.count_done += 1
        self.total_time += time

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

    def work_done(self, time):
        work = self.queue[0]
        del self.queue[0]
        self.done.append(work)
        work.job.done(time)
        if len(self.queue) == 0:
            self.first_pending_work = -1
        else:
            self.first_pending_work = self.queue[0].rank


if __name__ == "__main__":
    number_of_works = 0
    number_of_users = 0
    jobs = [Job("x"), Job("y"), Job("z")]
    users = [User("sajjad", 3), User("asghar", 2), User("akbar", 1)]

    threads = [threading.Thread(target=scenario0, args=(users[0],)),
               threading.Thread(target=scenario1, args=(users[1],)),
               threading.Thread(target=scenario2, args=(users[2],)),
               threading.Thread(target=assign)]
    for thread in threads:
        thread.start()
