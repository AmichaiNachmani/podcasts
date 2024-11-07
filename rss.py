from datetime import datetime
import xml.etree.ElementTree as ET

# Prompt user for the input and output file names
input_file = input("Enter the name of the RSS file (e.g., feed.xml): ")
output_file = input("Enter the name for the corrected output file (e.g., corrected_feed.xml): ")

# Load and parse the XML file
try:
    tree = ET.parse(input_file)
    root = tree.getroot()
except FileNotFoundError:
    print(f"File {input_file} not found.")
    exit()

# Function to format date
def format_date(date_str):
    # Parse the old format date string
    parsed_date = datetime.strptime(date_str, "%d %b %y %H:%M %z")
    # Format to RFC 2822
    return parsed_date.strftime("%a, %d %b %Y %H:%M:%S %z")

# Loop over each item and update pubDate
for item in root.findall(".//item"):
    pubDate = item.find("pubDate")
    if pubDate is not None:
        try:
            # Update the pubDate with correct format
            pubDate.text = format_date(pubDate.text)
        except ValueError:
            print(f"Skipping invalid date format: {pubDate.text}")

# Save the updated XML file
tree.write(output_file, encoding="UTF-8", xml_declaration=True)
print(f"Updated RSS feed saved to {output_file}")
