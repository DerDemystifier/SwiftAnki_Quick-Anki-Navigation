/* eslint-disable no-undef */
/* eslint-disable no-fallthrough */
'use strict';

/**
 * This script is fetched everytime the deck browser is switched to, so no need to worry about reloading the addon.
 */

const allDecksSelector = 'tr.deck';
const currentDeckSelector = 'tr.deck.current';

document.addEventListener('keydown', function (event) {
    const currentDeck = getCurrentDeck();
    if (!currentDeck) return;

    let direction;

    switch (event.code) {
        case 'ArrowUp':
        case 'Numpad8':
        case 'KeyK':
            direction = 'Up';
        case 'ArrowDown':
        case 'Numpad2':
        case 'KeyJ': {
            event.preventDefault();

            direction = direction || 'Down';

            const allDecks = getAllDecks();
            const currentIndex = allDecks.indexOf(currentDeck);
            const nextIndex = currentIndex + (direction === 'Up' ? -1 : 1);

            // Boundary conditions
            if (nextIndex === -1 || nextIndex === allDecks.length) {
                window.scrollBy({ top: direction === 'Up' ? -20 : 20, behavior: 'smooth' });
                return;
            }

            // Remove 'current' class from the current deck and add it to the next one
            const nextDeck = switchCurrentDeck(currentDeck, nextIndex);

            // Set the current selected deck. This is used in the backend to determine which deck is currently selected
            bridgeCommand(`setCurrentDeck:${nextDeck.id}`);

            // Scroll ahead and behind of selected deck first to show neighboring decks too and ensure it is in plain view.
            // First slice the array to get the decks ahead and behind of the selected deck, then scroll to the furthest.
            scrollDeckIntoView(nextDeck, 3);
            break;
        }
        case 'ArrowRight':
        case 'Numpad6':
        case 'KeyL':
        case 'ArrowLeft':
        case 'Numpad4':
        case 'KeyH': {
            selectDeck(currentDeck.id);

            // Simulate click on the collapse/expand link within the selected deck
            const collapseLink = currentDeck.querySelector('td.decktd > a.collapse');
            collapseLink?.click();
            break;
        }
        case 'KeyO': {
            selectDeck(currentDeck.id);

            // Simulate click on the options link within the selected deck
            const optsLink = currentDeck.querySelector('td.opts > a');
            optsLink?.click();
            break;
        }
        case 'KeyD':
            bridgeCommand('showDecks');
            break;
        case 'KeyA':
            bridgeCommand('addNote');
            break;
        case 'KeyB':
            selectDeck(currentDeck.id);
            pycmd('browseDeck');
            break;
        case 'KeyT':
            bridgeCommand('showStats');
            break;
        case 'KeyY':
            bridgeCommand('sync');
            break;
        case 'Enter':
        case 'NumpadEnter':
        case 'KeyS':
            bridgeCommand(`open:${currentDeck.id}`);
            break;
    }
});

(() => {
    // Observe the current deck to check if it is not in view the first time the deck browser is loaded
    setTimeout(() => {
        const currentDeck = getCurrentDeck();

        scrollDeckIntoView(currentDeck, 3);
    }, 500);
})();

/**
 * Selects the deck with the given id in the backend. This is important for the backend to determine which deck is currently selected.
 * Equivalent to mw.col.decks.select(currentDeck)
 * @param {number} deckId : The id of the deck to select
 */
function selectDeck(deckId) {
    if (deckId) {
        bridgeCommand('select:' + deckId);
    }
}

function getAllDecks() {
    return Array.from(document.querySelectorAll(allDecksSelector));
}

/**
 * Returns the current selected deck. If no deck is selected, the first deck is selected and returned.
 * @returns {HTMLElement} The current selected deck
 */
function getCurrentDeck() {
    return document.querySelector(currentDeckSelector) || switchCurrentDeck(undefined, 0);
}

/**
 * Removes the 'current' class from the current selected deck and adds it to the next deck.
 * @param {HTMLElement} currentDeck  The current selected deck
 * @param {number}  nextIndex The index of the next deck to select
 * @returns {HTMLElement} The next selected deck
 */
function switchCurrentDeck(currentDeck, nextIndex) {
    currentDeck?.classList.remove('current');
    const nextDeck = getAllDecks()[nextIndex];
    nextDeck.classList.add('current');
    return nextDeck;
}

function scrollDeckIntoView(deck, range) {
    const allDecks = getAllDecks();
    const currentIndex = allDecks.indexOf(deck);

    const decksWithinRange = allDecks.slice(currentIndex - range, currentIndex + range + 1);

    decksWithinRange.at(0)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    decksWithinRange.at(-1)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}
