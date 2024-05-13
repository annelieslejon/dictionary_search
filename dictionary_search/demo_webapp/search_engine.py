import dataclasses
import glob
import os
import random
from typing import List, Tuple

import numpy as np
from tqdm import tqdm


@dataclasses.dataclass
class DatabaseEntry:
    embedding: np.ndarray
    gloss: str


class SearchEngine:
    """Allows searching the database."""

    def __init__(self, database_path: str, max_entries: int):
        self.database = []

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
                      os.path.join(database_path, 'HERFST-B-4897.npy'), # Not in corpus.
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
        while max_entries == -1 or len(db_entries) < max_entries:
            if all_db_entries[index] not in db_entries:  # I know, not ideal, but it'll have to do.
                db_entries.append(all_db_entries[index])
            index += 1
        print(f'Collected {len(db_entries)} database entries.')
        for db_entry in db_entries:
            label: str = os.path.splitext(os.path.basename(db_entry))[0]
            self.database.append(DatabaseEntry(np.load(db_entry), label))



    def get_results(self, embedding: np.ndarray,random_embedding) -> List[Tuple[str, float]]:
        """Perform a search. Return a maximum number of results.

        :param embedding: The query embedding.
        :returns: The search results, a list of glosses and their distance to the query."""
        distances = []
        scaled_distances = []
        distances_random = []
        for i, key in enumerate(self.database):
            eucdist = np.linalg.norm(embedding - key.embedding)



            distances.append((eucdist, i))
        ordered = sorted(distances, key=lambda tup: tup[0])
        scores = np.random.rand(len(ordered))

        results = [(self.database[i].gloss, i, float(d)) for s,(d, i) in zip(scores,ordered)]


        return results
