from gensim import models

import json
import numpy as np

MODEL_VERSION = "glove-wiki-gigaword-300"
model = models.KeyedVectors.load_word2vec_format(MODEL_VERSION)


def get_word_vec(word_list):
    """
    This method will get the vector of the given word
    :param word_list: list of a single word string
    :return: the vector list of this word
    """
    result = {"status_code": "0000"}
    if len(word_list) > 1:
        result["status_code"] = "0001"
        result["result_info"] = "Expect one wordString for getVec"
        return result
    word = word_list[0]
    try:
        vec = model.get_vector(word)
        result["vec"] = str(np.array(vec).tolist())
    except Exception as e:
        result["status_code"] = "0001"
        result["result_info"] = str(e)
    return result


def get_sim_by_word(word_list):
    """
    This method will return a list of the similar words by the given word
    :param word_list: list of a single word string
    :return: the sim words list of the given word
    """
    result = {"status_code": "0000"}
    if len(word_list) > 1:
        result["status_code"] = "0001"
        result["result_info"] = "Expect one wordString for getSim"
        return result
    word = word_list[0]
    try:
        sim_words = model.similar_by_word(word)
        result["sim_words"] = sim_words
    except Exception as e:
        result["status_code"] = "0001"
        result["result_info"] = str(e)
    return result


def get_similarity_between(word_list):
    """
    This method will get the similarity of two given words
    :param word_list: list of two words A B for similarity calculation
    :return: cosine similarity of the two given words
    """
    result = {"status_code": "0000"}
    if len(word_list) != 2:
        result["status_code"] = "0001"
        result["result_info"] = "Expect two wordString for getSimBetween"
        return result
    try:
        word_a = word_list[0]
        word_b = word_list[1]
        similarity = model.similarity(word_a, word_b)
        result["similarity"] = str(similarity)
    except Exception as e:
        result["status_code"] = "0001"
        result["result_info"] = str(e)
    return result


method_dispatcher = {
    "getVec": lambda word_list,: get_word_vec(word_list),
    "getSim": lambda word_list,: get_sim_by_word(word_list),
    "getSimBetween": lambda word_list,: get_similarity_between(word_list)
}


def validate_event(event):
    """
    This function will validate the event send from API gateway to Lambda and raise exception if exists
    :param event:
    :return:
    """
    params = event["multiValueQueryStringParameters"]

    if "method" not in params.keys() or "wordString" not in params.keys():
        raise Exception('"method" and "wordString" are expected as the Query Params')
        # flag = False
    method = params.get("method")
    if len(method) != 1:
        # flag = False
        raise Exception('Expect one value for method param')
    method = method[0]
    if method not in method_dispatcher.keys():
        # flag = False
        raise Exception('method must be in one of ' + str(list(method_dispatcher.keys())))


def lambda_handler(event, context):
    result = {}
    response = {
        'statusCode': 200,
        'body': ""
    }
    try:
        validate_event(event)
    except Exception as e:
        result["status_code"] = "0001"
        result["result_info"] = str(e)
        result["request_info"] = event["multiValueQueryStringParameters"]
        result["model_version"] = MODEL_VERSION
        response["body"] = json.dumps(result)
        return response

    params = event["multiValueQueryStringParameters"]
    method = params["method"][0]
    word_list = params["wordString"]
    result = method_dispatcher[method](word_list)
    result["request_info"] = event["multiValueQueryStringParameters"]
    result["model_version"] = MODEL_VERSION
    response["body"] = json.dumps(result)
    print(response)
    return response


if __name__ == "__main__":
    f = open('mock_event.json')
    mock_event = json.load(f)
    f.close()
    print(lambda_handler(mock_event, context=""))
