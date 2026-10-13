
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# -------------------- CONFIGURATION --------------------

DATA_FILE = Path("student_performance.csv")
OUTPUT_DIR = Path("outputs")
PASS_THRESHOLD = 50

OUTPUT_DIR.mkdir(exist_ok=True)


# -------------------- DATA GENERATION --------------------

def create_sample_dataset():
    """Create a reproducible synthetic student dataset."""
    data = {
        "student_id": list(range(1, 21)),
        "study_hours": [
            1, 2, 3, 4, 5, 6, 2, 7, 8, 3,
            5, 9, 4, 6, 10, 1, 7, 8, 3, 9
        ],
        "attendance_percentage": [
            60, 65, 70, 75, 80, 85, 55, 90, 95, 68,
            78, 92, 72, 83, 98, 50, 88, 91, 66, 94
        ],
        "score": [
            35, 42, 48, 55, 62, 75, 38, 80, 88, 46,
            65, 92, 52, 73, 96, 30, 78, 85, 44, 90
        ],
    }

    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)
    print(f"Sample dataset created: {DATA_FILE}")

    return df


# -------------------- DATA LOADING --------------------

def load_dataset():
    """Load the CSV or create a sample dataset if missing."""
    if not DATA_FILE.exists():
        return create_sample_dataset()

    df = pd.read_csv(DATA_FILE)

    required_columns = {
        "student_id",
        "study_hours",
        "attendance_percentage",
        "score",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing)}"
        )

    return df


# -------------------- DATA CLEANING --------------------

def clean_dataset(df):
    """Validate numeric columns and remove invalid records."""
    df = df.copy()

    numeric_columns = [
        "student_id",
        "study_hours",
        "attendance_percentage",
        "score",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    original_count = len(df)

    df = df.dropna(subset=numeric_columns)
    df = df.drop_duplicates(subset=["student_id"])

    df = df[
        (df["study_hours"] >= 0)
        & (df["attendance_percentage"].between(0, 100))
        & (df["score"].between(0, 100))
    ].copy()

    print(f"Rows before cleaning: {original_count}")
    print(f"Rows after cleaning: {len(df)}")

    if df.empty:
        raise ValueError("No valid student records remain after cleaning.")

    return df


# -------------------- DATA ANALYSIS --------------------

def analyze_performance(df):
    """Summarize scores and identify students below the threshold."""
    print("\n" + "=" * 45)
    print("STUDENT PERFORMANCE ANALYSIS")
    print("=" * 45)

    print(f"\nNumber of students: {len(df)}")
    print(f"Average score: {df['score'].mean():.2f}")
    print(f"Median score: {df['score'].median():.2f}")
    print(f"Highest score: {df['score'].max():.2f}")
    print(f"Lowest score: {df['score'].min():.2f}")
    print(f"Average study hours: {df['study_hours'].mean():.2f}")
    print(
        "Average attendance: "
        f"{df['attendance_percentage'].mean():.2f}%"
    )

    below_threshold = df[df["score"] < PASS_THRESHOLD]

    print(f"\nStudents scoring below {PASS_THRESHOLD}:")
    if below_threshold.empty:
        print("No students found below the threshold.")
    else:
        print(
            below_threshold[
                ["student_id", "study_hours", "score"]
            ].to_string(index=False)
        )

    correlation = df["study_hours"].corr(df["score"])

    print(f"\nStudy hours vs score correlation: {correlation:.3f}")

    if pd.isna(correlation):
        print("The correlation could not be calculated.")
    elif correlation > 0:
        print("The dataset shows a positive relationship.")
    elif correlation < 0:
        print("The dataset shows a negative relationship.")
    else:
        print("The dataset shows no linear relationship.")

    # Compare score averages across study-hour groups.
    df["study_group"] = pd.cut(
        df["study_hours"],
        bins=[-1, 3, 6, float("inf")],
        labels=["0-3 hours", "4-6 hours", "7+ hours"],
    )

    group_summary = df.groupby(
        "study_group", observed=False
    )["score"].agg(["count", "mean"])

    print("\nAverage score by study-hour group:")
    print(group_summary.round(2).to_string())

    # Save cleaned data and summary.
    df.to_csv(OUTPUT_DIR / "cleaned_student_data.csv", index=False)
    group_summary.to_csv(OUTPUT_DIR / "study_group_summary.csv")

    summary = pd.DataFrame({
        "metric": [
            "student_count",
            "average_score",
            "median_score",
            "highest_score",
            "lowest_score",
            "average_study_hours",
            "average_attendance_percentage",
            "students_below_threshold",
            "study_hours_score_correlation",
        ],
        "value": [
            len(df),
            df["score"].mean(),
            df["score"].median(),
            df["score"].max(),
            df["score"].min(),
            df["study_hours"].mean(),
            df["attendance_percentage"].mean(),
            len(below_threshold),
            correlation,
        ],
    })

    summary.to_csv(OUTPUT_DIR / "performance_summary.csv", index=False)

    return df


# -------------------- VISUALIZATION --------------------

def create_scatter_plot(df):
    """Visualize study hours against student scores."""
    plt.figure(figsize=(9, 6))

    plt.scatter(
        df["study_hours"],
        df["score"],
        alpha=0.8,
    )

    plt.title("Student Study Hours vs Performance Score")
    plt.xlabel("Study Hours")
    plt.ylabel("Score (out of 100)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plot_path = OUTPUT_DIR / "study_hours_vs_score.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"\nScatter plot saved to: {plot_path}")


# -------------------- MAIN PROGRAM --------------------

def main():
    df = load_dataset()
    df = clean_dataset(df)
    df = analyze_performance(df)
    create_scatter_plot(df)

    print("\nAnalysis completed successfully.")
    print(f"Check the '{OUTPUT_DIR}' folder for output files.")


if __name__ == "__main__":
    main()
