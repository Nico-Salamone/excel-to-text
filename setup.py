try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name='excel-to-text',
	version='1.0.0',
	description='An Excel table converter.',
	url='https://github.com/Nico-Salamone/excel-to-text',
	author='Nico Salamone',
	author_email='nico.salamone2411@gmail.com',
	license='MIT',
	python_requires='>=3.0.*',
	install_requires=['tabulate'],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3 :: Only',
	],
	packages=['excel_to_text'],
	entry_points={'console_scripts': ['excel-to-text = excel_to_text.excel_to_text:_main']}
)
