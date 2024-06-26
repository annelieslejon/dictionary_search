import argparse
import csv
import dataclasses
import glob
import json
import os
import random
import time
from typing import List, Tuple, Dict

import numpy as np
from dictionary_search_model import Model

_DATABASE = []
_DATABASE_2 = []


@dataclasses.dataclass
class DatabaseEntry:
    embedding: np.ndarray
    gloss: str

def populate_db2(database_path: str, max_entries: int):
    # We first add the signs that are in the query set and then continue to add unique signs until we reach max_entries.
    # We do this in a deterministic manner of course...
    db_entries = [os.path.join(database_path, 'HEBBEN-A-4801.npy'),  # In corpus.
                  os.path.join(database_path, 'TELEFONEREN-D-11870.npy'),  # In corpus.
                  os.path.join(database_path, 'HAAS-A-16146.npy'),  # In corpus.
                  os.path.join(database_path, 'STRAAT-A-11560.npy'),  # In corpus.
                  os.path.join(database_path, 'PAARD-A-8880.npy'),  # In corpus.
                  os.path.join(database_path, 'HOND-A-5052.npy'),  # In corpus.
                  os.path.join(database_path, 'RUSTEN-B-10250.npy'),  # In corpus.
                  os.path.join(database_path, 'SCHOOL-A-10547.npy'),  # In corpus.
                  os.path.join(database_path, 'ONTHOUDEN-A-8420.npy'),  # In corpus.
                  os.path.join(database_path, 'WAT-A-13657.npy'),  # In corpus.

                  os.path.join(database_path, 'BOUWEN-G-1906.npy'),  # Not in corpus.
                  os.path.join(database_path, 'WAAROM-A-13564.npy'),  # Not in corpus.
                  os.path.join(database_path, 'MELK-B-7418.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VALENTIJN-A-16235.npy'),  # Not in corpus.
                  os.path.join(database_path, 'HERFST-B-4897.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VLIEGTUIG-B-13187.npy'),  # Not in corpus.
                  os.path.join(database_path, 'KLEPELBEL-A-1166.npy'),  # Not in corpus.
                  os.path.join(database_path, 'POES-G-9372.npy'),  # Not in corpus.
                  os.path.join(database_path, 'MOEDER-A-7676.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VADER-G-8975.npy')]  # Not in corpus.

    all_db_entries: List[str] = glob.glob(os.path.join(database_path, '*.npy'))
    indices = list(range(len(all_db_entries)))
    random.seed(10)
    random.shuffle(indices)
    with open('/tmp/indices.txt', 'w') as f:
        f.writelines([str(i) + '\n' for i in indices])
    all_db_entries = list(np.array(all_db_entries)[indices])
    index: int = 0
    while len(db_entries) < max_entries:
        if all_db_entries[index] not in db_entries:  # I know, not ideal, but it'll have to do.
            db_entries.append(all_db_entries[index])
        index += 1
    print(f'Collected {len(db_entries)} database entries.')
    for db_entry in db_entries:
        label: str = os.path.splitext(os.path.basename(db_entry))[0]
        _DATABASE_2.append(DatabaseEntry(np.load(db_entry), label))

