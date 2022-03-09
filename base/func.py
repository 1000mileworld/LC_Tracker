from xmlrpc.client import boolean
from .models import Problem
from itertools import chain
from datetime import date, timedelta
import random

#"rating": (min days until redo, max days)
RULES = {
    '1': (60, 90),
    '2': (30, 50),
    '3': (14, 28),
    '4': (7, 14),
    '5': (1, 5)
}
def gen_problems(num: int, overwrite: boolean) -> None:
    null_dates = Problem.objects.filter(next_solve__isnull=True)
    old_dates = Problem.objects.filter(next_solve__lt=date.today())
    problem_list = list(chain(null_dates,old_dates))
    for problem in problem_list:
        add_days = random.randint(RULES[problem.rating][0],RULES[problem.rating][1])
        problem.next_solve = date.today()+timedelta(days=add_days)
    Problem.objects.bulk_update(problem_list, ['next_solve'])

    #make sure number of problems within limit per day