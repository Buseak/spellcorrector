import random
import pyconll
import math
def change_chars_prev(word, choice):
    char_list = list(word)

    curr = char_list[choice]
    next = char_list[choice+1]

    char_list[choice+1]= curr
    char_list[choice] = next
        
    return ("".join(char_list))

def change_chars_next(word, choice):
    char_list = list(word)

    curr = char_list[choice]
    next = char_list[choice-1]
    char_list[choice-1]= curr
    char_list[choice] = next
        
    return ("".join(char_list))

all_chars = "qwertyuıopğüasdfghjklşizxcvbnmöç"
all_chars_list = list(all_chars)
consonants = "bcçdfgğhjklmnprsştvyzxwBCÇDFGĞHJKLMNPRSŞTVYZXW"
vowel = "aâeıioöuüAÂEIİOÖUÜ"

def add_random_char_prev(word, choice):
    #add a random character from all_chars
    char_list = list(word)
    char_to_insert = random.choice(all_chars_list)
    char_list.insert(choice,char_to_insert)

    return ("".join(char_list))

def add_random_char_next(word, choice):
    #add a random character from all_chars
    char_list = list(word)
    char_to_insert = random.choice(all_chars_list)
    char_list.insert(choice + 1,char_to_insert)

    return ("".join(char_list))

def change_with_random_char(word,choice):
    char_list = list(word)
    
    char_to_insert = random.choice(all_chars_list)    

    char_list[choice]=char_to_insert
    return ("".join(char_list))

def del_char(word,choice):
    char_list = list(word)
  
    char_list.pop(choice)

    return ("".join(char_list))

def same_char_repetition(word, choice):
    char_list = list(word)
    curr = char_list[choice]

    char_list.insert(choice,curr)
    return ("".join(char_list))


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

train_path = "tr_boun-ud-train.conllu"
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
    for sentence in sentence_list:
        words = sentence.split()
        sent_len = math.ceil(len(words)/2)
        
        available_words = get_index_of_available_words(sentence)

        new_sent = []

        if len(available_words) >= sent_len:
            for word_ind in available_words:
                min_error_index = error_counts.index(min(error_counts))
                rand_error_position = random.randint(1,len(words[word_ind])-2)
                word = words[word_ind]
                match min_error_index:
                    case 0: #change_chars_prev
                        new_word = change_chars_prev(word,rand_error_position)
                        error_counts[0] += 1
                    case 1: #change_chars_prev
                        new_word = change_chars_next(word,rand_error_position)
                        error_counts[1] += 1
                    case 2: #change_chars_prev
                        new_word = add_random_char_prev(word,rand_error_position)
                        error_counts[2] += 1
                    case 3: #change_chars_prev
                        new_word = add_random_char_next(word,rand_error_position)
                        error_counts[3] += 1
                    case 4: #change_chars_prev
                        new_word = change_with_random_char(word,rand_error_position)
                        error_counts[4] += 1
                    case 5: #change_chars_prev
                        indexes = [i for i, x in enumerate(list(word)) if x in consonants]
                        if len(indexes) > 1:
                            rand_consonant_position = random.choice(indexes)
                            new_word = del_char(word,rand_consonant_position)
                            error_counts[5] += 1
                    case 6: #change_chars_prev
                        indexes = [i for i, x in enumerate(list(word)) if x in vowel]
                        if len(indexes) > 1:
                            rand_vowel_position = random.choice(indexes)
                            new_word = del_char(word,rand_vowel_position)
                            error_counts[6] += 1
                    case 7: #change_chars_prev
                        new_word = same_char_repetition(word,rand_error_position)
                        error_counts[7] += 1

                new_sent.append(new_word)
            modified_sent_list.append(" ".join(new_sent))
        else:
            modified_sent_list.append(sentence)

    return modified_sent_list, error_counts

modified_sentences, errors = apply_errors(0,0, sentence_list,error_counts)

print(modified_sentences)
print(errors)
        
        



        
          


