from datetime import datetime
import os
import configparser
from src.web_scraper import fetch_text, sanitize_filename, get_output_folder

results_folder = get_output_folder()
config = configparser.ConfigParser()
config.read("config/config.ini")
is_testing = config["testing"].getboolean("is_testing")


def remove_empty_lines(text_lines):
    # Remove all empty lines
    return [line for line in text_lines if line.strip()]


def write_differences(file, original, compare):
    file.write("Differences between the original and comparison files:\n\n")
    for line_count, (orig_line, comp_line) in enumerate(zip(original, compare), start=1):
        if orig_line != comp_line:
            file.write("---------------------------------------------------------\n")
            file.write(f"Original ({line_count}): {orig_line}\n")
            file.write(f"Compare ({line_count}): {comp_line}\n")
            file.write(f"Difference: -{orig_line}+{comp_line}\n")
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

    text1 = remove_empty_lines(text1)
    text2 = remove_empty_lines(text2)

    # Ensure that both texts have the same number of lines by padding the shorter one
    while len(text1) < len(text2):
        text1.append("")
    while len(text2) < len(text1):
        text2.append("")

    # Save raw text if needed
    save_raw_text(is_saving_raw, text1, text2)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{sanitize_filename(url1)}_vs_{sanitize_filename(url2)}_{timestamp}.txt"

    with open(os.path.join(results_folder, filename), "w", encoding="utf-8") as file:
        write_differences(file, text1, text2)

    print(f"The differences have been saved to '{filename}'.")


if __name__ == "__main__":
    main()
