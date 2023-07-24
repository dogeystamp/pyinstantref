# pyinstantref

This is a Python rewrite of Gilles Castel's [Instant Reference](https://github.com/gillescastel/instant-reference) tool.
(I was not a fan of needing NPM rather than the system package manager to install some dependencies.)

pyinstantref allows you to copy a link to a specific page or header in a PDF with a single keybind in Zathura.
You can then paste this reference in your notes and other documents.

For now, it only works with my own [templates](https://github.com/dogeystamp/typst-templates) for [Typst](https://github.com/typst/typst),
but it should be easy to get the script to format in LaTeX instead
using Castel's original code as reference, or even in plain-text.

## installation

These instructions are for Arch Linux based distributions.
Package names will probably differ for other distros, especially with Python packages.

First, install the necessary packages:
    
    sudo pacman -S xsel xdotool xorg-xprop python-pydbus rofi

(Rofi is needed for section references.)

Then, clone this repo:

    git clone https://github.com/dogeystamp/pyinstantref
    cd pyinstantref

Install the .desktop file:

    mkdir -p ~/.local/share/applications
    cp pdfref.desktop ~/.local/share/applications/
    xdg-mime default pdfref.desktop x-scheme-handler/pdfref
    sudo update-desktop-database

Ensure this directory is in $PATH by adding this line to the bottom of `~/.profile` (change the location to point to this directory):

    export PATH="$HOME/pyinstantref:$PATH"

You might need to sign out then sign in to apply this change.

### shortcut

You can either set up a shortcut in your window manager/desktop environment,
or add the following to your `.config/zathura/zathurarc`:
    
```
map <C-l> exec copy_ref
```

This will make Ctrl-L copy a reference to the current page in Zathura.

## limitations

Currently, the following features are missing compared to Castel's version:
- ArXiv support
- LaTeX output
- Support for other PDF readers (e.g. Evince)

Feel free to send pull requests,
although this project is primarily for my own usage
and I can not make any guarantees.

Also:
- Section references are unreliable because titles might change,
  and there might be sections with the same title.
  Proper IDs for bookmarks are possible,
  but not until Typst resolves [issue #1352](https://github.com/typst/typst/issues/1352).
