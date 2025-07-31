from textnode import TextType, TextNode
import os
import shutil
from markdown import generate_page
#def main():
	#node = TextNode("Test text", TextType.BOLD, "http://dog.com")
	#print(node)

def find_files_by_extension(root_dir, extension):
	matches = []
	for dirpath, _, filenames in os.walk(root_dir):
		for filename in filenames:
			if filename.lower().endswith(extension.lower()):
				full_path = os.path.join(dirpath, filename)
				matches.append(full_path)
	return matches
"""
# Example usage
if __name__ == "__main__":
	root = "/path/to/start"
	ext = ".jpg"
	for fpath in find_files_by_extension(root, ext):
		print(fpath)
"""

import os

def replicate_dir_structure_from_cwd(file_path, output_base):
	cwd = os.getcwd()
	abs_path = os.path.abspath(file_path)

	# Get relative path from CWD to file's parent directory
	relative_dir = os.path.relpath(os.path.dirname(abs_path), start=cwd)

	# Create equivalent directory inside output_base
	new_dir = os.path.join(output_base, relative_dir)
	os.makedirs(new_dir, exist_ok=True)

	print(f"Created: {new_dir}")
	return new_dir
	
def remove_first_dir(path):
    parts = os.path.normpath(path).split(os.sep)
    trimmed = os.path.join(*parts[1:])  # Skip the first directory
    return trimmed

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	#print(f"Generating pages in directory: {dir_path_content}")
	index_md = find_files_by_extension(dir_path_content, '.md')
	#print(f"Found markdown files: {index_md}")
	for md_file in index_md:
	#	print(f"Processing markdown file: {md_file}")
		stripped_path = remove_first_dir(md_file)
	#	print(f"Stripped path: {stripped_path}")
		newdir = replicate_dir_structure_from_cwd(stripped_path, 'public') ##md_file, 'public')
		newdir = os.path.join(newdir, 'index.html')
	#	print(f"New directory for generated page: {newdir}")
		generate_page(md_file, 'template.html', newdir) #'public')
	
def copy_recursive(src, dst):
	if not os.path.exists(src):
		print(f"Source directory not found: {src}")
		return
	if os.path.exists(dst):
		for root, dirs, files in os.walk(dst, topdown=False):
			for name in files:
				file_path = os.path.join(root, name)
				print(f"Deleting file: {file_path}")
				os.remove(file_path)
			for name in dirs:
				dir_path = os.path.join(root, name)
				print(f"Deleting directory: {dir_path}")
				os.rmdir(dir_path)
		print(f"Deleting root public directory: {dst}")
		os.rmdir(dst)
		
	os.makedirs(dst)
	print(f"Created destination directory: {dst}")

	def _copy_dir(current_src, current_dst):
		for entry in os.listdir(current_src):
			src_path = os.path.join(current_src, entry)
			dst_path = os.path.join(current_dst, entry)
			if os.path.isdir(src_path):
				os.makedirs(dst_path, exist_ok=True)
				_copy_dir(src_path, dst_path)
			else:
				shutil.copy2(src_path, dst_path)
				print(f"Copied file: {dst_path}")
	_copy_dir(src, dst)






if __name__ == "__main__":
	#	main()
	copy_recursive('static', 'public')
	#generate_page('content/index.md', 'template.html', 'public/index.html')
	#generate_page('content/blog/glorfindel/index.md', 'template.html', 'public/index.html')
	#generate_page('content/blog/tom/index.md', 'template.html', 'public/index.html')
	#generate_page('content/blog/majesty/index.md', 'template.html', 'public/index.html')
	#generate_page('content/contact/index.md', 'template.html', 'public/index.html')
	generate_pages_recursive('content', 'template.html', 'public')
 
