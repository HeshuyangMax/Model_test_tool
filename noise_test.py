import pysepm
import os
import numpy as np
import soundfile as sf
from tqdm import tqdm
from math import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

clean_wavs = '测试数据集/clean_testset_wav_16k/'#这个路径，大家根据自己的需求进行修改
denoised_wavs = '测试数据集/cleaned_testset_wav_16k_48700/'#同理进行修改

def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.wav':
                L.append(os.path.join(root, file))
    return L

# get wav_lists
clean_lists = file_name(clean_wavs)
denoised_lists = file_name(denoised_wavs)
# Package files
zipped = zip(clean_lists, denoised_lists)

SNRsegscores = []
LLRscores = []
WSSscores = []
STOIscores = []
PESQscores = []
CDscores = []

CSIGs = []
CBAKs = []
COVLs = []

meanAbsoluteErrors = []
meanSquaredErrors = []
RMSEs = []
r2Scores = []

for (clean_wav, denoised_wav) in tqdm(zipped, 'the progressing ...'):
    # Gain speech parameters
    ref, sr0 = sf.read(clean_wav)
    deg, sr1 = sf.read(denoised_wav)

    '''
    # Method 1: SNRseg (分段信噪比)
        # from pysepm Call SNRseg to calculate its metrics
        # in this case we can choose our frame length =0.03*1000=30 ms , and the overlap =30 ms *0.75 =22.5 ms
        # 得分越高，质量越好
    '''
    SNRsegscore = pysepm.SNRseg(ref, deg, sr0)

    '''
    # Method 2: llr (对数似然比测度)
        # 
        # 得分越高，质量越好
    '''
    LLRscore = pysepm.llr(ref, deg, sr0)

    '''
    # Method 3: WSS (加权谱倾斜测度)
        # 
        # 得分越低，质量越好
    '''
    WSSscore = pysepm.wss(ref, deg, sr0)

    '''
    # Method 4: STOI (可短时客观可懂)
        # 
        # the score from 0-1 . The higher the score, the better the performance.
        #得分范围0~1,得分越高，质量越好
    '''
    STOIscore = pysepm.stoi(ref, deg, sr0)

    '''
    # Method 5: PESQ
        # when I try this commond , I faced some troubles   , so finally I gave up this commond,
        # use the PESQ.py to instead
        得分范围从 -0.5~ 4.5,得分越高，效果越好
    '''
    NaN, PESQscore = pysepm.pesq(ref,deg,sr0)

    '''
    # Method 6: CD (Cepstrum Distance)
        # 
        # 数值越高，得分越高.
    '''
    CDscore = pysepm.cepstrum_distance(ref, deg, sr0)

    '''
       # Method 7: LSD (对数谱距离)
            # This method I use the LSD.py to calculate the distance 
            # 数值越小，得分越高      
    '''

    '''
    Method 1 - 7 use this score to print
    '''
    # score append to scores
    SNRsegscores.append(SNRsegscore)
    LLRscores.append(LLRscore)
    WSSscores.append(WSSscore)
    STOIscores.append(STOIscore)
    PESQscores.append(PESQscore)
    CDscores.append(CDscore)

    '''
    # Method 8: Composite
        # In this method , It comes some errors, if you want to solve the error ,  see the step 8 in this file.
        # CSIG , CBAK , COVL all from 1 - 5 , The higher the score, the better the performance.
    '''
    CSIG, CBAK, COVL = pysepm.composite(ref, deg, sr0)
    CSIGs.append(CSIG)
    CBAKs.append(CBAK)
    COVLs.append(COVL)

    '''
    Method 9: 回归误差计算
    '''
    meanAbsoluteError = mean_absolute_error(ref, deg)
    meanSquaredError = mean_squared_error(ref, deg)
    rmse = sqrt(meanSquaredError)
    r2Score = r2_score(ref, deg)
    
    meanAbsoluteErrors.append(meanAbsoluteError)
    meanSquaredErrors.append(meanSquaredError)
    RMSEs.append(rmse)
    r2Scores.append(r2Score)


# print(SNRsegscores)
print('The average SegSNR evaluation is: ', sum(SNRsegscores) / len(SNRsegscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(SNRsegscores))
print('The variance is: ', np.var(SNRsegscores))
print('')

# print(LLRscores)
print('The average LLR evaluation is: ', sum(LLRscores) / len(LLRscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(LLRscores))
print('The variance is: ', np.var(LLRscores))
print('')

# print(WSSscores)
print('The average WSS evaluation is: ', sum(WSSscores) / len(WSSscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(WSSscores))
print('The variance is: ', np.var(WSSscores))
print('')

# print(STOIscores)
print('The average STOI evaluation is: ', sum(STOIscores) / len(STOIscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(STOIscores))
print('The variance is: ', np.var(STOIscores))
print('')

# print(PESQscores)
print('The average PESQ evaluation is: ', sum(PESQscores) / len(PESQscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(PESQscores))
print('The variance is: ', np.var(PESQscores))
print('')

# print(CDscores)
print('The average CD evaluation is: ', sum(CDscores) / len(CDscores))
# calculate the standard deviation & variance of the scores
print('The standard deviation is: ', np.std(CDscores))
print('The variance is: ', np.var(CDscores))
print('')

# print(CSIGs,CBAKs,COVLs)
print('The average CSIG evaluation is: ', sum(CSIGs) / len(CSIGs))
print('The average CBAK evaluation is: ', sum(CBAKs) / len(CBAKs))
print('The average COVL evaluation is: ', sum(COVLs) / len(COVLs))
print('')

# 回归误差计算
print("The average mean_absolute_error evaluation is: ", sum(meanAbsoluteErrors) / len(meanAbsoluteErrors))
print("The average mean_squared_error evaluation is: ", sum(meanSquaredErrors) / len(meanSquaredErrors))
print("The average RMSE evaluation is: ", sum(RMSEs) / len(RMSEs))
print("The average r2 score evaluation is: ", sum(r2Scores) / len(r2Scores))
print('')
