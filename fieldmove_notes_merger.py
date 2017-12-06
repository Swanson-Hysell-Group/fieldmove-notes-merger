# Data collected with the Fieldmove Clino app in the field can be exported into
# a number of discrete .csv files. The following code:
#   - imports these files into pandas dataframes
#   - combines these dataframes into a single dataframe
#   - filters the dataframe to only include data fields that are particularly relevant
#   - exports this filtered dataframe as a LaTeX table

# print a welcome message
print('')
print('WELCOME TO FIELDMOVE-NOTES-MERGER.')
print('')
print('Follow the prompts:')
print('')

# import necessary modules
import os
import pandas as pd
from dateutil.parser import parse
from numpy import zeros

# prompt user for directory path
print('> USER INPUT REQURED:')
folder_path = input('Enter the path to the .fm folder exported by Fieldmove Clino (e.g. /Users/yuempark/Documents/Berkeley/Research_China/FieldMove/project1.fm): ')
print('')

# read in the data
image = pd.read_csv(folder_path + '/image.csv')
note = pd.read_csv(folder_path + '/note.csv')
plane = pd.read_csv(folder_path + '/plane.csv')
line = pd.read_csv(folder_path + '/line.csv')

# print the number of entries in each file
print('image.csv imported with ' + str(image.shape[0]) + ' entries.')
print('note.csv imported with ' + str(note.shape[0]) + ' entries.')
print('plane.csv imported with ' + str(plane.shape[0]) + ' entries.')
print('line.csv imported with ' + str(line.shape[0]) + ' entries.')
print('')

# concatenate and sort
all_notes = pd.concat((image, note, plane, line))
all_notes['time'] = pd.to_datetime(all_notes[' timedate'])
all_notes.sort_values(by='time',inplace=True)
all_notes.reset_index(inplace=True)

# output to 'all_notes.csv', without any filtering
all_notes.to_csv(os.path.join(folder_path,r'all_notes.csv'),index=False)

# notify user of saved file
print('All notes concatenated and saved to all_notes.csv.')
print('')

# select columns that we want in our final LaTeX document
if ' localityName' in all_notes.columns:
    filtered_notes = all_notes[['time',
                                ' latitude',
                                ' longitude',
                                ' localityName',
                                ' notes',
                                ' image name',
                                ' heading',
                                ' planeType',
                                ' dipAzimuth',
                                ' dip',
                                ' lineationType',
                                ' plungeAzimuth',
                                ' plunge',
                                ' rockUnit',
                                ' declination']]

else:
    fill = zeros((all_notes.shape[0],1))
    all_notes[' localityName'] = fill
    filtered_notes = all_notes[['time',
                                ' latitude',
                                ' longitude',
                                ' localityName',
                                ' notes',
                                ' image name',
                                ' heading',
                                ' planeType',
                                ' dipAzimuth',
                                ' dip',
                                ' lineationType',
                                ' plungeAzimuth',
                                ' plunge',
                                ' rockUnit',
                                ' declination']]

# output to 'all_notes_filtered.csv':
filtered_notes.to_csv(os.path.join(folder_path,r'all_notes_filtered.csv'), index=False)

# notify user of saved file
print('All notes filtered and saved to all_notes_filtered.csv.')
print('')

# now convert notes to a LaTeX format

# first, input the necessary frontmatter (packages, etc.):
frontmatter = r'\documentclass[11pt]{article}' + '\n' +\
              r'\usepackage{amsmath}' + '\n' +\
              r'\usepackage{amsfonts}' + '\n' +\
              r'\usepackage{amssymb}' + '\n' +\
              r'\usepackage{wasysym}' + '\n' +\
              r'\usepackage{graphicx}' + '\n' +\
              r'\usepackage{pslatex}' + '\n' +\
              r'\usepackage{lscape}' + '\n' +\
              r'\usepackage[T1]{fontenc}' + '\n' +\
              r'\usepackage[latin1]{inputenc}' + '\n' +\
              r'\usepackage{fancyhdr}' + '\n' +\
              r'\usepackage{lastpage}' + '\n' +\
              r'\usepackage[english]{babel}' + '\n' +\
              r'\usepackage[usenames, dvipsnames]{color}' + '\n' +\
              r'\usepackage{color}' + '\n' +\
              r'\usepackage{booktabs}' + '\n' +\
              r'\usepackage{longtable}' + '\n' +\
              r'\usepackage{geometry}' + '\n' +\
              r'\geometry{hmargin={0.75in,0.75in},vmargin={1in,1in}}' + '\n'

# prompt user for a title for the notes:
print('> USER INPUT REQURED:')
titleIn = input('Enter the year and field area: ')
authorIn = input('Enter your name: ')
print('')
title = r'\title{' + titleIn + r' Fieldmove Notes' + r'}' + '\n' +\
        r'\author{' + authorIn + r'}' + '\n' +\
        r'\date{\vspace{-5ex}}' + '\n'

# prompt user for the directory of the images:
imageIn = input('Enter the folder name that contains your images (e.g. image_thumbnails): ')
print('')

