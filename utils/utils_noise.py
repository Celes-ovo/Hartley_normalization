def getstd(i_array):
    temp = np.std(i_array, axis=0)

    return temp

def get_noise(i_array, i_std):
    array_2 = np.zeros(shape=i_array.shape)
    n_row, n_col = array_2.shape
    for i in range(n_col):
        array_2[:, i] = np.random.normal(loc=0.0,
                                         scale=i_std[i],
                                         size=n_row)
    return array_2

# 
def noised_array(i_array, alpha=0.1):
    i_std = getstd(i_array)
    noise = get_noise(i_array, i_std)

    array_2 = i_array + alpha * noise

    return array_2