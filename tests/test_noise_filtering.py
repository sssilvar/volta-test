def test_wavelet_denoising():
    import wfdb
    from voltatest.preprocessing.noise_filtering import wavelet_denoising

    # Load a random record
    record = wfdb.rdrecord('../data/mitdb/106', sampto=3000)

    # Extract a specific channel of interest
    signal = record.p_signal[:, 0]

    # Perform wavelet denoising
    denoised_signal = wavelet_denoising(signal, wavelet='db4', level=1, plot=True)
    pass



