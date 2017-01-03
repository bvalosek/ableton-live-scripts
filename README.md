# MIDI Remote Scripts for Ableton Live 9

My personal MIDI Remote Scripts for Ableton 9.7.

## Devices

* DJ TechTools MIDI Fighter Twister

## Installation

* Download a release from [latest releases](https://github.com/bvalosek/ableton-live-scripts/releases)
  and extract the ZIP file
* Copy the desired controller script directories (all prefixed with `bvalosek_`) into the
  MIDI Remote Scripts directory for Ableton Live (see the [official documentation](https://www.ableton.com/en/help/article/install-third-party-remote-script/))

Alternatively, if you are familiar with git, you could clone this repo right
into the MIDI Remote Scripts directory:

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

### DJ TechTools MIDI Fighter Twister

> TBW

## License

MIT

