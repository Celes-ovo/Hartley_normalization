import numpy as np
from numpy.linalg import inv


# def min_max_norm(df, width, height):
#     df_2 = df.copy()

#     width = df_2['width'].to_numpy()[:, np.newaxis].astype('float32')
#     height = df_2['height'].to_numpy()[:, np.newaxis].astype('float32')

#     # df_3 = df_2.to_numpy()[:5, 2:8]
#     df_3 = df_2.to_numpy().astype('float32')

#     # df_3[:, 2:-2:2]   = df_3[:, 2:-2:2] / width
#     # df_3[:, 3:-2:2]   = df_3[:, 3:-2:2] / height
#     df_3[:, :-2:2]   = df_3[:, :-2:2] / np.concatenate((width[:879], width[:879]), axis=0)
#     df_3[:, 1:-2:2]   = df_3[:, 1:-2:2] / np.concatenate((height[:879], height[:879]), axis=0)

#     return width, height, df_3


# def get_center(df):
#     mean = []
#     print('전체 길이 :', len(df))
#     for i in range(len(df)):
#         mean.append([np.nanmean(df[i, ::2]), np.nanmean(df[i, 1::2])])

#     mean_arr = np.array(mean).astype('float32')

#     return mean_arr

# def distance(df):
#     center_coord = get_center(df)
#     center_coord_2 = np.repeat(center_coord, len(df.T)//2, axis=0).reshape(len(df), -1)
    
#     return center_coord_2


# def scaling_factor(df):
#     return df
#     # return np.sqrt(2)/df

# def matrix_calc(s_fact, x, y, x_mean, y_mean):
#     mat_calc = np.array([[(1/s_fact), 0, -1*(1/s_fact)*x_mean], [0, (1/s_fact), -1*(1/s_fact)*y_mean], [0, 0, 1]])
#     # mat_calc = np.array([[s_fact, 0, -1*s_fact*x_mean], [0, s_fact, -1*s_fact*y_mean], [0, 0, 1]])
#     output = (mat_calc @ (np.array([x, y, 1]).T))

#     return mat_calc, output, output.T[0], output.T[1]


# # 원래 좌표대로 복구
# def matrix_calc_inv(matrix_calc, matrix_out):
#     matrix_calc_inv = inv(matrix_calc)

#     output_2 = matrix_calc_inv @ matrix_out

#     return output_2[0], output_2[1]



def get_center(df):
    mean = [np.nanmean(df[::2]), np.nanmean(df[1::2])]
    mean_arr = np.array(mean).astype('float32')

    return mean_arr

def distance(df):
    center_coord = get_center(df)
    # center_coord_2 = np.tile(center_coord, len(df)//2)
    
    return center_coord

def matrix_calc(s_fact, x, y, x_mean, y_mean):
    mat_calc = np.array([[(1/s_fact), 0, -1*(1/s_fact)*x_mean], [0, (1/s_fact), -1*(1/s_fact)*y_mean], [0, 0, 1]])
    # mat_calc = np.array([[s_fact, 0, -1*s_fact*x_mean], [0, s_fact, -1*s_fact*y_mean], [0, 0, 1]])
    output = (mat_calc @ (np.array([x, y, 1]).T))

    return mat_calc, output.T[0], output.T[1]


# 원래 좌표대로 복구
def matrix_calc_inv(matrix_calc, matrix_out):
    matrix_calc_inv = inv(matrix_calc)

    output_2 = matrix_calc_inv @ matrix_out

    return output_2[0], output_2[1]