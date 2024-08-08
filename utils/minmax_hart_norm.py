import numpy as np

from utils.utils_common import distance, scaling_factor
from utils.convert_revert import preprocess_df, convert_minmax, convert_hart, revert_hart, revert_minmax

def minmax_hart_convert(df, label, width, height, parm = None):
    df_x = convert_minmax(df, width, height)
    df_x, df_y = preprocess_df(df_x, label, parm=parm)
    
    # 중심 좌표 구하기
    df_x2 = distance(df_x)
    
    temp_1 = ((df_x - df_x2)**2).astype('float32')
    temp_2 = temp_1[:, ::2] + temp_1[:, 1::2]
    temp_3 = np.nanmean(np.sqrt(temp_2), axis=1)
    
    s_factor = scaling_factor(temp_3)
    converted_arr, output_arr, mat_calc = convert_hart(df_x, df_x2, s_factor)
    
    return converted_arr, output_arr, mat_calc, df_y
    

def minmax_hart_revert(df, mat_calc, width, height, output_arr):
    reverted_output = revert_hart(df, mat_calc, output_arr)
    
    print(reverted_output.shape)
    
    final_output = revert_minmax(reverted_output, width, height)
    
    return final_output