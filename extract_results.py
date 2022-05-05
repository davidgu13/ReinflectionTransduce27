# This is a Python3 script for extracting the runs results to an Excel file, including final dev and test accuracies.
import os
from os.path import join, isdir
from itertools import product
import re

def are_substrings_in_string(target_string: str, substrings: tuple) -> bool:
    return all([substring in target_string for substring in substrings])

def find_float_in_line(line):
    matches = re.findall("\d+\.\d+", line)
    assert len(matches) == 1, "Invalid output!"
    return float(matches[0])

results_folder = join('.', 'Results')
analogy_types, seeds, io_formats  = ['None'], [100], ['g_g'] # to be extended

lang_pos_groups = dict(zip(range(1,16), ['kat_V', 'kat_N', 'fin_ADJ', 'swc_V', 'swc_ADJ', 'fin_V', 'sqi_V', 'hun_V',
                                         'bul_V', 'bul_ADJ', 'lav_V', 'lav_N', 'tur_V', 'tur_ADJ', 'fin_N']))
excel_results_file = "Test-Results None-100-g-g.xlsx"

def extract_accuracies_from_single_folder(folder):
    with open(join(folder, 'f.stats'), encoding='utf8') as file:
        lines = file.read().split('\n')
        return find_float_in_line(lines[-3]), find_float_in_line(lines[-2])


def main():
    accuracies = []
    for analogy, seed, io in product(analogy_types, seeds, io_formats):
        current_parent_folder = join(results_folder, f"{analogy}_{seed}_{io}")
        assert isdir(current_parent_folder), f"Folder Results doesn't exist!"

        folders = [join(current_parent_folder, folder) for folder in os.listdir(current_parent_folder) if isdir(folder)]
        for folder in folders:
            dev_accuracy, test_accuracy = extract_accuracies_from_single_folder(folder)
            accuracies.append([dev_accuracy, test_accuracy])

    from pandas import DataFrame
    df = DataFrame(accuracies, columns=['Dev Accuracy', 'Test Accuracy'])
    df = df.fillna("")
    df.to_excel(excel_results_file)

if __name__ == '__main__':
    main()