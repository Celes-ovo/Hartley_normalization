import numpy as np

def getstd(df):
    std = np.std(df, axis=0)

    return std

def get_noise(i_array, i_std):
    i_zero_array = np.zeros(shape=i_array.shape)
    print(i_zero_array.shape)
    for i in range(i_array.shape[0]):
        i_zero_array[i] = np.random.normal(loc=0.0, scale=i_std)
    return i_zero_array

def noised_array(i_array, alpha=0.01):
    i_std = getstd(i_array)
    noise = get_noise(i_array, i_std)

    array_2 = i_array + alpha * noise

    return array_2