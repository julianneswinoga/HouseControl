def wholeWordFind(text, word):
    word = word.strip().lower()
    nums = []
    tempText = text
    while (True): #Check for repeated occurances
        if (str.find(tempText, word) != -1):
            try:
                nums.append(str.find(tempText, word)+len(word)+nums[-1])
            except:
                nums.append(str.find(tempText, word))
            tempText = tempText[nums[-1]+len(word):]
        else:
            break
    for num in nums:
        if (num != -1):
            try:
                if (text[num-1] == " " and (num+len(word) == len(text) or text[num+len(word)] == " ")):
                    return True
                if (num == 0 and text[num+len(word)] == " "):
                    return True
            except:
                pass
    return False
