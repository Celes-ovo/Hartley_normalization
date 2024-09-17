import numpy as np

from utils.utils_common import distance
from utils.convert_revert import preprocess_df, convert_minmax, convert_hart, revert_hart, revert_minmax

# def minmax_hart_convert(df, width, height, parm = None):
#     df_x = convert_minmax(df, width, height)
#     df_x, df_y = preprocess_df(df_x, df_x, parm=parm)
    
#     # 중심 좌표 구하기
#     df_x2 = distance(df_x)
    
#     temp_1 = ((df_x - df_x2)**2).astype('float32')
#     temp_2 = temp_1[:, ::2] + temp_1[:, 1::2]
#     temp_3 = np.nanmean(np.sqrt(temp_2), axis=1)
    
#     # s_factor = scaling_factor(temp_3)
#     converted_arr, output_arr, mat_calc = convert_hart(df_x, df_x2, temp_3)
    
#     return converted_arr, output_arr, mat_calc, df_y
    

# def minmax_hart_revert(df, mat_calc, width, height, output_arr):
#     reverted_output = revert_hart(df, mat_calc, output_arr)
    
#     print(reverted_output.shape)
    
#     final_output = revert_minmax(reverted_output, width, height)
    
#     return final_output

def minmax_hart_convert(df, width, height, noise_arr, parm=None, noise=False, hart=True, alpha=0.1):
    df_x = convert_minmax(df, width, height)
    df_x, df_y = preprocess_df(df_x, df_x, noise=noise, noise_arr=noise_arr, alpha=alpha)

    # print(df_x[0])
    
    # 중심 좌표 구하기
    df_x2 = distance(df_x)

    if hart:
        converted_arr, mat_calc = convert_hart(df_x, df_x2)
        # df_x[np.where(df_x<0)] = parm
        converted_arr[np.isnan(df_x)] = parm
        # df_y[np.where(df_y<0)] = parm
        converted_arr[np.isnan(df_y)] = parm

        return converted_arr, mat_calc, df_y

    else:
        df_x[np.isnan(df_x)] = parm
        # df_y[np.where(df_y<0)] = parm
        df_x[np.isnan(df_y)] = parm

        converted_arr = df_x
    
        return converted_arr, df_y
    

def minmax_hart_revert(df, mat_calc, width, height, hart=True):
    
    if hart:
        reverted_output = revert_hart(df, mat_calc)

    else:
        reverted_output = df
    
    final_output = revert_minmax(reverted_output, width, height)
    
    return final_output



def convert_revert_all(df, width, height, mat_calc=None, mode=0):
    """
    - width = df[-2]
    - height = df[-1]
    """
    if mode==0:
        converted_arr, output_arr, mat_calc, df_y = minmax_hart_convert(df, width, height, parm = None)

        return converted_arr, output_arr, mat_calc, df_y
    
    elif mode==1:
        reverted_arr = minmax_hart_revert(df, mat_calc, width, height)

        return reverted_arr