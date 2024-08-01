# Webscraping - Webpage Content Comparison Script
# Overview
This Python script automates the process of fetching, storing, and comparing webpage content from a specified URL. It tracks changes by comparing the current and previous week’s content of internal links on the webpage. Differences are reported in a CSV file.


**Overall purpose of script:**
This is the main function of the script. It performs the following steps:
Fetches the content of the base URL and its internal links.
Creates folders for the current week and previous week.
Fetches and stores content for each internal link.
Compares the current week’s content with the previous week’s content.
Collects differences and saves them in a CSV report if changes are found.


# Dependencies
requests: For fetching web content
BeautifulSoup: For parsing HTML content
difflib: For comparing text content
csv: For handling CSV file operations
os: For interacting with the operating system
pandas: For advanced data manipulation (optional but recommended)
re: For regular expressions
datetime: For handling dates and times
urllib.parse: For URL handling

# Detailed Function Descriptions
1. **fetch_content(url)**
**Purpose:** Fetches the textual content of a webpage and returns both the plain text and a BeautifulSoup object.

**Parameters:**

**url (str):** The URL of the webpage to fetch.
**Returns:**

**content (str):** The plain text content of the webpage.
**soup (BeautifulSoup object)**: A BeautifulSoup object for further HTML parsing.
**Description:**
This function uses the requests library to fetch the HTML content of the webpage specified by the URL. It then parses this HTML content using BeautifulSoup to extract the plain text.

**2. store_content(content, filename)**
**Purpose:** Saves the provided content to a file.

**Parameters:**

**content (str):** The content to write to the file.
**filename (str):** The path of the file where the content will be saved.
**Returns:**
None

**Description:**
This function opens the specified file in write mode and writes the content to it. The file is encoded in UTF-8 to handle a wide range of characters.

**3.get_internal_links(base_url, soup)**
**Purpose:** Extracts internal links from a BeautifulSoup object.

**Parameters:**

**base_url (str):** The base URL of the website.
**soup (BeautifulSoup object):** A BeautifulSoup object representing the HTML of the webpage.
**Returns:**

**internal_links (list)**: A list of internal URLs found on the page.
**Description:**
This function searches for all anchor (<a>) tags with href attributes. It checks if these links are internal by ensuring they start with the base URL or a relative path. Internal links are collected into a set to avoid duplicates and then converted into a list.

**4.compare_content(file1, file2)**
**Purpose:** Compares the content of two files and returns the differences.

**Parameters:**

**file1 (str):** Path to the first file.
**file2 (str):** Path to the second file.
**Returns:**

**diff (list):** A list of differences between the files, formatted as a unified diff.
**Description:**
This function reads the content of both files and uses difflib.unified_diff to generate a list of differences. This diff format includes lines that were added, removed, or changed between the two files.

**5.save_diff(previous_file, current_file, base_url)**
**Purpose:** Identifies and formats the differences between two files.

**Parameters:**

**previous_file (str):** Path to the file containing the previous version of the content.
**current_file (str):** Path to the file containing the current version of the content.
**base_url (str):** The base URL of the website.
**Returns:**

**output (list):** A list of differences including line numbers, old content, new content, and URL.
**Description:**
This function reads both the previous and current content files and compares them using difflib.ndiff. It formats the differences into a list, including line numbers where changes occurred, and the respective old and new content. It also includes the URL for reference.

**5.get_previous_week_folder(base_folder)**
**Purpose:** Computes the path to the folder containing the previous week’s content.

**Parameters:**

**base_folder (str): ** The base folder where weekly folders are stored.
**Returns:**

**previous_week_folder (str):** Path to the folder for the previous week.
**Description:**
This function calculates the date for the previous week using datetime and formats it as YYYYMMDD. It then constructs and returns the path to the folder where the previous week’s content is stored.

**6. main(base_url, output_folder, reports_folder)**
**Purpose:** Orchestrates the process of fetching, storing, comparing, and reporting webpage content changes.

**Parameters:**

**base_url (str):** The base URL of the website.
**output_folder (str):** The folder where content files will be stored.
**reports_folder (str):** The folder where the summary report will be saved.
**Returns:**
None

