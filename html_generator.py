
#open notes
text_file = open('ipndnotes.txt', 'r')

#open file to write the generated html
html_file = open('ipndhtml.html', 'w')

#most text is parsed normally. <pre> code will be parsed in block format
parsing_state = 'normal'

#initializes an empty list
new_code_list = []

#parse headlines using "t1:" or "t2"
def get_headline(concept):
	headline = concept[3 : -1]
	return headline

#parse paragraph contents
def get_content(concept):
	#start_location = concept.find('p:') 
	#end_location = concept.find(':p') 
	description = concept[2 : -1]
	return description

#parse code blocks
def get_code(concept):
	end_location = concept.find(':c')
	if concept.find('c:') == 0:
		start_location = 2
	else:
		start_location = 0
	code = concept[start_location : end_location]
	return code

#adds each line of code to a list, so all code can be formatted and printed in block format
def code_list(line):
	global new_code_list
	new_code_list.append(line)
	return new_code_list
	


#html formatting for banner-title
def generate_banner_html(banner_headline):
	html_1 = '''
	<div class="banner-title">''' + banner_headline + '''</div>
	<div class="content-wrap">
	'''
	return html_1

#html formatting for H3 
def generate_sub_headline(sub_headline):
	html_1 = '''
		<h3>''' + sub_headline + '''</h3>
		'''
	return html_1

#html formatting for normal content. Has conditionals for inline code. 
#I called it "em" because it was originally italic, but I like the class inline-code more.
def generate_description(description):
	start_location = len(description)
	end_location = len(description)
	stuff_in_italics = ''
	content_wrap = ''
	em_start = ''
	em_end = ''

	if description.find('em:') != -1:
		start_location = description.find('em:')
		end_location = description.find(':em')
		stuff_in_italics = description[start_location+3 : end_location]
		em_start = '''<span class="inlinecode">'''
		em_end = '''</span>'''
	if description.find(':cw') != -1:
		content_wrap = '''</div>'''
		description = description[0:-3]
	html_1 = '''
		<p>''' + description[:start_location] + em_start + stuff_in_italics + em_end + description[end_location+3:] + '''</p>
		''' + content_wrap
	
	return html_1

#html formatting for a single line of code
def generate_code(code):
	html_1 = '''
		<pre>''' + code + '''</pre>'''
	return html_1

#html formatting for a code block
def generate_code_block(code_block):
	html_1 = '''
		<pre>'''
	for each_line in code_block:
		html_1 = html_1 + '\n' + each_line 
	html_1 = html_1 + '''
		</pre>'''
	return html_1

def normal_parsing(line):
#class = banner-title
	if line[0:3] == 't1:':
		banner_headline = get_headline(line)
		html = generate_banner_html(banner_headline)
		#print html
		html_file.write(html)
	#H3 headline	
	elif line[0:3] == 't2:':
		sub_headline = get_headline(line)
		html = generate_sub_headline(sub_headline)
		#print html
		html_file.write(html)
	#paragraph	
	elif line[0:2] == 'p:':
		description = get_content(line)
		html = generate_description(description)
		#print html
		html_file.write(html)
	#single line of formatted code	
	elif line[0:2] == 'c:' and line[-3:-1] == ':c':
		code_line = get_code(line)
		html = generate_code(code_line)
		#print html
		html_file.write(html)
	elif line[0:2] == 'c:':
		parsing_state = 'code_block'
		code_line = get_code(line)
		code_list(code_line)

def code_parsing(line):
	if line[-3:-1] != ':c':
		code_line = get_code(line)
		code_list(code_line)
	else:
		code_line = get_code(line)
		code_block = code_list(code_line)
		html = generate_code_block(code_block)
		#print html
		html_file.write(html)
		parsing_state = 'normal'
		new_code_list = []


#parsing of each line in the notes text file.
for line in text_file:
	if parsing_state == 'normal':
		normal_parsing(line)
	elif parsing_state == 'code_block':
		code_parsing(line)
		

	
		



