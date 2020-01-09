import re

from powerline.theme import requires_segment_info
from powerline.bindings.wm import get_i3_connection

def workspace_groups(w):
    group = []
    if w.focused:
        group.append('workspace:focused')
    if w.urgent:
        group.append('workspace:urgent')
    if w.visible:
        group.append('workspace:visible')
    group.append('workspace')
    return group

WS_ICONS = {
        "Terminal":   "",
        "Chromium":         "",
        "Google-chrome":    "",
        "Steam":            "",
        "jetbrains":        "",
        "Gimp":             "",
        "Pavucontrol":      "",
        "Lmms":             "",
        "Thunderbird":      "",
        "vifm":           "",
        "Skype":            "",
        "TelegramDesktop":  "",
        "feh":              "",
        "firefox":          "",
        "Evince":           "",
        "Okular":           "",
        "libreoffice-calc": "",
        "libreoffice-writer": "",
        "multiple":         ""
        }

def get_icon(w, separator, icons, show_multiple_icons, ws_containers):
    if w.num == -5:
        return ""
    icons_tmp = WS_ICONS
    icons_tmp.update(icons)
    icons = icons_tmp

    wins = [win for win in ws_containers[w.name].leaves() \
            if win.parent.scratchpad_state == 'none']
    if len(wins) == 0:
        return ""

    result = ""
    cnt = 0
    for key in icons:
        if not icons[key] or len(icons[key]) < 1:
            continue
        if any(key in win.window_class for win in wins if win.window_class):
            result += separator + icons[key]
            cnt += 1
    if not show_multiple_icons and cnt > 1:
        if 'multiple' in icons:
            return separator + icons['multiple']
        else:
            return ""

    return result

import copy
def get_next_ws(ws, outputs):
    names = [w.name for w in ws]
    for i in range(1, 100):
        if not str(i) in names:
            res_ls = []
            res = copy.deepcopy(ws[0])
            res.num = -5
            res.name = str(i)
            res.urgent = False
            res.focused = False
            res.visible = False
            for o in outputs:
                r2 = copy.deepcopy(res)
                r2.output = o
                res_ls += [r2]
            return res_ls
    return []

def is_empty_workspace(w, ws_containers):
    if w.num == -5:
        return False

    if w.focused or w.visible:
        return False

    wins = [win for win in ws_containers[w.name].leaves()]

    return False if len(wins) > 0 else True

