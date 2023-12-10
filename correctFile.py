# import sys

def correctFile(fileName):
	# fileName = sys.argv[1]

	with open(fileName, 'r') as file:
	    file_content = file.read()

	# Replace the pattern '}\n][\n{' with '},{' in the file content
	modified_content = file_content.replace('  }\n][\n  {', '  },\n  {')

	# Write the modified content back to the file
	with open(fileName, 'w') as file:
	    file.write(modified_content)