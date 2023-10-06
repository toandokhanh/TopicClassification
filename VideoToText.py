# dktoan: modify 02/10/2023
# dktoan: modify 06/10/2023
import time
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa
import argparse
import os
import noisereduce as nr
import soundfile as sf
import ffmpeg
import requests
import soundfile as sf
import re
from glob import glob
from noisereduce.generate_noise import band_limited_noise
from regex import F
from datetime import datetime
from underthesea import classify
from langdetect import detect
from googletrans import Translator
from gingerit.gingerit import GingerIt
from pyvi import ViTokenizer
from nltk.tokenize import sent_tokenize


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-video', type=str,
                        help='path to audiofile')
    parser.add_argument('-l','--language', type=str,
                        help='language: vi, en, ru,')
    parser.add_argument('-s','--step_time', type=int, default=55,
                        help='step_time: default : 55')
    parser.add_argument('-noise','--algorithm_noise',
                        help="---> Chọn thuật toán giảm nhiễu",default="no")
    # step_time = 50
    arguments = parser.parse_args()
    return arguments

def recognize(wav_filename, args):
    
    data, s = librosa.load(wav_filename)
    # librosa.output.write_wav('tmp.wav', data, s)
    sf.write('tmp/tmp.wav', data, s)
    y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    wavfile.write('tmp/tmp_32.wav', s, y)

    r = sr.Recognizer()
    with sr.AudioFile('tmp/tmp_32.wav') as source:
        audio = r.record(source)  

    print('audiofile loaded')

    try:
        # https://pypi.org/project/SpeechRecognition/
        result = r.recognize_google(audio, language = args.language).lower()
    except sr.UnknownValueError:
        print("cannot understand audio")
        result = ''
        os.remove(wav_filename)
    video_name = os.path.splitext(args.video)[0]
    with open( video_name +'_'+args.language+ '.txt', 'a', encoding='utf-8') as f:
        f.write(' {}'.format(result))
    

def get_audio(video):
    os.system('ffmpeg -y  -threads 4 -i {} -f wav -ab 192000 -vn {}'.format(video, 'tmp/current.wav'))
    
# def get_audio(video, name_file):
#     os.system('ffmpeg -y  -threads 4\
#  -i {} -f wav -ab 192000 -vn {}'.format(video, name_file))

def split_into_frames(audiofile, args, folder='samples'):
    data, sr = librosa.load(audiofile)
    print(data)
    print(sr)
    try:
        duration = librosa.get_duration(y=data, sr=sr)
    except:
        duration = librosa.get_duration(audiofile)
    #print('video duration, hours: {}'.format(duration/3600))
    print('video duration, seconds: {}'.format(duration))
    # tach moi file dai khoản 50s
    for i in range(0,int(duration-1),args.step_time):
        tmp_batch = data[(i)*sr:sr*(i+args.step_time)]
        # librosa.output.write_wav('samples/{}.wav'.format(chr(int(i/50)+65)), tmp_batch, sr)
        # librosa.output.write_wav('samples/'+str(int(i/50)+65), y=tmp_batch,sr= sr)

        #import soundfile as sf
        # sap xep theo bang chu cai
        # sf.write( folder +'/{}.wav'.format(chr(int(i/50)+65)), tmp_batch, sr)
        sf.write( folder +'/{}.wav'.format(str(i)), tmp_batch, sr)

def checkfolder (path):
    # path = 'tmp'
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The "+str(path)+" directory is created!")

def noise_reduce(file,file_out):
    y, sr = librosa.load(file)
    reduced_noise = nr.reduce_noise(y = y, sr=sr, thresh_n_mult_nonstationary=2,stationary=False)
    sf.write(file_out,reduced_noise, sr, subtype='PCM_24')
    print('Đang giảm nhiễu với thuật toán noise_reduce!')

def noise_deepfilternet(file,file_out):
    os.system('deepFilter {} -o {}'.format(file,file_out))
    print('Đang giảm nhiễu với thuật toán noise_deepfilternet!')

def rename(filename,newname): 
    os.rename(filename, newname)

def get_topic(text):
    translator = Translator()
    if args.language == 'vi':
        text_trans = text
    else:
        text_trans = translate_text(text, args.language, 'vi')
        with open(video_name +'_'+args.language+'_vi.txt', 'w', encoding='utf-8') as f:
            f.write(text_trans)
        if os.path.exists(video_name +'_'+args.language+'_vi.txt'):
            print("Save the sub-vi file successfully")
        else:
            print("Save the sub-vi file failed") 
    topic = '_'.join(classify(text_trans))
    return topic

def translate_text(text, src, dest):
    translator = Translator()
    chunk_size = 5000  # Kích thước mỗi phần nhỏ (giới hạn của Google Translate API)
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []
    for chunk in chunks:
        translation = translator.translate(chunk, src=src, dest=dest)
        translated_chunks.append(translation.text)
    translated_text = ' '.join(translated_chunks)
    return translated_text

if __name__ == '__main__':
    from time import gmtime, strftime
    time_text = str(strftime("%Y%m%d_%H%M%S", gmtime())) 
    folder = time_text
    checkfolder(folder)
    checkfolder('tmp')
    start = time.time()
    args = get_arguments()
    get_audio(args.video)
    split_into_frames('tmp/current.wav',args,folder)
    files = sorted(glob( folder + '/*.wav'), key = os.path.getmtime)
    print(files)
    # tao file de luu text
    video_name = os.path.splitext(args.video)[0]
    # if os.path.exists(video_name + '_' + args.language + '.txt'):
    #     print('ton tai file'+video_name + '_' + args.language + '.txt')
    # else:
    #     print('k ton tai file'+video_name + '_' + args.language + '.txt')
    open(video_name+'_'+args.language+'.txt', 'w', encoding = 'utf-8').write('')
    noises = args.algorithm_noise
    if noises:
        if noises == 'deep':
            print("Use DeepFilterNet")
            for file in files:
                path = file[:file.rindex('/') + 1]
                nameFile = file[file.rindex('/') + 1:file.rindex('.')]
                noise_deepfilternet(file,path)
                rename(path+nameFile+'_DeepFilterNet2.wav',file)
            for file in files:
                recognize(file,args)
            pass
        elif noises == 'noise':
            print("Use NoiseReduce")
            for file in files:
                noise_reduce(file,file)
            for file in files:
                recognize(file,args)
        else:
            print("Do not use reduce_noise algorithm")
            for file in files:
                recognize(file,args)
            pass
    
    video_name = os.path.splitext(args.video)[0]
    file_path = video_name+'_'+args.language+'.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    topic = get_topic(text)
    new_file_path = video_name.split('_')[0] + '_'+topic+'.txt'
    # Đổi tên tệp từ file_path sang new_file_path
    os.rename(file_path, new_file_path)
    end = time.time()
    print('elapsed time: {}'.format(end - start))
    # os.system('rm tmp/*')
