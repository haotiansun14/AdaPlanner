basic_info = '''
# You are a household agent. Here is some Python code defining a household environment:

# Use literal_eval to convert the answer from ask() to a list.
from ast import literal_eval

# In the environment, you can ask questions to an assistant by ask():
from large_language_model import ask_gpt as ask
# for example: You have a list of receptacles, and you want to sort them by the likelihood of a soapbar appearing in them. You can do this by asking the assistant:
receptacles = ['countertop 1', 'garbagecan 1', 'sinkbasin 2', 'sinkbasin 1', 'toilet 1', 'toiletpaperhanger 1', 'towelholder 1']
answer = ask(f'Sort the list of receptacles, starting from the one a soapbar is most likely to appear: {receptacles}. You should return a Python list.')
# answer = ['sinkbasin 1', 'sinkbasin 2', 'countertop 1', 'towelholder 1', 'toiletpaperhanger 1', 'garbagecan 1', 'toilet 1']

# Agent class represents the state of the agent, including its location,
# what it's holding as well as the actions it can take.
class Agent:
    def __init__(self, receptacles):
        self.location = None
        self.holding = None
        self.receptacles = receptacles

    # Here are the admissible actions the agent can take:
    
    # Go to a receptacle and update the agent's location. 
    # For example, 'On the countertop 1, you see a candle 1, a cloth 2, and a soapbar 1.' = goto('countertop 1')
    # For example, 'On the sidetable 2, you see nothing.' = goto('sidetable 2')
    def goto(self, receptacle):
        ...

    # Take an object from a receptacle if the agent is not holding anything. 
    # For example, 'You pick up the soapbar 1 from the towelholder 1.' = take('soapbar 1', 'towelholder 1')
    def take(self, object, receptacle):
        ...
        
    # Put an object in or on a receptacle if the agent is holding it. 
    # For example, 'You put the soapbar 1 in/on the cabinet 1.' = put('soapbar 1', 'cabinet 1')
    def put(self, object, receptacle):
        ...

    # Open a receptacle and observe its contents. 
    # For example, 'You open the cabinet 1. The cabinet 1 is open. In it, you see a cloth 1.' = open_receptacle('cabinet 1')
    def open_receptacle(self, receptacle):
        ...

    # Clean an object with a receptacle. 
    # For example, 'You clean the soapbar 1 using the sinkbasin 1.' = clean('soapbar 1', 'sinkbasin 1')
    def clean(self, object, receptacle):
        ...

    # Heat an object with a receptacle. 
    # For example, 'You heat the tomato 1 using the microwave 1.' = heat('tomato 1', 'microwave 1')
    def heat(self, object, receptacle):
        ...

    # Cool an object with a receptacle. 
    # For example, 'You cool the pan 2 using the fridge 1.' = cool('pan 2', 'fridge 1')
    def cool(self, object, receptacle):
        ...

    # Turn on an object. 
    # For example, 'You turn on the desklamp 1.' = turn_on('desklamp 1')
    def turn_on(self, object):
        ...

    # Report agent's current state, including its location, what it's holding, and last action and observation.
    # This function should only be used in assertion.
    def report(self):
        ...
'''.strip()

get_solution_prompt = f'''
{basic_info}
    
# Now complete the function solution() below to solve the task by composing the agent's methods to interact with the environment. 
# For each step you plan to take, 1) mark with '[Step xx]', 2) give a reason why you think it is a good step to take 3) write an assertion to check if the step is successful.

# Here is an example of a solution to the task:

<example>

# Here is the actual task.
# define environment and agent
receptacles = <receptacle_list>
agent = Agent(receptacles)

# <task>
# You should complete your solution function below:
def solution(agent, start_from=1):
'''.strip()

