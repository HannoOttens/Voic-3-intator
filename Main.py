import PhonemeDecoder as pd
import audioop
import array

pdecoder = pd.PhonemeDecoder()
pdecoder.addToPhonemeProfile('goforward.raw')
profile = pdecoder.getProfile()

print("RECORDED:", profile.recordedPhonemes())

newaudioclip = array.array('f')

slience = array.array('f')
for i in range(640):
    slience.append(0.0)
# lilsilence = "" 
# for i in range(1000):
#     lilsilence += "  "


g = profile.getPhonemeClip

# newaudioclip += slience
# newaudioclip += g("R")
# newaudioclip += g("OW")
newaudioclip.extend(slience)
newaudioclip.extend(g("G"))
newaudioclip.extend(g("R"))
newaudioclip.extend(g("AO"))
newaudioclip.extend(g("OW"))
newaudioclip.extend(g("N"))
newaudioclip.extend(g("NG"))
newaudioclip.extend(slience)
newaudioclip.extend(g("G"))
newaudioclip.extend(g("OW"))
newaudioclip.extend(g("T"))
newaudioclip.extend(slience)
newaudioclip.extend(g("T"))
newaudioclip.extend(g("AE"))
newaudioclip.extend(g("N"))
newaudioclip.extend(g("NG"))
newaudioclip.extend(g("T"))
newaudioclip.extend(slience)
newaudioclip.extend(g("F"))
newaudioclip.extend(g("R"))
newaudioclip.extend(g("AO"))
newaudioclip.extend(g("G"))


f = open('result.raw',  'wb')
newaudioclip.tofile(f)
f.close()




# for key,phoneme in pdecoder.profile.phonemes.items():
#     print(key + " \t " + (str(phoneme.accuracy) + "\t" + phoneme.clip.replace('\n', '').replace('\r', '')  if phoneme is not None else "!MISSING!"))
#     print('================')
# import matplotlib.pyplot as plt
# from scipy.fftpack import fft
# from scipy.io import wavfile # get the api
# import numpy as np
# import matplotlib.animation as anim

# # read
# fs, data = wavfile.read('Windows XP Startup.wav')
# # select the channel
# a = data.T[0]
# b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)

# # calculate fourier transform (complex numbers list)
# increase = 5000

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)

# def update(i):
#     index = i*increase
#     ax.clear()
#     print(index)
#     c = fft(b[index:index+increase]) 
#     # ax.set_ylim([0,20000])
#     ax.plot(abs(c[0:len(c)/2]), 'r')
#     #plt.pause(0.1)

# am = anim.FuncAnimation(fig, update, frames=a.size/increase, repeat=False)

# plt.show()

