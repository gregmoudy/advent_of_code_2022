# --- Day 21: Monkey Math ---
# The monkeys are back! You're worried they're going to try to steal your stuff again, 
# but it seems like they're just holding their ground and making various monkey noises at you.

# Eventually, one of the elephants realizes you don't speak monkey and comes over to interpret. 
# As it turns out, they overheard you talking about trying to find the grove; they can show you a shortcut if you answer their riddle.

# Each monkey is given a job: either to yell a specific number or to yell the result of a math operation. 
# All of the number-yelling monkeys know their number from the start; however, 
# the math operation monkeys need to wait for two other monkeys to yell a number, and those two other monkeys might also be waiting on other monkeys.

# Your job is to work out the number the monkey named root will yell before the monkeys figure it out themselves.

# For example:

# root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32
# Each line contains the name of a monkey, a colon, and then the job of that monkey:

# A lone number means the monkey's job is simply to yell that number.
# A job like aaaa + bbbb means the monkey waits for monkeys aaaa and bbbb to yell each of their numbers; 
# the monkey then yells the sum of those two numbers.
# aaaa - bbbb means the monkey yells aaaa's number minus bbbb's number.
# Job aaaa * bbbb will yell aaaa's number multiplied by bbbb's number.
# Job aaaa / bbbb will yell aaaa's number divided by bbbb's number.
# So, in the above example, monkey drzm has to wait for monkeys hmdt and zczc to yell their numbers. 
# Fortunately, both hmdt and zczc have jobs that involve simply yelling a single number, so they do this immediately: 32 and 2. 
# Monkey drzm can then yell its number by finding 32 minus 2: 30.

# Then, monkey sjmn has one of its numbers (30, from monkey drzm), and already has its other number, 5, from dbpl. 
# This allows it to yell its own number by finding 30 multiplied by 5: 150.

# This process continues until root yells a number: 152.

# However, your actual situation involves considerably more monkeys. What number will the monkey named root yell?

# --- Part Two ---
# Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

# First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. 
# The correct operation for monkey root should be =, which means that it still listens for two numbers 
# (from the same two monkeys as before), but now checks that the two numbers match.

# Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. 
# Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. 
# (The number that appears after humn: in your input is now irrelevant.)

# In the above example, the number you need to yell to pass root's equality test is 301. 
# (This causes root to get the same number, 150, from both of its monkeys.)

# What number do you yell to pass root's equality test?


import sympy
import timeit
import tqdm


MONKEYS = dict()
HUMN = sympy.symbols('humn')


class Monkey:
    def __init__(self, name, job):
        self.name = name
        self.job = job

        self._val = None
        job_split = job.split(' ')
        if len(job_split) == 1:
            self._val = int(job_split[0])


    def get_job_parts(self):
        job_parts = (None, None, None)
        job_split = self.job.split(' ')
        if len(job_split) == 3:
            job_parts = tuple(job_split)
        
        return job_parts


    def get_value(self, use_humn_symbol=False):
        if self.name == 'humn' and use_humn_symbol:
            return HUMN

        if self._val is None:
            job_split = self.job.split(' ')
            if len(job_split) == 3:
                job_monkey_name_1, job_operator, job_monkey_name_2 = job_split
                val1 = MONKEYS[job_monkey_name_1].get_value(use_humn_symbol=use_humn_symbol)
                val2 = MONKEYS[job_monkey_name_2].get_value(use_humn_symbol=use_humn_symbol)
                self._val = sympy.parsing.sympy_parser.parse_expr(f"({val1}){job_operator}({val2})")

        return self._val
        


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    global MONKEYS
    MONKEYS = dict()
    for line in lines:
        name, job = line.split( ': ')
        monkey = Monkey(name, job)
        MONKEYS[name] = monkey



def get_answer_1(input_file):
    read_input(input_file)
    answer = MONKEYS['root'].get_value()
    return answer



def get_answer_2(input_file):
    read_input(input_file)
    m1, _op, m2 = MONKEYS['root'].get_job_parts()
    val1 = MONKEYS[m1].get_value(use_humn_symbol=True)
    val2 = MONKEYS[m2].get_value(use_humn_symbol=True)
    answer = sympy.solve_linear(val1, val2)[1]
    return answer



def run():
    print('DAY 21')

    # Part 1 Answer
    answer_1_sample = get_answer_1('./day_21_input_sample.txt')
    print(f'Answer 1 Sample: {answer_1_sample}') # 152
    answer_1 = get_answer_1('./day_21_input.txt')
    print(f'What number will the monkey named root yell? : {answer_1}') # 121868120894282

    # Part 2 Answer
    answer_2_sample = get_answer_2('./day_21_input_sample.txt')
    print(f'Answer 2 Sample: {answer_2_sample}') # 301
    answer_2 = get_answer_2('./day_21_input.txt')
    print(f"What number do you yell to pass root's equality test? : {answer_2}") # 3582317956029



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
