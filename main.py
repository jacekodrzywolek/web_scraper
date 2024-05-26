import difflib
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

    filename = f"{sanitize_filename(url1)}_differences.txt"

    with open(results_folder + filename, "w", encoding="utf-8") as file:
        file.write(f"Differences between '{url1}' and '{url2}':\n\n")
        for line in diff:
            if line.startswith("-"):
                file.write(f"Original: {line[2:]}" + "\n")
            elif line.startswith("+"):
                file.write(f"Compare: {line[2:]}" + "\n")

    print(f"The differences have been saved to '{filename}'.")


if __name__ == "__main__":
    main()