def populate_db(database_path: str, max_entries: int):
    # We first add the signs that are in the query set and then continue to add unique signs until we reach max_entries.
    # We do this in a deterministic manner of course...
    db_entries = [os.path.join(database_path, 'HEBBEN-A-4801.npy'),  # In corpus.
                  os.path.join(database_path, 'TELEFONEREN-D-11870.npy'),  # In corpus.
                  os.path.join(database_path, 'HAAS-A-16146.npy'),  # In corpus.
                  os.path.join(database_path, 'STRAAT-A-11560.npy'),  # In corpus.
                  os.path.join(database_path, 'PAARD-A-8880.npy'),  # In corpus.
                  os.path.join(database_path, 'HOND-A-5052.npy'),  # In corpus.
                  os.path.join(database_path, 'RUSTEN-B-10250.npy'),  # In corpus.
                  os.path.join(database_path, 'SCHOOL-A-10547.npy'),  # In corpus.
                  os.path.join(database_path, 'ONTHOUDEN-A-8420.npy'),  # In corpus.
                  os.path.join(database_path, 'WAT-A-13657.npy'),  # In corpus.

                  os.path.join(database_path, 'BOUWEN-G-1906.npy'),  # Not in corpus.
                  os.path.join(database_path, 'WAAROM-A-13564.npy'),  # Not in corpus.
                  os.path.join(database_path, 'MELK-B-7418.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VALENTIJN-A-16235.npy'),  # Not in corpus.
                  os.path.join(database_path, 'HERFST-B-4897.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VLIEGTUIG-B-13187.npy'),  # Not in corpus.
                  os.path.join(database_path, 'KLEPELBEL-A-1166.npy'),  # Not in corpus.
                  os.path.join(database_path, 'POES-G-9372.npy'),  # Not in corpus.
                  os.path.join(database_path, 'MOEDER-A-7676.npy'),  # Not in corpus.
                  os.path.join(database_path, 'VADER-G-8975.npy')]  # Not in corpus.

    all_db_entries: List[str] = glob.glob(os.path.join(database_path, '*.npy'))
    indices = list(range(len(all_db_entries)))
    random.seed(10)
    random.shuffle(indices)
    with open('/tmp/indices.txt', 'w') as f:
        f.writelines([str(i) + '\n' for i in indices])
    all_db_entries = list(np.array(all_db_entries)[indices])
    index: int = 0
    while len(db_entries) < max_entries:
        if all_db_entries[index] not in db_entries:  # I know, not ideal, but it'll have to do.
            db_entries.append(all_db_entries[index])
        index += 1
    print(f'Collected {len(db_entries)} database entries.')
    for db_entry in db_entries:
        label: str = os.path.splitext(os.path.basename(db_entry))[0]
        _DATABASE.append(DatabaseEntry(np.load(db_entry), label))


def search(raw_keypoint_file: str, model: Model, model2: Model, k: int) -> Tuple[str, List[str]]:
    """Search through the database with a given file containing keypoints.

    :param raw_keypoint_file: File containing keypoints.
    :param model: SLR model.
    :param k: Top-k results will be returned.
    :return: The label of the keypoint file (ground truth) and the search results."""
    embedding1: np.ndarray = model.get_embedding(np.load(raw_keypoint_file))
    embedding2: np.ndarray = model2.get_embedding(np.load(raw_keypoint_file))
    with open(raw_keypoint_file.replace('npy', 'json')) as f:
        d: Dict = json.load(f)
        label: str = d['ground_truth']
    search_results: List[str] = get_results(embedding1, embedding2, k)
    return label, search_results


def get_results(embedding1: np.ndarray, embedding2, k: int) -> List[str]:
    distances: List[List[float, int]] = []
    for i, key in enumerate(_DATABASE):
        eucdist: float = np.linalg.norm(embedding1 - key.embedding)

        distances.append([eucdist, i])
    for i, key in enumerate(_DATABASE_2):
        eucdist: float = np.linalg.norm(embedding2 - key.embedding)

        distances[i] = [0.5 * (eucdist + distances[i][0]), i]
    ordered = sorted(distances, key=lambda tup: tup[0])  # Sort by ascending distance.
    results: List[str] = [_DATABASE[i].gloss for i in [tup[1] for tup in ordered]][:k]
    return results  # Glosses, distances.


def print_list(array: np.ndarray, indices=(1, 2, 3, 5, 10, 20)) -> str:
    result: str = '['
    for i, el in enumerate(array):
        if i + 1 in indices:  # For the 0th element, prints top-1 accuracy, for the 1st, prints top-2 accuracy...
            result += str(el) + ', '
    result = result[:-2]  # Drop last comma and space.
    result += ']'
    return result