simple_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: put soapbar on countertop.
# here is a solution:
def solution(agent, start_from=1):
    # General Plan: I need to get a list of receptacles where the soapbar is likely to appear, and then go to each receptacle in the list until seeing a soapbar. Then I can put get the identifier of the soapbar and take it. Finally I can go to the countertop and put the soapbar.
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where the soapbar is likely to appear")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a soapbar in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a soapbar")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a soapbar is in/on the receptacle.
            if 'soapbar' in observation:
                break
        # expectation: I should be able to find a receptacle where a soapbar is in/on it.
        assert 'soapbar' in observation, f'Error in [Step 2]: There is no soapbar in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] identify the soapbar I juts found and take it")
        # I need to get the identifier of the soapbar. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the soap? Only Output a single number without any other words. ')
        found_soapbar = f'soapbar {answer}'
        observation = agent.take(found_soapbar, receptacle)
        # expectation: I should be able to take the soapbar from the receptacle.
        assert agent.holding == found_soapbar, f'Error in [Step 3]: I cannot take {found_soapbar} from the {receptacle}. {agent.report()}'

    if start_from <= 4:
        print("[Step 4] go to a countertop and put the soapbar on it")
        # There are multiple countertops, and I only need to go to one of them.
        observation = agent.goto('countertop 1')
        # check if the countertop is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('countertop 1')
        observation = agent.put(found_soapbar, 'countertop 1')
        # expectation: I should be able to put the soapbar on the countertop.
        assert f'You put the {found_soapbar} in/on the countertop 1.' in observation, f'Error in [Step 4]: I cannot put the {found_soapbar} on the countertop 1. {agent.report()}'
'''.strip()

clean_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: put a clean lettuce in diningtable / clean a lettuce and put it in diningtable.
# here is a solution:
def solution(agent, start_from=1):
    # General plan: I need to get a list of receptacles to find the lettuce, take the lettuce to the sinkbasin, clean it and put it in a diningtable.
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where the lettuce is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a lettuce in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a lettuce")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a lettuce is in/on the receptacle.
            if 'lettuce' in observation:
                break
        # expectation: I should be able to find a receptacle where a lettuce is in/on it.
        assert 'lettuce' in observation, f'Error in [Step 2]: There is no lettuce in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] identify the lettuce I juts found and take it")
        # I need to get the identifier of the lettuce. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the lettuce? Only Output a single number without any other words. ')
        found_lettuce = f'lettuce {answer}'
        observation = agent.take(found_lettuce, receptacle)
        # expectation: I should be able to take the lettuce from the receptacle.
        assert agent.holding == found_lettuce, f'Error in [Step 3]: I cannot take {found_lettuce} from the {receptacle}. {agent.report()}'
    
    if start_from <= 4:
        print("[Step 4] go to a sinkbasin to clean the lettuce. ")
        # I should go to the sinkbasin first if I want to clean the lettuce.
        observation = agent.goto('sinkbasin 1')
        # check if the sinkbasin is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('sinkbasin 1')
        observation = agent.clean(found_lettuce, 'sinkbasin 1')
        # expectation: I should be able to clean the lettuce.
        assert f'You clean the {found_lettuce} using the sinkbasin 1.' in observation, f'Error in [Step 4]: I cannot clean the {found_lettuce} using the sinkbasin 1. {agent.report()} I should have been at sinkbasin 1 and holding {found_lettuce}.'
    
    if start_from <= 5:
        print("[Step 5] go to a diningtable and put the lettuce on it. ")
        # There are multiple diningtables, and I only need to go to one of them.
        observation = agent.goto('diningtable 1')
        # check if the diningtable is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('diningtable 1')
        observation = agent.put(found_lettuce, 'diningtable 1')
        # expectation: I should be able to put the lettuce on the diningtable.
        assert f'You put the {found_lettuce} in/on the diningtable 1.' in observation, f'Error in [Step 5]: I cannot put the {found_lettuce} on the diningtable 1. {agent.report()}'
'''.strip()

