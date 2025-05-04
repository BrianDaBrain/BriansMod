
#--------------------> System Imports <---------------------------|
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import extension
from libqtile.utils import guess_terminal
from qtile_extras.layout.plasma import Plasma


import os
from subprocess import Popen
#--------------------> Local Imports <----------------------------| 
from briansmod import style
import sys  

#--------------------> Helpers <----------------------------------|
mod = "mod4"
terminal = guess_terminal()

theme = style.LoadTheme("mytheme.theme")

@hook.subscribe.startup_once
def runner():
    Popen(os.path.expanduser("~/.config/qtile/startup.sh"))


def grp(n):
    return Group(str(n))

def grpm(n, m):
    return Group(str(n), matches = Match(wm_class=m))

def initGroups():
    g = [
            grpm(1, "Alacritty"),
            grpm(2, "Brave"),
            grpm(3, "Discord"),
            ]
    for i in range(4, 10):
        g.append(grp(i))
    return g


#--------------------> Key Binds <--------------------------------|
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-icons"),
        desc="Spawn a command using Rofi Drun"),


 
    Key([mod], "s", lazy.spawn("rofi -show window -show-icons"), desc="quickswitch"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = initGroups() #originally:[Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(**theme.window_defaults),
    layout.Max(**theme.window_defaults),
    # Try more layouts by unleashing below layouts.
    layout.Stack(**theme.window_defaults),
    layout.Bsp(**theme.window_defaults),
    # layout.Matrix(),
    layout.MonadTall(**theme.window_defaults),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(**theme.window_defaults),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    Plasma(**theme.window_defaults),
]
widget_defaults = theme.widget_defaults
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=theme.white,
                    inactive=theme.black,
                    highlight_color=theme.gold,
                    highlight_method=theme.group_highlight_method,
                    disable_drag=True,
                    margin=theme.groupbox_margin,
                    ),
                widget.CurrentLayout(
                    fmt="[{}]"
                    ),
                #widget.Prompt(),
                widget.Spacer(
                    length=150
                    ),
                widget.WindowName(
                    fmt="<u><b>{}</b></u>",
                    foreground=theme.gold,
                    ),
                widget.Chord(
                    chords_colors={
                        "launch": (theme.gold, theme.white),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                #WifiIcon(),
                widget.PulseVolume(
                    fmt=" Vol:{} "
                    ),
                widget.BatteryIcon(),
                widget.Clock(format=theme.clockformat, foreground=theme.gold),
                widget.QuickExit(default_text="[X]",
                                 countdown_format="[{}]"),
            ],
            24,
            background=theme.barcolor,
            opacity=0.6,
            margin=theme.bar_margin,
            border_width=theme.bar_border_width,  # Draw top and bottom borders
            border_color=theme.bar_border_colors,  # Borders are magenta
        ),
        # x11_drag_polling_rate = 60,
        wallpaper=theme.wallpaper,
        wallpaper_mode=theme.wallpaper_mode,
    ),
    Screen(),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), 
         start=lazy.window.get_size()),
    Click([mod], "Button2", 
          lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="onboard"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"




