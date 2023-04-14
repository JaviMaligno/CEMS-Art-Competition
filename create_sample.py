import sys
from CEMSArt import CEMS_Art

'''To create a sample with a given file name from a given data directory and with a given duration in seconds.
On a terminal, run: python create_sampl.py file_name data_directory duration
where file_name, data_directory and duration are your chosen parameters. If duration is not provided it is set to 20 seconds by default.
The user is warned that it takes several hours to produce a 20 second video 
so if you just want to have a look, it is adviced to choose less than 3 seconds'''

file_name = sys.argv[1]
data_directory = sys.argv[2]
duration = sys.argv[3] if len(sys.argv) > 3 else 20

if __name__ == "__main__":
    CEMS_Art(file_name, data_directory, duration=duration)