@requires_segment_info
def workspaces(pl, segment_info, only_show=None, output=None, strip=0, separator=" ",
        icons=WS_ICONS, show_icons=True, show_multiple_icons=True, show_dummy_workspace=False,
        show_output=False, priority_workspaces=[], hide_empty_workspaces=False):
    '''Return list of used workspaces

        :param list only_show:
                Specifies which workspaces to show. Valid entries are ``"visible"``,
                ``"urgent"`` and ``"focused"``. If omitted or ``null`` all workspaces
                are shown.
        :param string output:
                May be set to the name of an X output. If specified, only workspaces
                on that output are shown. Overrides automatic output detection by
                the lemonbar renderer and bindings.
                Use "__all__" to show workspaces on all outputs.
        :param int strip:
                Specifies how many characters from the front of each workspace name
                should be stripped (e.g. to remove workspace numbers). Defaults to zero.
        :param string separator:
                Specifies a string to be inserted between the workspace name and program icons
                and between program icons.
        :param dict icons:
                A dictionary mapping a substring of window classes to strings to be used as an icon for that
                window class. The following window classes have icons by default:
                ``Xfce4-terminal``, ``Chromium``, ``Steam``, ``jetbrains``, ``Gimp``, ``Pavucontrol``, ``Lmms``,
                ``Thunderbird``, ``Thunar``, ``Skype``, ``TelegramDesktop``, ``feh``, ``Firefox``, ``Evince``,
                ``Okular``, ``libreoffice-calc``, ``libreoffice-writer``.
                You can override the default icons by defining an icon for that window class yourself, and disable
                single icons by setting their icon to "" or None.
                Further, there is a ``multiple`` icon for workspaces containing more than one window (which is used if
                ``show_multiple_icons`` is ``False``)
        :param boolean show_icons:
                Determines whether to show icons. Defaults to True.
        :param boolean show_multiple_icons:
                If this is set to False, instead of displaying multiple icons per workspace,
                the icon "multiple" will be used.
        :param boolean show_dummy_workspace:
                If this is set to True, this segment will always display an additional, non-existing
                workspace. This workspace will be handled as if it was a non-urgent and non-focused
                regular workspace, i.e., click events will work as with normal workspaces.
        :param boolean show_output:
                Show the name of the output if more than one output is connected and output is not
                set to ``__all__``.
        :param string list priority_workspaces:
                A list of workspace names to be sorted before any other workspaces in the given
                order.
        :param boolean hide_empty_workspaces:
                Hides all workspaces without any open window. (Does not remove the dummy workspace.)
                Also hides non-focussed workspaces containing only an open scratchpad.

        Highlight groups used: ``workspace`` or ``workspace:visible``, ``workspace`` or ``workspace:focused``, ``workspace`` or ``workspace:urgent`` or ``output``.

        Click values supplied: ``workspace_name`` (string) for workspaces and ``output_name`` (string) for outputs.
        '''

    channel_name = 'i3wm.workspaces'
    conn = get_i3_connection()

    channel_value = None
    if 'payloads' in segment_info and channel_name in segment_info['payloads']:
        channel_value = segment_info['payloads'][channel_name]

    if channel_value:
        # Shrink the segment as far as possible
        only_show = ['focused', 'visible']
        show_multiple_icons = False

    output_count = 1
    if not output == "__all__":
        output = output or segment_info.get('output')
        if show_output:
            output_count = len([o for o in conn.get_outputs() if o.active])
    else:
        output = None
    if output:
        output = [output]
    else:
        output = [o.name for o in conn.get_outputs() if o.active]


    def sort_ws(ws):
        import re
        def natural_key(ws):
            str = ws.name
            return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', str)]
        ws = sorted(ws, key=natural_key)
        result = []
        for n in priority_workspaces:
            result += [w for w in ws if w.name == n]
        return result + [w for w in ws if not w.name in priority_workspaces] \
            + (get_next_ws(ws, output) if show_dummy_workspace else [])

    ws_containers = {w_con.name : w_con for w_con in conn.get_tree().workspaces()}
    if len(output) <= 1:
        res = []
        if output_count > 1:
            res += [{
                'contents': output[0],
                'payload_name': channel_name,
                'highlight_groups': ['output'],
                'click_values': {'output_name': output[0]}
                }]
        res += [{
            'contents': w.name[min(len(w.name), strip):] \
                    + (get_icon(w, separator, icons, show_multiple_icons, ws_containers) \
                        if show_icons else ""),
            'highlight_groups': workspace_groups(w),
            'payload_name': channel_name,
            'click_values': {'workspace_name': w.name}
            } for w in sort_ws(conn.get_workspaces())
            if (not only_show or any(getattr(w, typ) for typ in only_show))
            if w.output == output[0]
            if not (hide_empty_workspaces and is_empty_workspace(w, ws_containers))
            ]
        return res
    else:
        res = []
        for n in output:
            res += [{
                'contents': n,
                'highlight_groups': ['output'],
                'payload_name': channel_name,
                'click_values': {'output_name': n}
                }]
            res += [{'contents': w.name[min(len(w.name), strip):] \
                + (get_icon(w, separator, icons, show_multiple_icons, ws_containers) \
                if show_icons else ""),
                'highlight_groups': workspace_groups(w),
                'payload_name': channel_name,
                'click_values': {'workspace_name': w.name}} \
                        for w in sort_ws(conn.get_workspaces())
                if (not only_show or any(getattr(w, typ) for typ in only_show))
                if w.output == n
                if not (hide_empty_workspaces and is_empty_workspace(w, ws_containers))
                ]
        return res

