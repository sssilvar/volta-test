import numpy as np
import wfdb
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.signal import find_peaks
import pywt

# Load a partitucular record
record = wfdb.rdrecord('data/mitdb/100', sampto=3000)

# Extract annotations
annotation = wfdb.rdann('data/mitdb/100', 'atr', sampto=3000)
wfdb.plot_wfdb(record=record, annotation=annotation, title='Record 100 from MIT-BIH Arrhythmia Database',
               figsize=(10, 5))
plt.show()

# Perform spectral analysis
fs = record.fs  # Sampling frequency
time = np.arange(len(record.p_signal[:, 0])) / fs  # Convert sample index to time (seconds)

# Compute the power spectral density (PSD) using Welch's method
frequencies, psd = welch(record.p_signal[:, 0], fs)

# # Plot the PSD
# plt.figure(figsize=(8, 4))
# plt.plot(frequencies, psd)
# plt.title('Power Spectral Density')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Power')
# plt.show()

# Extract a specific channel of interest
signal = record.p_signal[:, 0]

# Find peaks using the find_peaks() function
auto_peaks, _ = find_peaks(signal, distance=100)

# Plot the signal with ground-truth and detected peaks
plt.figure(figsize=(10, 5))
plt.plot(time, signal, label='ECG Signal')
plt.plot(annotation.sample / fs, signal[annotation.sample], 'bo', markersize=5, label='Ground-Truth Peaks')
plt.plot(auto_peaks / fs, signal[auto_peaks], 'ro', markersize=5, label='Detected Peaks')
plt.title('Ground-Truth and Auto Peak Detection')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.legend()
plt.show()


# Perform Wavelet Decomposition
wavelet_name = 'db4'  # Select the desired wavelet (e.g., Daubechies 4)
level = 5  # Specify the decomposition level

# Perform wavelet decomposition
coeffs = pywt.wavedec(signal, wavelet=wavelet_name, level=level)

# Plot the wavelet coefficients
plt.figure(figsize=(10, 10))
for i, coeff in enumerate(coeffs):
    plt.subplot(level + 1, 1, i + 1)
    plt.plot(coeff)
    plt.title(f'Level {i+1} Coefficients')
    plt.xlabel('Sample Index')
    plt.ylabel('Coefficient Value')
plt.tight_layout()
plt.show()

# Perform Wavelet Transform
wavelet_name = 'morl'  # Select the desired wavelet (e.g., Morlet)
scales = np.arange(1, 64)  # Specify the range of scales

# Perform continuous wavelet transform
coef, freqs = pywt.cwt(record.p_signal[:, 0], scales, wavelet=wavelet_name)

# Calculate the wavelet power spectrum
power = (np.abs(coef)) ** 2

# Plot the wavelet power spectrum
plt.figure(figsize=(10, 6))
plt.imshow(power, extent=[0, len(record.p_signal), freqs[0], freqs[-1]], aspect='auto', cmap='jet')
plt.colorbar(label='Power')
plt.title('Wavelet Power Spectrum')
plt.xlabel('Sample Index')
plt.ylabel('Frequency (Hz)')
plt.show()

# Detect peaks of power spectrum
peaks_w, _ = find_peaks(power.sum(0), height=10)