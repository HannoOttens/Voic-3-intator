import PhonemeDecoder as pdec
import PhomeneDictionary as pdict
import array

MODELDIR = "C:\Users\hanno\Google Drive\Vakken\Y3S1\Onderzoeksmethoden\Voice decoder\Voic-3-intator\models"
DATADIR = "Recordings"
SEGDIR = "Segments"

#Make dictionary and phoneme decoder
dictionary = pdict.PhonemeDictionary(MODELDIR + "\\en-us\\cmudict-en-us.dict")
pdecoder = pdec.PhonemeDecoder(MODELDIR, DATADIR,SEGDIR)

#Read in supplied files
#MULTIPLE FILES
# for i in range(1,7):
#     print('DEMO-0' + str(i) + '.raw')
#     pdecoder.addToPhonemeProfile('RIS3-' + str(i).zfill(2) + '.raw')
#SINGLE FILE
pdecoder.addToPhonemeProfile('Sentence2.raw')

#Create sequence out of recorded phonemes
profile = pdecoder.getProfile()
print("RECORDED:", profile.recordedPhonemes())
phones = dictionary.getPhonemesForSentence("research is awesome(2)")
print phones
newaudioclip = profile.createSequence(phones)

#Save the result
f = open('result.raw',  'wb')
newaudioclip.tofile(f)
f.close()