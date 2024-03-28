# Natural Disaster Data Analysis Project
## Summary
This project was created for the Software Design midterm project, Spring 2024.

The Natural Disaster Data Analysis Project analyzes government data on the most
expensive natural disasters in the US from 1980 to 2023. The code requests,
extracts, and organizes data on natural disasters by location, year, and
disaster type. The code also sorts information on the monetary cost and total
deaths resulting from each natural disaster and generates graphs to visualize
the data. All of the information on the project is explained in the form of a
computational essay.

The central product of this project is the computational essay, which can be
found in comp_essay.ipynb. This file intersperses code throughout an 
academically structured essay that walks readers through the research question,
methodology, results, and interpretation of this data science project.

The functions that request and extract the dataset can be found in
fetch_data.py. The functions that process the original dataset into more easily
graphable and analyzable formats can be found in process_data.py. Finally, the
functions that generate plots of the processed data are in graph_data.py.

The simplest way to interact with this project is to run the comp_essay.ipynb
file and read the computational essay. For those who are especially interested
in the methodology of accessing, processing, and graphing the data, reading
the three .py files will also be interesting.

## Libraries and other Requirements
### Imported Libraries
We imported the following libaries for this project:
- requests (to access the dataset from the Internet)
- tarfile (to extract the data from its compressed format)
- math (to aid in the numerical analysis of the data)
- pandas (to organize data in the form of dataframes)

### System Tools
This project was created in VSCode in Python 3.11.8 and uses Jupyter Notebooks.
Users should be sure that their Python is up to date and can handle .ipynb
files. For more information, users can look at the Software Design
Computational Setup: https://softdes.olin.edu/docs/setup/setup-instructions/

### Other Requirements
For additional information, please look at the requirements.txt file. This file
was generated using code provided by the Software Design teaching team.

## Recreating This Project
### Accessing the Data
The dataset used in this project was programatically retrieved from the data
catalogues of the US Government. The link to this data can be found at their
website: https://catalog.data.gov/dataset/u-s-billion-dollar-weather-and-climate-disasters-1980-present-ncei-accession-02092681

The code used to request and extract this dataset programatically can be found
in the file fetch_data.py. Additionally, relevant functions are run in the
comp_essay.ipynb file for ease of access.

### Processing the Data
The code used to process the dataset into a useful and graphable data structure
can be found in the file process_data.py. Additionally, relevant functions are
run in the comp_essay.ipynb file for ease of access.

### Graphing the Data
The code used to generate visual plots of the processed data can be found in
the file graph_data.py. Additionally, the graphs themselves are generated in
the comp_essay.ipynb file for ease of access.