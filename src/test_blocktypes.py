import unittest
from  markdown import is_valid_unordered_list, is_valid_ordered_list

class TestMarkdownListValidation(unittest.TestCase):

	# Ordered list tests
	def test_valid_ordered_list(self):
		lines = [
			"1. First item",
			"2. Second item",
			"3. Third item"
		]
		self.assertTrue(is_valid_ordered_list(lines))

	def test_ordered_list_skips_number(self):
		lines = [
			"1. First item",
			"3. Second item"
		]
		self.assertFalse(is_valid_ordered_list(lines))

	def test_ordered_list_starts_wrong(self):
		lines = [
			"2. First item",
			"3. Second item"
		]
		self.assertFalse(is_valid_ordered_list(lines))

	def test_ordered_list_with_blank_lines(self):
		lines = [
			"1. First item",
			"",
			"2. Second item",
			"3. Third item"
		]
		self.assertTrue(is_valid_ordered_list(lines))

	def test_ordered_list_with_invalid_format(self):
		lines = [
			"1 First item",  # missing dot
			"2. Second item"
		]
		self.assertFalse(is_valid_ordered_list(lines))

	# Unordered list tests
	def test_valid_unordered_list(self):
		lines = [
			"- Apples",
			"- Bananas",
			"- Cherries"
		]
		self.assertTrue(is_valid_unordered_list(lines))

	def test_unordered_list_mixed_bullets(self):
		lines = [
			"- Apples",
			"* Bananas",
			"+ Cherries"
		]
		self.assertTrue(is_valid_unordered_list(lines))

	def test_unordered_list_missing_space(self):
		lines = [
			"-Apples",
			"- Bananas"
		]
		self.assertFalse(is_valid_unordered_list(lines))

	def test_unordered_list_extra_spaces(self):
		lines = [
			"-  Apples",  # two spaces after bullet
			"- Bananas"
		]
		self.assertFalse(is_valid_unordered_list(lines))

	def test_unordered_list_with_blank_lines(self):
		lines = [
			"- Apples",
			"",
			"- Bananas"
		]
		self.assertTrue(is_valid_unordered_list(lines))

	def test_unordered_list_with_non_list_line(self):
		lines = [
			"- Apples",
			"Bananas",  # not a list item
			"- Cherries"
		]
		self.assertFalse(is_valid_unordered_list(lines))

