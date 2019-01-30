from __future__ import unicode_literals


def createTwitterHandleVariations(twitter_handle):

    twitter_handle_with_removed_illegal_characters = ''
    twitter_handle_variation_list = []


    def splitTwitterHandleAndRemoveIllegalCharacters(): #Splits handle into a list and removes illegal characters
        splitted_handle = []
        for letter in twitter_handle:
            if letter == '.' or letter == ',' or letter == '@': pass
            elif letter == '-': splitted_handle.append('_')            #Assume OCR misinterpretation because
            else: splitted_handle.append(letter)                              #          hyphens are illegal
        twitter_handle_variation_list.append(''.join(splitted_handle)) #Adds to list with only modification being

        return splitted_handle                                         #        the removal of illegal characters


    def addUnderscore():
        cleaned_twitter_handle = twitter_handle_variation_list[0].split()
        cleaned_twitter_handle = cleaned_twitter_handle[0]
        cleaned_twitter_handle_with_additions = []
        for letter_index in range(0, len(cleaned_twitter_handle)):
            letter = cleaned_twitter_handle[letter_index]
            print("Letter: "+letter)
            cleaned_twitter_handle_with_additions.append(letter)
            if letter == '_' and cleaned_twitter_handle[letter_index-1] != '_' and letter_index+1 != len(cleaned_twitter_handle) and cleaned_twitter_handle[letter_index+1] != '_':   #Second conditional avoids inserting if it has
                cleaned_twitter_handle_with_additions.append('_')                    # already been done, or if two already exist

        twitter_handle_variation_list.append(''.join(cleaned_twitter_handle_with_additions))
        print("Final Add Underscore: "+ ''.join(cleaned_twitter_handle_with_additions))

    def removeUnderscoreIfTwoArePresent():
        cleaned_twitter_handle = twitter_handle_variation_list[0].split()
        cleaned_twitter_handle = (str(cleaned_twitter_handle[0]))
        cleaned_twitter_handle_with_removals = []
        for letter_index in range(0, len(cleaned_twitter_handle)-1):
            letter = cleaned_twitter_handle[letter_index]
            print(letter)
            if letter == '_' and letter_index+1 != len(cleaned_twitter_handle) and cleaned_twitter_handle[letter_index+1] == '_':
                print('Here')
                cleaned_twitter_handle_with_removals = cleaned_twitter_handle[:letter_index] + cleaned_twitter_handle[letter_index+1:]
                twitter_handle_variation_list.append(''.join(cleaned_twitter_handle_with_removals))
            if letter == '_' and cleaned_twitter_handle[letter_index-1] == '_' and letter_index == len(cleaned_twitter_handle)-1:
                cleaned_twitter_handle_with_removals = cleaned_twitter_handle[:letter_index] + cleaned_twitter_handle[letter_index + 1:]
                print("Splitted Handle With Removals: "+str(cleaned_twitter_handle_with_removals))
                twitter_handle_variation_list.append(''.join(cleaned_twitter_handle_with_removals))
                break

    splitTwitterHandleAndRemoveIllegalCharacters()
    handle_with_illegal_characters_removed = twitter_handle_variation_list[0]
    if '_' in handle_with_illegal_characters_removed:
        addUnderscore()
        removeUnderscoreIfTwoArePresent()

    return twitter_handle_variation_list





def get_tweet_variations(tweet_text):
    tweet_text_string = ''
    for x in range(0, len(tweet_text)):    #Combining lines into one string
        line = tweet_text[x]
        print("This is line before splitting: "+str(line))
        splitted_line = line.split(' ')
        print("Splitted Line: "+str(splitted_line))
        for y in range(0, len(splitted_line)):
            tweet_text_string += (splitted_line[y] + " ")
    combined_lines = tweet_text_string.split()
    print("Tweet Text String: "+tweet_text_string)


    spell_checked = []
    combinations = []

    full_phrase = ''
    for word in splitted_line:
        if word != ' ':
            full_phrase = full_phrase + word +" "

    combinations.append(full_phrase)



    def reset_list():   #Python was being difficult
        new_list = []
        for x in range(0, len(combined_lines)):
            new_list.append(combined_lines[x])
        return new_list


    for search in range(0, len(combined_lines)):
        new_list = reset_list()   #Gross, I know.
        new_list.pop(search)
        if search == len(combined_lines):
            sentence = ''
            for x in range(0, len(combined_lines)-1):
                sentence = sentence + str(combined_lines[x])
            combinations.append(sentence)
        else:
            pass

        combinations.append(' '.join(new_list))

    return (combinations)
