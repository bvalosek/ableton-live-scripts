# MIDI Remote Scripts for Ableton Live 9

My personal MIDI Remote Scripts for Ableton 9 (tested on Ableton Live Suite
9.7.2)

> I frequently iterate on this repo as my gear / setup changes. See the [v2
> iteration circa early
> 2017](https://github.com/bvalosek/ableton-live-scripts/tree/v2.6.0) or the
> [v1 iteration circa
> 2015](https://github.com/bvalosek/ableton-live-scripts/tree/v1.0.0) for
> previous incarnations of my custom scripts

## Devices

* DJ TechTools Midi Fighter Twister

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

* Select `bvalosek Midi Fighter Twister` for the Control Surface
* Select `Midi Fighter Twister` for the input
* Select `Midi Fighter Twister` for the output

All of the Control Surface scripts in this repo will be prefixed with
`bvalosek`.

Selecting input/output `track`, `sync`, and `remote` are not required to get
the custom scripts working, although you'll likely want to select some of these
depending on how you're using your hardware.

## Controllers

Detailed information about each controller's customization

### DJ TechTools Midi Fighter Twister

> Make sure to update your Twister to the latest firmware via the [Midi Fighter
> Utility
> app](https://store.djtechtools.com/products/midi-fighter-twister#downloads_and_support)
> from DJ Tech Tools

## License

[MIT](https://github.com/bvalosek/ableton-live-scripts/blob/master/LICENSE)