heat_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: put a hot lettuce in diningtable / heat some lettuce and put it in diningtable.
# here is a solution:
def solution(agent, start_from=1):
    # General plan: I need to get a list of receptacles to find the lettuce, take the lettuce to the microwave, heat it and put it in a diningtable.
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where the lettuce is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a lettuce in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a lettuce")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a lettuce is in/on the receptacle.
            if 'lettuce' in observation:
                break
        # expectation: I should be able to find a receptacle where a lettuce is in/on it.
        assert 'lettuce' in observation, f'Error in [Step 2]: There is no lettuce in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] identify the lettuce I juts found and take it")
        # I need to get the identifier of the lettuce. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the lettuce? Only Output a single number without any other words. ')
        found_lettuce = f'lettuce {answer}'
        observation = agent.take(found_lettuce, receptacle)
        # expectation: I should be able to take the lettuce from the receptacle.
        assert agent.holding == found_lettuce, f'Error in [Step 3]: I cannot take {found_lettuce} from the {receptacle}. {agent.report()}'
    
    if start_from <= 4:
        print("[Step 4] go to a microwave to heat the lettuce")
        # I should go to a microwave to heat the lettuce.
        observation = agent.goto('microwave 1')
        # check if the microwave is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('microwave 1')
        observation = agent.heat(found_lettuce, 'microwave 1')
        # expectation: I should be able to heat the lettuce.
        assert f'You heat the {found_lettuce} using the microwave 1.' in observation, f'Error in [Step 4]: I cannot heat the {found_lettuce} using the microwave 1. {agent.report()} I should have been at microwave 1 and holding {found_lettuce}. '
    
    if start_from <= 5:
        print("[Step 5] go to a diningtable and put the lettuce on it")
        # There are multiple diningtables, and I only need to go to one of them.
        observation = agent.goto('diningtable 1')
        # check if the diningtable is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('diningtable 1')
        observation = agent.put(found_lettuce, 'diningtable 1')
        # expectation: I should be able to put the lettuce on the diningtable.
        assert f'You put the {found_lettuce} in/on the diningtable 1.' in observation, f'Error in [Step 5]: I cannot put the {found_lettuce} on the diningtable 1. {agent.report()}'
'''.strip()

cool_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: put a cold lettuce in diningtable / cool some lettuce and put it in diningtable.
# here is a solution:
def solution(agent, start_from=1):
    # General plan: I need to get a list of receptacles to find the lettuce, take the lettuce to the fridge, cool it and put it in a diningtable.
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where the lettuce is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a lettuce in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a lettuce")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a lettuce is in/on the receptacle.
            if 'lettuce' in observation:
                break
        # expectation: I should be able to find a receptacle where a lettuce is in/on it.
        assert 'lettuce' in observation, f'Error in [Step 2]: There is no lettuce in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] identify the lettuce I juts found and take it")
        # I need to get the identifier of the lettuce. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the lettuce? Only Output a single number without any other words. ')
        found_lettuce = f'lettuce {answer}'
        observation = agent.take(found_lettuce, receptacle)
        # expectation: I should be able to take the lettuce from the receptacle.
        assert agent.holding == found_lettuce, f'Error in [Step 3]: I cannot take {found_lettuce} from the {receptacle}. {agent.report()}'
    
    if start_from <= 4:
        print("[Step 4] go to a fridge to cool the lettuce")
        # I should go to a fridge to cool the lettuce.
        observation = agent.goto('fridge 1')
        # check if the fridge is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('fridge 1')
        observation = agent.cool(found_lettuce, 'fridge 1')
        # expectation: I should be able to cool the lettuce.
        assert f'You cool the {found_lettuce} using the fridge 1.' in observation, f'Error in [Step 4]: I cannot cool the {found_lettuce} using the fridge 1. {agent.report()} I should have been at fridge 1 and holding {found_lettuce}.'
    
    if start_from <= 5:
        print("[Step 5] go to a diningtable and put the lettuce on it")
        # There are multiple diningtables, and I only need to go to one of them.
        observation = agent.goto('diningtable 1')
        # check if the diningtable is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('diningtable 1')
        observation = agent.put(found_lettuce, 'diningtable 1')
        # expectation: I should be able to put the lettuce on the diningtable.
        assert f'You put the {found_lettuce} in/on the diningtable 1.' in observation, f'Error in [Step 5]: I cannot put the {found_lettuce} on the diningtable 1. {agent.report()}'
'''.strip()

