import mmap


class PhonemeDictionary:
    def __init__(self, file):
        self.file = file

    def getPhonemesForSentence(self, sentence):
        phones = []
        #Split sentence into words
        for word in sentence.split():
            phones.append("SIL")
            phones += self.getPhonemesForWord(word)
        phones.append("SIL")
        return phones        

    #RETURNS: Array of phonemes for a word
    def getPhonemesForWord(self, word):
        #Covert to lowercase to match dict
        word = "\n" + word.lower() + " "
        phonStr = self.lookUp(word)
        if phonStr is None:
            return None
        return phonStr.split(' ')

    #RETURNS: A string with space-separated phonemes
    def lookUp(self, word):
        #Open the file
        f = open(self.file)
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        idx = s.find(word)
        if(idx >= 0):
            #increase index by the word length to only get the phonemes
            s.seek(idx + len(word))
            #cut off the newline
            phones = s.readline()[:-1]
            return phones
        return None
