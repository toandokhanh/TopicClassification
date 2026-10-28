# Video topic-tagging experiments

A small 2023 experiment extracting speech from video and using Underthesea's existing Vietnamese classifier to tag transcript topics. This repository does not train a new topic-classification model.

## Scripts

```sh
python3 VideoToText.py -video data/input.mp4 -l vi -noise no
python3 compareText_final.py data/reference-transcripts data/processed-transcripts
```

The first script requires FFmpeg, speech recognition and the historical dependencies listed in `requirements.txt`. The optional `deep` noise mode also requires DeepFilterNet's `deepFilter` executable. Run from the repository root. Dataset files are not included.

The comparison utility matches related transcript filenames and writes `result/result.txt`:

- Pairwise TF-IDF cosine similarity measures transcript overlap.
- Filename-label agreement compares topic tags encoded in filenames. It is **not an independent classifier-accuracy measurement**. Any use as an evaluation requires documenting how those tags were produced and supplying independent ground-truth labels.

`compareText.py` and `compareText_v1.py` are earlier comparison variants. `convert.py` converts numeric words in text; its unused import of a missing subtitle utility was removed during cleanup.

This is preserved as an exploratory research component. It has not been rerun against its original dataset or validated with current external APIs. See [third-party notices](THIRD_PARTY_NOTICES.md).
