# Phone information and tools

When the user prompts for help about his system, see if leveraging termux commands will simplify your job. Do not try the standard linux commands, custom python script, and utilities unless it cannot be achieved with one of the termux commands.

| Command                                       | Explanation                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| `termux-battery-status`                       | Use this to get battery information level, temperature, and health.      |
| `termux-camera-info`                          | Check if the user has camera(s) on the device.                           |
| `termux-camera-photo -c 0 image.jpg`          | Takes a photo using camera 0 and saves it as image.jpg                   |
| `termux-torch on`                             | Turns the phone torch on.                                                |
| `termux-torch off`                            | Turns the torch off if already turned on.                                |
| `termux-sensor`                               | Dumps a list of all available sensors and their names.                   |
| `termux-sensor -s "accelerometer"`            | Starts streaming live data from a specific sensor - eg: accelerometer.   |
| `termux-sensor -n 1 -d 1000`                  | Gets a single reading from all sensors arter delaying for 1 second       |
| `termux-sensor -c`                            | Cleans up (stops) all running sensor listeners.                          |
| `termux-tts-engines`                          | Lists the available Text-To-Speech (TTS) engines on the device.          |
| `termux-tts-speak "Hello from Krubot"`        | Uses the default TTS engine to speak text aloud.                         |
| `termux-tts-speak -p <pitch>`                 | Speaks text with a specified vocal pitch (e.g., `1.5` for higher).       |
| `termux-tts-speak -r <rate>`                  | Speaks text at a specified speech rate (e.g., `0.5` for slower).         |
| `termux-microphone-record`                    | Starts recording audio from the microphone.                              |
| `termux-microphone-record -f rec.wav -l 5`    | Records for 5 seconds and saves to a file.                               |
| `termux-microphone-record -q`                 | Quits the current recording.                                             |
| `termux-media-player play <file>`             | Plays a media file (audio or video).                                     |
| `termux-media-player pause`                   | Pauses the currently playing media.                                      |
| `termux-media-player stop`                    | Stops the currently playing media.                                       |
| `termux-media-player info`                    | Displays information about the currently playing media.                  |
| `termux-infrared-frequencies`                 | Gets the available infrared carrier frequencies (on supported devices).  |
| `termux-infrared-transmit -f <freq> <pattern>`| Transmits an infrared pattern.                                           |

