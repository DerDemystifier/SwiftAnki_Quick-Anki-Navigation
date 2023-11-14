import os
import sys
from aqt import QCoreApplication, QEvent, QMouseEvent, QPoint, QTimer, QWidget, Qt, mw
from aqt import gui_hooks, deckbrowser
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.utils import tooltip
from aqt.utils import showInfo
from aqt.debug_console import show_debug_console
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence
from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt.deckbrowser import DeckBrowserContent

from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt.deckbrowser import DeckBrowserContent
from aqt.main import MainWindowState

addon_path = os.path.dirname(os.path.realpath(__file__))


# For debugging
sys_path_count = len(sys.path)

# from PyQt6.QtWidgets import QShortcut


@gui_hooks.deck_browser_did_render.append
def browser_render(browser: deckbrowser.DeckBrowser):
    # For debugging
    if len(sys.path) > sys_path_count:
        return


@gui_hooks.collection_did_load.append
def on_collection_load(col):
    # For debugging
    if len(sys.path) > sys_path_count:
        return


@gui_hooks.deck_browser_will_render_content.append
def on_deck_browser_will_render_content(
    deck_browser: DeckBrowser, content: DeckBrowserContent
):
    # For debugging
    if len(sys.path) > sys_path_count:
        return

    # Your custom JavaScript code
    with open(os.path.join(addon_path, "deckbrowser_code.js"), "r") as f:
        custom_js = f"<script>{f.read()}</script>"

    content.tree += custom_js  # Append your custom JavaScript to the tree_html


@gui_hooks.state_shortcuts_will_change.append
def on_state_shortcuts_will_change(state, shortcuts):
    # For debugging
    # if len(sys.path) > sys_path_count:
    #     return

    # showInfo("NOPE")
    pass


@gui_hooks.state_did_change.append
def on_state_did_change(new_state: MainWindowState, old_state: MainWindowState):
    # For debugging
    if len(sys.path) > sys_path_count:
        return

    # showInfo(new_state)

    tooltip(new_state)

    if new_state == "deckBrowser":
        # Retrieve all QShortcut objects that are children of the main window
        switchShortcutsTo("ASD", False)
        # widgets = [child for child in mw.children() if isinstance(child, QWidget)]
        # widgets = [child for child in widgets[0].children() if isinstance(child, QWidget)]
        # with open('R:/aa.txt', 'w') as f:
        #     f.write(str(widgets))
        # widgets[1].setFocus()
        mw.web.setFocus()
    else:
        switchShortcutsTo("ASD", True)


# @gui_hooks.state_shortcuts_will_change.append
# def on_state_shortcuts_will_change(state, shortcuts):
# # For debugging
# if len(sys.path) > sys_path_count:
# return

# switchShortcutsTo("ASD", True)


def switchShortcutsTo(keys_string: str, state: bool):
    shortcuts = [child for child in mw.children() if isinstance(child, QShortcut)]

    # Now you can print out the key sequences of these shortcuts
    for shortcut in shortcuts:
        key_sequence = shortcut.key().toString(QKeySequence.SequenceFormat.NativeText)
        if key_sequence.upper() in keys_string:
            # showInfo(key_sequence)
            shortcut.setEnabled(state)
            # mw.releaseShortcut(shortcut)


@gui_hooks.webview_did_receive_js_message.append
def on_webview_did_receive_js_message(
    handled: tuple[bool, object], message: str, context: any
):
    if not isinstance(context, DeckBrowser):
        # not reviewer, pass on message
        return handled

    if message == "openAddDialog":
        # our message, call onMark() on the reviewer instance
        mw.onAddCard()
        # and don't pass message to other handlers
        return (True, None)
    else:
        # some other command, pass it on
        return handled


@gui_hooks.focus_did_change.append
def on_focus_did_change(new: QWidget, old: QWidget):
    if mw.web.isVisible():
        mw.web.setFocus()
