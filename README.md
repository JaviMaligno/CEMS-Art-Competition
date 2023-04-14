# DATA ART COMPETITION

The Data Art Competition was a contest organised by the collaboration bewteen the CEMS division of the University of Kent and the Institute of Cultural and Creative Industries ([iCCi](https://www.kent.ac.uk/institute-cultural-creative-industries))  in 2023. The aim is to create digital generative art based on human bio data. The data was obtained from 80 participants watching a live performance (for approximately 1 hour) while wearing a commercial wristband. A sample of the data can be found in the Data folder.

The participants are required to write a piece of software, taking the [PPG](https://en.wikipedia.org/wiki/Photoplethysmogram) as input and output an animation of 2D/3D visualisation.  This will require an algorithm to process the PPG data for each individual participant to output the visualisations specific to the person. A soundscape generated from the data can be included as part of the animation.

The file `CEMSArt.py` contains most of the code, including everything related to create the animation. The file `sound_scape.py` contains the methods to create the soundscape from the audio folder and add the sound to the video. The file `create_sample.py` can be used to create a full piece of a specific duration provided a file name and a data directory.

A sample video showing a few animations has been added to the repository. The user is warned that producing a 20 second video may take anywhere between 3 to 6 hours.

## My work

I have used [Julia sets](https://en.wikipedia.org/wiki/Julia_set) as a basis for my work. The construction depends on a complex parameter $c\in\mathbb{C}$ that I have defined from the PPG. For each value of the PPG, a different value of $c$ is produced, and thus a different Julia set. These different sets are put together to create an animation. Each PPG also determines a choice of color map, so that the Julia set has a different color palette. This animation is saved to an .mp4 video.

The video is supported by breathing and heartbeat sounds. This has been produced using the `scaper` module, that allows to create randomized sound scapes from a few audio files. The audio is pitched according to the PPG.

A video showing a few examples can be found in the samples folder.
