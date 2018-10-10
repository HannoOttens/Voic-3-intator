import PhonemeDecoder as pd

pdecoder = pd.PhonemeDecoder()
pdecoder.getPhonemeProfile('pangram-3.raw')



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

