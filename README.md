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
The system is composed of *Modules*, which output (and optionally input) video (TOP) streams. Modules can be grouped into *Chains*, which are themselves modules.

### Parts of a Module:
* zero or more video (TOP) inputs
* zero or one video (TOP) output - note: this may later be changed to support multiple outputs
* zero or more *parameters* which control its behavior
* a UI panel with a standardized header
* several standard switches including bypass, solo, preview, collapse/expand UI, show/hide viewers

### Types of Modules
* Source: something that outputs a video stream but does not take any video inputs. For example: video clip players, video generators, source selectors (grabbing the output from other modules)
* Filter: something that inputs one or more video streams and outputs a video stream. For example: delay effects, color adjustments, etc.
* Chain: a wrapper that contains other modules feeding into each other in series. For example: layers, master effects chains.
* Special: a module that exists to group parameters but does not directly have video input or output. For example: the global control group that applies to multiple modules such as global playback rate.

### Parameters
Each module has zero or more parameters. A parameter is a named value that controls some aspect of a module's behavior. Each parameter shows in the module's UI. Currently, the only type of supported parameter is a float value, which is shown as a slider with a value range of 0.0 to 1.0 (see issues #16 and #52 for efforts to add other parameter types).
