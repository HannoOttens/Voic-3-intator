import PhonemeDecoder as pdec
import PhomeneDictionary as pdict
import array

MODELDIR = "C:\Users\hanno\Google Drive\Vakken\Y3S1\Onderzoeksmethoden\Voice decoder\Voic-3-intator\models"
DATADIR = "Recordings"

#Make dictionary and phoneme decoder
dictionary = pdict.PhonemeDictionary(MODELDIR + "\\en-us\\cmudict-en-us.dict")
pdecoder = pdec.PhonemeDecoder(MODELDIR, DATADIR)

#Read in supplied files
for i in range(1,13):
    print('DEMO-0' + str(i) + '.raw')
    pdecoder.addToPhonemeProfile('DEMO-' + str(i).zfill(2) + '.raw')

#Create sequence out of recorded phonemes
profile = pdecoder.getProfile()
print("RECORDED:", profile.recordedPhonemes())
newaudioclip = profile.createSequence(
    dictionary.getPhonemesForSentence("Hello world")
)

#Save the result
f = open('result.raw',  'wb')
newaudioclip.tofile(f)
f.close()