import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_first_n_samples(record, annotation, n_samples):
    # Some descriptive information about the record
    data = {
        'Record Name': record.record_name,
        'Length of Record': len(record.p_signal),
        'Number of Channels': record.n_sig,
        'Sampling Rate': record.fs,
        'Number of Annotations': len(annotation.sample)
    }
    record_desc = pd.Series(data)
    print(record_desc.to_string())

    # Get the first 3000 samples of the first channel (or n_annots if less than 3000)
    n_samples = min(3000, len(annotation.sample))
    t_sample = np.arange(n_samples) / record.fs  # Time in seconds
    sample = record.p_signal[:n_samples, :]
    annot = np.array(list(filter(lambda x: x < n_samples, annotation.sample)))

    # Extract annotation symbols
    annot_symbols = [annotation.symbol[i] for i in annot]

    fig, axs = plt.subplots(2, 1, figsize=(15, 6), sharex=True)

    axs[0].plot(t_sample, sample[:, 0])
    axs[0].scatter(annot / record.fs, sample[annot, 0], c='g')

    # Add text to the annotations with symbols (using arrows)
    for i, annot_i in enumerate(annot):
        axs[0].annotate(annot_symbols[i], xy=(annot_i / record.fs + 2, sample[annot_i, 0]),
                        xytext=(annot_i / record.fs, sample[annot_i, 0] + 0.1))
        # Add a vertical line to highlight the annomalies (!=N)
        if annot_symbols[i] != 'N':
            axs[0].axvline(x=annot_i / record.fs, c='r', linestyle='--')

    axs[0].set_title('Channel 1')
    axs[1].plot(t_sample, sample[:, 1])
    axs[1].scatter(annot / record.fs, sample[annot, 1], c='g')

    for i, annot_i in enumerate(annot):
        axs[1].annotate(annot_symbols[i], xy=(annot_i / record.fs, sample[annot_i, 1]),
                        xytext=(annot_i / record.fs, sample[annot_i, 1] + 0.1))
        # Add a vertical line to highlight the annomalies (!=N)
        if annot_symbols[i] != 'N':
            axs[1].axvline(x=annot_i / record.fs, c='r', linestyle='--')

    axs[1].set_title('Channel 2')
    axs[1].set_xlabel('Time (s)')

    plt.suptitle(f'First {n_samples} samples of the first record')
    plt.legend(['ECG', 'Annotations'])
    return fig