# Data Engineering Takehome Exam

This Github repo is my submission for the Statistics Canada Data Science Fellowship Program's Takehome Exam. I chose the Data Engineering stream, and my solutions to the individual tasks are entirely contained here. This readme contains instructions on how to run the code for each task, as well as any required documentation.

## Dependencies

I've included a `requirements.txt` that you can use to install required Python dependencies. I'll be using Python 3.10.8 for this assignment.

## Installation

The following installation instructions are intended for use on macOS 12.5.1, but should be adaptable to other versions / operating systems. It is assumed that you have Python, pip, and python-tk already installed.

Run the following in your console in the root of this repository:

```
pip install -r requirements.txt
```

## Usage

### Task 1
```
python3.10 download_data.py
```
You should see console output as the data for each month (January - November of 2022) downloads and extracts to your hard drive.

### Task 2

```
python3.10 create_mapping.py
```

You should see console output as the mapping for each variable of interest for each month of the downloaded data is created and saved to disk.

#### Worth Noting

- There was a typo in one of the column names ("Start / Fin" instead of "End / Fin") for January - April. This doesn't have any effect on this or any other tasks, though.
- I noticed that later tasks required additional variables to be mapped, so I added these later and left comments in the file.
- I noticed that several variable names had leading and/or trailing whitespace that was affecting my work in later tasks, so I stripped these out as I can't see any reason to keep it.

## Task 3

```
python3.10 apply_mapping_and_merge_data.py
```

You should see console output as individual datasets are mapped and then merged into a final output dataset.

### Worth Noting
- The task asks for data to be output in a certain schema with a certain specification. Upon looking at later tasks, I realized that this requested schema / specification would NOT be enough to complete said tasks. I took the intitiative to modify the output of this task so that future tasks wouldn't need to redo some of the work in this task. I'm unsure if this was a mistake in the assignment itself, or to check whether we are able to assess business requirements and adjust accordingly. I'm assuming it's the latter.

## Task 4

```
python3.10 tracking_goal_eight.py
```

For each question, you should see console output containing requested table and visualization. To show the results for the next question, close the visualization window.

## Task 5
For this task, I decided to pursue indicator 5.5.2 (Proportion of women in managerial positions) as I felt it would be the most likely to be easily solvable with the given dataset. I would love to dive into 5.4.1 (Proportion of time spent on unpaid domestic and care work, by sex, age and location) in the future, but I felt due to time considerations, 5.5.2 would be the best choice for now.

```
python 3.10 tracking_goal_five.py
```

You will see a table showing `% in Management` by `Sex`, as well as a bar graph visualizing the same data. As is clear from the data (men are in managerial positions at a rate almost double that of women), we have quite a ways to go.

# Future Work
## Weights

I noticed that there was a variable showing weight for records, and I did not incorporate those weights into this analysis.

## Converting from a collection of scripts to a library

Right now, my code is a collection of scripts. I would normally factor these scripts into data pipeline stages, each containing a set of processing functions, as well as its own schematized input and output. This would allow for unit testing as well as enforcing schema and data quality checks.

## Testing

As mentioned above, I didn't write any tests as I wasn't sure what was expected here given the timeframe. Unit tests allow for easy incremental changes to bits and pieces of the pipeline, without being afraid of breaking other parts. The data scientist writes sample input and output data for each stage, and tests those changes both locally before pushing out code, and also automatically as part of CI/CD steps. This is a standard best practice in industry, but I didn't feel like the timeframe given for the project would allow me to do a good job of this. 

## Schematization & Data Quality Checks
As mentioned above, I would normally put more effort into enforcing pipeline stage schema and data quality checking, but again, the timeframe of this project limited the practicality of that.