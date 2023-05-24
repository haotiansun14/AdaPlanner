basic_info = '''
# Interact with the HTML webpage to finish the computer task. Here is some Python code defining a computer task environment:
<ask_action>
# Agent class represents current state of the HTML webpage and the actions it can take.
class Agent:
    def __init__(self, initial_state):
        self.current_state = initial_state

    # Here are the admissible actions the agent can take:
    # Action: type a string into the input box
    # this function returns the string of the HTML code after taking the action
    # e.g., new_html_state = agent.type("hello")
    def type(self, characters: str) -> str:
        ...

    # Action: press a key on the keyboard, the input can be one of the following:
    # enter, space, arrow_left, arrow_right, arrow_up, arrow_down, backspace
    # this function returns the string of the HTML code after taking the action
    # e.g., new_html_state = agent.press_key("enter")
    def press_key(self, key: str) -> str:
    	  ...

    # Action: click a <select> element in a list with an XPath
    # this function returns the string of the HTML code after taking the action
    # e.g., new_html_state = agent.click_option("//select[@id='cars']/option[1]")
    def click_option(self, xpath_of_option: str) -> str:
		    ...

    # Action: click an HTML element with its XPath
    # this function returns the string of the HTML code after taking the action
    # e.g., new_html_state = agent.click_xpath("//button[@id='button1']")
    def click_xpath(self, xpath_of_element: str) -> str:
		    ...

    # Action: move the mouse cursor on an HTML element with an XPath
    # this function returns the string of the HTML code after taking the action
    # e.g., new_html_state = agent.move_mouse_on("//button[@id='button1']")
    def move_mouse_on(self, xpath_of_element: str) -> str:
    	  ...
'''.strip()

get_solution_prompt_OL = f'''
{basic_info}

<example>

# Now complete the function solution() below to solve the task by composing the agent's methods to interact with the environment. 
# For each step you plan to take, 1) mark with '[Step xx]' and 2) write the code to take the step. Your code should not return any value.

# Here is the actual task.
# define environment and agent. The state is the list of HTML elements of the webpage.
initial_state = \'''
<initial_state>
\'''
agent = Agent(initial_state)

# Task: <task>
# You should complete your solution function below:
def solution(agent):
'''.strip()

get_solution_prompt_CL = f'''
{basic_info}

<example>

# Now complete the function solution() below to solve the task by composing the agent's methods to interact with the environment. 
# In the solution function, start with a commented "# General plan: ". For each step you plan to take, mark with '[Step xx]', and write an assertion to check if the step is successful.

# Here is the actual task.
# define environment and agent. The state is the list of HTML elements of the webpage.
initial_state = \'''
<initial_state>
\'''
agent = Agent(initial_state)

# Task: <task>
# Here is the solution:
def solution(agent, start_from=1):
'''.strip()

code_check_prompt = '''
You are given a Python code snippet define a function called solution. 

[Code]
<solution_func>

Question 1: Are there any syntax error present in the code? Answer Yes/No.
Question 2: Fix the syntax errors and output an error-free version of the code. Only Output the revised code after [Revised code] without any other words.
'''.strip()

skill_template = '''
# Here is an example of solution.
# Task: <task>
# Here is the solution:
<solution>
'''.strip()

ask_action = '''
# In the environment, you can ask questions to an assistant by ask():
from large_language_model import ask_gpt as ask
# for example: You want to solve a algebra problem x + 3 = 6. You can ask the assistant to directly solve it for you.
answer = ask('Solve an algebra problem. You should directly output the value of the unknown. For example, solve 'y + 1 = 2' -> 1. Now solve 'x + 3 = 6' ->')
# answer = '3'
'''

get_solution_prompt_OL_no_ask = get_solution_prompt_OL.replace('<ask_action>', '')
get_solution_prompt_OL_with_ask = get_solution_prompt_OL.replace('<ask_action>', ask_action)

get_solution_prompt_CL_no_ask = get_solution_prompt_CL.replace('<ask_action>', '')
get_solution_prompt_CL_with_ask = get_solution_prompt_CL.replace('<ask_action>', ask_action)

feedback_fix_prompt = f'''
{basic_info}

# Task: <task>
You have generated code of solution() to solve the task:
<solution_func>

However, you executed the solution() function and get an error message:
[Error message]
<feedback>

Let's think step by step. You must output the revised solution function based on the error message. You must only complete the revised solution function without any other words. 
# In the solution function, start with a commented "# General plan: ". For each step you plan to take, mark with '[Step xx]', and write an assertion to check if the step is successful.
def solution(agent, start_from=1):
'''.strip()

feedback_fix_prompt_no_ask = feedback_fix_prompt.replace('<ask_action>', '')
feedback_fix_prompt_with_ask = feedback_fix_prompt.replace('<ask_action>', ask_action)

get_start_from_prompt = f'''
Previously, you generated some code defining a solution function as in [Previous solution]. The previous code is executed and outputs some error. Now you just revised the code as in [Revised solution]. Determine from which step these two version differs. You should only output the step number without saying any other words.

[Previous solution]
<previous_solution>

[Revised solution]
<revised_solution>
'''.strip()


