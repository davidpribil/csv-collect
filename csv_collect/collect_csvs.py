import csv
import argparse
from pathlib import Path
import numpy as np

TARGET_FOLDER_LENGTH = 4
RESULTS_FILENAME = "Average_PBP2xSpy_Repair.fxout"
LINE_BEFORE_HEADER = "Output type: BuildModel"
TARGET_HEADER = "total energy"
FIRST_COLUMN = (
    "AA",
    "A",
    "R",
    "N",
    "D",
    "C",
    "Q",
    "E",
    "G",
    "H",
    "I",
    "L",
    "K",
    "M",
    "F",
    "P",
    "S",
    "T",
    "W",
    "Y",
    "V",
)


def folder_walker(input_folder: Path):
    for folder in input_folder.iterdir():
        if folder.is_dir() and len(folder.name) == TARGET_FOLDER_LENGTH:
            yield folder


def read_results(folder: Path, filename: str):
    with (folder / filename).open() as fr:
        for line in fr:
            if line.startswith(LINE_BEFORE_HEADER):
                break

        reader = csv.DictReader(fr, delimiter="\t")
        return [row[TARGET_HEADER] for row in reader]


def print_output(values, output_csv_path: Path):
    values_transposed = np.transpose(values)
    with output_csv_path.open("w") as fw:
        fw.writelines(
            [
                f"{FIRST_COLUMN[idx]}\t{values[0]}\t{values[1]}\n"
                for idx, values in enumerate(values_transposed)
            ]
        )


def main(input_folder: Path, output_csv_path: Path):
    values = []
    print(f"Collecting data from {str(input_folder)}")
    for folder in folder_walker(input_folder):
        values.append([folder.name, read_results(folder, RESULTS_FILENAME)])

    print(f"Collected data from {len(values)} folders. Sorting.")

    def sort_func(value):
        return value[0][1:]

    values.sort(key=sort_func)
    values = [[value[0]] + value[1] for value in values]

    print(f"Sorting completed. Writing output to: {str(output_csv_path)}")
    print_output(values, output_csv_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_folder", type=Path)
    parser.add_argument("output_csv_path", type=Path)
    args = parser.parse_args()
    main(args.input_folder, args.output_csv_path)
