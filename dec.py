import os

def convert_to_6_decimal(input_filename, output_filename):
    # Open the input file for reading
    with open(input_filename, 'r') as input_file:
        # Read lines from the input file
        lines = input_file.readlines()
        
        # Process each line
        formatted_lines = []
        for line in lines:
            # Split the line into the first element and the rest of the elements
            parts = line.split(maxsplit=1)
            first_element = parts[0]
            rest_elements = parts[1] if len(parts) > 1 else ''
            
            # Split the rest of the elements into individual numbers
            numbers = rest_elements.split()
            
            # Convert and format each number to 6 decimal places
            formatted_numbers = [f'{float(number):.6f}' for number in numbers]
            
            # Join the formatted numbers with spaces and combine with the first element
            formatted_line = first_element + ' ' + ' '.join(formatted_numbers)
            
            # Append the formatted line to the list
            formatted_lines.append(formatted_line)
    
    # Write the formatted lines to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write('\n'.join(formatted_lines))

def process_directory(input_directory, output_directory):
    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            # Construct full paths for input and output files
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename)
            
            # Perform conversion
            convert_to_6_decimal(input_file, output_file)

# Example usage
input_directory = '.'   # Change this to your input folder path
output_directory = '.' # Change this to your output folder path
process_directory(input_directory, output_directory)
