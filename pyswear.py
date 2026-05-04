def messageProfanity(message, debug=False, profanity_percent = 0.85):
    # threshold based profanity checking
    # checks first letter for swears in list, and then checks rest of word for equality
    # longer messages are less sensitive to swears

    message = message.lower()

    profanity = [
        'fuck', 'shit', 'bollocks', 'penis', 'bitch', 'cunt', 'epstein', 'nigger', 'nigga', 
        'pork', 'damn', 'slut', 'daddy', 'digger', 'sexy', 'sloppy', 'toppy', 'pervert', 'perverted', 
        'sucking', 'dick', 'vagina', 'coochie', 'sahur', 'tung', 'pegged', 'pegging', 'twerk']
    
    for a in profanity: # simple first check
        if a in message:
            return True, a
        

    formatted_message = "" # remove spaces
    for all in message:
        if (all!=" "):
            formatted_message+=all

    percent_allowed = profanity_percent

    aliases = "1234567890-=!@#$%^&*()_+~"
    
    for swear in profanity:
        curr_index = 0
        for letter in formatted_message:
            
            if letter == swear[0]:
                if debug:
                    print("")
                    print(f"Possible swear at {curr_index}: {letter} ({swear})")
                num_right = 1
                skipping_letters = False # true if possible skipping of letters

                found_swear = []

                # begin swear search
                for i in range(len(swear)):

                    if curr_index+i+1 < len(formatted_message):
                        if debug:
                            print(f"")

                        if (skipping_letters and (i==(len(swear)-1))):
                            continue # skip, because there might be skipping of letters.
                    
                        if formatted_message[curr_index+i] == swear[i]:
                            num_right+=1
                            found_swear.append((swear[i], curr_index+i, "exact")) # add to plausible swear
                            if debug:
                                print(f"Swear {swear[i]} matches letter {formatted_message[curr_index+i]}")
                            continue
                        
                        if formatted_message[curr_index+i+1] == swear[i]:
                            num_right +=0.7 # a stretch but we'll see
                            found_swear.append((swear[i], curr_index+i+1, "partial")) # add to plausible swear
                            if debug:
                                print(f"Swear {swear[i]} may match letter {formatted_message[curr_index+i+1]}")
                            continue

                        if (len(swear) > i+1):
                            if formatted_message[curr_index+i] == swear[i+1]:
                                num_right +=0.65 - (curr_index/(10*len(swear))) # a stretch but we'll see
                                
                                skipping_letters = True

                                found_swear.append((swear[i+1], curr_index+i, "skipped")) # add to plausible swear
                                if debug:
                                    print(f"Swear {swear[i+1]} may match letter {formatted_message[curr_index+i]} (skipped letter in swear)")
                                continue

                        # check to see if it's an alias
                        if formatted_message[curr_index+i] in aliases:
                            num_right+=0.5
                            found_swear.append((formatted_message[curr_index+i], curr_index+i, "alias")) # add to plausible swear
                            if debug:
                                print(f"Swear {swear[i]} may be alias for {formatted_message[curr_index+i]}")
                            continue

                        else: 
                            
                            num_right-=0.5 + (curr_index/(85*len(swear))) # may be incorrect!
                            if debug:
                                print(f"Letter {formatted_message[curr_index+i]} probably not part of swear")

                if skipping_letters:
                    computed = (num_right)/(len(swear)-1)
                    
                else:
                    computed = (num_right)/len(swear)
                
                if computed >= percent_allowed:
                    if debug:
                        print(f"Swear found! {swear}, {computed}")
                    return True, swear
                if debug:
                    print(f"Did not find swear, threshold: {computed}")
            
            curr_index+=1
                
    return False, None,

