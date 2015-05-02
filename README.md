vjzual
======

vjzual is a vj system built with TouchDesigner.

## Structure
The system is composed of *Modules*, which output (and optionally input) video (TOP) streams. Modules can be grouped into *Chains*, which are themselves modules.

### Parts of a Module:
* 0-\* video (TOP) inputs
* 1 video (TOP) output - note: this may later be changed to support multiple outputs
* 0-\* *parameters* which control its behavior
* a UI panel with a standardized header
* several standard switches including bypass, solo, preview, collapse/expand UI, show/hide viewers

## Goals and/or Requirements
* be awesome
* ... other things
