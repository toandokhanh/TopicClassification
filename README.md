# Video-based topic classification
This project focuses on video-based topic classification, enabling you to categorize the topics of videos by analyzing the text content extracted from them. The project comprises two primary components:
### VideoToText.py: A Python script for converting videos into text using speech recognition technology. You can execute this script with the following parameters:
    python3 VideoToText.py -video {path/to/video/video.mp4} -l vi -noise {noise/no/deep}
- {path/to/video/video.mp4}: Path to the video file you wish to extract text from.
- -l vi: Specify the video's language (e.g., Vietnamese).
- -noise {noise/no/deep}: Define the level of noise in the video (options: "noise," "no," or "deep").

### CompareText_final.py: A Python script for comparing and categorizing the topics of text segments extracted from videos. You can run this script with the following parameters:

    python3 compareText_final.py {path/txt/origin} {path/video}
- {path/txt/origin}: Path to the directory containing the original text files.
- {path/video}: Path to the folder with the video-to-text conversion results.
