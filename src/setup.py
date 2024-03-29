################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "This Python module contains components for analyzing the use of system resources by processes. It covers two use cases: a) monitoring other processes and b) monitoring one's own process.",
	include_package_data = True,
	install_requires = [
		"jk_appmonitoring",
	],
	keywords = [
		"...",
	],
	license = "Apache2",
	name = "jk_appmonitoring",
	package_data = {
		"": [
		],
	},
	packages = [
		"jk_sysinfo",
		"jk_cmdoutputparsinghelper",
		"jk_prettyprintobj",
		"jk_utils",
	],
	scripts = [
	],
	version = '0.2023.5.20',
	zip_safe = False,
	long_description = readme(),
	long_description_content_type = "text/markdown",
)
