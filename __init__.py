import os
import sys
from aqt import QWidget, mw, gui_hooks
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.toolbar import TopToolbar
from aqt.utils import tooltip, showText
from aqt.qt import QShortcut, QKeySequence
from aqt.main import MainWindowState

addon_path = os.path.dirname(os.path.realpath(__file__))

if not mw:
    quit()

# For debugging
sys_path_count = len(sys.path)


@gui_hooks.deck_browser_did_render.append
def browser_render(browser: DeckBrowser):
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
        switchShortcutsTo("ASDT", False)
        # widgets = [child for child in mw.children() if isinstance(child, QWidget)]
        # widgets = [child for child in widgets[0].children() if isinstance(child, QWidget)]
        # with open('R:/aa.txt', 'w') as f:
        #     f.write(str(widgets))
        # widgets[1].setFocus()
        mw.web.setFocus()
    else:
        switchShortcutsTo("ASDT", True)


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


currentDeck = 0


@gui_hooks.webview_did_receive_js_message.append
def on_webview_did_receive_js_message(
    handled: tuple[bool, object], message: str, context: any
):
    global currentDeck

    # For debugging
    if len(sys.path) > sys_path_count:
        return handled

    if not mw or not mw.col:
        return handled

    if not isinstance(context, DeckBrowser) and not isinstance(context, TopToolbar):
        # We're only concerned with the deck browser and tooltip
        return handled

    if "setCurrentDeck" in message:
        # our message, call onMark() on the reviewer instance
        currentDeck = int(message.split(":")[1])

        # and don't pass message to other handlers
        return (True, None)
    elif message == "openAddDialog":
        # our message, call onMark() on the reviewer instance
        mw.onAddCard()
        # and don't pass message to other handlers
        return (True, None)
    elif message == "addNote":
        # Now select the deck with the given ID
        mw.col.decks.select(currentDeck)

        mw.onAddCard()

        return (True, None)
    elif message == "showDecks":
        # Now select the deck with the given ID
        mw.col.decks.select(currentDeck)

        mw.moveToState("deckBrowser")

        return (True, None)
    elif message == "showStats":
        # Now select the deck with the given ID
        mw.col.decks.select(currentDeck)

        mw.onStats()

        return (True, None)
    else:
        # some other command, pass it on
        return handled


@gui_hooks.focus_did_change.append
def on_focus_did_change(new: QWidget, old: QWidget):
    # If the focus is on the toolbar or the bottom web, then we want to focus the main web view
    if mw.toolbar.web.hasFocus() or mw.bottomWeb.hasFocus():
        mw.web.setFocus()


@gui_hooks.top_toolbar_did_init_links.append
def on_top_toolbar_did_init_links(links: list[str], top_toolbar):
    # showText(str(links))
    for index, link in enumerate(links):
        if "pycmd('add')" in link:
            links[index] = link.replace("pycmd('add')", "pycmd('addNote')")
        elif "pycmd('decks')" in link:
            links[index] = link.replace("pycmd('decks')", "pycmd('showDecks')")
        elif "pycmd('stats')" in link:
            links[index] = link.replace("pycmd('stats')", "pycmd('showStats')")
