# Webcam to ASCII Converter

A Python project that converts a live webcam feed into ASCII art in real time using OpenCV and Pillow.

I originally started this as a small experiment to see if I could turn a webcam feed into ASCII characters. It quickly turned into a project where I could explore image processing, rendering techniques, visual effects, performance profiling, and other computer vision concepts.

The goal isn't just to build an ASCII webcam. Now it's gonna be a fully fledged project and also a way for me to learn how visual effects are created, experiment with different ideas, and document the things I discover along the way.

## Features

- Real-time webcam to ASCII conversion
- Multiple ASCII character sets
- Matrix-style digital rain effect
- Toggleable rain mode
- auto switch rain ON if changed to Matrix mode
- Adjustable rain stream count(10 - 100)
- Green Matrix mode and standard white mode
- Real-time blur controls
- Automatic histogram equalization(good for low lighting conditions)
- FPS counter and on-screen debug information
- Fullscreen display mode
- Runtime keyboard controls
- Cycle through multiple ASCII character sets

## Controls

| Key | Action |
|------|----------|
| `M` | Toggle Matrix mode |
| `N` | Toggle rain effect |
| `[` | Decrease rain streams |
| `]` | Increase rain streams |
| `P` | Increase blur |
| `O` | Decrease blur |
| `R` | Reset blur |
| `Space` | Cycle through ASCII character sets |
| `Q` | Quit |

## Built With

- Python
- OpenCV
- Pillow
- NumPy

## Things I Learned While Building This

- Converting images into ASCII characters
- Rendering text-based graphics with Pillow
- Basic image processing with OpenCV
- Working with coordinate systems and animation
- Managing state in real-time applications
- Building visual effects from scratch
- Measuring performance using `time.perf_counter()`
- Identifying bottlenecks through profiling instead of guessing

## Performance Notes

The interesting discoverie was that generating the ASCII characters wasn't the main performance bottleneck. Profiling showed that rendering thousands of characters with Pillow every frame was significantly more expensive than the ASCII conversion itself.

The project also includes experiments with different resolutions, character sets, blur levels, and rendering effects to better understand the performance trade-offs involved in real-time ASCII rendering.

## Future Ideas

- Enhancing the Performence(Top priority)
- make code modular
- Additional rendering styles
- User-defined ASCII character presets
- Color customization
- Support for images and video files
- Saving screenshots
- Performance optimizations
- Web version using NiceGUI