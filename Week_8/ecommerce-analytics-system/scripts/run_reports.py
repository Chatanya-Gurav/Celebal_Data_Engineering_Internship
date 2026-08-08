import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_DIR = BASE_DIR / "sql"
OUTPUT_DIR = BASE_DIR / "output" / "sample_reports"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# SQL Files
# ---------------------------------------------------------

SQL_FILES = [
    "basic_queries.sql",
    "intermediate_queries.sql",
    "advanced_queries.sql",
    "cohort_analysis.sql"
]


# ---------------------------------------------------------
# Remove SQL Comments
# ---------------------------------------------------------

def remove_sql_comments(sql_text):
    lines = sql_text.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        # Skip full-line comments
        if stripped.startswith("--"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ---------------------------------------------------------
# Execute SQL File
# ---------------------------------------------------------

def execute_sql_file(connection, sql_file):

    sql_path = SQL_DIR / sql_file

    print(f"\nRunning: {sql_file}")

    sql_text = sql_path.read_text(
        encoding="utf-8"
    )

    # Remove comments correctly
    sql_text = remove_sql_comments(sql_text)

    # Split SQL statements
    statements = [
        statement.strip()
        for statement in sql_text.split(";")
        if statement.strip()
    ]

    output_file = OUTPUT_DIR / (
        sql_file.replace(
            ".sql",
            "_output.txt"
        )
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as output:

        output.write(
            "E-COMMERCE ANALYTICS REPORT\n"
        )

        output.write(
            f"SQL FILE: {sql_file}\n"
        )

        output.write(
            "=" * 80
        )

        output.write("\n\n")

        report_number = 1

        for statement in statements:

            # Ignore PRAGMA
            if statement.upper().startswith(
                "PRAGMA"
            ):
                continue

            try:

                cursor = connection.execute(
                    statement
                )

                rows = cursor.fetchall()

                output.write(
                    f"REPORT {report_number}\n"
                )

                output.write(
                    "-" * 80
                )

                output.write("\n")

                if cursor.description:

                    columns = [
                        column[0]
                        for column in cursor.description
                    ]

                    # Column headers
                    output.write(
                        " | ".join(columns)
                    )

                    output.write("\n")

                    output.write(
                        "-" * 80
                    )

                    output.write("\n")

                    # Rows
                    for row in rows:

                        values = [
                            str(value)
                            for value in row
                        ]

                        output.write(
                            " | ".join(values)
                        )

                        output.write("\n")

                    output.write(
                        f"\nRows returned: "
                        f"{len(rows)}\n"
                    )

                else:

                    output.write(
                        "Statement executed successfully.\n"
                    )

                output.write("\n")

                report_number += 1

            except sqlite3.Error as error:

                output.write(
                    f"SQL ERROR: {error}\n"
                )

                output.write(
                    f"Statement:\n{statement}\n"
                )

                output.write("\n")

    print(
        f"Saved: {output_file}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("E-COMMERCE SQL REPORT GENERATOR")
    print("=" * 70)

    try:

        connection = sqlite3.connect(
            DB_PATH
        )

        print(
            f"\nConnected to: {DB_PATH}"
        )

        for sql_file in SQL_FILES:

            execute_sql_file(
                connection,
                sql_file
            )

        connection.close()

        print("\n" + "=" * 70)
        print("REPORT GENERATION COMPLETED")
        print("=" * 70)

        print(
            f"\nReports saved in:\n"
            f"{OUTPUT_DIR}"
        )

    except sqlite3.Error as error:

        print(
            f"\nDatabase error: {error}"
        )


if __name__ == "__main__":
    main()