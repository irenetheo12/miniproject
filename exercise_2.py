import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# Create a Pulse Width Modulation (PWM) object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

# Define the frequency of each note
# song: Twinkle, Twinkle Little Star. Notes: C4(261.63 Hz), G4(392.00 Hz), A4(440.00 Hz), F4(349.23 Hz)
notes = {
    'C4': 261,  # C4 note
    'G4': 392,  # G4 note
    'A4': 440,  # A4 note
    'F4': 349,  # F4 note
    'E4': 330,  # E4 note
    'D4': 294   # D4 note
}

#define the duration of each note
note_duration = 0.5  

# Fn to play the tone at a specific freq & dur
def playtone(frequency, duration):
    speaker.duty_u16(1000)  # Set duty cycle to 50% for a clear tone
    speaker.freq(frequency)  # Set the freq
    utime.sleep(duration)  # Play for the specified duration
    speaker.duty_u16(0)  # Stop the sound by setting duty cycle to 0

# Define the song as a sequence of notes
song = [
    ('C4', note_duration), ('C4', note_duration), ('G4', note_duration), ('G4', note_duration),
    ('A4', note_duration), ('A4', note_duration), ('G4', 1.0),  # "Twinkle, twinkle, little star"
    ('F4', note_duration), ('F4', note_duration), ('E4', note_duration), ('E4', note_duration),
    ('D4', note_duration), ('D4', note_duration), ('C4', 1.0)  # "How I wonder what you are"
]

# Play the song
for note, duration in song:
    playtone(notes[note], duration)
    utime.sleep(0.1)  # create a short pause between the notes

# Turn off the PWM
speaker.deinit()
