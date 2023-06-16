"""
=============================
Noise Filtering
=============================
"""
import numpy as np
import pywt
from matplotlib import pyplot as plt


def wavelet_denoising(signal: np.ndarray, wavelet='db4', level=1, plot=False):
    """
    Perform wavelet denoising on a 1D signal.
    Args:
        signal (array): 1D signal to be denoised.
        wavelet (str): Name of the wavelet to use.
        level (int): Level of the wavelet decomposition.
        plot (bool): Whether to plot the wavelet decomposition.
    Returns:
        array: Denoised signal.
    """
    # Assert that the signal is 1D
    assert len(signal.shape) == 1, 'The signal must be 1D.'

    # Decompose the signal using the wavelet filter
    wavelet_coeffs = pywt.wavedec(signal, wavelet=wavelet, level=level)

    # Set the threshold for denoising (universal threshold proposed by Donoho and Johnstone, 1994)
    threshold = np.std(wavelet_coeffs[-level]) * np.sqrt(2 * np.log(len(signal)))

    new_coeffs = []
    for coeff in wavelet_coeffs:
        new_coeffs.append(pywt.threshold(coeff, threshold, 'soft'))
    # Reconstruct the signal using the thresholded coefficients
    denoised_signal = pywt.waverec(new_coeffs, wavelet=wavelet)
    if plot:
        # Plot the original and denoised signals
        plt.figure(figsize=(10, 5), facecolor='white')
        plt.plot(signal, label='Original Signal')
        plt.plot(denoised_signal, label='Denoised Signal')
        plt.title('Wavelet Denoising')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')

        # Add an overlayed zoomed-in plot
        sample_index = np.arange(200, 400)
        ax = plt.axes([0.6, 0.5, 0.25, 0.25])  # Create a new axes

        ax.plot(sample_index, signal[200:400], label='Original Signal')
        ax.plot(sample_index, denoised_signal[200:400], label='Denoised Signal')
        ax.set_title('Zoomed-In Wavelet Denoising')
        ax.set_xlabel('Sample Index')
        ax.set_ylabel('Amplitude')
        ax.set_facecolor('lightgrey')

        plt.legend()
        plt.show()
    return denoised_signal
