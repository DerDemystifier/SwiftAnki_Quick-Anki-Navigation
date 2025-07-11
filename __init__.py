import os
from aqt import QWidget, mw, gui_hooks
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.toolbar import TopToolbar
from aqt.qt import QShortcut, QKeySequence
from aqt.main import MainWindowState
from anki.decks import DeckId  # DeckId is an alias for int

# imports used for debugging
from aqt.utils import showInfo, showText

from typing import Union


addon_path = os.path.dirname(os.path.realpath(__file__))

# tracks the current deck that is selected using the injected JS code
currentDeck: DeckId = DeckId(0)

# tracks whether the default shortcuts are disabled or not
keys_disabled = False


@gui_hooks.deck_browser_will_render_content.append
def on_deck_browser_will_render_content(deck_browser: DeckBrowser, content: DeckBrowserContent):
    # Load our custom JavaScript for handling keyboard shortcuts
    with open(os.path.join(addon_path, "deckbrowser_code.js"), "r") as f:
        custom_js = f"<script>{f.read()}</script>"

    content.tree += custom_js  # Append your custom JavaScript to the tree_html


@gui_hooks.state_did_change.append
def on_state_did_change(new_state: MainWindowState, old_state: MainWindowState):
    global keys_disabled

    if not mw:
        return

    if new_state == "deckBrowser":
        # We will only disable the shortcuts when the user changes the selected deck later on
        mw.web.setFocus()
    else:
        # Enable the shortcuts when the user is not in the deck browser
        switchShortcutsTo("ASDTBY", True)
        keys_disabled = False


def switchShortcutsTo(keys_string: str, state: bool):
    """Switches the shortcuts to the given state

    Args:
        keys_string (str): the keys to switch
        state (bool): the state to switch to
    """
    if not mw:
        return

    # Retrieve all the shortcuts in the main window
    shortcuts = [child for child in mw.children() if isinstance(child, QShortcut)]

    for shortcut in shortcuts:
        key_sequence = shortcut.key().toString(QKeySequence.SequenceFormat.NativeText)
        if key_sequence.upper() in keys_string:
            shortcut.setEnabled(state)


@gui_hooks.webview_did_receive_js_message.append
def on_webview_did_receive_js_message(handled: tuple[bool, object], message: str, context: object):
    global currentDeck, keys_disabled

    if not mw or not mw.col:
        return handled

    if not isinstance(context, DeckBrowser) and not isinstance(context, TopToolbar):
        # We're only concerned with the deck browser and tooltip
        return handled

    if any(
        message.startswith(f"{keyword}:")
        for keyword in ["setCurrentDeck", "open", "collapse", "opts"]
    ):
        # Update the current selected deck with the current deck ID
        currentDeck = DeckId(int(message.split(":")[1]))

        if not keys_disabled:
            # Disable the native shortcuts in the deck browser since the selected deck has changed
            # The native shortcuts will function on the selected deck, not on the newly focused-on deck.
            switchShortcutsTo("ASDTBY", False)
            keys_disabled = True

        return handled
    else:
        # Now select the deck with the given ID
        mw.col.decks.select(currentDeck)

        if message == "addNote":
            mw.onAddCard()  # Open the add dialog for the current deck
        elif message == "showDecks":
            mw.moveToState("deckBrowser")
        elif message == "browseDeck":
            mw.onBrowse()  # Open the browser for the current deck
        elif message == "showStats":
            mw.onStats()
        elif message == "sync":
            mw.onSync()
        else:
            # Return unhandled
            return handled

        # and don't pass message to other handlers
        return (True, None)


@gui_hooks.focus_did_change.append
def on_focus_did_change(new: Union[QWidget, None], old: Union[QWidget, None]):
    if not mw:
        return

    # If the focus is on the toolbar or the bottom web, then we want to switch focus to the main web view
    if mw.toolbar.web.hasFocus() or mw.bottomWeb.hasFocus():
        mw.web.setFocus()
