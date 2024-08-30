def filter_emails(input_file, output_file):
    # Set of image file extensions to filter out
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.webp'}
    
    # Set of programming and sensitive file extensions to filter out
    programming_extensions = {
        '.js', '.py', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.swift', 
        '.go', '.ts', '.pl', '.sh', '.bat', '.html', '.css', '.xml', 
        '.jsp', '.asp', '.aspx', '.ps1', '.r', '.kt', '.scala', '.vb',
        '.exe', '.dll', '.bin', '.cmd', '.vbs', '.bash', '.zsh',
        '.conf', '.ini', '.json', '.yaml', '.yml', '.config', 
        '.env', '.password', '.key', '.pem', '.crt', '.cer'
    }

    # Read emails from the input file and filter them
    try:
        with open(input_file, 'r') as infile:
            emails = set(line.strip() for line in infile if line.strip())  # Remove duplicates and empty lines
    except FileNotFoundError:
        print(f"[-] Error: '{input_file}' file not found.")
        return

    # Filter out .gov emails (case-insensitive) and emails ending with image, programming, or sensitive file extensions
    filtered_emails = set()
    for email in emails:
        domain = email.split('@')[-1].lower()  # Convert domain to lowercase
        if not domain.endswith('.gov') and not any(email.lower().endswith(ext) for ext in image_extensions | programming_extensions):
            filtered_emails.add(email)

    # Save the filtered emails to the output file
    with open(output_file, 'w') as outfile:
        for email in sorted(filtered_emails):
            outfile.write(email + '\n')

    print(f"[+] Filtered {len(filtered_emails)} emails saved to '{output_file}'.")


if __name__ == "__main__":
    # Input and output file names
    input_filename = 'total.txt'
    output_filename = 'filtered_emails.txt'

    # Run the email filtering function
    filter_emails(input_filename, output_filename)
