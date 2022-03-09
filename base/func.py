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

MAX_DAYS = 90 #program won't generate problems past this number of days in advance

def gen_problems(user, problems_limit: int) -> None:
    null_dates = Problem.objects.filter(user=user, next_solve__isnull=True)
    old_dates = Problem.objects.filter(user=user, next_solve__lt=date.today())
    problem_list = list(chain(null_dates,old_dates))
    for problem in problem_list:
        add_days = random.randint(RULES[problem.rating][0],RULES[problem.rating][1])
        problem.next_solve = date.today()+timedelta(days=add_days)
    Problem.objects.bulk_update(problem_list, ['next_solve'])

    move_problems = []
    changed_problems = []
    for i in range(MAX_DAYS):
        day = date.today()+timedelta(days=i)
        problems_today = Problem.objects.filter(user=user, next_solve=day)
        move_problems.extend(problems_today[problems_limit:]) #if there are more problems than allowed, append to list
        if move_problems and len(problems_today)<problems_limit:
            count = len(problems_today)
            while move_problems and count<problems_limit: #move problems to this day if there are available spots
                update = move_problems.pop()
                update.next_solve = day
                changed_problems.append(update)
                count+=1
    
    #get any remaining problems and set to null since there's no room in the next MAX_DAYS to add them
    for problem in move_problems:
        problem.next_solve = None
    changed_problems.extend(move_problems)
    Problem.objects.bulk_update(changed_problems, ['next_solve'])

def shift_problems(user): #by 1 day
    has_dates = Problem.objects.filter(user=user, next_solve__isnull=False)
    for problem in has_dates:
        problem.next_solve = problem.next_solve+timedelta(days=1)
    Problem.objects.bulk_update(has_dates, ['next_solve'])