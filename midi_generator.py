     """
Example:
	python3 midi_generator.py -pd 16 -min 1 -max 4  -i


TODO:
- Melodies (minus 4th and 7th as an options)
- Only triads or 7th or ...
- Ignore dimished chords
- https://www.musical-u.com/learn/exploring-common-chord-progressions/


"""

import random
import argparse

from midiutil import MIDIFile

# Constants

BASE_MIDI_NUMBER = 60


NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Scales / Keys
SCALES = {
	'Major': {
		'Notes': [0, 2, 4, 5, 7, 9, 11],
		'TriadColor': {
			'I': 'Major', 
			'ii': 'Minor', 
			'iii': 'Minor', 
			'IV': 'Major', 
			'V': 'Major', 
			'vi': 'Minor', 
			'VII': 'Diminished'
		}
	},
	'Minor': {
		'Notes': [0, 2, 3, 5, 7, 8, 10],
		'TriadColor': {
			'i': 'Minor', 
			'ii': 'Diminished', 
			'III': 'Major', 
			'iv': 'Minor', 
			'v': 'Minor', 
			'VI': 'Major', 
			'VII': 'Major'
		}
	}
}

CHORDS = {
	# Triads
	'I': [0, 2, 4],
	'II': [1, 3, 5],
	'III': [2, 4, 6],
	'IV': [3, 5, 0],
	'V': [4, 6, 1],
	'VI': [5, 0, 2],
	'VII': [6, 1, 3],
	# 7th
	'I-7': [0, 2, 4, 6],
	'II-7': [1, 3, 5, 0],
	'III-7': [2, 4, 6, 1],
	'IV-7': [3, 5, 0, 2],
	'V-7': [4, 6, 1, 3],
	'VI-7': [5, 0, 2, 4],
	'VII-7': [6, 1, 3, 5],
}

def roman_to_integer(roman):
	return {'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6}[roman]

def generate_chord(base_note='I', notes_amount=3):
	return [(roman_to_integer(base_note) + note*2) % 7 for note in range(0, notes_amount)]

def cl_args_parser():
	"""
	Parse command line arguments
	"""
	parser = argparse.ArgumentParser(description='MIDI generator')

	parser.add_argument('-bn', '--base-note', action="store", dest="base_note", type=str, default=random.choice(NOTES))
	parser.add_argument('-s', '--scale', action="store", dest="scale", type=str, default=random.choice(list(SCALES.keys())))
	parser.add_argument('-pn', '--progression-name', action="store", dest="progression_name", type=str, default='')

	parser.add_argument('-pl', '--progression-length', action="store", dest="progression_length", type=int, default=0)
	parser.add_argument('-cd', '--chord-duration', action="store", dest="chord_duration", type=int, default=0)

	parser.add_argument('-pd', '--progression-duration', action="store", dest="progression_duration", type=int, default=0)
	parser.add_argument('-min', '--min-chord-duration', action="store", dest="min_chord_duration", type=int, default=0)
	parser.add_argument('-max', '--max-chord-duration', action="store", dest="max_chord_duration", type=int, default=0)

	parser.add_argument('-i', '--auto-inversions', action="store_true", dest="auto_inversions_enabled")


	return parser.parse_args()

# Common chord progressions
PROGRESSIONS = {
	'II-V-I': ['II', 'V', 'I'],
	'I-V-VI-IV': ['I', 'V', 'VI', 'IV'],
	'I-IV-V-I': ['I', 'IV', 'V', 'I'],
	'wow': ['VI', 'VII-7']
}

if __name__ == '__main__':
	# Get command line arguments
	args = cl_args_parser()

	# Set params from command line erguments
	base_note = args.base_note
	scale = args.scale
	progression_name = args.progression_name

	progression_length = args.progression_length
	chord_duration = args.chord_duration

	progression_duration = args.progression_duration
	min_chord_duration = args.min_chord_duration
	max_chord_duration = args.max_chord_duration

	auto_inversions_enabled = args.auto_inversions_enabled
	
	
	track    = 0
	channel  = 0
	time     = 0    # In beats
	tempo    = 60   # In BPM
	volume   = 100  # 0-127, as per the MIDI standard

	MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
	MyMIDI.addTempo(track, time, tempo)
	

	# Determine rythm of chord progression
	if len(progression_name) > 0:
		durations = [chord_duration for i in PROGRESSIONS[progression_name]]
	elif progression_length > 0 and chord_duration > 0:
		durations = [chord_duration for i in range(0, progression_length)]
	elif progression_duration > 0 and min_chord_duration > 0 and max_chord_duration > 0:
		durations = []
		progression_duration_left = progression_duration
		while progression_duration_left > 0:
			chord_duration = random.randint(min_chord_duration, max_chord_duration)
			if chord_duration > progression_duration_left:
				chord_duration = progression_duration_left
			durations.append(chord_duration)
			progression_duration_left -= chord_duration

	# Determine chords in chord progression
	if len(progression_name) > 0:
		progression = PROGRESSIONS[progression_name]
	elif progression_length > 0 and chord_duration > 0:
		progression = random.choices(list(CHORDS.keys()), k=progression_length)
	elif progression_duration > 0 and min_chord_duration > 0 and max_chord_duration > 0:
		progression = random.choices(list(CHORDS.keys()), k=len(durations))

	# Create chord progression
	print(base_note, scale, progression)
	chord_progression = []
	for chord, duration in zip(progression, durations):
		current_chord = []
		for note_in_chord in CHORDS[chord]:
			current_chord.append(SCALES[scale]['Notes'][note_in_chord] + NOTES.index(base_note) + BASE_MIDI_NUMBER)

		# Bring notes to order
		for i, _ in enumerate(current_chord[1:]):
			note = current_chord[i+1]
			while note < current_chord[i]:
				note += 12
				current_chord[i+1] = note

		# Use inversion to decrease spread of notes
		if auto_inversions_enabled:
			for i, note in enumerate(current_chord):
				while note > BASE_MIDI_NUMBER + NOTES.index(base_note) + 12:
					note -= 12
					current_chord[i] = note

		chord_progression.append({
				'chord': current_chord,
				'duration': duration
			})

	# Add notes to MIDI file
	current_time = time
	for i, chord in enumerate(chord_progression):	
		for pitch in chord['chord']:
			MyMIDI.addNote(track, channel, pitch, current_time, chord['duration'], volume)
		current_time += chord['duration']

	# Write MIDI file
	with open("{}_{}.mid".format(base_note, scale), "wb") as output_file:
	    MyMIDI.writeFile(output_file)