import math

def cosine_similarity(vec1, vec2):
    words = vec1.keys()
    num = 0
    den1 = 0
    den2 = 0
    den = 0
    vec1_vals = list(vec1.values())
    vec2_vals = list(vec2.values())

    for word in words:
        if word in vec1 and word in vec2:
            num += vec1.get(word) * vec2.get(word)

    for i in range(len(vec1_vals)):
        temp = (vec1_vals[i])**2
        den1 += temp
    
    for i in range(len(vec2_vals)):
        temp = (vec2_vals[i])**2
        den2 += temp
    
    den = (den1 * den2)**0.5
    return num/den

def build_semantic_descriptors(sentences):
    descriptor = {}

    for sentence in sentences:
        s_vocab = {}
        for word in sentence:
            # Create a dictionary with all the words from the sentence
            word = word.lower()
            n = s_vocab.get(word, 0)
            s_vocab.update({word : n+1})
        for word in sentence:
            # a) Remove the word of interest from the dictionary, and b) combine
            # it with the descriptor that the word previously had. 
            count = s_vocab.pop(word)
            cur_desc = descriptor.get(word, {})

            for entry in s_vocab:
                if entry in cur_desc:
                    cur_desc[entry] += s_vocab[entry]
                else: cur_desc.update({entry : s_vocab[entry]})
                descriptor.update ({word : cur_desc})
            
            s_vocab.update({word: count})
    return descriptor


def build_semantic_descriptors_from_files(filenames):
    sentences_list = []
    for doc in filenames:
        f = open(doc, "r", encoding="utf-8")
        f = f.read()
        f = f.lower()
        # replace punctuation with spaces
        f = f.replace(",", " ")
        f = f.replace("-", " ")
        f = f.replace("--", " ")
        f = f.replace(":", " ")
        f = f.replace(";", " ")
        f = f.replace("\n", " ")
        f = f.replace("'", " ")
        f = f.replace("'", " ")
        f = f.replace('"', " ")
        f = f.replace('“', " ")
        f = f.replace('”', " ")
        f = f.replace("  ", " ")
        f = f.replace("‘", " ")
        f = f.replace("’", " ")
        f = f.replace("...", " ")
        # replace '!', '?' with periods
        f = f.replace("!", ".")
        f = f.replace("?", ".")

        sentences = f.split(".")
        for sentence in sentences:
            sentences_list.append(sentence.split())
        desc = build_semantic_descriptors(sentences_list)
    return desc


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    word = word.lower()
    sim_list = []
    for i in range(len(choices)):
        choices[i] = choices[i].lower()
        if choices[i] not in semantic_descriptors:
            sim_list.append(-1)
        else: sim_list.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]]))
    best = max(sim_list)
    ind = sim_list.index(best)
    return choices[ind]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding ='utf-8')
    f = f.read()
    f = f.lower()
    f = f.split("\n")
    lines = []
    for item in f:
        if item != "":
            lines.append(item.split())
    correct_count = 0
    for line in lines:
        if most_similar_word(line[0], line[2:], semantic_descriptors, similarity_fn) == line[1]:
            correct_count += 1
    return correct_count/len(lines) * 100

if __name__ == '__main__':
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
