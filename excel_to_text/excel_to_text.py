#!/usr/bin/env python

from tabulate import tabulate # https://github.com/astanin/python-tabulate

import argparse
from platform import python_version_tuple

if python_version_tuple() >= ('3', '3', '0'):
	from collections.abc import Iterable
else:
	from collections import Iterable

# Available formats and column alignments in python-tabulate: https://github.com/astanin/python-tabulate.
AVAILABLE_FORMATS = ['plain', 'simple', 'github', 'grid', 'fancy_grid', 'pipe', 'orgtbl', 'rst', 'mediawiki', 'html',
	'latex', 'latex_raw', 'latex_booktabs', 'tsv']
AVAILABLE_COL_ALIGNS = ['right', 'center', 'left', 'decimal', 'none']

# Default values of optional arguments.
DEFAULT_TABLE_FORMAT = 'simple'
DEFAULT_FLOAT_FORMAT = 'g'
DEFAULT_COL_ALIGN = ['center']

def get_num_columns(table):
	"""
	Get the number of columns of a table.

	:table: The table. It is a list of lists where each one is a row of the table.
	:return: The number of columns of the table.
	"""

	return max((len(row) for row in table))

def parse_file(file_path, separator='\t'):
	"""
	Parse a file containing a table. This one is returned as a list of lists where each one is a row of the table.

	:file_path: The file path.
	:separator: The separator between columns.
	:return: The table as a list of lists.
	"""

	table = []
	with open(file_path) as file:
		for line in file:
			# Remove newline character.
			line = line.rstrip('\n')
			
			# Parse the line.
			row = line.split(separator)

			table.append(row)

	return table

def write_table(table, file_path):
	"""
	Write a table as text to a file.

	:table: The table as text.
	:file_path: The file path.
	"""

	with open(file_path, 'w') as file:
		file.write(table)

def format_table(table, use_header=True, table_format=DEFAULT_TABLE_FORMAT, float_format=DEFAULT_FLOAT_FORMAT,
		col_align=DEFAULT_COL_ALIGN):
	"""
	Format a table to text according to a given format.

	:table: The table. It is a list of lists where each one is a row of the table.
	:use_header: If `True`, set the first row of the table as a header in the formatted table. Otherwise, do no set any
		header.
	:table_format: The table format. Available formats are listed and detailed on the following website:
		https://github.com/astanin/python-tabulate.
	:float_format: The floating point number format. Refer to the Python's documentation:
		https://docs.python.org/3/library/string.html#formatspec.
	:col_align: The alignment of columns. It can be:
		- a list containing the alignment of each column;
		- a single alignment (string) for setting the same alignment for all columns.
		Available column alignments are listed and detailed on the following website:
		https://github.com/astanin/python-tabulate.
	:return: The table as a text.
	"""

	num_cols = get_num_columns(table)

	# Parse parameters.
	headers = 'firstrow' if use_header else ()
	if isinstance(col_align, Iterable) and not isinstance(col_align, str):
		# Convert each `'none'` into `None`.
		col_align = [
			None if align.lower() == 'none' else align
			for align in col_align
		]
	else:
		# Convert `'none'` into `None`.
		if col_align.lower() == 'none':
			col_align = None

		col_align = (col_align,) * num_cols

	formatted_table = tabulate(table, headers=headers, tablefmt=table_format, floatfmt=float_format, colalign=col_align)
	
	return formatted_table

def _main():
	# Parse arguments.
	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
		help='Show this help message and exit.')
	parser.add_argument('file',
		help='Path of the input text file.')
	parser.add_argument('-1', '--no-header', action='store_true',
		help='Do not use the first row of data as a table header.')
	parser.add_argument('-o', '--output',
		help='Print table to an output file. It defaults to `stdout`.')
	parser.add_argument('-F', '--float', default=DEFAULT_FLOAT_FORMAT,
		help='Floating point number format. It defaults to `{}`. Refer to the Python\'s documentation: '\
		'https://docs.python.org/3/library/string.html#formatspec'.format(DEFAULT_FLOAT_FORMAT))
	parser.add_argument('-f', '--format', choices=AVAILABLE_FORMATS, default=DEFAULT_TABLE_FORMAT,
		help='Output table format. It defaults to `{}`. Available formats detailed on the following website: ' \
			'https://github.com/astanin/python-tabulate'.format(DEFAULT_TABLE_FORMAT))
	parser.add_argument('-c', '--col-align', choices=AVAILABLE_COL_ALIGNS, default=DEFAULT_COL_ALIGN, nargs='+',
		help='Alignment of columns. If more than one alignment is provided, set alignment for each column separately. '\
			'It defaults to `{}`. Available column alignments detailed on the following website: ' \
			'https://github.com/astanin/python-tabulate'.format(DEFAULT_COL_ALIGN))

	args = parser.parse_args()

	input_file = args.file
	output_file = args.output
	use_header = not args.no_header
	table_format = args.format
	float_format = args.float
	col_align = args.col_align if len(args.col_align) > 1 else args.col_align[0]

	# Parse the input file.
	table = parse_file(input_file)

	# Format the table.
	formatted_table = format_table(table, use_header=use_header, table_format=table_format, float_format=float_format,
		col_align=col_align)

	# Write the table.
	if output_file is None:
		print(formatted_table)
	else:
		write_table(formatted_table, output_file)

if __name__ == '__main__':
	_main()