puttwo_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: put two cellphone in cabinet / find two cellphone and put them in cabinet
# here is a solution:
def solution(agent, start_from=1):
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where a cellphone is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a cellphone in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # remove the destination from the list
        recep_to_check.remove('cabinet 1')
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'
        
    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a cellphone")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a cellphone is in/on the receptacle.
            if 'cellphone' in observation:
                break
        # expectation: I should be able to find a receptacle where a cellphone is in/on it.
        assert 'cellphone' in observation, f'Error in [Step 2]: There is no cellphone in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] identify the first cellphone found and take it")
        # I need to get the identifier of the cellphone. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation}. The identifier of the cellphone? Only Output a single number without any other words. ')
        found_cellphone1 = f'cellphone {answer}'
        observation = agent.take(found_cellphone1, receptacle)
        # expectation: I should be able to take the cellphone from the receptacle.
        assert agent.holding == found_cellphone1, f'Error in [Step 3]: I cannot take {found_cellphone1} from the {receptacle}. {agent.report()}'
   
    if start_from <= 4:
        print("[Step 4] go to a cabinet and put the first cellphone found on it. ")
        # There are multiple countertops, and I only need to go to one of them.
        observation = agent.goto('cabinet 1')
        # check if the cabinet is closed. If so, open it.
        if 'closed' in observation:
            observation = agent.open_receptacle('cabinet 1')
        observation = agent.put(found_cellphone1, 'cabinet 1')
        # expectation: I should be able to put the cellphone1 on the countertop.
        assert f'You put the {found_cellphone1} in/on the cabinet 1.' in observation, f'Error in [Step 4]: I cannot put the {found_cellphone1} on the cabinet 1. {agent.report()}'

    if start_from <= 5:
        print("[Step 5] go to each of the remaining receptacle in the list until seeing a second cellphone")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a cellphone is in/on the receptacle.
            if 'cellphone' in observation:
                break
        # expectation: I should be able to find a receptacle where a cellphone is in/on it.
        assert 'cellphone' in observation, f'Error in [Step 5]: There is no second cellphone in/on {recep_to_check}. {agent.report()}'

    if start_from <= 6:
        print("[Step 6] identify the second cellphone I just found and take it")
        # I need to get the identifier of the cellphone. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation}. The identifier of the cellphone? Only Output a single number without any other words. ')
        found_cellphone2 = f'cellphone {answer}'
        observation = agent.take(found_cellphone2, receptacle)
        # expectation: I should be able to take the cellphone from the receptacle.
        assert agent.holding == found_cellphone2, f'Error in [Step 6]: I cannot take {found_cellphone2} from the {receptacle}. {agent.report()}'
   
    if start_from <= 7:
        print("[Step 7] go to a cabinet and put the second cellphone found on it")
        observation = agent.goto('cabinet 1')
        observation = agent.put(found_cellphone2, 'cabinet 1')
        # expectation: I should be able to put the cellphone2 on the countertop.
        assert f'You put the {found_cellphone2} in/on the cabinet 1.' in observation, f'Error in [Step 7]: I cannot put the {found_cellphone2} on the cabinet 1. {agent.report()}'
'''.strip()

examine_example = '''
# define environment and agent
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)

