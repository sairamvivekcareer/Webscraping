import requests
from bs4 import BeautifulSoup
import difflib
import csv
import re
import os
import pandas as pd
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text(), soup

def store_content(content, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def get_internal_links(base_url, soup):
    internal_links = set()
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.startswith('/'):
            url = urljoin(base_url, url)
        if base_url in url:
            internal_links.add(url)
    return list(internal_links)

def compare_content(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
        diff = difflib.unified_diff(text1, text2, lineterm='', fromfile=file1, tofile=file2)
        return list(diff)

def save_diff(previous_file, current_file, base_url):
    with open(previous_file, 'r', encoding='utf-8') as f1, open(current_file, 'r', encoding='utf-8') as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
        diff = difflib.ndiff(text1, text2)
        output = []

        previous_line_num = 0
        current_line_num = 0

        for line in diff:
            if line.startswith('- '):
                previous_line_num += 1
                output.append([previous_line_num, line[2:].strip(), '', base_url])
            elif line.startswith('+ '):
                current_line_num += 1
                if output and output[-1][2] == '':
                    output[-1][2] = line[2:].strip()
                else:
                    output.append([previous_line_num, '', line[2:].strip(), base_url])
            elif line.startswith('  '):
                previous_line_num += 1
                current_line_num += 1
    return output

def get_previous_week_folder(base_folder):
    current_date = datetime.now()
    previous_week_date = current_date - timedelta(days=7)
    previous_week_folder = previous_week_date.strftime("%Y%m%d")
    return os.path.join(base_folder, previous_week_folder)

def main(base_url, output_folder, reports_folder):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_content, base_soup = fetch_content(base_url)
    internal_links = get_internal_links(base_url, base_soup)

    weekly_folder = datetime.now().strftime("%Y%m%d")
    current_week_folder = os.path.join(output_folder, weekly_folder)
    os.makedirs(current_week_folder, exist_ok=True)

    previous_week_folder = get_previous_week_folder(output_folder)
    all_diffs = []

    for link in internal_links:
        link_content, _ = fetch_content(link)
        link_name = link.replace(base_url, '').replace('/', '_').strip('_')
        current_file_name = os.path.join(current_week_folder, f"{link_name}.txt")

        if os.path.exists(previous_week_folder):
            previous_file = os.path.join(previous_week_folder, f"{link_name}.txt")
            if os.path.exists(previous_file):
                store_content(link_content, current_file_name)
                diffs = save_diff(previous_file, current_file_name, link)
                all_diffs.extend(diffs)
            else:
                store_content(link_content, os.path.join(current_week_folder, f"{link_name}.txt"))
        else:
            store_content(link_content, os.path.join(current_week_folder, f"{link_name}.txt"))

    if all_diffs:
        print('Changes identified')
        current_date = datetime.now().date()
        summary_file = os.path.join(reports_folder, f"Regeneron_diff_summary_{current_date}.csv")
        with open(summary_file, 'w', newline='', encoding='utf-8') as df:
            writer = csv.writer(df)
            writer.writerow(['line number', 'Previous content', 'Current content', 'URL'])
            writer.writerows(all_diffs)
    else:
        print('No Differences found')

if __name__ == "__main__":
    base_url = "https://www.regeneron.com/"
    output_folder = "./Regeneron"
    reports_folder = "./Regeneron/reports"
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(reports_folder, exist_ok=True)
    main(base_url, output_folder, reports_folder)
