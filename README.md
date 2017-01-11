# MIDI Remote Scripts for Ableton Live 9

My personal MIDI Remote Scripts for Ableton 9.

> Tested on Ableton Live Suite 9.7.1

## Devices

* Akai MPK249 Keyboard
* Alesis VI 49 Keyboard
* DJ TechTools MIDI Fighter Twister

## Installation

* Download a release from [latest releases](https://github.com/bvalosek/ableton-live-scripts/releases)
  (most recent version [here](https://github.com/bvalosek/ableton-live-scripts/releases/latest))
* Copy **ALL** directories prefixed with `bvalosek_` into the MIDI Remote Scripts
  directory for Ableton Live (see the [official documentation](https://www.ableton.com/en/help/article/install-third-party-remote-script/))
* You may need to restart Ableton or at least reload your current Set to see
  the newly added scripts

> You should copy ALL directories even if you only have a specific controller,
> as code is shared between the scripts.

Alternatively, if you are familiar with git and want to run the absolute latest
(potentially unreleased) code, you could clone this repo right into the MIDI
Remote Scripts directory:

```bash
# in your MIDI Remote Scripts directory
$ git init
$ git remote add origin git@github.com:bvalosek/ableton-live-scripts.git
$ git fetch
$ git checkout -t origin/master
```

## Setup

Once the scripts are installed via the above instructions, open Live and go to
Preferences -> Link / MIDI and set the Control Surface, Input, and Output
sections for the corresponding controllers you are using.

For example, for the DJTT MIDI Fighter Twister:

* Select `bvalosek MF Twister` for the Control Surface
* Select `Midi Fighter Twister` for the input
* Select `Midi Fighter Twister` for the output

All of the Control Surface scripts in this repo will be prefixed with
`bvalosek`.

Selecting input/output `track`, `sync`, and `remote` are not required to get
the custom scripts working, although you'll likely want to select some of these
depending on how you're using your hardware.

## Controllers

Detailed information about each controller's customization

### Akai MPK249

* Faders 1-8 control track volume for tracks 1-8
* Buttons 1-8 select and arm tracks 1-8
* Transport functions as expected, but:
  * Record acts as a hybrid session record / new (like Launchpad, Push, etc)

### Alesis VI 49 Keyboard

* Knobs 1-8 control the currently selected device
* Knobs 9-12 control the first four sends of the selected track
* Transport functions as expected, but:
  * Record acts as a hybrid session record / new (like Launchpad, Push, etc)

Consider adjusting the *Takeover Mode* in the Ableton Live Preference window to
adjust how values are transitioned when the hardware knob is in a different
position than the currently selected device

#### MIDI Mapping

This should just be the factory settings:

> All on MIDI Channel 1

* Knobs 1-12: CC 20-31
* Switches 1-12: Toggle, CC 48-59
* Switches 13-24: Toggle, CC 64-75
* Switches 24-36: Toggle, CC 80-91
* Transport: Momentary
  * Record: CC 114
  * Loop: CC 115
  * Rewind: CC 116
  * Fast Forward: CC 117
  * Stop: CC 118
  * Play: CC 119

### DJ TechTools MIDI Fighter Twister

> Still in development

## License

MIT

