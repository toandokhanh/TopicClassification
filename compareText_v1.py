from fileinput import filename
import os, re
import sys
from datetime import datetime
import time
from regex import P
# from convert import handleFile
import argparse

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

def Tong(test_content):
    tong = len(re.findall(r'\w+', test_content))
    return tong

# Thời gian bắt đầu thực thi
start_time = datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument('directory1', help="First directory containing text files for comparison")
parser.add_argument('directory2', help="Second directory containing text files for comparison")
args = parser.parse_args()

path1 = args.directory1 + '/'
path2 = args.directory2 + '/'

def readfile(filename):
    file_input = open(filename, "r", encoding="utf-8")
    read_file = file_input.read()  # Đọc nội dung của File
    read_file = read_file.lower()
    return read_file

def check_similarity(file1, file2):
    vector1 = []

    read_file1 = readfile(file1)
    read_file2 = readfile(file2)

    vector1.append(read_file1)
    vector1.append(read_file2)

    # Tính độ quan trọng và số lần xuất hiện
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    # Tính Sine dựa vào tích vô hướng
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    vector = vectorize(vector1)
    result = similarity(vector[0], vector[1])[0][1]
    return round(result * 100, 5)

if __name__ == "__main__":
    today = datetime.today()
    time = today.strftime("%H") + "h" + today.strftime("%M")
    date = today.strftime("%Y-%m-%d") 
    dateVN = today.strftime("%d-%m-%Y")
    f = open('result/result.txt', 'w', encoding='utf-8')
    f.write("Thực hiện: " + str(time) + " " + str(dateVN) + "\n")
    f.write("\n==== ==== ==== ==== ==== ====\n")
    
    files1 = [doc for doc in os.listdir(path1) if (doc.endswith('.txt'))]
    files2 = [doc for doc in os.listdir(path2) if (doc.endswith('.txt'))]
    
    result = []
    i = 0
    
    for file1 in files1:
        for file2 in files2:
            if file1.split('_')[0] == file2.split('_')[0]:
                file1_path = path1 + file1
                file2_path = path2 + file2
                
                similarity = str(check_similarity(file1_path, file2_path)) 
                kq = '{},{},{}'.format(file1, file2, similarity)
                i += 1
                f.write(kq + "\n")
                result.append(kq)
    
    end_time = datetime.now()
    f.write('\n=> Tổng số có {} file đã thực thi '.format(i))
    f.write('\n=> Thời gian thực thi: ' + str(end_time - start_time))
