###Traer todas las constnates del codigo para crear una clase con los nombres y tratamientos

import re
import os

# Define the directory containing the .py files
directory = './'

# Regex to match "tratamiento = [value]" expressions
tratamiento_regex = r'tratamiento\s*=\s*(.*)'

# Create an empty set to store the treatments
treatments = set()

# Loop over all .py files in the directory
for filename in os.listdir(directory):
    if filename.endswith('Evaluar.py'):
        # Open the file and read the contents
        with open(os.path.join(directory, filename), 'r') as f:
            file_contents = f.read()

        # Use the regular expression to find all "tratamiento = [value]" expressions in the file
        tratamiento_matches = re.findall(tratamiento_regex, file_contents)

        # Add the treatments to the set
        for tratamiento_match in tratamiento_matches:
            treatments.add(tratamiento_match)

# Define a class to hold the treatments
class Tratamientos:
    pass

# Add the treatments as class attributes
for i, tratamiento in enumerate(treatments):
    setattr(Tratamientos, f'tratamiento_{tratamiento}', tratamiento)

# Print the treatments as class attributes
print(Tratamientos.__dict__)


