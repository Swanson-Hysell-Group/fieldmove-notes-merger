# fieldmove-notes-merger

This repository contains a Jupyter notebook **combine_notes.ipynb** (developed using a Python 3 kernel) that merges and sorts .csv files created by Fieldmove, discards unnecessary fields, then outputs the result to a presentable LaTeX document.

Outputs:
* **all_notes.csv**
* **all_notes_filtered.csv**
* **latexoutput.tex**

The notebook is well documented and can be readily executed from start to finish - however, user input is required at 3 stages (all clearly marked in the notebook):
* First, the user must set the variable *folder_path* to the path which leads to the directory in which the Fieldmove .csv’s are stored.
* Second, the user must input their name and a desired title for the final LaTeX document.
* Third, the user must compile the resulting **latexoutput.tex** in a .tex compiler of their choice.

All output files will be created in the same directory in which the Fieldmove .csv’s are stored.
