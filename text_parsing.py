import enchant
english_dict = enchant.Dict("en_US")


def parse_text(ocr_output):

    def compare_method_outputs(split_text_tuple):
       line_comparisons = {}
       a = split_text_tuple[0]
       b = split_text_tuple[1]

       print(a, b)

       comparable_lines = None
       comparable_line_length = None
       if len(a) >= len(b):
           comparable_lines = len(b)
       else:
           comparable_lines = len(a)

       for x in range (0, comparable_lines):
           similarities = 0
           differences = 0
           comparable_line_a = a[x]
           comparable_line_b = b[x]

           if len(comparable_line_a) >= len(comparable_line_b):
               comparable_line_length = len(comparable_line_b)
           else:
               comparable_line_length = len(comparable_line_a)

           for y in range(0, comparable_line_length):
               if comparable_line_a[y] == comparable_line_b[y]:
                   similarities+=1
               else:
                   differences+=1

               if y == comparable_line_length -1:
                   print ("Similarities: " + str(similarities))
                   print ("Differences: " + str(differences))

                   print("Line A: " +comparable_line_a)
                   print("Line B: "+comparable_line_b)


    def combine_line(spell_checked_line_list):
        combined = ''
        for x in range(0, len(spell_checked_line_list)):
            combined = combined + spell_checked_line_list[x]
        return combined


    def get_username(ocr_output):  # Finds username by searching for first '@' symbol in text


        for searching in range(0, len(ocr_output)):
            line = ocr_output[searching].split()
            print(str(line))
            for word in range(0, len(line)):
                selected_word = line[word]
                # print("This is selected word: " +selected_word)
                if '@' in selected_word:
                    print("@ found in image")

                    if len(selected_word) == 1:   #If standalone '@' is found, not associated with handle
                        print('Unaccompanied @')

                    elif selected_word[len(selected_word)-1] == '@': #ex: Neil deGrasse Tyson@  @neiltyson
                        print('@ at the end of word')
                        break

                    elif len(selected_word) < 4:                      #Minimum length is now four characters
                        break

                    else:
                        for letter in range(0, len(selected_word)):
                            if '@' == selected_word[letter]:
                                starting_char = letter
                                twitter_handle = selected_word[starting_char:]
                                print("Found Twitter Handle: " + twitter_handle)
                                line_found_on = searching

                                return twitter_handle, line_found_on

                            else:
                                pass
                else:
                    pass
        return None




    def find_viable_lines(splittedText, twitter_handle_line):  # Find lines that aren't largely made up of numbers
        print("Finding Viable Lines...")
        first_alpha_line_found = False
        viable_lines = []
        numbers = 0

        for lineSearch in range((twitter_handle_line) + 1, len(splittedText)):
            line_being_searched = splittedText[lineSearch]

            for chars in range(0, len(line_being_searched)):
                char = line_being_searched[chars]
                if char.isalpha():
                    first_alpha_line_found = True

            if line_being_searched == '' and first_alpha_line_found == False:  #Blank lines, indicated by '' , usually refer to the end of a tweet body and the start of a photo
                pass
            elif line_being_searched == '' and first_alpha_line_found == True:
                return viable_lines

            for char_search in range(0, len(line_being_searched)):
                char = line_being_searched[char_search]  # Character in Word

                if char.isalpha():
                    pass
                else:
                    numbers += 1

            if numbers >= (len(line_being_searched) / 2):
                pass
            else:
                viable_lines.append(line_being_searched)
                numbers = 0

        return viable_lines   #list


    def spell_check_lines(viable_lines): #Parses lines and removes words that were most likely interpreted incorrectly

        spell_checked_lines_list = []

        for lines in range(0, len(viable_lines)):
            line = viable_lines[lines]
            new_line = ''
            words = line.split()
            print("Spell checking line #"+str(lines))
            all_words_good = True
            for word in range(0, len(words)):
                if english_dict.check(words[word]):
                   new_line = new_line + " "+ words[word]
                else:
                    pass
            print("New Line: "+new_line)
            spell_checked_lines_list.append(new_line)

        return spell_checked_lines_list   #list



    def preCheckOfWordCount(spell_checked_list):
        print("Printing Words: ")

        for line in spell_checked_list:
            if len(line.split()) <=2 and len(spell_checked_list) == 1:
                print("None")
                return None
            else:
                print("Done Pre Check of Words")
                return spell_checked_list


    def get_search_terms(spell_checked):
        #Only use lines larger than or equal to three lines
        #Checking how many words are in the spell checked lines
        if len(spell_checked) >= 3:
            search_terms = spell_checked[0] + spell_checked[1]   # Combine two lines in order to (hopefully) increase odds of finding the tweet
        else:
            try:
                search_terms = spell_checked[0]
            except:
                return ' '

        return search_terms


    def method_handler(split_text_tuple):    #Method initiated when function is called
        getUsername_output = get_username(split_text_tuple)
        if getUsername_output is None: return None
        else:
            username_found_on_line = getUsername_output[1]
            username = getUsername_output[0]
            viable_lines = find_viable_lines(ocr_output, username_found_on_line)   #list
            spell_checked_lines_list = spell_check_lines(viable_lines)             #list
            spell_checked_lines_list = preCheckOfWordCount(spell_checked_lines_list) #list or None
            return username, spell_checked_lines_list


    username_and_tweetlines = method_handler(ocr_output)
    return username_and_tweetlines