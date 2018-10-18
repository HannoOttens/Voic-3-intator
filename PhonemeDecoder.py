from os import environ, path, remove
import wave
import PhonemeProfile as pp
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import numpy as N
import array


class PhonemeDecoder:
    "Keep a profile for the entire duration, this makes it so we can decode multiple files for a complete profile"
    def __init__(self, modeldir, datadir, segmentdir):
        self.profile = pp.PhonemeProfile("en-en")
        self.modeldir = modeldir
        self.datadir = datadir
        self.segmentdir = segmentdir
    
    def addToPhonemeProfile(self, filename):
        filepath = path.join(self.datadir, filename)
        print filepath        
        nWords = self.splitToWords(filepath)
        for n in range(nWords):
            self.decode(path.join(self.segmentdir, self.getNthSegmentName(n)))

    def splitToWords(self, filename):
        decoder = self.getDictionaryDecoder()
        filelen = 0
        decoder.start_utt()
        with open(filename, 'rb') as stream:
            while True:
              buf = stream.read(1024)
              if buf:
                decoder.process_raw(buf, False, False)
                filelen += (len(buf))
              else:
                break
        decoder.end_utt()
        segments = [seg for seg in decoder.seg()]

        #In 100ths of a second
        filetime = filelen/(320.0/4.0) 
         
        #Read bindary from file
        fileobj = open(filename, mode='rb')
        binvalues = array.array('f')
        binvalues.read(fileobj, filelen/4)

        filelen = float(filelen)
        n = 0
        for seg in segments:
            #skip silences
            if seg.word in ["<s>","<sil>","</s>"]:
                continue
            startbyte = int(filelen*(seg.start_frame/filetime))
            endbyte = int(filelen*(seg.end_frame/filetime))
            self.saveSegment(n, binvalues[startbyte:endbyte])
            n+=1
        return n        

    def saveSegment(self, n, segment):
        filename = self.getNthSegmentName(n)
        print filename
        f = open(path.join(self.segmentdir,filename),  'wb')
        segment.tofile(f)
        f.close()

    def getNthSegmentName(self, n):
        return '{}.raw'.format(n)


    def decode(self, filename):
        #First break it up into words


        # Create a decoder with certain model
        decoder = self.getPhonemeDecoder()
        filelen = 0

        decoder.start_utt()
        with open(filename, 'rb') as stream:
            while True:
              buf = stream.read(1024)
              if buf:
                decoder.process_raw(buf, False, False)
                filelen += (len(buf))
              else:
                break
        decoder.end_utt()
        segments = [seg for seg in decoder.seg()]

        #In 100ths of a second
        filetime = filelen/(320.0/4.0) 
         
        #Read bindary from file
        fileobj = open(filename, mode='rb')
        binvalues = array.array('f')
        binvalues.read(fileobj, filelen/4)

        filelen = float(filelen)
        for seg in segments:
            startbyte = int(filelen*(seg.start_frame/filetime))
            endbyte = int(filelen*(seg.end_frame/filetime))
            self.profile.addPhoneme(seg.word, seg.ascore, binvalues[startbyte:endbyte])


    #RETURNS: A phoneme decoder with configurated settings
    #TODO: De-hardcode this stuff
    def getPhonemeDecoder(self):
        logpath = path.join(self.modeldir, 'log.txt')
        # if(path.exists(logpath)):
        #     remove(logpath)

        config = Decoder.default_config()
        config.set_string('-hmm', path.join(self.modeldir, 'en-us\\en-us'))
        config.set_string('-allphone', path.join(self.modeldir, 'en-us\\en-us-phone.lm.dmp'))
        config.set_string('-logfn', logpath)
         
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-10)
        config.set_float('-pbeam', 1e-10)

        # Decode streaming data.
        return Decoder(config)

    #RETURNS: A decoder trying to find words from a dictionary
    def getDictionaryDecoder(self):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(self.modeldir, 'en-us/en-us'))
        config.set_string('-lm', path.join(self.modeldir, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', path.join(self.modeldir, 'en-us/cmudict-en-us.dict'))
        return Decoder(config)


    #RETURNS: The created profile
    def getProfile(self):
        return self.profile
