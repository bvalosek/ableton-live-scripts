# MIDI Remote Scripts for Ableton Live 9

Performance-oriented custom controller scripts for the Akai MPK249, MIDI
Fighter Twister, and Novation Launchpad.

## Overview

These mappings were built specifically for how I use my gear, not for having
huge amounts of flexibility. I use the Twister only for interacting with
devices, the controls on the MPK249 only for managing track state, and my
Launchpad for recording and clip launching.

This keeps each controller associated with a specific role when jamming.

## Installation

Copy the entire repo contents into the MIDI Remote Scripts directory for
Ableton Live (see the [official
documentation](https://www.ableton.com/en/help/article/install-third-party-remote-script/)).

Alternatively, you could clone this repo right into the MIDI Remote Scripts
directory.

```bash
# in your MIDI Remote Scripts directory
$ git init
$ git remote add origin git@github.com:bvalosek/ableton-live-scripts.git
$ git fetch
$ git checkout -t origin/master
```

If you aren't familiar with git and just want a download, go to the [latest
releases](https://github.com/bvalosek/ableton-live-scripts/releases) and
download a ZIP file and copy all contents into the MIDI Remote Scripts
directory.

## Setup

Once the scripts are installed via the above instructions, open Live and go to
Preferences -> MIDI and set the Control Surface, Input, and Output sections as
follows:

![MIDI Control Surface settings](bvalosek_common/screenshots/midi-menu.png)

Setting Control Surface to None for MPK249 (Port A) prevents the default MPK
mapping from loading.

In order for the MPK249 script to work, a custom preset in location 25 must be
loaded. Press the DUMP button in the MPK249 row (see above picture). This will
**overwrite** the current contents of preset 25 with a new preset called
`bvalosek` that is to be used with this script.

## Controllers

### MPK249

* Controls used primarily for mixing and managing track state during performances
* Only BANK A of the controls are mapped, B and C are unmapped
* Transport controls (other than loop and record) are mapped as expected
* Track offset position follows Launchpad (if present)
* Record button functions as SHIFT button to alter role of encoders, faders,
  buttons, and transport section
* Keys on MIDI Channel 1, Pads on MIDI Channel 2 (with colors corresponding to
  GM drum instrument types). Only BANK A of the pads is used.
* Make sure to use the corresponding preset `25: bvalosek`, loaded via the DUMP
  button in Ableton Live (See Setup instructions above)

#### Mapping

The controls work as following:

|            | Normal       | Shift (REC button)     |
|------------|--------------|------------------------|
| Encoders A | Track pan    | Track send amount      |
| Faders A   | Track volume | Track volume           |
| Buttons A  | Track select | Track arm (and select) |

### MIDI Fighter Twister

* Used for managing devices, their parameters, state, and nested chains.
* Only BANK 1 is used, the other 3 banks are unmapped.
* Colors used to identify parameter and device chains by name. The first word
  determines the color, so things named similarly will be visibly related.
* Factory Default firmware mappings are fine (though I tend to adjust the
  sensitivity)

#### Mapping

...

## License

MIT

