from os import environ, path
import wave
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "C:\Users\hanno\Google Drive\Vakken\Y3S1\Onderzoeksmethoden\Voice decoder\Voic-3-intator\models"
DATADIR = "/"

class PhonemeDecoder:
    def getPhonemeProfile(self, filename):
        segments = self.decode(filename)
        #TODO: Make phoneme profile out of segments

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

        segments = [seg for seg in decoder.seg()]
        segmentStrings = [seg.word + " ("+str(seg.start_frame)+","+str(seg.end_frame)+")\n" for seg in segments]

        segmentString = ""
        for ss in segmentStrings:
          segmentString += ss

        print(segmentString)

        return segments

    def getDecoder(self):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(MODELDIR, 'en-us\\en-us'))
        config.set_string('-allphone', path.join(MODELDIR, 'en-us\\en-us-phone.lm.dmp'))
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-10)
        config.set_float('-pbeam', 1e-10)

        # Decode streaming data.
        return Decoder(config)
