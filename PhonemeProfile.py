import array

"Codes matching sphinx output"
class PhonemeProfile:
    def __init__(self, name):
        self.name = name
        self.phonemes = {
            "AA": None,
            "AE": None,
            "AH": None,
            "AO": None,
            "AW": None,
            "AY": None,
            "B": None,
            "CH": None,
            "D": None,
            "DH": None,
            "EH": None,
            "ER": None,
            "EY": None,
            "F": None,
            "G": None,
            "HH": None,
            "IH": None,
            "IY": None,
            "JH": None,
            "K": None,
            "L": None,
            "M": None,
            "N": None,
            "NG": None,
            "OW": None,
            "OY": None,
            "P": None,
            "R": None,
            "S": None,
            "SH": None,
            "T": None,
            "TH": None,
            "UH": None,
            "UW": None,
            "V": None,
            "W": None,
            "Y": None,
            "Z": None,
            "ZH": None,
            "SIL": None,
            "+SPN+": None,
            "+NSN+": None,
            # "ue": 0,
        }

    #Replaces a phoneme when the accuracy of the recognition is higher (or when it wasn't filled in yet)
    def addPhoneme(self, word, accuracy, segmentClip):
        if(self.phonemes[word] is None 
            #Check if this prediction is more accurate than the previous, if so, replace it.
            or self.phonemes[word].accuracy > accuracy):
            # print "UPDATED: " + word + " \t|| ACC: " + str(accuracy) + "\t|| CLIPSIZE:" + str(len(segmentClip)) 
            self.phonemes[word] = Phoneme(accuracy, segmentClip, word)

    #RETURNS: If all the phonmes of the profile are filled in
    def isComplete(self):
        for phoneme in self.phonemes.itervalues():
           if(phoneme is None): 
               return False
        return True

    #RETURNS: The percentage (float) of filled in phonemes
    def completePercentage(self):
        return reduce(lambda a,b: a + (1 if b is not None else 0), self.phonemes.itervalues(), 0) / float(len(self.phonemes))
       
    #RETURNS: A list of to-be recorded phonemes
    def missingPhonemes(self):
        misPhones = []
        for key,phoneme in self.phonemes.iteritems():
           if(phoneme is None): 
               misPhones.append(key)
        return misPhones

    #RETURNS: A list of recorded phonemes
    def recordedPhonemes(self):
        recPhones = []
        for key,phoneme in self.phonemes.iteritems():
           if(phoneme is not None): 
               recPhones.append(key)
        return recPhones

    #RETURNS: Average accuracy of phoneme recognition
    def phonemeAccuracy(self):
        #exception when the model is incomplete
        if(not self.isComplete):
            raise ValueError("The phoneme model wasn't not complete")
        #add all of te phonemes up and devide by the total
        return reduce(lambda a,b: a + b.accuracy, self.phonemes, 0) / float(len(self.phonemes))
        
    #RETURNS: An array of floats represeting the sound of the phoneme
    def getPhonemeClip(self, phoneme):
        if(phoneme is 'SIL'):
            return self.getSilence()

        p = self.phonemes[phoneme]
        if p is not None:
            return p.clip

        print "[ERROR] MISSING PHONEME: " + phoneme
        return []

    #RETURNS: An array of floats, representing the audio equivalent of silence (1280x0.0)
    def getSilence(self): 
        silence = array.array('f')
        for i in range(1280):
            silence.append(0.0)
        return silence
    
    #RETURNS: An array of floats, representing the audio equivalent of silence (1280x0.0)
    def getPadding(self): 
        padding = array.array('f')
        for i in range(8):
            padding.append(0.0)
        return padding

    #RETURNS: A clip of phonemes sequenced back-to-back
    def createSequence(self, phonemes):
        clip = array.array('f')
        for phon in phonemes:
            clip.extend(self.getPadding())
            clip.extend(self.getPhonemeClip(phon))
        return clip 

class Phoneme:
    def __init__(self, accuracy, clip, word):
        self.accuracy = accuracy
        self.clip = clip
        self.word = word

"Original Codes"
# class PhonemeProfile:
#     def __init__(self, name):
#         self.name = name
#         self.phonemes = {
#             "/b/": 0,
#             "/d/": 0,
#             "/f/": 0,
#             "/g/": 0,
#             "/h/": 0,
#             "/j/": 0,
#             "/k/": 0,
#             "/l/": 0,
#             "/m/": 0,
#             "/n/": 0,
#             "/ng/": 0,
#             "/p/": 0,
#             "/r/": 0,
#             "/s/": 0,
#             "/t/": 0,
#             "/v/": 0,
#             "/w/": 0,
#             "/y/": 0,
#             "/z/": 0,
#             "/sh/": 0,
#             "/th_u/": 0,
#             "/d_v/": 0,
#             "/a/": 0,
#             "/e/": 0,
#             "/i/": 0,
#             "/o/": 0,
#             "/u/": 0,
#             "/oo/": 0,
#             "/a_/": 0,
#             "/e_/": 0,
#             "/i_/": 0,
#             "/o_/": 0,
#             "/u_/": 0,
#             "/y_u/": 0,
#             "/oi/": 0,
#             "/ow/": 0,
#             "/_e_/": 0,
#             "/_a_/": 0,
#             "/-a-/": 0,
#             "/_u_/": 0,
#             "/_o_/": 0,
#             "/ea/": 0,
#             "/ue/": 0,
#         }