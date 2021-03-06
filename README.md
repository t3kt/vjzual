vjzual
======

vjzual is a vj system built with TouchDesigner.

## Goals and/or Requirements
* Modularity
* Configurability
* Live performance controls
* Load/save settings and state
* Awesomeness
* ... other things

## Structure
The system is composed of *Modules*, which can input and/or output video (TOP) streams. Modules can be grouped into *Chains*, which are themselves modules.

The general structure is a flow from one or more sources through some series of filters, combined in a mixer and sent to the system's output.

### Types of Modules
* Source: something that outputs a video stream but does not take any video inputs. For example: video clip players, video generators, source selectors (grabbing the output from other modules)
* Filter: something that inputs one or more video streams and outputs a video stream. For example: delay effects, color adjustments, etc.
* Chain: a wrapper that contains other modules feeding into each other in series. For example: layers, master effects chains.
* Special: a module that exists to group parameters but does not directly have video input or output. For example: the global control group that applies to multiple modules such as global playback rate.

### Parts of a Module:
* zero or more video (TOP) inputs
* zero or one video (TOP) output - note: this may later be changed to support multiple outputs
* zero or more *parameters* which control its behavior (see below)
* a UI panel with a standardized header
* several standard switches including bypass, solo, preview, collapse/expand UI, show/hide viewers

### Parameters
Each module has zero or more parameters. A parameter is a named value that controls some aspect of a module's behavior. Parameter values can be loaded and saved (see the paramstate.txt file).

Most parameters are float values, ranging from 0 to 1, which are represented by a clone of the float_param.tox component. This component provides a UI with a slider, name label, and support for loading/saving values, resetting to defaults, mapping to MIDI controls, and LFO/audio modulation. These parameters each have an instance of the vjzual.VjzParam extension class.

Some parameters are considered virtual parameters, and do not have a corresponding float_param.tox component. They currently exist as specialized load/save handlers in modules, which allow various other types of values to be used which aren't supported by the standard component. They can be strings, booleans, or any other type that can be converted to/from strings.

## Development Process
I began my previous efforts to develop this sort of system by trying to first determine what the system's structure should be, then develop the module shells, and then fill them in. This tended to result in over-engineered incomplete systems that didn't do anything useful. So, rather than attempting to start with a completely pre-planned structure, I started vjzual as a large (disorganized) video processing network. Once that was working, I grouped parts of the network into logical units (such as a feedback loop, a delay effect, a disortion effect, or a source clip). Once that was done, I identified parts of the modules that were common to all of them, and started to standardize them and create shared subsystems and components to help with that process.


## Setup Instructions and Workarounds
There are currently some bugs which require workarounds when launching the system. To deal with them:

1. right-click /_/init and select "clear script errors"
2. right click /_/RUN_init and select "run script"
3. in the ui panel switch box (/_/ui_switches), toggle the switches for anything that shows up as enabled, and reenable anything that you want to show (see [issue #38](https://github.com/t3kt/issues/38))
