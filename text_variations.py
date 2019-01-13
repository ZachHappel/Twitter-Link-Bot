from __future__ import unicode_literals


def get_screenname_variations(username, character):
    combinations_to_return = []


    def get_username_list():
        username_list = []
        for adding in range(0, len(username)):
            if '.' == username[adding]:
                pass
            elif '@' == username[adding]:
                pass
            else:
                username_list.append(username[adding])
        return username_list



    def create_vars_add(char, count, username_list):    #Adding extra "-"/"_"
        locations = []
        to_add = char*count
        modified_username_list = username_list
        for search in range(0, len(username)):
            if username[search] == char:
                locations.append(search)
        for location in range(0, len(locations)):
            modified_username_list.insert(locations[location], to_add)
        return modified_username_list



    def create_vars_sub(char, count, username_list):    #Subtracting extra "-"/"_"
        locations = []


        modified_username_list = username_list
        for search in range(0, len(username)):
            if username[search] == char:
                locations.append(search)

        for location in range(0, len(locations)):
            modified_username_list.pop(locations[location])


        return modified_username_list

  #     Handling '-' '_' characters     #

    #            Adding               #
    username_list = get_username_list()
    if character != ' ':
        new_username_list = (create_vars_add(character, 1, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)
        new_username_list = (create_vars_add(character, 2, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)
        new_username_list = (create_vars_sub(character, 2, username_list))
        combination = ''.join(new_username_list)
        combinations_to_return.append(combination)



        #           Other               #
    if username[len(username) - 1] == 'a':  # Creating combinations without the 'a' at the end
        combinations_to_return.append(username)  # Some mobile screenshots will appear to have an 'a' at the end if verified symbol is present
        for searching in range(0, len(combinations_to_return)):
            selected_username = combinations_to_return[searching]
            combinations_to_return.append(selected_username[:len(selected_username) - 1])
    else:
        pass

    duplicates_removed = [username]

    for x in range(0, len(combinations_to_return)):
        combo = combinations_to_return[x]
        if combo in duplicates_removed:
            pass
        else:
            duplicates_removed.append(combo)

    return duplicates_removed


#print(get_screenname_variations("zach--happela"))


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
