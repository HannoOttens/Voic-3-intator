import PhonemeDecoder as pd
import array
pdecoder = pd.PhonemeDecoder()

for i in range(1,10):
    print('DEMO-0' + str(i) + '.raw')
    pdecoder.addToPhonemeProfile('DEMO-0' + str(i) + '.raw')
pdecoder.addToPhonemeProfile('DEMO-10.raw')
pdecoder.addToPhonemeProfile('DEMO-11.raw')
pdecoder.addToPhonemeProfile('DEMO-12.raw')
profile = pdecoder.getProfile()

print("RECORDED:", profile.recordedPhonemes())

newaudioclip = profile.createSequence(
    ["HH","EH","L","OW","SIL", "W","ER","L","T"]
)

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