# Your task is to: look at the bowl under the desklamp / examine the bowl with the desklamp
# here is a solution:
def solution(agent, start_from=1):
    # General plan: I need to get a list of receptacles to find the bowl and take the bowl with me, then I get another list of receptacles to find the desklamp and turn it on.
    if start_from <= 1:
        print("[Step 1] get a list of receptacles where a bowl is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a bowl in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 1]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 2:
        print("[Step 2] go to each receptacle in the list until seeing a bowl")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a bowl is in/on the receptacle.
            if 'bowl' in observation:
                break
        # expectation: I should be able to find a receptacle where a bowl is in/on it.
        assert 'bowl' in observation, f'Error in [Step 2]: There is no bowl in/on {recep_to_check}. {agent.report()}'

    if start_from <= 3:
        print("[Step 3] take the bowl from the receptacle")
        # I need to get the identifier of the bowl so that I can take it. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the pen? Only Output a single number without any other words. ')
        found_bowl = f'bowl {answer}'
        observation = agent.take(found_bowl, receptacle)
        # expectation: I should be able to take the bowl from the receptacle.
        assert agent.holding == found_bowl, f'Error in [Step 3]: I cannot take {found_bowl} from the {receptacle}. {agent.report()}'

    if start_from <= 4:
        print("[Step 4] get a list of receptacles where a desklamp is likely to appear.")
        # I can ask the assistant to do that.
        answer = ask(f'Given a list of receptacles, please sort them in descending order based on the likelihood of finding a desklamp in each of them. The list of receptacles is: {agent.receptacles}. You should directly return a Python list.')
        recep_to_check = literal_eval(answer)
        # expectation: the returned recep_to_check should not be empty.
        assert recep_to_check, f'Error in [Step 4]: recep_to_check should not be empty. {agent.report()}'

    if start_from <= 5:
        print("[Step 5] go to each receptacle in the list until seeing a desklamp")
        for receptacle in recep_to_check:
            observation = agent.goto(receptacle)
            # check if the receptacle is closed. If so, open it.
            if 'closed' in observation:
                observation = agent.open_receptacle(receptacle)
            # check if a desklamp is in/on the receptacle.
            if 'desklamp' in observation:
                break
        # expectation: I should be able to find a receptacle where a desklamp is in/on it.
        assert 'desklamp' in observation, f'Error in [Step 5]: There is no desklamp in/on {recep_to_check}. {agent.report()}'

    if start_from <= 6:
        print("[Step 6] turn on desklamp")
        # There might be multiple desklamps in the environment, and I need to get the identifier of the desklamp. I can ask the assistant to do that.
        answer = ask(f'From the observation, get the identifier of an object. For example, On the cabinet 1, you see a cloth 2, and a toiletpaper 2. The identifier of cloth is 2. Now, {observation} The identifier of the desklamp? Only Output a single number without any other words.')
        found_desklamp = f'desklamp {answer}'
        # I can directly turn on the desklamp that I just found.
        observation = agent.turn_on(found_desklamp)
        # expectation: the desklamp should be turned on now.
        assert 'turn on' in observation, f'Error in [Step 6]: I cannot turn on {found_desklamp} in/on {receptacle}. {agent.report()}'
'''.strip()

code_check_prompt = '''
You are given a Python code snippet define a function called solution. 

[Code]
<solution_func>

Question 1: Are there any syntax error present in the code? Answer Yes/No.
Question 2: Fix the syntax errors and output an error-free version of the code. Only Output the revised code after [Revised code] without any other words.
'''.strip()

feedback_fix_prompt = f'''
{basic_info}

# Here is a example of successful solution for solving a similar task:
[Successful example]
receptacles = ['diningtable 1','drawer 2', 'drawer 1', 'sinkbasin 1', 'toilet 1', 'sidetable 2', 'sidetable 1', 'cabinet 1', 'countertop 1', 'microwave 1', 'fridge 1']
agent = Agent(receptacles)
<example>

# Here is the actual task.
# define environment and agent
receptacles = <receptacle_list>
agent = Agent(receptacles)

# <task>
You have generated code of solution() to solve the task. However, you executed the solution() function and get an error message:
<error_msg>

Let's think step by step. Referring to the successful case and the error message, you should complete the solution function with the correct code.
def solution(agent, start_from=1):
'''.strip()

get_start_from_prompt = f'''
Previously, you generated some code defining a solution function as in [Previous solution]. The previous code is executed and outputs some error. Now you just revised the code as in [Revised solution]. Determine from which step these two version differs. You should only output the step number without saying any other words.

[Previous solution]
<previous_solution>

[Revised solution]
<revised_solution>
'''.strip()