def main(input_directory: str, db_directory: str, db_directory2, model_path_1: str,model_path_2, k: int, n: int):
    """Convert the videos in `input_directory` to embeddings with the model stored at `model_path` and write them to `output_directory`.

    :param input_directory: The path to the directory containing the dictionary videos.
    :param db_directory: The path to the directory containing the database.
    :param model_path: The path to the model (that generates the embeddings) checkpoint.
    :param k: The top-k accuracy will be computed.
    :param n: The maximum amount of database entries to compare to.
    """
    model1: Model = Model(model_path_1)
    model2: Model = Model(model_path_2)

    populate_db(db_directory, n)
    populate_db2(db_directory2, n)

    query_filenames: List[str] = glob.glob(os.path.join(input_directory, '*.npy'))

    # Global accuracy.
    start_time = time.time()
    correct = np.zeros((k,))
    total = 0
    for filename in query_filenames:
        label, results = search(filename, model1, model2, k)
        for i, result in enumerate(results):
            if result == label:
                correct[i:] += 1
        total += 1
    print(f'Global top-{k} accuracy: {print_list(correct / total)}')
    end_time = time.time()
    print(f'Average look-up time: {1000 * (end_time - start_time) / len(query_filenames):.4f} ms')

    # In corpus versus not in corpus.
    incorpus = ['HEBBEN-A-4801', 'PAARD-A-8880', 'STRAAT-A-11560', 'HAAS-A-16146', 'TELEFONEREN-D-11870',
                'HOND-A-5052', 'RUSTEN-B-10250', 'SCHOOL-A-10547', 'ONTHOUDEN-A-8420', 'WAT-A-13657']
    notincorpus = ['BOUWEN-G-1906', 'WAAROM-A-13564', 'MELK-B-7418', 'VALENTIJN-A-16235', 'HERFST-B-4897',
                   'VLIEGTUIG-B-13187', 'KLEPELBEL-A-1166', 'POES-G-9372', 'MOEDER-A-7676', 'VADER-G-8975']
    correct_incorpus = np.zeros((k,))
    correct_notincorpus = np.zeros((k,))
    total_incorpus = 0
    total_notincorpus = 0
    for filename in query_filenames:
        label, results = search(filename, model1, model2, k)
        for i, result in enumerate(results):
            if result == label:
                if label in incorpus:
                    correct_incorpus[i:] += 1
                else:
                    correct_notincorpus[i:] += 1
        if label in incorpus:
            total_incorpus += 1
        else:
            total_notincorpus += 1
    print(f'In corpus top-{k} accuracy: {print_list(correct_incorpus / total_incorpus)}')
    print(f'Not in corpus top-{k} accuracy: {print_list(correct_notincorpus / total_notincorpus)}')

    # Per class accuracy.
    correct = {label.gloss: np.zeros((k,)) for label in _DATABASE[:20]}
    total = {label.gloss: 0 for label in _DATABASE[:20]}
    for filename in query_filenames:
        label, results = search(filename, model1, model2, k)
        for i, result in enumerate(results):
            if result == label:
                correct[label][i:] += 1
        total[label] += 1
    for label in correct:
        print(f'Label "{label}" ({total[label]} entries) top-{k} accuracy: {print_list(correct[label] / total[label])}')

    # Write a file that can be parsed by pandas to generate all kinds of pretty plots with seaborn.
    with open(args.output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['query', ''])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input_directory', type=str, help='The path to the directory containing the query videos.')
    parser.add_argument('db_directory', type=str,
                        help='The path to the directory containing the database.')
    parser.add_argument('db_directory2', type=str,
                        help='The path to the directory containing the database.')
    parser.add_argument('model_path_1', type=str,
                        help='The path to the model (that generates the embeddings) checkpoint.')
    parser.add_argument('model_path_2', type=str,
                        help='The path to the model (that generates the embeddings) checkpoint.')
    parser.add_argument('k', type=int, help='Compute top-k accuracy.')
    parser.add_argument('n', type=int, help='Consider a maximum of n database entries to compare to.')

    args = parser.parse_args()

    main(args.input_directory, args.db_directory, args.db_directory2, args.model_path_1, args.model_path_2, args.k, args.n)
