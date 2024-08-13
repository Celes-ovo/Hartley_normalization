import numpy as np

# Our modules
from utils.utils_common import matrix_calc, matrix_calc_inv
from utils.utils_noise import noised_array

# def convert_minmax(df, width, height):
#     df_copy = df.copy()
    
#     df_odd = df_copy[:, ::2]
#     df_even = df_copy[:, 1::2]
    
#     # print(df_odd.shape[1])
    
#     width_dup = np.repeat(width, df_odd.shape[1], axis=1)
#     height_dup = np.repeat(height, df_even.shape[1], axis=1)
    
#     df_width_converted = df_odd / width_dup
#     df_height_converted = df_even / height_dup

#     df_copy[:, ::2] = df_width_converted
#     df_copy[:, 1::2] = df_height_converted

#     return df_copy

# def preprocess_df(df, label, parm=0):
#     # df_2 = convert_minmax(df, width, height)
#     # if parm==None:
#     #     df_x = df
#     #     df_y = label
#     # else:
#     #     df_x = df[:, 2:parm]
#     #     df_y = label[:, 2:parm]

#     #     if parm > 70:
#     #         df_x = df[:, 2:parm]
#     #         df_y = label[:, 2:parm]
    
#     df_x = df
#     df_y = label
    
#     df_x[np.where(df_x<0)] = parm
#     df_x[np.isnan(df_x)] = parm
    
#     df_y[np.where(df_y<0)] = parm
#     df_y[np.isnan(df_y)] = parm
    
#     return df_x, df_y


# def revert_minmax(df, width, height):
#     df_copy = df.copy()
    
#     df_odd = df_copy[:, ::2]
#     df_even = df_copy[:, 1::2]
    
#     width_dup = np.repeat(width, df_odd.shape[1], axis=1)
#     height_dup = np.repeat(height, df_even.shape[1], axis=1)
    
#     df_width_converted = df_odd * width_dup
#     df_height_converted = df_even * height_dup

#     df_copy[:, ::2] = df_width_converted
#     df_copy[:, 1::2] = df_height_converted
    
#     return df_copy


# def convert_hart(df, mean_df, s_fact):
#     df_2 = df.copy()
#     output_arr  = []
#     mat         = []

#     for i in range(len(df_2)):
#         for j in range(0, len(df_2.T)-1, 2):
#             mat_calc, output, x_t, y_t = matrix_calc(s_fact[i], df_2[i, j], df_2[i, j+1], mean_df[i, j], mean_df[i, j+1])
            
#             # 
#             # print(i, j)
#             # print(s_fact[i], df_2[i, j], df_2[i, j+1], mean_df[i, j], mean_df[i, j+1])
#             # print(mat_calc, output, x_t, y_t)
#             # print(np.min(mat_calc))
#             # print(np.min(output))
#             # print(np.min(x_t))
#             # print(np.min(y_t))

#             df_2[i, j]      = x_t
#             df_2[i, j+1]    = y_t

#             output_arr.append(output)
#             mat.append(mat_calc)

#     return df_2, np.array(output_arr), np.array(mat)

# def revert_hart(df, matrix_calc, matrix_out):
#     output = []
#     for i in range(len(matrix_out)):
#         x_t, y_t = matrix_calc_inv(matrix_calc[i], matrix_out[i])
#         output.append([x_t, y_t])

#     return np.array(output).reshape(df.shape)


def convert_minmax(df, width, height):
    df_copy = df.copy()
    
    df_odd = df_copy[::2]
    df_even = df_copy[1::2]
    
    df_width_converted = df_odd / width
    df_height_converted = df_even / height

    df_copy[::2] = df_width_converted
    df_copy[1::2] = df_height_converted

    return df_copy

def preprocess_df(df, label, parm=0, noise=False):   
    df_x = df
    df_y = label
    
    df_x[np.where(df_x<0)] = parm
    df_x[np.isnan(df_x)] = parm
    
    df_y[np.where(df_y<0)] = parm
    df_y[np.isnan(df_y)] = parm

    if noise:
        df_x = noised_array(df_x, alpha=1.2)
    
    return df_x, df_y


def revert_minmax(df, width, height):
    df_copy = df.copy()
    
    df_odd = df_copy[::2]
    df_even = df_copy[1::2]
    
    df_width_converted = df_odd * width
    df_height_converted = df_even * height

    df_copy[::2] = df_width_converted
    df_copy[1::2] = df_height_converted
    
    return df_copy


def convert_hart(df, mean_xy):
    df_2 = df.copy()
    df_3 = np.tile(mean_xy, len(df_2)//2)

    temp_1 = ((df_2 - df_3)**2).astype('float32')
    temp_2 = temp_1[::2] + temp_1[1::2]
    s_fact = np.nanmean(np.sqrt(temp_2))

    for i in range(0, len(df_2.T)-1, 2):
        mat_calc, x_t, y_t = matrix_calc(s_fact, df_2[i], df_2[i+1], mean_xy[0], mean_xy[1])

        df_2[i]      = x_t
        df_2[i+1]    = y_t

    return df_2, mat_calc

def revert_hart(df, matrix_calc):
    output = []
    for i in range(0, len(df)-1, 2):
        matrix_out = np.array([df[i], df[i+1], 1])
        x_t, y_t = matrix_calc_inv(matrix_calc, matrix_out)
        output.append([x_t, y_t])

    return np.array(output).reshape(df.shape)