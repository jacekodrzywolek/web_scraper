import difflib
import re
import requests
from bs4 import BeautifulSoup


def fetch_text(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract text from the parsed HTML (modify as needed to target specific elements)
        return soup.get_text()
    else:
        return "Error fetching webpage."


def sanitize_filename(url):
    """Sanitize the URL to be used as a valid filename"""
    return re.sub(r"[^\w\-\. ]", "", url)  # Replace disallowed characters with underscores


# Take URLs input from the user
url1 = input("Enter the URL for the original website: ")
url2 = input("Enter the URL for the website to compare: ")

# Fetch text from both websites
text1 = fetch_text(url1)
text2 = fetch_text(url2)

# Compare the texts and generate a diff
differ = difflib.Differ()
diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

# Create a sanitized filename from the original URL
filename = sanitize_filename(url1) + "_differences.txt"

# Create and write the differences to a text file
with open(filename, "w") as file:
    file.write(f"Differences between '{url1}' and '{url2}':\n\n")
    for line in diff:
        if line.startswith("-"):
            file.write("Original: " + line[2:] + "\n")
        elif line.startswith("+"):
            file.write("Compare: " + line[2:] + "\n")

print(f"The differences have been saved to '{filename}'.")