example_list = {
    'enter-date': 
'''
# Here is an example of solution.
# Task: Enter 08/20/2022 as the date and hit submit.
# Here is the solution:
def solution(agent):
# General plan: I should click the input box, then press the left_arrow twice to move the cursor to the beginning of the input box, finally type 08/20/2022 and click the submit button.
	print('[Step 1] click the input box of date')
	agent.click_xpath('//*[@id="tt"]')

	print('[Step 2] press the left_arrow twice to move the cursor to the beginning of the input box')
	for _ in range(2):
		agent.press('arrow_left')

	print('[Step 3] type 08/20/2022 in the input box')
	agent.type('08/20/2022')

	print('[Step 4] click the submit')
	agent.click_xpath('//*[@id="subbtn"]')
'''.strip(),
    'enter-time': 
'''
# Here is an example of solution.
# Task: Enter 5:20 PM as the time and press submit.
# Here is the solution:
def solution(agent):
# General plan: I should click the input box, then type the time and click the submit button.
    print('[Step 1] click the input box of date')
    agent.click_xpath('//*[@id="tt"]')

    print('[Step 2] format the time')
    # I must type 0520PM because the ':' and space will be automatically added by the webpage. Note that a zero is added before 5 to satisfy the format HHMMAM or HHMMPM.
    formatted_time = '0520PM'

    print('[Step 3] type the time in the input box')
    agent.type(formatted_time)

    print('[Step 4] click the submit')
    agent.click_xpath('//*[@id="subbtn"]')
'''.strip(),
    'click-menu':
'''
# Here is an example of solution.
# Task: Select Alice > Bob > Carol
# Here is the solution:
def solution(agent):
# General plan: I should move mouse to Alice to make the submenu show up, then I should move mouse to Bob make the submenu show up, finally I should click Carol.
	print('[Step 1] move mouse to Alice')
	agent.move_mouse_on('//*[text()="Alice"]')

	print('[Step 2] move mouse to Bob')
	agent.move_mouse_on('//*[text()="Bob"]')

	print('[Step 3] click Carol')
	agent.click_xpath('//*[@text()="Carol"]')
'''.strip(),
    'click-collapsible-2':
'''
# Here is an example of solution.
# Task: Expand the sections below, to find and click on the link "alice".
# Here is the solution:
def solution(agent):
# General plan: I should expand the section containing "alice", then I should click on "alice".
	print('[Step 1] expand the section containing "alice"')
    agent.click_xpath('//*[@id="ui-id-19"]')

    print(f'[Step 2] click on "alice" in the expanded section')
    agent.click_xpath('//span[@class='alink' and contains(text(), 'alice')])
'''.strip(),
    'grid-coordinate':
'''
# Here is an example of solution.
# Task: Click on the grid coordinate (-3,-2).
# Here is the solution:
def solution(agent):
# General plan: I should directly click the element at (-3,-2).
	print('[Step 1] click on the grid coordinate (-3,-2)')
    agent.click_xpath('//*[@id="(-3,-2)"]')
'''.strip(),
    'enter-text':
'''
# Here is an example of solution.
# Task: Enter "Ronda" into the text field and press Submit.
# Here is the solution:
def solution(agent):
# General plan: I should click the input box, then type "Ronda" and click the submit button.
    print('[Step 1] click the input box')
    agent.click_xpath("//input[@id='tt']")

    print('[Step 2] Type "Ronda" into the input box')
    agent.type("Ronda")

    print('[Step 3] Click the submit button')
    agent.click_xpath("//button[@id='subbtn']")
'''.strip(),
    'enter-text-dynamic':
'''
# Here is an example of solution.
# Task: Enter "DDDV3" into the text field and press Submit.
# Here is the solution:
def solution(agent):
# General plan: I should click the input box, then type "DDDV3" and click the submit button.
    print('[Step 1] click the input box')
    input_xpath = "//input[@id='tt']"
    agent.click_xpath(input_xpath)

    print('[Step 2] Type "DDDV3" into the input box')
    agent.type("DDDV3")

    print('[Step 3] Click the submit button')
    submit_button_xpath = "//button[@id='subbtn']"
    agent.click_xpath(submit_button_xpath)
'''.strip(),
    'use-spinner':
'''
# Here is an example of solution.
# Task: Select 7 with the spinner and hit Submit.
# Here is the solution:
def solution(agent):
# General plan: Since 7 is a positive number, I should click the up arrow 7 times, then I should click the submit button.
    print('[Step 1] click the up arrow 7 times')
    for _ in range(7):
        agent.click_xpath("clickxpath //*[@id="area"]/span/a[1]/span[1]")
    
    print('[Step 2] click the submit button')
    submit_button_xpath = "//*[@id="subbtn"]"
    agent.click_xpath(submit_button_xpath)
'''.strip(),
    'click-tab-2-hard':
'''
# Here is an example of solution.
# Task: Switch between the tabs to find and click on the link "apple".
# Here is the solution:
def solution(agent):
# General plan: I should first click the proper tab containing "apple" and then click the link.
	print('[Step 1] click the tab containing the link')
	agent.click_xpath('//a[text()="2"]')

	print('[Step 2] click the link "apple"')
	agent.click_xpath('//*[@id="tabs-2"]/p/span[text()="apple"]')
'''.strip(),
    'click-widget':
'''
# Here is an example of solution.
# Task: Click on a "radio" widget.
# Here is the solution:
def solution(agent):
# General plan: I should find the xpath of the widget whose data-type is "radio", then I should click on it.
    print('[Step 1] find the XPath of the widget whose data-type is "radio"')
    # There might be more than one radio widgets on the page, so I should use the first one.
    xpath_of_radio = "(//input[@data-type='radio'])[1]"

    print('[Step 2] click on the "radio" widget')
    agent.click_xpath(xpath_of_radio)
'''.strip(),
    'click-tab-2':
'''
# Here is an example of solution.
# Task: Switch between the tabs to find and click on the link "apple".
# Here is the solution:
def solution(agent):
# General plan: I should first click the proper tab containing "apple" and then click the link.
	print('[Step 1] click the tab containing the link')
	agent.click_xpath('//a[text()="Tab #2"]')

	print('[Step 2] click the link "apple"')
	agent.click_xpath(//*[@id="tabs-2"]/p/span[text()="apple"])
'''.strip(),
    'click-scroll-list':
'''
# Here is an example of solution.
# Task: Select Banana, Apple and Orange from the scroll list and click Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first select Banana, Apple and Orange from the scroll list, and then click the Submit button.
    print('[Step 1] make a list of items to select')
    items_to_select = ['Banana', 'Apple', 'Orange']

    print('[Step 2] select the items from the scroll list')
    for item in items_to_select:
        agent.click_xpath(f'//option[text()="{item}"]')
    
    print('[Step 3] click the submit button')
    agent.click_xpath('//*[@id="subbtn"]')
'''.strip(),
'social-media':
'''
# Here is an example of solution.
Task: Click on the "Block" button for the user @briana.
Here is the solution:
def solution(agent):
# General plan: I should first click the "more" button for a tweet from @briana, and then click the "Block" button.
    print('[Step 1] Click the "more" button for a tweet from @briana')
    agent.click_xpath("//div[@data-result='i']//span[@class='more']")

    print('[Step 2] Click the "Block" button')
    agent.click_xpath("//div[@data-result='i']//li[@class='block']")
'''.strip(),
    'social-media-some':
'''
# Here are two examples of solution.
# Task: Click the "Reply" button on 2 posts by @sergio and then click Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first click the "Reply" button for 2 posts by @sergio, and then click the Submit button.
    print('[Step 1] Click the "Reply" button for 2 posts by @sergio')
    # I can click the first unselected "Reply" button twice in a loop
    for i in range(2):
        agent.click_xpath(f"//div[@class='media'][.//span[@class='username' and text()='@sergio']][{i+1}]//span[@class='reply']")

    print('[Step 2] Click the Submit button')
    agent.click_xpath("//button[@type='button']")

# Task: Click the "Like" button on 1 post by @alice and then click Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first click the "Like" button for only 1 post by @alice, and then click the Submit button.
    print('[Step 1] Click the "Like" button for 1 post by @alice')
    # I only need to click the first "Like" button once
    xpath_of_like_button = "//div[@class='media'][.//span[@class='username' and text()='@alice']][1]//span[@class='like']")
    agent.click_xpath(xpath_of_like_button)

    print('[Step 2] Click the Submit button')
    agent.click_xpath("//button[@type='button']")
'''.strip(),
    'click-dialog-2':
'''
# Here is an example of solution.
# Task: Click the button in the dialog box labeled "x".
# Here is the solution:
def solution(agent):
# General plan: I should click the button labeled "x" in the dialog box.
    print('[Step 1] Click the button labeled "x" in the dialog box')
    agent.click_xpath("//button[@class='ui-button ui-corner-all ui-widget ui-button-icon-only ui-dialog-titlebar-close']")
'''.strip(),
    'navigate-tree':
'''
# Here is an example of solution.
# Task: Navigate through the file tree. Find and click on the folder or file named "Alice".
# Here is the solution:
def solution(agent):
# General plan: I should first generate the hierarchical list of folders to "Alice", and then click them one by one.
    print('[Step 1] Generate the hierarchical list of folders towards "Alice", from parent to child')
    # as indicated in the HTML code, the path to the folder "Alice" is "Thaddeus/Alice"
    list_of_folders = ['Thaddeus', 'Alice']
    
    print('[Step 2] Click the elements in the list one by one')
    for folder in list_of_folders:
        agent.click_xpath(f"//span[text()='{folder}']")
'''.strip(),
    'click-checkboxes-large':
'''
# Here is an example of solution.
# Task: Select aaa, bbb, ccc, ddd, eee, fff, ggg and click Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first generate the list of items to select, then click them one by one, and finally click submit button.
    print('[Step 1] Generate the list of items to select')
    list_of_items = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg']

    print('[Step 2] Click the elements in the list one by one')
    for item in list_of_items:
    # I can use the text of the label to find the checkbox: //label[text()='{item}']/input "
        agent.click_xpath(f"//label[text()='{item}']/input ")

    print('[Step 3] Click the submit button')
    agent.click_xpath("//button[@id='subbtn']")
'''.strip(),
    'simple-algebra':
'''
# Here is an example of solution.
# Task: Solve for x and type your answer into the textbox. Press Submit when done.
# Here is the solution:
def solution(agent):
# General plan: I should first solve for x, then locate and type the answer into the textbox, and finally click submit button.
    print('[Step 1] Solve for x')
    # I should get the equation from the HTML code
    equation = 'x + 3 = 7'
    # I should solve for x. I can ask assistant to do it for me.
    answer = ask(f"Solve an algebra problem. You should directly output the value of the unknown. For example, solve 'y + 1 = 2' -> 1. Now solve '{equation}' ->")

    print('[Step 2] Locate the input box and type the answer')
    # I should locate the input box
    agent.click_xpath("//input[@id='math-answer']")
    # I should type the answer into the input box
    agent.type(answer)

    print('[Step 3] Click the submit button')
    agent.click_xpath("//button[@id='subbtn']")
'''.strip(),
    'click-shades':
'''
# Here is an example of solution.
# Task: Select all the shades of green and press Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first click all elements corresponding to green color, and then click submit button.
    print('[Step 1] Click all elements corresponding to green color')
    agent.click_xpath("//span[@data-color='green']")

    print('[Step 2] Click the submit button')
    agent.click_xpath("//button[@id='subbtn']")
'''.strip(),
    'click-shape':
'''
# Here are two examples of solution.
# Task: Click on the large 9.
# Here is the solution:
def solution(agent):
# General plan: I should first locate the large 9, and then click it.
    print('[Step 1] Locate the large 9')
    # the large 9 is a text element with large font-size. In the HTML code, it is the text element "9" with font-size="20px" and fill="aqua"
    xpath_of_large_9 = "//*[name()='svg']//*[name()='text' and @fill='aqua' and @font-size='20px' and text()='9']"

    print('[Step 2] Click the large 9')
    agent.click_xpath(xpath_of_large_9)

# Task: Click on the red letter.
# Here is the solution:
def solution(agent):
# General plan: I should first locate the red letter, and then click it.
    print('[Step 1] Locate the red letter')
    # the red letter is a text element with fill='red'. In the HTML code, it is the text element with fill='red'
    # there are multiple red letters, but I only need to click one of them, so I should pick up one of them. Here, I pick up the letter 'S'.
    xpath_of_red_letter = "//*[name()='svg']//*[name()='text' and @fill='red' and text()='S']"

    print('[Step 2] Click the red letter')
    agent.click_xpath(xpath_of_red_letter)
'''.strip(),
    'identify-shape':
'''
# Here is an example of solution.
# Task: Click the button that best describes the figure below.
# Here is the solution:
def solution(agent):
    # General plan: I should first identify the shape of the figure, and then click the button that best describes the figure.
    print('[Step 1] Identify the shape of the figure')
    # from the HTML code, the svg element depicts the figure. I should copy the svg element from the HTML code.
    svg_figure = '<svg id="area_svg" data-wob_ref="4" data-wob_eps="e2"><text x="22" y="22" fill="red" text-anchor="middle" alignment-baseline="central" font-size="30px" style="cursor:pointer;" data-wob_ref="5" data-wob_eps="e2">7</text></svg>'
    # I should get the shape of the figure from the HTML code. I can ask assistant to do it for me.
    shape = ask(f"The html code below depicts a figure:\\n{svg_figure}\\nBased on the code, answer the question:\nWhich of (rectangle, triangle, circle, digit, letter) best describes the figure below. You must directly output an answer without saying anything else.")

    print('[Step 2] Click the button that best describes the figure')
    # I should click the button that best describes the figure
    agent.click_xpath(f"//button[@id='{shape}']")
'''.strip(),
    'count-shape':
'''
# Here is an example of solution.
# define environment and agent. The state is the list of HTML elements of the webpage.
initial_state = \'''
<div id="wrap" data-wob_ref="2" data-wob_eps="e1">
  <div id="query"><div>How many large blue items are there?</div><div></div></div>
  <div id="area" data-wob_ref="3" data-wob_eps="e1">
    <svg id="area_svg" data-wob_ref="4" data-wob_eps="e1"><circle cx="90" cy="10" r="10" fill="blue" style="cursor:pointer;" data-wob_ref="5" data-wob_eps="e1"></circle><text x="30" y="110" fill="blue" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="6" data-wob_eps="e1">m</text><text x="130" y="70" fill="magenta" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="7" data-wob_eps="e1">q</text><circle cx="30" cy="30" r="10" fill="yellow" style="cursor:pointer;" data-wob_ref="8" data-wob_eps="e1"></circle><text x="30" y="50" fill="black" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="9" data-wob_eps="e1">b</text><rect x="100" y="100" width="20" height="20" fill="aqua" style="cursor:pointer;" data-wob_ref="10" data-wob_eps="e1"></rect><circle cx="90" cy="30" r="5" fill="yellow" style="cursor:pointer;" data-wob_ref="11" data-wob_eps="e1"></circle><text x="70" y="110" fill="black" text-anchor="middle" alignment-baseline="central" font-size="20px" style="cursor:pointer;" data-wob_ref="12" data-wob_eps="e1">2</text></svg>
    <div id="count-buttons" data-wob_ref="13" data-wob_eps="e1"><button data-wob_ref="14" data-wob_eps="e1">9</button><button data-wob_ref="15" data-wob_eps="e1">1</button><button data-wob_ref="16" data-wob_eps="e1">3</button><button data-wob_ref="17" data-wob_eps="e1">0</button><button data-wob_ref="18" data-wob_eps="e1">6</button></div>
  </div>
</div>
\'''
agent = Agent(initial_state)

# Task: How many large blue items are there?
# Here is the solution:
def solution(agent):
# General plan: I should first count the number of large blue items, then click the button corresponding to the answer.
    print('[Step 1] Count the number of large blue items')
    # from the HTML code, the svg element depicts the figure. I must copy the svg element from the HTML code.
    svg_figure = '<svg id="area_svg" data-wob_ref="4" data-wob_eps="e1"><circle cx="90" cy="10" r="10" fill="blue" style="cursor:pointer;" data-wob_ref="5" data-wob_eps="e1"></circle><text x="30" y="110" fill="blue" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="6" data-wob_eps="e1">m</text><text x="130" y="70" fill="magenta" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="7" data-wob_eps="e1">q</text><circle cx="30" cy="30" r="10" fill="yellow" style="cursor:pointer;" data-wob_ref="8" data-wob_eps="e1"></circle><text x="30" y="50" fill="black" text-anchor="middle" alignment-baseline="central" font-size="10px" style="cursor:pointer;" data-wob_ref="9" data-wob_eps="e1">b</text><rect x="100" y="100" width="20" height="20" fill="aqua" style="cursor:pointer;" data-wob_ref="10" data-wob_eps="e1"></rect><circle cx="90" cy="30" r="5" fill="yellow" style="cursor:pointer;" data-wob_ref="11" data-wob_eps="e1"></circle><text x="70" y="110" fill="black" text-anchor="middle" alignment-baseline="central" font-size="20px" style="cursor:pointer;" data-wob_ref="12" data-wob_eps="e1">2</text></svg>'
    # I must also create a list of the multiple-choices from answer buttons in the HTML code. In the code, there are five <button> with number shown on them: "9", "1", "3", "0", "6"
    multiple_choices = [9, 1, 3, 0, 6]
    # I should get the number of large blue items from the HTML code. I can ask assistant to do it for me.
    number_of_large_blue_items = ask(f"Here is a part of html code that draws some svg figures:\\n{svg_figures}\\nBased on the code above, answer the question: How many large blue items are there? You must choose an answer between {multiple_choices} and only output the number without saying any words.")

    print('[Step 2] Click the button corresponding to the answer')
    # I should click the button corresponding to the answer
    agent.click_xpath(f"//button[text()='{number_of_large_blue_items}']")
'''.strip(),
    'click-checkboxes-soft':
'''
# Here is an example of solution.
# define environment and agent. The state is the list of HTML elements of the webpage.
initial_state = \'''
<div id="wrap" data-wob_ref="2" data-wob_eps="e0">
  <div id="query">Select words similar to detest and click Submit.</div>
  <div id="area" data-wob_ref="3" data-wob_eps="e0">
    <div id="boxes" data-wob_ref="4" data-wob_eps="e0"><label data-wob_ref="5" data-wob_eps="e0"><input type="checkbox" id="ch0" data-wob_ref="6" data-wob_eps="e0">despise</label><br><label data-wob_ref="7" data-wob_eps="e0"><input type="checkbox" id="ch1" data-wob_ref="8" data-wob_eps="e0">fires</label><br><label data-wob_ref="9" data-wob_eps="e0"><input type="checkbox" id="ch2" data-wob_ref="10" data-wob_eps="e0">delicious</label><br></div>
    <br>
    <button id="subbtn" class="secondary-action" data-wob_ref="11" data-wob_eps="e0">Submit</button>
  </div>
</div>
\'''
agent = Agent(initial_state)

# Task: Select words similar to detest and fire and click Submit.
# Here is the solution:
def solution(agent):
# General plan: I should first get the list of words similar to detest, then click the checkboxes corresponding to the words, and finally click the submit button.
# Use literal_eval to convert the answer from ask() to a list.
from ast import literal_eval
    print('[Step 1] Get the list of words similar to detest')
    # I must create a list of the multiple-choices from answer buttons in the HTML code. In the code, there are three <checkbox> with words shown on them: "despise", "fires", "delicious"
    multiple_choices = ["despise", "fires", "delicious"]
    # I should get the list of words similar to detest from the HTML code. I can ask assistant to do it for me.
    words_similar_to_detest = ask(f'Among the Python list of words:{multiple_choices}, generate a subset of list containing the words with similar meanings to ['detest', 'fire']. You must only output the Python list without saying any words.')
    words_similar_to_detest = literal_eval(words_similar_to_detest)

    print('[Step 2] Click the checkboxes corresponding to the words')
    # I should click the checkboxes corresponding to the words
    for word in words_similar_to_detest:
        agent.click_xpath(f"//label[text()='{word}']")

    print('[Step 3] Click the submit button')
    # I should click the submit button
    agent.click_xpath("//button[@id='subbtn']")
'''.strip(),
    'guess-number':
'''
# Here is an example of solution.
# Task: Guess the number between 0-9 and press Submit. Use the feedback below to find the right number.
# Here is the solution:
def solution(agent, start_from = 1):
# General plan: Given a list of possible_numbers, I will try the number in the middle of the list and get feedback from the html state.
# Now the given list of possible_numbers is [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]. 
    if start_from <= 1:
        print('[Step 1] maintain a list of the possible numbers left and try the middle one')
        # before making a guess, I should store the html state for future comparison.
        state_before_interaction = agent.current_state
        # I will choose the number 5, which is in the middle of possible_numbers.
        guess_number = 5
        # click the input box, type the number I guessed and click submit.
        agent.click_xpath("//input[@id='tt']")
        agent.press_key("backspace")
        agent.type(str(guess_number))
        state_after_interaction = agent.click_xpath('//*[@id="subbtn"]')
        # after input and submit the guessed number, the html_state should be changed and contain the feedback. Otherwise this step is not successful.
        assert state_after_interaction != state_before_interaction, 'I did [Step 1] but the html state did not change.'
   
    if start_from <= 2:
        print('[Step 2] get the feedback information from the new html state')
        # If the guess is successful, the keyword "higher" or "lower" should not be present in the observation. Otherwise I should use assert to jump out to pass the feedback.
        observation = ask(f'Answer a question based on the html code below: {state_after_interaction} Question: Which one is displayed? "The number is lower than" or "The number is higher than"? You must only output the displayed sentence without saying any other words.')
        assert "higher" not in observation, f'You tried the number {guess_number} in [Step 1], and the correct number is greater than this number. I need to revise solution function according to the new plan: Now the given list of possible_numbers is [6, 7, 8, 9].'
        assert "lower" not in observation, f'You tried the number {guess_number} in [Step 1], and the correct number is smaller than this number. I need to revise solution function according to the new plan: Now the given list of possible_numbers is [0, 1, 2, 3, 4].'
'''.strip(),
    'login-user-popup':
'''
# Here is an example of solution.
# Task: Enter the username "kanesha" and the password "oT" into the text fields and press login.
def solution(agent, start_from=1):
# General plan: I should first click on the username field, then type in the username, then click on the password field, then type in the password, then click on the login button.
    if start_from <= 1:
        print('[Step 1] Click on the username field')
        state_after_interaction = agent.click_xpath("//input[@id=\'username\']")
        # during interaction, some popups may appear. If so, I need to jump out to handle the popups.
        assert 'popup' not in state_after_interaction, f'After [Step 1], some popups appeared, you need to close the popup at the beginning of [Step 1]. The current html is: {state_after_interaction} You need to add some code at the beginning of [Step 1] to cancel the popup before any other actions.'

    if start_from <= 2:
        print('[Step 2] Type in the username')
        state_after_interaction = agent.type('kanesha') 
        # during interaction, some popups may appear. If so, I need to jump out to handle the popups.
        assert 'popup' not in state_after_interaction, f'After [Step 2], some popups appeared, you need to close the popup at the beginning of [Step 2]. The current html is: {state_after_interaction} You need to add some code at the beginning of [Step 2] to cancel the popup before any other actions.'
    
    if start_from <= 3:
        print('[Step 3] Click on the password field')
        state_after_interaction = agent.click_xpath("//input[@id=\'password\']")
        # during interaction, some popups may appear. If so, I need to jump out to handle the popups.
        assert 'popup' not in state_after_interaction, f'After [Step 3], some popups appeared, you need to close the popup at the beginning of [Step 3]. The current html is: {state_after_interaction} You need to add some code at the beginning of [Step 3] to cancel the popup before any other actions.'
    
    if start_from <= 4:
        print('[Step 4] Type in the password')
        state_after_interaction = agent.type('oT') 
        # during interaction, some popups may appear. If so, I need to jump out to handle the popups.
        assert 'popup' not in state_after_interaction, f'After [Step 4], some popups appeared, you need to close the popup at the beginning of [Step 4]. The current html is: {state_after_interaction} You need to add some code at the beginning of [Step 4] to cancel the popup before any other actions.'
    
    if start_from <= 5:
        print('[Step 5] Click on the login button')
        state_after_interaction = agent.click_xpath("//button[@id='subbtn']")
        # during interaction, some popups may appear. If so, I need to jump out to handle the popups.
        assert 'popup' not in state_after_interaction, f'After [Step 5], some popups appeared, you need to close the popup at the beginning of [Step 5]. The current html is: {state_after_interaction} You need to add some code at the beginning of [Step 5] to cancel the popup before any other actions.'
'''.strip(),
    'tic-tac-toe':
"""
# Here is an example of solution.
# Task: Playing as 'X', win a game of tic-tac-toe. 
def solution(agent, start_from=1):
# The board layout and corresponding html xpath: top-left("//*[@id='ttt-0']"), top-center("//*[@id='ttt-1']"), top-right("//*[@id='ttt-2']"), middle-left("//*[@id='ttt-3']"), middle-center("//*[@id='ttt-4']"), middle-right("//*[@id='ttt-5']"), bottom-left("//*[@id='ttt-6']"), bottom-center("//*[@id='ttt-7']"), bottom-right("//*[@id='ttt-8']").  Note that "mark-o" indicates the 'O' placed on board, "mark-x" indicates the 'X' placed on board.
# General plan: Currently, no grid is occupied. The plan is 1) put an 'X' in the middle-center("//*[@id='ttt-4']"), 2) put an 'X' in the top-left("//*[@id='ttt-0']"), 3) put an 'X' in the bottom-right("//*[@id='ttt-8']").
    place_to_put_X = ['4', '0', '8']
    for idx, place_id in enumerate(place_to_put_X):
        print(f'[Step {idx}] put an X in {place_id}')
        # before interaction, I need to store the current state so that I can compare it with the state after interaction.
        state_before_interaction = agent.current_state
        state_after_interaction = agent.click_xpath(f"//*[@id='ttt-{place_id}']")
        # if the current state does not change after interaction, that means I cannot put an 'X' in the desired location, and that location is already occupied and the plan will not work. 
        assert state_before_interaction != state_after_interaction, f'''I cannot do [Step {idx}] put an X in the "//*[@id='ttt-{place_id}']", because it is occupied. I need to revise solution function according to the new plan. ''' + \
            ask(f'''Playing as 'X', win a game of tic-tac-toe. The board layout and corresponding html xpath: top-left("//*[@id='ttt-0']"), top-center("//*[@id='ttt-1']"), top-right("//*[@id='ttt-2']"), middle-left("//*[@id='ttt-3']"), middle-center("//*[@id='ttt-4']"), middle-right("//*[@id='ttt-5']"), bottom-left("//*[@id='ttt-6']"), bottom-center("//*[@id='ttt-7']"), bottom-right("//*[@id='ttt-8']").Note that "mark-o" indicates the 'O' placed on board, "mark-x" indicates the 'X' placed on board. The game in progress is represented in html code: {agent.current_state} Report current board situation and generate a plan that the 'X' player should follow to continue this game. Use the format like "Currently, 'X' has been placed at <position>("//*[@id='ttt-x']") and 'O' has been placed at <position>("//*[@id='ttt-x']"). Therefore, the plan is to: 1) put an 'X' in the <position>("//*[@id='ttt-x']") 2) put an 'X' in the ..."''')
""".strip(),
    'search-engine':
"""
# Here is an example of solution.
# Task: Use the textbox to enter "Alice" and press "Search", then find and click the 7th search result.
def solution(agent, start_from=1):
# General plan: I should first click on the inputbox, then type "Alice", then click on the "Search" button, finally look through pages and click on the 7th result.
    if start_from <= 1:
        print('[Step 1] click on the inputbox and type "Alice"')
        agent.click_xpath('//*[@id="search-text"]')
        agent.type('Alice')
        state_after_interaction = agent.click_xpath('//*[@id="search"]')
        # the search content should be displayed on page.
        assert 'search-desc' in state_after_interaction, 'I cannot do [Step 1] correctly. The search content is not displayed on the page.'
    
    if start_from <= 2:
        print('[Step 2] calculate the page number of the 7th result and click on the page')
        # I should count the number of results on each page, iteratively turn to next page until seeing the 7th result.
        # I can use the following code to count the number of results on each page.
        num_results_displayed_per_page = state_after_interaction.count('search-desc')
        num_page = (7 - 1) // num_results_displayed_per_page
        state_after_interaction = agent.click_xpath(f'//*[@id="pagination"]/li[{3+num_page}]/a')
        # I should click on the 7th result.
        num_to_click = 7 - num_results_displayed_per_page * num_page
        state_after_interaction = agent.click_xpath(f'//*[@id="page-content"]/div[{num_to_click}]/a')
""".strip(),
    'terminal':
"""
# Here is an example of solution.
# Task: Use the terminal below to delete a file ending with the extension .gif
def solution(agent, start_from=1):
# General plan: I should first type "ls" to list all files in the terminal, then identify the filename ending with ".gif" and type "rm [filename].gif" to delete the identified file.
    if start_from <= 1:
        print('[Step 1] type "ls" to list all files in the terminal')
        agent.type('ls')
        state_after_interaction = agent.press_key('enter')
        # the file list should be displayed on terminal.
        assert 'gif' in state_after_interaction, f'I cannot do [Step 1] correctly. The file list is not displayed on the terminal. Current state: {state_after_interaction}'
    
    if start_from <= 2:
        print('[Step 2] identify the filename ending with ".gif" and type "rm [filename].gif" to delete the identified file')
        # I should identify the filename ending with ".gif". I can ask assistant to do that.
        filename = ask(f'You are given some html code as follows: {state_after_interaction} What is the file ending with the extension .gif? You must directly output the full file name, including the extension.')
        agent.type(f'rm {filename}')
        state_after_interaction = agent.press_key('enter')
        assert 'not found' not in state_after_interaction, f'I cannot do [Step 2] correctly. The file ending with the extension .gif is not deleted. Current state: {state_after_interaction}'
""".strip(),
    'email-inbox':
'''
# Here are three examples of solution.
# Task: Find the email by Brittani and reply to them with the text "Aliquet. Sollicitudin nam lectus.".
def solution(agent, start_from=1):
# General plan: I should first click on the email by Brittani, then click on the reply button, then type the text "Aliquet. Sollicitudin nam lectus." and finally click on the send button.
    if start_from <= 1:
        print('[Step 1] click on the email by Brittani')
        agent.click_xpath("//div[@class='email-sender' and text()='Brittani']")
        state_after_interaction = agent.click_xpath("//span[@class='email-reply']")
        # the reply content should be displayed on page.
        assert 'reply-text' in state_after_interaction, 'I cannot do [Step 1] correctly. The reply button is not displayed on the page.'
    
    if start_from <= 2:
        print('[Step 2] type the text "Aliquet. Sollicitudin nam lectus."')
        agent.click_xpath("//textarea[@id='reply-text']")
        agent.type('Aliquet. Sollicitudin nam lectus.')
        state_after_interaction = agent.click_xpath("//*[@id='send-reply']")

# Task: Find the email by Blanca and forward that email to Agathe.
def solution(agent, start_from=1):
# General plan: I should first click on the email by Blanca, then click on the forward button, then type "Agathe" and finally click on the send button.
    if start_from <= 1:
        print('[Step 1] click on the email by Blanca')
        agent.click_xpath("//div[@class='email-sender' and text()='Blanca']")
        state_after_interaction = agent.click_xpath("//span[@class='email-forward']")
        # the forward content should be displayed on page.
        assert 'forward-sender' in state_after_interaction, 'I cannot do [Step 1] correctly. The forward button is not displayed on the page.'
    
    if start_from <= 2:
        print('[Step 2] type "Agathe"')
        agent.click_xpath("//input[@class='forward-sender']")
        agent.type('Agathe')
        state_after_interaction = agent.click_xpath("//*[@id='send-forward']")

# Task: Find the email by Salli and click the trash icon to delete it.
def solution(agent, start_from=1):
# General plan: I should first click on the email by Salli, then click on the trash icon.
    if start_from <= 1:
        print('[Step 1] click on the email by Salli')
        agent.click_xpath("//div[@class='email-sender' and text()='Salli']")
        agent.click_xpath("//span[@class='trash']")
'''.strip(),
    'email-inbox-nl-turk':
'''
# Here are three examples of solution.
# Task: "Aliquet. Sollicitudin nam lectus." is my reply to Brittani's most recent email / Find the email by Brittani and reply to them with the text "Aliquet. Sollicitudin nam lectus.".
def solution(agent, start_from=1):
# General plan: I should first click on the email by Brittani, then click on the reply button, then type the text "Aliquet. Sollicitudin nam lectus." and finally click on the send button.
    if start_from <= 1:
        print('[Step 1] click on the email by Brittani')
        agent.click_xpath("//div[@class='email-sender' and text()='Brittani']")
        state_after_interaction = agent.click_xpath("//span[@class='email-reply']")
        # the reply content should be displayed on page.
        assert 'reply-text' in state_after_interaction, 'I cannot do [Step 1] correctly. The reply button is not displayed on the page.'
    
    if start_from <= 2:
        print('[Step 2] type the text "Aliquet. Sollicitudin nam lectus."')
        agent.click_xpath("//textarea[@id='reply-text']")
        agent.type('Aliquet. Sollicitudin nam lectus.')
        state_after_interaction = agent.click_xpath("//*[@id='send-reply']")

# Task: Find the last email by Blanca and send it to Agathe / Find the email by Blanca and forward that email to Agathe.
def solution(agent, start_from=1):
# General plan: I should first click on the email by Blanca, then click on the forward button, then type "Agathe" and finally click on the send button.
    if start_from <= 1:
        print('[Step 1] click on the email by Blanca')
        agent.click_xpath("//div[@class='email-sender' and text()='Blanca']")
        state_after_interaction = agent.click_xpath("//span[@class='email-forward']")
        # the forward content should be displayed on page.
        assert 'forward-sender' in state_after_interaction, 'I cannot do [Step 1] correctly. The forward button is not displayed on the page.'
    
    if start_from <= 2:
        print('[Step 2] type "Agathe"')
        agent.click_xpath("//input[@class='forward-sender']")
        agent.type('Agathe')
        state_after_interaction = agent.click_xpath("//*[@id='send-forward']")
        
# Task: Delete this email from Salli / Please find Salli's email in the inbox and delete it.
def solution(agent, start_from=1):
# General plan: I should first click on the email by Salli, then click on the trash icon.
    if start_from <= 1:
        print('[Step 1] click on the email by Salli')
        agent.click_xpath("//div[@class='email-sender' and text()='Salli']")
        agent.click_xpath("//span[@class='trash']")
'''.strip(),
    'email-inbox-forward-nl':
'''
# Here is an example of solution.
# task: Send Alice the email from Beth / navigate to the message from Beth and send it to Alice.
def solution(agent, start_from=1):
# General plan: I should first click on the email from Beth, then click on the "Forward" button, then type "Alice" in the "To" inputbox, finally click on the "Send" button.
    if start_from <= 1:
        print('[Step 1] click on the email from Beth')
        agent.click_xpath('//*[@class="email-sender" and text()="Beth"]')
        state_after_interaction = agent.click_xpath('//span[@class="email-forward"]')
        # the "To" inputbox should be displayed on page.
        assert 'forward-sender' in state_after_interaction, f'I cannot do [Step 1] correctly. The "To" inputbox is not displayed on the page. Current state: {state_after_interaction}'
    
    if start_from <= 2:
        print('[Step 2] type "Alice" in the "To" inputbox')
        agent.click_xpath('//input[@class="forward-sender"]')
        agent.type('Alice')
        state_after_interaction = agent.click_xpath('//span[@id="send-forward"]')
        # the email should be sent successfully.
        assert 'email-sender' in state_after_interaction, f'I cannot do [Step 2] correctly. The email is not sent successfully. Current state: {state_after_interaction}'
'''.strip(),
    'email-inbox-forward-nl-turk':
'''
# Here is an example of solution.
# task: Send Alice the email from Beth / navigate to the message from Beth and send it to Alice / I want to forward the email from Beth over to Alice
def solution(agent, start_from=1):
# General plan: I should first click on the email from Beth, then click on the "Forward" button, then type "Alice" in the "To" inputbox, finally click on the "Send" button.
    if start_from <= 1:
        print('[Step 1] click on the email from Beth')
        agent.click_xpath('//*[@class="email-sender" and text()="Beth"]')
        state_after_interaction = agent.click_xpath('//span[@class="email-forward"]')
        # the "To" inputbox should be displayed on page.
        assert 'forward-sender' in state_after_interaction, f'I cannot do [Step 1] correctly. The "To" inputbox is not displayed on the page. Current state: {state_after_interaction}'
    
    if start_from <= 2:
        print('[Step 2] type "Alice" in the "To" inputbox')
        agent.click_xpath('//input[@class="forward-sender"]')
        agent.type('Alice')
        state_after_interaction = agent.click_xpath('//span[@id="send-forward"]')
        # the email should be sent successfully.
        assert 'email-sender' in state_after_interaction, f'I cannot do [Step 2] correctly. The email is not sent successfully. Current state: {state_after_interaction}'
'''.strip()
}