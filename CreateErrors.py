import random
import pyconll
import math
import pandas as pd

def add_dummy_char(word):
    char_list = list(word)
    return ("ß".join(char_list)+"ß")

print(add_dummy_char("Fenerrbahçe Teknik Dirketörü İsmaill Kartal, Alanyasspor ilke 2-2 berbaere kaldıkıları maççın adrından konuştuu."))

def change_chars_prev(word, choice): #olması gerekn gold wordün bli hali
    error_word = list(word)

    curr = error_word[choice]
    next = error_word[choice+1]

    error_word[choice+1]= curr
    error_word[choice] = next
    
    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word)

    return (word_with_error, input_word, output_word)

def change_chars_next(word, choice): #olması gereken gold wordün b li hali
    error_word = list(word)

    curr = error_word[choice]
    next = error_word[choice-1]
    error_word[choice-1]= curr
    error_word[choice] = next

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word)

    return (word_with_error, input_word, output_word)

keyboard_closest_chars = {
    "a": ["w","s","q"],
    "s": ["a","d"],
    "e": ["w","r"],
    "r": ["e","t"],
    "o": ["u","ı", "i"],
    "ı": ["ı","o","k"],
    "i": ["ü"],
    "ü": ["i"],
    "l": ["k"],
    "k": ["l", "m"],
    "m": ["k", "m", "n"],
    "g": ["f","h"],
    "h": ["j","g"],
    "b": ["v", "m"],
    "z": ["a","s"],
    "y": ["u"],
    "t": ["r"],
    "n": ["b","m"],
    "d": ["s","a"],
    "q":["w","a"]
}
consonants = "bcçdfgğhjklmnprsştvyzxwBCÇDFGĞHJKLMNPRSŞTVYZXW"
vowel = "aâeıioöuüAÂEIİOÖUÜ"

def add_random_char_prev(word, choice): #olması gerekn eklenen charda b olması
    #add a random character from all_chars
    error_word = list(word)
    char_to_insert = random.choice(all_chars_list)
    error_word.insert(choice,char_to_insert)

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word_with_error)

    output_chars = list(output_word)
    correction_index = choice + choice-1 +1
    output_chars[correction_index] = "ß"
    correct_output = "".join(output_chars)

    return (word_with_error, input_word, correct_output)

def add_random_char_next(word, choice): #eklenen charda b olması
    #add a random character from all_chars
    error_word = list(word)
    char_to_insert = random.choice(all_chars_list)
    error_word.insert(choice + 1,char_to_insert)

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word_with_error)

    output_chars = list(output_word)
    correction_index = choice + choice +1  +1
    output_chars[correction_index] = "ß"
    correct_output = "".join(output_chars)

    return (word_with_error, input_word, correct_output)

def change_with_random_char(word,choice): #gold wordün bli hali
    error_word = list(word)
    
    char_to_insert = random.choice(all_chars_list)    

    error_word[choice]=char_to_insert

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word)

    return (word_with_error, input_word, output_word)

def del_char(word,choice): #
    error_word = list(word)
    deleted_char = error_word[choice]
    error_word.pop(choice)

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word_with_error)

    output_chars = list(output_word)
    correction_index = choice + choice -1
    output_chars[correction_index] = deleted_char
    correct_output = "".join(output_chars)

    return (word_with_error, input_word, correct_output)

def same_char_repetition(word, choice): #eklenen yere b ekle
    error_word = list(word)
    curr = error_word[choice]

    error_word.insert(choice,curr)

    word_with_error = "".join(error_word)
    input_word = add_dummy_char(word_with_error)
    output_word = add_dummy_char(word_with_error)

    output_chars = list(output_word)
    correction_index = choice + choice-1 + 1
    output_chars[correction_index] = "ß"
    correct_output = "".join(output_chars)

    return (word_with_error, input_word, correct_output)
    
word = "merhaba"
choice = 3

print(change_chars_prev(word,choice))
print(change_chars_next(word,choice))
print(add_random_char_prev(word,choice))
print(add_random_char_next(word,choice))
print(change_with_random_char(word,choice))
print(del_char(word,choice))
print(same_char_repetition(word,choice))


def parse_sents(path):
# Use the iterate version over a larger corpus to save memory
  huge_corpus_iter = pyconll.iter_from_file(path)

  sentences = []
  count = 0
  for sentence in huge_corpus_iter:
    if count != 926 and count != 5459:
      sentences.append(sentence)
    else:
      print(count)
    count+=1

  sentence_text_list= []
  for sentence in sentences:
    if len(sentence.text.split(" "))>1:
        sentence_text_list.append(sentence.text)

  return(sentence_text_list)

train_path = "tr_boun-ud-test.conllu"
sentence_list = parse_sents(train_path)


def get_index_of_available_words(sentence):
  words = sentence.split()
  available_word_indices = [i for i in range(len(words)) if (len(words[i]) > 3 and words[i].isnumeric() == False)]
  return available_word_indices

word_cnt = 0
for sent in sentence_list:
    sent_len = math.ceil(len(sent.split())/2)
    available_words = get_index_of_available_words(sent)
    if len(available_words) > sent_len:
        word_cnt += len(sent)

