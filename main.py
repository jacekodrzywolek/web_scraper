import difflib
from datetime import datetime
import os
from src.web_scaper import fetch_text, sanitize_filename, get_output_folder

results_folder = get_output_folder()


def main():
    """
    Main function of the program.
    """
    url1 = input("Enter the URL for the original website: ")
    url2 = input("Enter the URL for the website to compare: ")

    text1 = fetch_text(url1)
    text2 = fetch_text(url2)

    differ = difflib.Differ()
    diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{sanitize_filename(url1)}_differences.txt"

    with open(os.path.join(results_folder, filename), "w", encoding="utf-8") as file:
        file.write(f"Differences between '{url1}' and '{url2}':\n\n")
        original_line_num = 0
        compare_line_num = 0
        differences_found = False
        for line in diff:
            if line.startswith("- "):
                differences_found = True
                original_line_num += 1
                file.write("---------------------------------------------------------\n")
                file.write(f"Original ({original_line_num}): {line[2:]}\n")
            elif line.startswith("+ "):
                differences_found = True
                compare_line_num += 1
                file.write(f"Compare ({compare_line_num}): {line[2:]}\n")
                original_text = line[2:]
                compare_text = line[2:]
                differences = list(difflib.ndiff([original_text], [compare_text]))
                for diff_line in differences:
                    if diff_line.startswith("? "):
                        file.write(f"Difference: {diff_line[2:]}\n")
                file.write("---------------------------------------------------------\n")

        if not differences_found:
            file.write("No differences found between the webpages.\n")

    print(f"The differences have been saved to '{filename}'.")


if __name__ == "__main__":
    main()
