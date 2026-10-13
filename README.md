
# Python Data Analysis: Student Performance Exploration

A beginner-friendly Python data analysis project that explores
student scores, study hours, and attendance using a synthetic dataset.

## Features

- Generate a reproducible sample CSV dataset
- Load and clean student performance data with Pandas
- Calculate mean, median, minimum, and maximum scores
- Identify students scoring below a configurable threshold
- Calculate the correlation between study hours and scores
- Compare average scores across study-hour groups
- Create a scatter plot using Matplotlib
- Export cleaned data and analysis summaries to CSV files

## Tech Stack

- Python 3.10+
- Pandas
- Matplotlib

## Project Structure

```text
student-performance-analysis/
├── student_performance.py
├── student_performance.csv
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/
    ├── cleaned_student_data.csv
    ├── performance_summary.csv
    ├── study_group_summary.csv
    └── study_hours_vs_score.png
```

The CSV file is generated automatically if it does not exist.
Output files are created when the analysis runs.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-analysis.git
cd student-performance-analysis
```

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Analysis

```bash
python student_performance.py
```

The program prints its findings in the terminal and saves
CSV summaries and a scatter plot in the `outputs/` folder.

## Analysis Questions

1. What is the average student score?
2. Which students scored below the selected threshold?
3. Is there a relationship between study hours and scores?
4. How do average scores differ across study-hour groups?
5. What limitations should be considered when interpreting the results?

## Dataset

The default dataset is synthetic and is intended for learning
and testing. It does not represent real student outcomes.

You can replace it with a CSV containing these columns:

- student_id
- study_hours
- attendance_percentage
- score

## Limitations

- Synthetic data may not reflect real-world student behavior.
- Correlation does not establish causation.
- The dataset is small and may not represent a wider population.
- The selected score threshold is a configurable analysis choice.
- The analysis does not account for other factors that influence performance.

## Future Improvements

- Add more exploratory data visualizations.
- Analyze missing values and outliers in more depth.
- Add unit tests and automated validation.
- Build an interactive dashboard with Streamlit.

## Author

Varada Surendra Naidu
