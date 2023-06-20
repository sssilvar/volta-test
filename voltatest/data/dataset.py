# Load MIT-BIH Arrhythmia Database as a torch Dataset
from pathlib import Path

import wfdb


class MITBIHDataset:
    def __init__(self, dl_dir: str):
        self.dl_dir = Path(dl_dir).resolve()

        # Save a list of all record names (not the data itself)
        self.record_names = [f.stem for f in self.dl_dir.glob('*.dat')]

    def __getitem__(self, index):
        """Load the record and annotation"""
        if isinstance(index, int):
            subject_id = self.record_names[index]
        else:
            subject_id = index
        record = wfdb.rdrecord(str(self.dl_dir / subject_id))
        annotation = wfdb.rdann(str(self.dl_dir / subject_id), 'atr')
        return record, annotation

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return len(self.record_names)
