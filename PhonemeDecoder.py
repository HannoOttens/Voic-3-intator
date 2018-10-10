from os import environ, path
import wave
import PhonemeProfile as pp
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "C:\Users\hanno\Google Drive\Vakken\Y3S1\Onderzoeksmethoden\Voice decoder\Voic-3-intator\models"
DATADIR = "/"

class PhonemeDecoder:
    "Keep a profile for the entire duration, this makes it so we can decode multiple files for a complete profile"
    def __init__(self):
        self.profile = pp.PhonemeProfile("en-en")
    
    def addToPhonemeProfile(self, filename):
        segments = self.decode(filename)
        for seg in segments:
            #TODO: Get the audio segments related to the phonemes
            self.profile.addPhoneme(seg.word, seg.prob, [])

        print("Is complete: ", self.profile.isComplete())
        print("Complete %: ", self.profile.completePercentage()*100)
        print("Missing phones: ", reduce(lambda a,b: a + " " + b, self.profile.missingPhonemes(), ""))

    def decode(self, filename):
        # Create a decoder with certain model
        decoder = self.getDecoder()
        decoder.start_utt()
        stream = open(filename, 'rb')
        while True:
          buf = stream.read(1024)
          if buf:
            decoder.process_raw(buf, False, False)
          else:
            break
        decoder.end_utt()

        # segmentStrings = [seg.word + " ("+str(seg.start_frame)+","+str(seg.end_frame)+")\n" for seg in segments]
        # segmentString = ""
        # for ss in segmentStrings:
        #   segmentString += ss
        # print(segmentString)

        segments = [seg for seg in decoder.seg()]
        return segments

        

    #RETURNS: A phoneme decoder with configurated settings
    #TODO: De-hardcode this stuff
    def getDecoder(self):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(MODELDIR, 'en-us\\en-us'))
        config.set_string('-allphone', path.join(MODELDIR, 'en-us\\en-us-phone.lm.dmp'))
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-10)
        config.set_float('-pbeam', 1e-10)

        # Decode streaming data.
        return Decoder(config)

    #RETURNS: The created profile
    def getProfile(self):
        return self.profile
