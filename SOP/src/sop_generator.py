import os
import csv


SOP_FILEPATH = 'src/sop_template.tex'
REFERENCES_FILEPATH = 'references.bib'
OUTPUT_PATH = 'src/build/'
sop, references = None, None
universities = []

# Default LaTeX variables.
variables = {
    '\\hw': 'Heriot-Watt University',
    '\\supervisor': '\\textbf{Professor Neamat El Gayar}',
    '\\project': 'Multi-Element Association Rule Derivation from Minimum Spanning Trees'
}


def read_universities():
    global universities
    with open('universities.csv', 'r') as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader):
            if i == 0:
                pass
            universities.append(row)

 
def init():
    global sop, references, universities
    # Read in document
    with open(SOP_FILEPATH, 'r') as f:
        sop = f.read()
        # sop = sop.replace('\\ ', ' ')

    # Read in docuemnts
    with open(REFERENCES_FILEPATH, 'r') as f:
        references = f.read()

    # Write out references
    with open(f'{OUTPUT_PATH}/references.bib', 'w+') as f:
        f.write(references)

    # Read in universities
    read_universities()

    # Move into src directory
    os.chdir(OUTPUT_PATH)


def make_pdf(university_details):
    
    # Merge two dictionaries in the local scope
    commands = variables.copy()
    commands.update(university_details)

    # Extract university name
    university = commands['\\uni']
    # Add 'the' prefix if first word is University
    if university.lower().split(' ')[0] == 'university':
        commands['\\uni'] = f'the {university}'

    # LaTeX commands string to prefix
    latex_commands = ''
    for key, value in commands.items():
        latex_commands += '\\newcommand{'+key+'}{'+value+'}\n'
    
    
    university = university.replace(' ', '_')
    # Write out .tex file
    output_file = f'{university}.tex'
    with open(output_file, 'w+') as f:
        f.write(latex_commands + sop)
    
    # PdfLatex + Biber + PdfLatex (x2)
    pdflatex = f'pdflatex -synctex=1 -interaction=nonstopmode -shell-escape {output_file}'
    biber = f'biber {university}'
    compilation = [pdflatex, biber, pdflatex, pdflatex]
    print(f'Currently in {os.getcwd()}')

    for cmd in compilation:
        print(f'Running `{cmd}`')
        os.system(cmd)
    
    # Move pdf to compile folder
    os.system(f'mv {university}.pdf compiled/')
    # Clear build folder
    build_file_extensions = ['aux', 'bbl', 'bcf', 'blg', 'log', 'run.xml', 'synctex.gz']
    for extension in build_file_extensions:
        os.system(f'rm *.{extension}')



if __name__ == '__main__':
    init()
    for uni in universities:
        make_pdf(uni)

    



