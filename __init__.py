import os
import sys
from aqt import mw
from aqt import gui_hooks, deckbrowser
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.utils import tooltip
from aqt.utils import showInfo
from aqt.debug_console import show_debug_console

addon_path = os.path.dirname(os.path.realpath(__file__))


# For debugging
sys_path_count = len(sys.path)

# from PyQt6.QtWidgets import QShortcut


@gui_hooks.deck_browser_did_render.append
def browser_render(browser: deckbrowser.DeckBrowser):
    # For debugging
    if len(sys.path) > sys_path_count:
        return

    if not mw:
        return

    # globalShortcuts = [
    #     # ("Ctrl+:", show_debug_console),
    #     ("d", lambda: ""),
    #     ("s", lambda: ""),
    #     ("a", lambda: ""),
    #     # ("b", mw.onBrowse),
    #     # ("t", mw.onStats),
    #     # ("Shift+t", mw.onStats),
    #     # ("y", mw.on_sync_button_clicked),
    # ]
    # scuts = mw.applyShortcuts(globalShortcuts)
    # scuts[2].setEnabled(False)
    # mw.stateShortcuts: list[QShortcut] = []
    # mw.clearStateShortcuts()

    # scut = QShortcut("a", mw)
    # scut.setAutoRepeat(False)
    # scut.setEnabled(False)
    # scut.disconnect()
    # scut.deleteLater()
    # mw.releaseShortcut(scut)
    tooltip(sys_path_count)


from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence


deck_list = []


def get_deck_list():
    return sorted(mw.col.decks.all(), key=lambda x: x["name"].lower())


@gui_hooks.collection_did_load.append
def on_collection_load(col):
    global deck_list
    deck_list = get_deck_list()

    # Retrieve all QShortcut objects that are children of the main window
    shortcuts = [child for child in mw.children() if isinstance(child, QShortcut)]

    # Now you can print out the key sequences of these shortcuts
    for shortcut in shortcuts:
        key_sequence = shortcut.key().toString(QKeySequence.SequenceFormat.NativeText)
        if key_sequence.upper() in "ASD":
            showInfo(key_sequence)
            shortcut.setEnabled(False)
            # mw.releaseShortcut(shortcut)


def get_current_deck():
    return mw.col.decks.current()


def select_deck(direction):
    decks = deck_list  # Get all decks
    current_deck = get_current_deck()  # Get the current deck
    current_deck_idx = next(
        (index for (index, d) in enumerate(decks) if d["id"] == current_deck["id"]),
        None,
    )

    if current_deck_idx is not None:
        if direction == "up":
            range_to_check = range(current_deck_idx - 1, -1, -1)
        elif direction == "down":
            range_to_check = range(current_deck_idx + 1, len(decks))
        else:
            return  # Invalid direction

        for idx in range_to_check:
            deck = decks[idx]
            if not is_deck_hidden(deck):  # Check if the deck is not hidden
                mw.col.decks.select(deck["id"])
                mw.deckBrowser.show()
                break


# This is the function that will be called when your shortcut is pressed
def goUp():
    select_deck("up")


def goDown():
    select_deck("down")


# Add shortcut
# shortcut = QShortcut(QKeySequence("Up"), mw)
# shortcut.activated.connect(goUp)

# shortcut = QShortcut(QKeySequence("Down"), mw)
# shortcut.activated.connect(goDown)


from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt.deckbrowser import DeckBrowserContent

from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt.deckbrowser import DeckBrowserContent


@gui_hooks.deck_browser_will_render_content.append
def on_deck_browser_will_render_content(
    deck_browser: DeckBrowser, content: DeckBrowserContent
):
    # For debugging
    if len(sys.path) > sys_path_count:
        return
    tree_html = content.tree
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
