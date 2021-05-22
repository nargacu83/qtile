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
    Key([mod], "e", lazy.spawn("nautilus"), desc="Spawn nautilus"),
    
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

group_names = [("1", {'layout': 'monadtall'}),
               ("2", {'layout': 'monadtall'}),
               ("3", {'layout': 'monadtall'}),
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
                    inactive = colors[2],
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
                # widget.Prompt(),
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
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(guess_terminal() + ' -e htop')},
                    format = "{MemUsed}M / {MemTotal}M",
                    measure_mem = 'M',
                    padding = 10
                ),
                # widget.CheckUpdates(
                #     update_interval = 1800,
                #     distro = "Arch_checkupdates",
                #     display_format = "{updates} MAJs",
                #     foreground = colors[2],
                #     # background = colors[4],
                #     padding = 10
                # ),
                widget.Systray(
                    padding=10
                ),
                widget.CurrentLayout(
                    padding=10
                ),
                widget.Clock(
                    format='%a %d %b %Y   %H:%M',
                    foreground = colors[2],
                    # background = colors[4],
                    padding=10
                ),
                # widget.Volume(
                #     foreground = colors[2],
                #     background = colors[5],
                #     mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(guess_terminal() + ' -e htop')},
                #     padding = 5
                # ),
                # widget.QuickExit(),
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

dgroups_key_binder = None

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download and error.
        *layout.Floating.default_float_rules,
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        
        # Rules for Unity (bugged for the moment)
        # Match(title='UnityEditor.PopupWindow'),
        # Match(title='UnityEditor.AddComponent.AddComponentWindow'),
    ],
    **layout_theme)

auto_fullscreen = True
focus_on_window_activation = "smart"


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