print(word_cnt)

#total word count = 607746
#8 tane hata var
#her cümlede 1 tane hatalı sözcük her sözcükte 1 hata

error_counts = [0,0,0,0,0,0,0,0]

def apply_errors(error_count_by_word, error_percent_by_sent,sentence_list, error_counts):
    modified_sent_list = []
    error_by_sent = []
    error_counts_by_word = []

    input_sents = []
    output_sents = []

    for sentence in sentence_list:
        sent_errors = [0,0,0,0,0,0,0,0]
        
        words = sentence.split()
        error_by_word = [0] * len(words)
        input_words = [""] * len(words)
        output_words = [""] * len(words)
        sent_len = math.ceil(len(words)/(1/error_percent_by_sent))
        
        available_words = get_index_of_available_words(sentence)

        new_sent = []

        if len(available_words) >= sent_len:
            rand_word_indices = random.sample(available_words,sent_len)
            rand_word_indices.sort()
            for word_ind in rand_word_indices:
                min_error_index = error_counts.index(min(error_counts))
                rand_error_position = random.randint(1,len(words[word_ind])-2)
                word = words[word_ind]
                error_by_word[word_ind] += 1
                match min_error_index:
                    case 0: #change_chars_prev
                        errored_word, input_word, output_word = change_chars_prev(word,rand_error_position)
                        error_counts[0] += 1
                        sent_errors[0] += 1
                    case 1: #change_chars_prev
                        errored_word, input_word, output_word = change_chars_next(word,rand_error_position)
                        error_counts[1] += 1
                        sent_errors[1] += 1
                    case 2: #change_chars_prev
                        errored_word, input_word, output_word = add_random_char_prev(word,rand_error_position)
                        error_counts[2] += 1
                        sent_errors[2] += 1
                    case 3: #change_chars_prev
                        errored_word, input_word, output_word = add_random_char_next(word,rand_error_position)
                        error_counts[3] += 1
                        sent_errors[3] += 1
                    case 4: #change_chars_prev
                        errored_word, input_word, output_word = change_with_random_char(word,rand_error_position)
                        error_counts[4] += 1
                        sent_errors[4] += 1
                    case 5: #change_chars_prev
                        indexes = [i for i, x in enumerate(list(word)) if x in consonants]
                        if len(indexes) > 1:
                            rand_consonant_position = random.randint(1,len(indexes)-1)
                            if indexes[rand_consonant_position] == len(word)-1:
                                rand_consonant_position += -1
                            errored_word, input_word, output_word = del_char(word,indexes[rand_consonant_position])
                            error_counts[5] += 1
                            sent_errors[5] += 1
                        else:
                            errored_word, input_word, output_word = word, add_dummy_char(word), add_dummy_char(word)
                    case 6: #change_chars_prev
                        indexes = [i for i, x in enumerate(list(word)) if x in vowel]
                        if len(indexes) > 1:
                            rand_vowel_position = random.randint(1,len(indexes)-1)
                            if indexes[rand_vowel_position] == len(word)-1:
                                rand_vowel_position += -1
                            errored_word, input_word, output_word = del_char(word,indexes[rand_vowel_position])
                            error_counts[6] += 1
                            sent_errors[6] += 1
                        else:
                            errored_word, input_word, output_word = word, add_dummy_char(word), add_dummy_char(word)
                    case 7: #change_chars_prev
                        errored_word, input_word, output_word = same_char_repetition(word,rand_error_position)
                        error_counts[7] += 1
                        sent_errors[7] += 1

                words[word_ind] = errored_word
                input_words[word_ind] = input_word
                output_words[word_ind] = output_word
            new_sent.append(words)
            modified_sent_list.append(" ".join(new_sent[0]))
        else:
            modified_sent_list.append(sentence)
        error_by_sent.append(sent_errors)
        error_counts_by_word.append(error_by_word)

        for w in range(len(input_words)):
            if input_words[w] == "":
                inp_word = add_dummy_char(words[w])
                input_words[w] = inp_word
            if output_words[w] == "":
                out_word = add_dummy_char(words[w])
                output_words[w] = out_word
        input_sents.append(" ".join(input_words))
        output_sents.append(" ".join(output_words))


    return modified_sent_list, error_counts, error_by_sent, error_counts_by_word, input_sents, output_sents

modified_sentences, errors, errors_for_sentence, errors_for_word, input_sentences, output_sentences = apply_errors(0,0.5, sentence_list,error_counts)


# df = pd.DataFrame({"Original_sent": sentence_list, "Error_sent": modified_sentences, "Errors_for_sentence": errors_for_sentence, "Errors_for_word": errors_for_word})
# df.to_excel("boun_test_spelling_mistakes_050.xlsx")

# df_inp_out = pd.DataFrame({"Input_sentences": input_sentences, "Output_sentences": output_sentences})
# df_inp_out.to_excel("boun_test_050_inp_out.xlsx")


print(errors)
# #print(errors_for_word)
        
        



        
          