@requires_segment_info
def mode(pl, segment_info, names={'default': None}):
    '''Returns current i3 mode

        :param str default:
            Specifies the name to be displayed instead of "default".
                By default the segment is left out in the default mode.

        Highlight groups used: ``mode``
        '''

    current_mode = segment_info['mode']

    if current_mode in names:
        return names[current_mode]
    return current_mode

def scratchpad_groups(w):
    group = []
    if w.urgent:
        group.append('scratchpad:urgent')
    if w.nodes[0].focused:
        group.append('scratchpad:focused')
    if w.workspace().name != '__i3_scratch':
        group.append('scratchpad:visible')
    group.append('scratchpad')
    return group


SCRATCHPAD_ICONS = {
        'fresh': 'O',
        'changed': 'X',
        }


def scratchpad(pl, icons=SCRATCHPAD_ICONS):
    '''Returns the windows currently on the scratchpad

        :param dict icons:
            Specifies the strings to show for the different scratchpad window states. Must
                contain the keys ``fresh`` and ``changed``.

        Highlight groups used: ``scratchpad`` or ``scratchpad:visible``, ``scratchpad`` or ``scratchpad:focused``, ``scratchpad`` or ``scratchpad:urgent``.
        '''

    windows = get_i3_connection().get_tree().descendants()
    return [{'contents': icons.get(w.scratchpad_state, icons['changed']),
        'highlight_groups': scratchpad_groups(w)
        } for w in windows if w.scratchpad_state != 'none']



# Global menu support heavily influenced by https://github.com/jamcnaughton/hud-menu
def compute_appmenu_menu(window_id):
    import dbus, time
    try:
        sbus = dbus.SessionBus()
        areg = sbus.get_object('com.canonical.AppMenu.Registrar',
                '/com/canonical/AppMenu/Registrar')
        aregi = dbus.Interface(areg, 'com.canonical.AppMenu.Registrar')

        dbmenu, dbmenu_path = aregi.GetMenuForWindow(window_id)

        dbo = sbus.get_object(dbmenu, dbmenu_path)
        dboi = dbus.Interface(dbo, 'com.canonical.dbusmenu')
        db_items = dboi.GetLayout(0, -1, ["label"])

        def explore(item):
            item_id = item[0]
            item_props = item[1]

            if 'children-display' in item_props:
                dboi.AboutToShow(item_id)
                dboi.Event(item_id, "opened", "not used", dbus.UInt32(time.time())) #fix firefox
            try:
                item = dboi.GetLayout(item_id, 1, ["label", "children-display"])[1]
            except:
                return { }

            item_children = item[2]

            name = 'Root'
            if 'label' in item_props:
                name = item_props['label'].replace('_', '')

            if len(item_children) == 0:
                return { name: lambda: dboi.Event(item_id, 'clicked', 0, 0) }
            else:
                res = {}
                for child in item_children:
                    res.update(explore(child))
                return { name : { r:res[r] for r in res if r != 'Root' } }

        itm = explore(db_items[1])
        if 'Root' in itm:
            return itm['Root']
        else:
            return itm
    except dbus.exceptions.DBusException:
        return None

