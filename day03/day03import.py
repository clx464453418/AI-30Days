import random


tasks = ["学习Python", "学习Prompt", "做一个AI小项目"]


def get_task():
   return random.choice(tasks)

print(get_task())