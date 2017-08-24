
import alsaaudio
import struct
import math

device='default'

pcm_rate = 44100
sin_freq = 2000

period_size = 160


def generate_sine(phase, freq, sample_rate, length):
    points = ''
    for i in range(0, length):
        res = math.sin(2*math.pi*freq*float(i)/sample_rate+phase) * 32767
        points += struct.pack('<h', round(res))
    return (points, (2*math.pi*freq*length/sample_rate+phase)%(2*math.pi))

if __name__ == '__main__':

    out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device=device)

    # Set attributes: Mono, 16 bit little endian frames
    out.setchannels(1)
    out.setrate(pcm_rate)
    out.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    out.setperiodsize(period_size)


    phase = 0
    (data, phase) = generate_sine(phase, sin_freq, pcm_rate, period_size)
    while True:
        out.write(data)
        (data, phase) = generate_sine(phase, sin_freq, pcm_rate, period_size)