gtk_click = None
def compute_gtk_menu(window_id):
    try:
        from Xlib import display, protocol, X
        import dbus

        dis = display.Display()
        win = dis.create_resource_object('window', window_id)

        def get_prop(prop):
            atom = win.get_full_property(dis.get_atom(prop), X.AnyPropertyType)
            if atom:
                return atom.value

        gtk_bus_name = get_prop('_GTK_UNIQUE_BUS_NAME')
        gtk_menu = get_prop('_GTK_MENUBAR_OBJECT_PATH')
        gtk_app = get_prop('_GTK_APPLICATION_OBJECT_PATH')
        gtk_win = get_prop('_GTK_WINDOW_OBJECT_PATH')
        gtk_unity = get_prop('_UNITY_OBJECT_PATH')
        gtk_bus_name, gtk_menu, gtk_app, gtk_win, gtk_unity = \
                [i.decode("utf8") if isinstance(i, bytes) \
                else i for i in [gtk_bus_name, gtk_menu, gtk_app, gtk_win, gtk_unity]]

        gtk_actions = list(set([gtk_win, gtk_menu, gtk_app, gtk_unity]))

        if not gtk_bus_name or not gtk_menu:
            return None

        session_bus = dbus.SessionBus()
        gtk_menu_o = session_bus.get_object(gtk_bus_name, gtk_menu)
        gtk_menu_i = dbus.Interface(gtk_menu_o, dbus_interface='org.gtk.Menus')

        gtk_menubar_action_dict = dict()
        gtk_menubar_action_target_dict = dict()

        usedLayers = []
        def Start(i):
            usedLayers.append(i)
            return gtk_menu_i.Start([i])

        no_data = dict()
        no_data["not used"] = "not used"
        def explore(parent):
            res = {}
            for node in parent:
                content = node[2]
                for element in content:
                    if 'label' in element:
                        if ':section' in element or ':submenu' in element:
                            if ':submenu' in element:
                                res.update({ element['label'].replace('_', ''):
                                    explore(Start(element[':submenu'][0])) })
                            if ':section' in element:
                                if element[':section'][0] != node[0]:
                                    res.update(explore(Start(element[':submenu'][0])))
                        elif 'action' in element:
                            menu_action = str(element['action']).split(".",1)[1]
                            target = []
                            if 'target' in element:
                                target = element['target']
                            if not isinstance(target, list):
                                target = [target]
                            res.update({ element['label'].replace('_', ''): (menu_action, target) })
                    else:
                        if ':submenu' in element or ':section' in element:
                            if ':section' in element:
                                if element[':section'][0] != node[0]:
                                    res.update(explore(Start(element[':section'][0])))
                            if ':submenu' in element:
                                res.update(explore(Start(element[':submenu'][0])))
            return res

        menuKeys = explore(Start(0))
        gtk_menu_i.End(usedLayers)

        def click(menu_action, target):
            for action_path in gtk_actions:
                if action_path == None:
                    continue
                try:
                    ao = session_bus.get_object(gtk_bus_name, action_path)
                    ai = dbus.Interface(ao, dbus_interface='org.gtk.Actions')
                    ai.Activate(menu_action, target, no_data)
                except Exception as e:
                    print('_'*20)
                    print(action_path)
                    print(str(e))
        global gtk_click
        gtk_click = click
        return menuKeys
    except:
        return None


def compute_menu(window_id):
    amen = compute_gtk_menu(window_id)
    if amen == None:
        amen = compute_appmenu_menu(window_id)
    return amen

def compute_highlight(ws, window):
    highlight_groups = []
    desc = [d.layout in ['tabbed', 'stacked'] for d in ws.descendants() \
            if d.parent.type == 'workspace' and d.floating in ['user_off', 'auto_off'] \
            and d.type != 'floating_con']

    if len([w for w in ws.leaves() if w.floating in ['user_off', 'auto_off']]) == 1:
        highlight_groups = ['active_window_title:single', 'active_window_title']
    elif len(desc) > 0 and all(desc) and (not window or window.floating) in ['user_on', 'auto_on']:
        highlight_groups = ['active_window_title:stacked_unfocused',
                'active_window_title']
    elif len(desc) > 0 and all(desc) and (not window or not window.focused):
        highlight_groups = ['active_window_title:stacked_unfocused',
                'active_window_title']
    elif len(desc) > 0 and all(desc):
        highlight_groups = ['active_window_title:stacked', 'active_window_title']
    else:
        highlight_groups = ['active_window_title']

    return highlight_groups

def split_layer(layer, max_length, item_length):
    res = []
    ln = 0
    cur = {}
    lst = list(layer.keys())
    for i in range(0, len(lst)):
        cl = min(len(lst[i]), item_length)
        if ln + cl > max_length:
            res += [cur]
            cur = {}
            ln = 0
        ln += cl
        cur.update({lst[i]: layer[lst[i]]})
    if ln:
        res += [cur]
    return res


active_window_state = 0
last_active_window = None
last_active_window_name = None
last_oneshot = 0
menu_items = None
current_layer = None
start = 0
path = []

