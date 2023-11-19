import os
from aqt import QWidget, mw, gui_hooks
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.toolbar import TopToolbar
from aqt.qt import QShortcut, QKeySequence
from aqt.main import MainWindowState

addon_path = os.path.dirname(os.path.realpath(__file__))
currentDeck = 0  # tracks the current deck that is selected using the injected JS code


@gui_hooks.deck_browser_will_render_content.append
def on_deck_browser_will_render_content(
    deck_browser: DeckBrowser, content: DeckBrowserContent
):
    # Load our custom JavaScript for handling keyboard shortcuts
    with open(os.path.join(addon_path, "deckbrowser_code.js"), "r") as f:
        custom_js = f"<script>{f.read()}</script>"

    content.tree += custom_js  # Append your custom JavaScript to the tree_html


@gui_hooks.state_did_change.append
def on_state_did_change(new_state: MainWindowState, old_state: MainWindowState):
    if not mw:
        return

    if new_state == "deckBrowser":
        # Disable the shortcuts in the deck browser
        switchShortcutsTo("ASDT", False)
        mw.web.setFocus()
    else:
        switchShortcutsTo("ASDT", True)


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
def on_webview_did_receive_js_message(
    handled: tuple[bool, object], message: str, context: any
):
    global currentDeck

    if not mw or not mw.col:
        return handled

    if not isinstance(context, DeckBrowser) and not isinstance(context, TopToolbar):
        # We're only concerned with the deck browser and tooltip
        return handled

    if "setCurrentDeck" in message:
        # The arrow keys were pressed, so we need to update the current selected deck
        currentDeck = int(message.split(":")[1])

        # and don't pass message to other handlers
        return (True, None)
    else:
        # Now select the deck with the given ID
        mw.col.decks.select(currentDeck)

        if message == "addNote":
            mw.onAddCard()  # Open the add dialog for the current deck
        elif message == "showDecks":
            mw.moveToState("deckBrowser")
        elif message == "showStats":
            mw.onStats()
        else:
            # Return unhandled
            return handled

        # and don't pass message to other handlers
        return (True, None)


@gui_hooks.focus_did_change.append
def on_focus_did_change(new: QWidget, old: QWidget):
    if not mw:
        return

    # If the focus is on the toolbar or the bottom web, then we want to switch focus to the main web view
    if mw.toolbar.web.hasFocus() or mw.bottomWeb.hasFocus():
        mw.web.setFocus()


@gui_hooks.top_toolbar_did_init_links.append
def on_top_toolbar_did_init_links(links: list[str], top_toolbar):
    # Replace the default links in the toolbar with our own
    for index, link in enumerate(links):
        if "pycmd('add')" in link:
            links[index] = link.replace("pycmd('add')", "pycmd('addNote')")
        elif "pycmd('decks')" in link:
            links[index] = link.replace("pycmd('decks')", "pycmd('showDecks')")
        elif "pycmd('stats')" in link:
            links[index] = link.replace("pycmd('stats')", "pycmd('showStats')")
