from fileinput import filename
import os,re
import sys
from datetime import datetime
import time
from regex import P
from convert import handleFile
import argparse

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

def Tong(test_content):
    tong = len(re.findall(r'\w+', test_content))
    return tong

# Thời gian bắt đầu thực thi
start_time = datetime.now()


parser = argparse.ArgumentParser()
parser.add_argument('-train', '--train', help="---> văn bản dự đoán cần được so sánh")
parser.add_argument('-compare', '--file_origin', help="---> văn bản gốc")

args = parser.parse_args()

path = ''
path2 = ''
try:
    path = args.train + '/'
    train_files =[doc for doc in os.listdir(path) if (doc.endswith('.txt') )]

    path2 = args.file_origin + '/'
    compare_files =[doc for doc in os.listdir(path2) if (doc.endswith('.txt') )]

except:
    print("")

def readfile(filename):
    file_input = open(filename, "r", encoding="utf-8")
    read_file = file_input.read()  # Đọc nội dung của File
    read_file = read_file.lower()
    return read_file

def check_similarity(file1,file2):
    vector1 = []

    read_file = readfile(file1)
    
    read_file2 = readfile(file2)

    vector1.append(read_file)
    vector1.append(read_file2)

    # Tính độ quan trọng và số lần xuất hiện
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    # Tính Sine dựa vào tích vô hướng
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    vector = vectorize(vector1)
    result = similarity(vector[0],vector[1])[0][1]
    return round(result*100,5)

if __name__ == "__main__":
    today = datetime.today()
    time = today.strftime("%H") + "h" + today.strftime("%M")
    date = today.strftime("%Y-%m-%d") 
    dateVN = today.strftime("%d-%m-%Y")
    f = open('result/result.txt', 'w',encoding = 'utf-8')
    f.write("Thực hiện: "+str(time) + " " + str(dateVN) +"\n")
    f.write("\n==== ==== ==== ==== ==== ====\n")
    result = []
    i=0
    for train in train_files:
        file1 = path+train
        file2 = path2+train[:train.index('.')]+'_mau.txt'


        if(os.path.isfile(file2)==False):
            print('Đường dẫn thư mục {} không tồn tại'.format(file2))
            continue
        else:
            
            similarity = str(check_similarity(file1,file2)) 
            kq = '{} so sanh voi {}: {} %'.format(train,train[:train.index('.')]+'_mau.txt',similarity)
            i+=1
            f.write(kq+"\n")
        result.append(kq)
    end_time = datetime.now()
    f.write('\n=> Tổng số có {} file đã thực thi '.format(i))
    f.write('\n=> Thời gian thực thi: '+str(end_time - start_time))
    