@requires_segment_info
def active_window(pl, segment_info, cutoff=100, global_menu=False, item_length=20, \
        max_width=80, auto_expand=False, show_empty=False, **kwargs):
        '''
        Returns the title of the currently active window.
        To enhance the global menu support, add the following to your ``.bashrc``:

        .. code-block:: shell

            if [ -n "$GTK_MODULES" ]; then
                GTK_MODULES="${GTK_MODULES}:appmenu-gtk-module"
            else
                GTK_MODULES="appmenu-gtk-module"
            fi

            if [ -z "$UBUNTU_MENUPROXY" ]; then
                UBUNTU_MENUPROXY=1
            fi

            export GTK_MODULES
            export UBUNTU_MENUPROXY


        :param int cutoff:
            Maximum title length. If the title is longer, the window_class is used instead.
        :param boolean global_menu:
            Activate global menu support (experimental)
        :param int item_length:
            Maximum length of a menu item.
        :param int max_width:
            Maximum total length of the content.
        :param bool auto_expand:
            Add spaces to center the segment.
        :param bool show_empty:
            Show the sehment if no window is focused.

        Highlight groups used: ``active_window_title:single`` or ``active_window_title:stacked_unfocused`` or ``active_window_title:stacked`` or ``active_window_title``.
        '''

        global active_window_state
        global last_active_window
        global last_active_window_name
        global last_oneshot
        global menu_items
        global current_layer
        global start
        global path

        conn = get_i3_connection()

        if len(path) > 0:
            max_width = max_width - len('Main Menu')
        if len(path) > 1:
            max_width = max_width - len('Up a Level')

        channel_name = 'i3wm.active_window'

        channel_value = None
        if global_menu and 'payloads' in segment_info and channel_name in segment_info['payloads']:
            channel_value = segment_info['payloads'][channel_name]

        focused = conn.get_tree().find_focused()
        ws = focused.workspace()

        o_name = [w.output for w in conn.get_workspaces() \
                if w.name == ws.name][0]
        output = segment_info.get('output')

        if last_active_window != focused.window and last_active_window:
            # Please, don't kill me for this line
            if global_menu and last_active_window and 'payloads' in segment_info \
                    and 'i3wm.workspaces' in segment_info['payloads']:
                segment_info['payloads']['i3wm.workspaces'] = None

            last_active_window = None
            last_active_window_name = None
            active_window_state = 0
            start = 0
            menu_items = None
            current_layer = None
            path = []


        if o_name != output:
            if not show_empty:
                return None
            # Get visible workspace
            ws = [w for w in conn.get_workspaces() if w.output == output \
                    and w.visible]
            if not len(ws):
                return None
            ws = [w for w in focused.workspaces() if w.name == ws[0].name]
            if not len(ws):
                return None

            highlight = compute_highlight(ws[0], None)

            return [{
                'contents': '',
                'width': 'auto',
                'highlight_groups': highlight,
                'click_values': { 'segment': '' },
                'payload_name': 'DROP'
                }]

        if focused.name == focused.workspace().name:
            if not show_empty:
                return None
            return [{
                'contents': '',
                'width': 'auto',
                'highlight_groups': compute_highlight(ws, None),
                'click_values': { 'segment': '' },
                'payload_name': 'DROP'
                }]

        cont = [focused.name]
        if cutoff and len(cont) > cutoff:
            cont = [focused.window_class]

        main_cont = cont[0]

        if channel_value and not isinstance(channel_value, str) and len(channel_value) == 2 \
                and channel_value[0].startswith('menu_click') and channel_value[1] > last_oneshot:
            last_oneshot = channel_value[1]
            click_area = channel_value[0].split(':')[1]
            if active_window_state == 0:
                last_active_window = focused.window
                last_active_window_name = focused.name
                menu_items = compute_menu(focused.window)
                current_layer = split_layer(menu_items, max_width, item_length)
                path = []
                active_window_state = 1
            elif click_area == 'Main Menu':
                start = 0
                current_layer = split_layer(menu_items, max_width, item_length)
                path = []
            elif click_area == 'Up a Level':
                start = 0
                path = path[:-1]
                current_layer = menu_items
                cnt = 0
                for i in path:
                    current_layer = current_layer[i]
                    cnt += 1
                    if cnt > 1:
                        current_layer.update({'Up a Level': ''})
                    current_layer.update({'Main Menu': ''})
                current_layer = split_layer(current_layer, max_width, item_length)
            elif click_area == '$<':
                start = max(0, start - 1)
            elif click_area == '$>':
                start = min(len(current_layer) - 1, start + 1)
            elif click_area != '':
                if isinstance(current_layer[start][click_area], dict):
                    current_layer = current_layer[start][click_area]
                    if len(path) > 0:
                        current_layer.update({'Up a Level': ''})
                    current_layer.update({'Main Menu': ''})
                    current_layer = split_layer(current_layer, max_width, item_length)
                    start = 0
                    path += [click_area]
                else:
                    if isinstance(current_layer[start][click_area], tuple):
                        gtk_click(current_layer[start][click_area][0], current_layer[start][click_area][1])
                    else:
                        current_layer[start][click_area]()
                    current_layer = split_layer(menu_items, max_width, item_length)
                    path = []
                    start = 0

        if channel_value and not isinstance(channel_value, str) and len(channel_value) == 2 \
                and channel_value[0] == 'menu_off' and channel_value[1] > last_oneshot:
            last_oneshot = channel_value[1]
            active_window_state = 0
        if channel_value and not isinstance(channel_value, str) and len(channel_value) == 2 \
                and channel_value[0] == 'menu_on' and channel_value[1] > last_oneshot:
            last_oneshot = channel_value[1]
            active_window_state = 1
            if last_active_window != focused.window:
                last_active_window = focused.window
                last_active_window_name = focused.name
                menu_items = compute_menu(focused.window)
                current_layer = split_layer(menu_items, max_width, item_length)
                path = []
                start = 0

        if current_layer and active_window_state:
            cont = list(current_layer[start].keys())

        highlight = compute_highlight(ws, focused)
        res = []

        show_prev = start > 0 and active_window_state > 0
        show_next = current_layer and active_window_state > 0 \
                and start < len(current_layer) - 1

        def shorten(string, length):
            if len(string) < length - 1:
                return string
            return string[:length-1] + '…'

        if global_menu and (auto_expand or show_prev):
            res += [{
                'contents': '<' if show_prev else '',
                'highlight_groups': highlight,
                'payload_name': channel_name if show_prev else 'DROP',
                'draw_soft_divider': False,
                'draw_inner_divider': True if show_prev else False,
                'width': 'auto' if auto_expand else None,
                'align': 'r',
                'click_values': { 'segment': '$<' }
            }]

        total_len = 0
        for i in range(0, len(cont)):
            total_len += min(len(cont[i]), item_length) if cont[i] != main_cont \
                        else min(len(cont[i]), max_width)

        def truncate(pl, wd, seg):
            nl = max(5 * len(cont), int(total_len) - wd)
            if int(total_len) <= nl:
                return seg['contents']
            shr = (int(total_len) - nl) // len(cont)
            return shorten(seg['contents'], len(seg['contents']) - shr)


        for i in range(0, len(cont)):
            draw_div = i != 0 or show_prev or not auto_expand
            res += [{
                'contents': (shorten(cont[i],item_length) if cont[i] != main_cont \
                        else shorten(cont[i], max_width)),
                'highlight_groups': highlight,
                'payload_name': channel_name,
                'draw_inner_divider': draw_div,
                'draw_soft_divider': True ,
                'click_values': { 'segment': cont[i] if cont[i] != main_cont else '' },
                'truncate': truncate
                }]

        if global_menu and (auto_expand or show_next):
            res += [{
                'contents': '>' if show_next else '',
                'highlight_groups': highlight,
                'payload_name': channel_name if show_next else 'DROP',
                'width': 'auto' if auto_expand else None,
                'click_values': { 'segment': '$>' },
                'draw_inner_divider': bool(show_next),
            }]
        return res

