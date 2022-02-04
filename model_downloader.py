import gensim.downloader as api
import json
info = api.info()
print(json.dumps(info, indent=4))

print(api.load('glove-wiki-gigaword-300', return_path=True))
# print(api.load('word2vec-google-news-300', return_path=True))