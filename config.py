# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),

    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    # Launch file manager
    Key([mod], "e", lazy.spawn("nemo"), desc="Spawn file manager"),
    
    # Launcher with Rofi
    Key([mod], "p", lazy.spawn("rofi -no-lazy-grab -show drun -modi drun -theme ~/.config/rofi/style_nargou"), desc="Spawn rofi in drun mode"),

    # Switch window with Rofi
    Key([alt], "Tab", lazy.spawn("rofi -no-lazy-grab -show window -modi window -theme ~/.config/rofi/style_nargou"), desc="Spawn Rofi in window mode"),

    # Screenshot with Rofi
    Key([mod], "Print", lazy.spawn(os.path.expanduser('~') + "/.config/rofi/screenshot"), desc="Spawn screenshot menu with Rofi"),

    # Power menu with Rofi
    Key([mod, "control"], "Escape", lazy.spawn("rofi -no-lazy-grab -show power-menu -modi power-menu:~/.config/rofi/rofi-power-menu/rofi-power-menu -theme ~/.config/rofi/style_nargou"), desc="Spawn Rofi in window mode"),
    
    # Disable floating window
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

]

group_names = [("1", {'layout': 'monadtall', 'matches': [Match(wm_class=["freetube"])]}),
               ("2", {'layout': 'monadtall', 'matches': [Match(wm_class=["vscodium", "jetbrains-rider", "unityhub", "Unity"])]}),
               ("3", {'layout': 'monadtall', 'matches': [Match(wm_class=["discord", "element"])]}),
               ("4", {'layout': 'monadtall'})]

group_keys = ["ampersand",
              "eacute",
              "quotedbl",
              "apostrophe"]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 0):
    # Switch to another group
    keys.append(Key([mod], group_keys[i], lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], group_keys[i], lazy.window.togroup(name)))


colors = [["#282c34", "#282c34"], # panel background
          ["#1D2330", "#1D2330"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name 

layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
]

widget_defaults = dict(
    font='Cantarell Bold',
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    disable_drag = True,
                    margin = 5,
                    padding = 5,
                    borderwidth = 3,
                    active = colors[2],
                    inactive = colors[0],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "block",
                    this_current_screen_border = colors[3],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[0],
                    other_screen_border = colors[0],
                    foreground = colors[2],
                    # background = colors[0]
                ),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Memory(
                    foreground = colors[2],
                    # background = colors[5],
                    mouse_callbacks = {'Button1': lambda qtile: qtile.spawncmd(terminal + ' -e htop')},
                    format = "{MemUsed: .0f}M / {MemTotal: .0f}M",
                    measure_mem = "M",
                    padding = 10
                ),
                widget.CheckUpdates(
                    update_interval = 1800,
                    distro = "Arch_checkupdates",
                    display_format = "{updates} MAJs",
                    foreground = colors[2],
                    mouse_callbacks = {'Button1': lambda qtile: qtile.spawncmd(terminal + ' -e paru -Syu')},
                    background = colors[4]
                ),
                widget.Systray(
                    padding=10
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6
                ),
                widget.Clock(
                    format='%a %d %b %Y   %H:%M',
                    foreground = colors[2],
                    padding=10
                ),
            ],
            35,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
# A function which generates group binding hotkeys. It takes a single argument, the DGroups object, and can use that to set up dynamic key bindings.
dgroups_key_binder = None

# A list of Rule objects which can send windows to various groups based on matching criteria.
dgroups_app_rules = []

# Controls whether or not to automatically reconfigure screens when there are changes in randr output configuration.
reconfigure_screens = True

# Controls whether or not focus follows the mouse around as it moves across windows in a layout.
follow_mouse_focus = False

# When clicked, should the window be brought to the front or not. If this is set to “floating_only”, only floating windows will get affected (This sets the X Stack Mode to Above.)
bring_front_click = False

# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window. When switching focus between screens, If there are no windows in the screen, the cursor will warp to the center of the screen.
cursor_warp = False

# If a window requests to be fullscreen, it is automatically fullscreened. Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = True

# If things like steam games want to auto-minimize themselves when losing focus, should we respect this or not?
auto_minimize = False

# Behavior of the _NET_ACTIVATE_WINDOW message sent by applications
# urgent: urgent flag is set for the window 
# focus: automatically focus the window 
# smart: automatically focus if the window is in the current group 
# never: never automatically focus any window that requests it
focus_on_window_activation = "smart"

default_float_rules = [
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(func=lambda c: c.has_fixed_size())
    # Match(func=lambda c: c.has_fixed_ratio())
]


floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download and error.
        *default_float_rules,
        Match(wm_class='pavucontrol'),
        Match(wm_class='kdenlive'),
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class='Tor Browser'),
        Match(wm_class='origin.exe'),
        
        # Rules for Unity (bugged for the moment)
        # Match(title='UnityEditor.PopupWindow'),
        # Match(title='UnityEditor.AddComponent.AddComponentWindow'),
    ],
    **layout_theme)

@hook.subscribe.startup_once
def startup_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/startup_once.sh'])

# @hook.subscribe.shutdown
# def shutdown():
#     home = os.path.expanduser('~')
#     subprocess.call([home + '/.config/qtile/shutdown.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
