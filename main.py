import difflib
from datetime import datetime
import os
import configparser
from src.web_scraper import fetch_text, sanitize_filename, get_output_folder

results_folder = get_output_folder()
config = configparser.ConfigParser()
config.read("config/config.ini")
is_testing = config["testing"].getboolean("is_testing")


def clean_text(text_lines):
    # Remove all empty lines and lines that are only whitespace, and strip each line
    return [line.strip() for line in text_lines if line.strip()]


def write_differences(file, unmatched_lines):
    file.write("Unmatched lines from the original file:\n\n")
    for line in unmatched_lines:
        file.write("---------------------------------------------------------\n")
        file.write(f"{line}\n")
        file.write("---------------------------------------------------------\n")


def save_raw_text(is_saving_raw, original_lines, compare_lines):
    if is_saving_raw:
        with open(os.path.join(results_folder, "original_raw.txt"), "w", encoding="utf-8") as file:
            file.write("\n".join(original_lines))
        with open(os.path.join(results_folder, "compare_raw.txt"), "w", encoding="utf-8") as file:
            file.write("\n".join(compare_lines))


def main():
    """
    Main function of the program.
    """
    is_saving_raw = config["settings"].getboolean("is_saving_raw")

    if is_testing:
        url1 = "https://docs.python.org/3.8/library/stdtypes.html#dict"
        url2 = "https://docs.python.org/3.9/library/stdtypes.html#dict"
    else:
        url1 = input("Enter the URL for the original website: ")
        url2 = input("Enter the URL for the website to compare: ")

    text1 = fetch_text(url1).splitlines()
    text2 = fetch_text(url2).splitlines()

    text1 = clean_text(text1)
    text2 = clean_text(text2)

    # Save raw text if needed
    save_raw_text(is_saving_raw, text1, text2)

    unmatched_lines = [line for line in text1 if line not in text2]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{sanitize_filename(url1)}_vs_{sanitize_filename(url2)}_{timestamp}.txt"

    with open(os.path.join(results_folder, filename), "w", encoding="utf-8") as file:
        write_differences(file, unmatched_lines)

    print(f"The differences have been saved to '{filename}'.")


if __name__ == "__main__":
    main()