def cleanAsciiArt(message, debug=False):
    # checks for things like l< == k and |~| = h by finding them in the text
    # and replacing them with actual characters

    ascii_counterparts = {
        "k":["l<", "]<", "|<", "[<", "I<"],
        "h":["|~|", "|-|", "]-[", "]~["],
        "o":["[]", "()"],
        "n":["||", r"|\|", r"]\["],
        "a":["/\\"],
        "i":["|", "][", ";"]
    }
    formatted_message = "" # remove spaces
    for all in message:
        if (all!=" "):
            formatted_message+=all

    message = formatted_message 

    message_mods = [] # should contain an index and then a copy of the character to replace

    for x in range(len(message)):
        for key in ascii_counterparts.keys():
            for item in ascii_counterparts.get(key):
                valid = True
                for i in range(len(item)):
                    if item[i]!=message[x+i]:
                        valid = False
                        break
                if valid:
                    message_mods.append([x, item, key])
                    
    message_mods.sort(key=lambda x: (len(x[1])), reverse=True)
    if debug:
        print(message_mods)



    for mod in message_mods:
        position = mod[0]
        ascii_char = mod[1]
        replacement_char = mod[2]
        

        if message[position] != ascii_char[0]:
            break # already fixed all ascii characters.
        
        message = message[0:position:] + replacement_char + message[position+len(ascii_char):len(message):]
        
        # loop through and update all mods for future positions
        for mod2 in message_mods:
            if position<mod2[0]:
                mod2[0]-=len(ascii_char)-1

    if debug:
        print(message)

    return message

def letterSwap(message, debug = False):
    # check before running main check, as this one requires spacing
    word_groups = []
    processed_words = []

    profanity = [
        'fuck', 'shit', 'bollocks', 'penis', 'bitch', 'cunt', 'epstein', 'nigger', 'nigga', 
        'pork', 'damn', 'slut', 'daddy', 'digger', 'sexy', 'sloppy', 'toppy', 'pervert', 'perverted', 
        'sucking', 'dick', 'vagina', 'coochie', 'sahur', 'tung', 'pegged', 'pegging', 'twerk']


    # split into words
    currword = ""
    for i in range(len(message)):
        if message[i]==" ":
            word_groups.append(currword)
            currword=""
        if i+1==len(message):
            if len(currword)>1:
                word_groups.append(currword + message[i])
        else:
            currword+=message[i]

    currword = ""

    for word in word_groups:
        for char in word:
            if char!=" ":
                currword+=char
        processed_words.append(currword)
        currword = ""
                

    for word in processed_words:
        if word in profanity:
            return True, word # most likely will not happen, they'll be smarter
        
    if debug:
        print(processed_words)
        
    for i in range(len(processed_words)):
        if i+1<len(processed_words):
            temp = processed_words[i][0] + processed_words[i+1][1::]
            if debug:
                print(f"Letters swapped is: {temp}")

        else:
            temp = processed_words[i][0] + processed_words[0][1::]
            if debug:
                print(f"Letters swapped is: {temp}")
        if temp in profanity:
            return True, temp
    return False, None
    


def validate_text(message, ascii_clean = True, allow_utf8=False, letter_swap_test = True, check_reverse = False, debug = False, profanity_percent = 0.85):

    # check ascii
    if not allow_utf8:
        if not message.isascii():
            return True, "Message uses non-ASCII characters. Please only use ASCII characters."
    message = message.lower()

    # clean ascii art
    if ascii_clean:
        message = cleanAsciiArt(message, debug)

    # check letter swapping
    if letter_swap_test:
        res, reas = letterSwap(message, debug)
        if res:
            return True, "Message contains letter swap based profanity: " +reas

    # main check
    val, reason = messageProfanity(message, debug)
    if val:
        return val, reason

    if check_reverse:
        if not val:
            val, reason = messageProfanity(message[::-1], debug)
    return val, reason



# although the filter may have some issues, as they roll in I'll fix them ASAP.

msg = r""


val, swear = validate_text(msg, debug=True)
print(f"\nprofanity found: {val} \nreason: {swear} \n")
