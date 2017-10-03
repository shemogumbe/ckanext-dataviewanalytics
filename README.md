
[![PyPI version](https://badge.fury.io/py/ckanext-dataviewanalytics.svg)](https://badge.fury.io/py/ckanext-dataviewanalytics)
[![GitHub issues](https://img.shields.io/github/issues/shemogumbe/ckanext-dataviewanalytics.svg)](https://github.com/shemogumbe/ckanext-dataviewanalytics/issues)
[![GitHub forks](https://img.shields.io/github/forks/shemogumbe/ckanext-dataviewanalytics.svg)](https://github.com/shemogumbe/ckanext-dataviewanalytics/network)
[![GitHub stars](https://img.shields.io/github/stars/shemogumbe/ckanext-dataviewanalytics.svg)](https://github.com/shemogumbe/ckanext-dataviewanalytics/stargazers)
[![GitHub license](https://img.shields.io/badge/license-AGPLv3-blue.svg)](https://raw.githubusercontent.com/shemogumbe/ckanext-dataviewanalytics/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/shemogumbe/ckanext-dataviewanalytics/network.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

DataViewAnalytics CKAN Extension
=========================



This extension displays analytics on resources by analysing the country and occupation of visitors to every resource/data.
This extension is presently on development and is not officially released for use yet. You should only install if you are a developer and want to contribute to the project.

## Requirements
This extension has been tested with versions of CKAN from 2.6.3 onwards and works well on these versions

To install and set up CKAN, visit [CKAN Documentation](http://docs.ckan.org/en/latest/maintaining/installing/index.html)

Then follow the steps below to install the DataViewAnalytics extension:

Step 1:

* Activate your virtual environment; use the path to your virtual environment. On Mac OSX, you may have to use `/usr/local/lib/ckan/default/bin/activate`. You can copy the code as is below, including the preceeding dot.

```bash
. /usr/lib/ckan/default/bin/activate
```

Step 2:

* Install the extension


>You can download the source code and install the extension manually. To do so, execute the following command:
> ```bash
> pip install -e git+https://github.com/shemogumbe/ckanext-dataviewanalytics.git#egg=ckanext-dataviewanalytics
> ```
> **Alternatively**: You can clone this repo (preferably into the /src directory where you installed CKAN), cd into ckanext-dataviewanalytics and run
>```bash
> python setup.py develop
> ```
> Install necessary requirements
>```bash
> pip install -r requirements.txt
> ```

Step 3:

* Modify your configuration file (generally in `/etc/ckan/default/production.ini`) and add `dataviewanalytics` to the `ckan.plugins` property.

```bash
ckan.plugins = dataviewanalytics <OTHER_PLUGINS>
```

Step 4:

* Restart your server:

```bash
paster serve /etc/ckan/default/production.ini
```

OR

```bash
paster serve --reload /etc/ckan/default/production.ini
```

With `--reload`, your server is restarted automatically whenever you make changes to your source code.



Support
-------

If you've found a bug/issue in the extension, please open a new issue [here](https://github.com/shemogumbe/ckanext-dataviewanalytics/issues/new) (try
searching first to see if there's already an [issue](https://github.com/shemogumbe/ckanext-dataviewanalytics/issues) for your bug).



Contributing to DataViewAnalytics CKAN Extension
---------------------------------------------

If you have interest in contributing to the development of DataViewAnalytics extension, you are welcome. A good starting point
will be reading the CKAN general [Contributing guide](http://docs.ckan.org/en/ckan-2.7.0/contributing/index.html). Then you can check out 
existing [issues](https://github.com/shemogumbe/ckanext-dataviewanalytics/issues) that are open for contribution; new features and issues are welcome.
To work on any issue, comment on the issue to indicate your interest and the issue will be assigned to you. It is always a good idea to seek
for clarification (where necessary) on any issue before you work on it.

**It is important that changes that require some form of configuration be documented in the README.**

Copying and License
--------------------

This project is copyright (c) 2017 Andela.

It is open and licensed under the GNU Affero General Public License (AGPL) v2.0

Find the full text here, http://www.gnu.org/licenses/gpl-2.0.html.
