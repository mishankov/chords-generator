# Chords generator
Command line utility that generates MIDI file with chord progression

## Parameters

Short name | Long name | Type |Description
------------ | ------------- | ------------- | ------------- |
-bn | --base-note | string | Base or root note of the scale from `NOTES` constant
-s | --scale | string | Scale name from `SCALES` constant
-pn | --progression-name | string | Name of chord progression from `PROGRESSIONS` constant
-pl | --progression-length | integer | Number of chords in chord progression
-cd | --chord-duration | int | Chords duration in beats
-pd | --progression-duration | int | Chord progression duration in beats
-min | --min-chord-duration | int | Minimum chords duration on beats
-max | --max-chord-duration | int | Maximum chords duration on beats
-i | --auto-inversions | flag | Use inverted chords to make notes  closer to base note of the scale


### Example 
```bash
python3 midi_generator.py -pd 16 -min 1 -max 4  -i
```

Script above generates 16 beats long chord progression with random base note, random scale, random chords duration between 1 and 4 beats, with inverted chords