# create a header for each page:
header = r'\pagestyle{fancy}' + '\n' +\
         r'\rhead {\emph{\textcolor{blue}{' + authorIn + r'}, \thepage ~of \pageref{LastPage}}}' + '\n' +\
         r'\lhead{' + titleIn + r'}' + '\n' +\
         r'\cfoot{}' + '\n' +\
         r'\renewcommand{\headrulewidth}{0.4pt}' + '\n'

# some more necessary LaTeX commands before starting the table:
start = r'\begin{document}' + '\n' +\
        r'\maketitle' + '\n' +\
        r'Summary of field notes made on an iPad using the Fieldmove app.' +\
        r' All coordinates are in WGS84.' +\
        r' Plane dip directions and line azimuths are corrected for local magnetic declination.' + '\n' +\
        r'\begin{longtable}{lllr}' + '\n' +\
        r'\endhead' + '\n' +\
        r'\endfoot' + '\n' +\
        r'\endlastfoot' + '\n'

# necessary LaTeX commands after the table ends:
end = r'\end{longtable}' + '\n' +\
      r'\end{document}'

# a little function to make text bold:
def bold(string):
    out = r'\textbf{' + string + '}'
    return out

# generate the main body of the LaTeX code:
# note that certain special characters need special treatment, otherwise LaTeX will fail to compile.
body = ''

for i in range(filtered_notes.shape[0]-1):
    entry = ''

    entry += r'\hline' + '\n'
    entry += r'$_{' + str(i+1) + r'}$&&&\\' + '\n'
    entry += bold('time:') + ' ' + str(filtered_notes['time'][i]) + r' & '
    entry += bold('lat:') + ' ' + str(filtered_notes[' latitude'][i]) + r' & '
    entry += bold('lon:') + ' ' + str(filtered_notes[' longitude'][i]) + r' & '

    # if we have locality data, include it
    if filtered_notes[' localityName'][i] != 0:
        entry += bold('locality:') + ' ' + str(filtered_notes[' localityName'][i]) + r' \\' + '\n'
    else:
        entry += r'\\' + '\n'

    # always include notes
    entry += r'\multicolumn{4}{p{6.5 in}}{'
    entry += bold('note:') + ' ' + str(filtered_notes[' notes'][i]) + r'} \\' + '\n'

    # if we have photos, include it
    try:
        temp = filtered_notes[' image name'][i].split('_') #special character
        # some images have weird names - make sure the full name is included
        temp_entry = temp[0]
        for j in range(1, len(temp)):
            temp_entry += r'\_' + temp[j]
        entry += bold('image:') + ' ' + temp_entry + r' & '
        entry += bold('heading:') + ' ' + str(round(filtered_notes[' heading'][i],1)) + r' & '
        entry += r'& '
        entry += '\includegraphics[width=2 in]{' + imageIn + '/' +  filtered_notes[' image name'][i].strip() + '}'
        entry += r' \\' + '\n'
    except:
        pass

    # if we have a formation name, include it
    if str(filtered_notes[' rockUnit'][i]) == 'nan':
        pass
    else:
        entry += bold('fm:') + ' ' + str(filtered_notes[' rockUnit'][i]) + r' & '
        entry += r'& & \\' + '\n'

    # if we have plane data, include it
    if str(filtered_notes[' dip'][i]) == 'nan':
        pass
    else:
        entry += bold('plane:') + ' ' + str(filtered_notes[' planeType'][i]) + r' & '
        entry += bold('dip:') + ' ' + str(round(filtered_notes[' dip'][i],1)) + r' & '
        entry += bold('dip dir.:') + ' ' + str(round(filtered_notes[' dipAzimuth'][i],1)) + r' & '
        entry += r'\\' + '\n'
        entry += bold('mag. dec.:') + ' ' + str(round(filtered_notes[' declination'][i],1)) + r' & '
        entry += r'& & \\' + '\n'

    # if we have line data, include it
    if str(filtered_notes[' plunge'][i]) == 'nan':
        pass
    else:
        entry += bold('line:') + ' ' + str(filtered_notes[' lineationType'][i]) + r' & '
        entry += bold('plunge:') + ' ' + str(round(filtered_notes[' plunge'][i],1)) + r' & '
        entry += bold('azimuth:') + ' ' + str(round(filtered_notes[' plungeAzimuth'][i],1)) + r' & '
        entry += bold('mag. dec.:') + ' ' + str(round(filtered_notes[' declination'][i],1))
        entry += r'\\' + '\n'

    body += entry

body += r'\hline' + '\n'

# special characters
body = body.replace('%',r'\%')
body = body.replace('<',r'$<$')
body = body.replace('>',r'$>$')
body = body.replace('~',r'\textasciitilde')
body = body.replace('#',r'\#')

# combine all the strings, and prepare for output into a .tex file:
toLatex = frontmatter + header + title + start + body + end

# output to 'latexoutput.tex':
afile = open(os.path.join(folder_path,r'latexoutput.tex'), 'wt')
afile.write(toLatex)

# print a final message to compile
print('Open latexoutput.tex with your favourite .tex editor and compile! latexoutput.pdf is the final product.')
print('')
