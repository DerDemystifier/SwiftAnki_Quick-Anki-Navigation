import os
import sys
from aqt import mw
from aqt import gui_hooks, deckbrowser
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.utils import tooltip
from aqt.utils import showInfo

addon_path = os.path.dirname(os.path.realpath(__file__))


# Function to select a deck by its name
def select_deck_by_name(deck_name: str):
    # Access the collection
    col = mw.col

    tooltip(f"Selecting deck {deck_name}")

    # Decks are stored in a dictionary-like object
    # Use the deck name to get its ID
    deck_id = col.decks.id(deck_name)

    # Now select the deck with the given ID
    col.decks.select(deck_id)
    col.decks.selected()
    col.decks.current()
    col.decks.all()

    # Update the GUI to reflect the deck change
    mw.moveToState("deckBrowser")
    mw.deckBrowser.show()


def show_tooltip():
    showInfo("YAY!")


# For debugging
sys_path_count = len(sys.path)


@gui_hooks.deck_browser_did_render.append
def browser_render(browser: deckbrowser.DeckBrowser):
    # For debugging
    if len(sys.path) > sys_path_count:
        return

    globalShortcuts = [
        ("j", show_tooltip),
    ]
    mw.applyShortcuts(globalShortcuts)

    tooltip(sys_path_count)


from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence


def is_deck_hidden(deck):
    # Base case: if the deck is a top-level deck, it's not hidden.
    if "::" not in deck["name"]:
        return False

    # Split the deck name to check each parent
    parent_names = deck["name"].split("::")[:-1]

    # Iterate through each parent deck from top to bottom level
    for i in range(len(parent_names)):
        # Construct the parent deck's name
        parent_name = "::".join(parent_names[: i + 1])
        parent_deck = mw.col.decks.byName(parent_name)
        # If any parent deck is collapsed, the deck is hidden
        if parent_deck["collapsed"]:
            return True

    # If no parents are collapsed, the deck is visible
    return False


deck_list = []


def get_deck_list():
    return sorted(mw.col.decks.all(), key=lambda x: x["name"].lower())


@gui_hooks.collection_did_load.append
def on_collection_load(col):
    global deck_list
    deck_list = get_deck_list()


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
    tree_html = content.tree
    # Your custom JavaScript code
    custom_js = """
    <script>
    var keypressTimeout;

    document.addEventListener('keydown', function(event) {
        var currentDeck = document.querySelector('tr.deck.current');
        if (!currentDeck) return;

        switch (event.code) {
            case 'ArrowUp':
            case 'ArrowDown':            
                event.preventDefault();
                
                var decks = Array.from(document.querySelectorAll('tr.deck'));
                var currentIndex = decks.indexOf(currentDeck);
                var nextIndex = currentIndex + (event.code === 'ArrowDown' ? 1 : -1);
                
                // Boundary conditions
                if (nextIndex < 0 || nextIndex >= decks.length) return;
                
                // Remove 'current' class from the current deck and add it to the next one
                currentDeck.classList.remove('current');
                var nextDeck = decks[nextIndex];
                nextDeck.classList.add('current');
                
                // Scroll into view if out of viewport
                nextDeck.scrollIntoView({block: 'nearest', behavior: 'smooth'});
                
                
                // Clear any existing timeout to reset the timer
                clearTimeout(keypressTimeout);

                // Set a new timeout
                keypressTimeout = setTimeout(function() {
                    var deckId = currentDeck.id;
                    if (deckId) {
                        pycmd("select:" + deckId);
                    }
                }, 100); // Wait for 100ms before running the pycmd command
                break;
            case 'ArrowRight':
            case 'ArrowLeft':
                // Get the id of the current deck
                var deckId = currentDeck.id;
                // Check if a deckId was found and construct the pycmd
                if (deckId) {
                    pycmd("select:" + deckId);
                }
                // Simulate click on the collapse/expand link within the selected deck
                var collapseLink = currentDeck.querySelector('td.decktd > a.collapse');
                if (collapseLink) collapseLink.click();
                break;
            case 'KeyO':
                // Get the id of the current deck
                var deckId = currentDeck.id;
                // Check if a deckId was found and construct the pycmd
                if (deckId) {
                    pycmd("select:" + deckId);
                }
                // Simulate click on the options link within the selected deck
                var optsLink = currentDeck.querySelector('td.opts > a');
                if (optsLink) optsLink.click();
                break;
            case 'KeyD':
                // Get the id of the current deck
                var deckId = currentDeck.id;
                // Check if a deckId was found and construct the pycmd
                if (deckId) {
                    pycmd("select:" + deckId);
                }
                break
            case 'Enter':
                // Simulate click on the deck link within the selected deck
                var deckLink = currentDeck.querySelector('td.decktd > a.deck');
                if (deckLink) deckLink.click();
                break;

        }
    });
    </script>
    """
    content.tree += custom_js  # Append your custom JavaScript to the tree_html
