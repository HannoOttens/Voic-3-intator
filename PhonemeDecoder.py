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
        self.decode(filename)
        
        print("Is complete: ", self.profile.isComplete())
        print("Complete %: ", self.profile.completePercentage()*100)
        print("Missing phones: ", reduce(lambda a,b: a + " " + b, self.profile.missingPhonemes(), ""))

    def decode(self, filename):
        # Create a decoder with certain model
        decoder = self.getPhonemeDecoder()
        
        file = "";
        decoder.start_utt()
        buflen = 0
        with open(filename, 'rb') as stream:
            while True:
              buf = stream.read(1024)
              if buf:
                decoder.process_raw(buf, False, False)
                buflen += (len(buf))
                file += buf;
              else:
                break
        decoder.end_utt()
        segments = [seg for seg in decoder.seg()]
        filelen = len(file)
        filetime = len(file)/(320.0/4.0) #In 100ths of a second

        print("FILELENGTH: ",len(file))
        print("BUFLEN: ",buflen)
        print("FILETIME: ", filetime)
        endbyte = int(filelen*(segments[-1].end_frame/filetime))
        print("PROJECTED ENDBYTE: ",endbyte)
        print("ENDFRAM: ", segments[-1].end_frame)

        import numpy as N
        import array
        fileobj = open(filename, mode='rb')
        binvalues = array.array('f')
        binvalues.read(fileobj, filelen/4)

        # data = N.array(binvalues, dtype=float)

        for seg in segments:
            startbyte = int(filelen*(seg.start_frame/filetime))
            endbyte = int(filelen*(seg.end_frame/filetime))
            print(seg.word, startbyte, endbyte)
            self.profile.addPhoneme(seg.word, abs(seg.ascore), binvalues[startbyte:endbyte])

        

        # segmentStrings = [seg.word + " ("+str(seg.start_frame)+","+str(seg.end_frame)+")\n" for seg in segments]
        # segmentString = ""
        # for ss in segmentStrings:
        #   segmentString += ss
        # print(segmentString)

        

    #RETURNS: A phoneme decoder with configurated settings
    #TODO: De-hardcode this stuff
    def getPhonemeDecoder(self):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(MODELDIR, 'en-us\\en-us'))
        config.set_string('-allphone', path.join(MODELDIR, 'en-us\\en-us-phone.lm.dmp'))
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-10)
        config.set_float('-pbeam', 1e-10)

        # Decode streaming data.
        return Decoder(config)

    def getDictionaryDecoder(self):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
        config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
        return Decoder(config)


    #RETURNS: The created profile
    def getProfile(self):
        return self.profile
