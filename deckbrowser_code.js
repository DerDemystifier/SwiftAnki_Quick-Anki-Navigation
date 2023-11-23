"use strict";

const all_decks_selector = "tr.deck";
const currentDeckSelector = "tr.deck.current";

document.addEventListener("keydown", function (event) {
    var currentDeck = document.querySelector(currentDeckSelector);
    if (!currentDeck) return;

    switch (event.code) {
        case "ArrowUp":
            var direction = "Up";
        case "ArrowDown":
            event.preventDefault();

            var direction = direction || "Down";

            var all_decks = Array.from(document.querySelectorAll(all_decks_selector));
            var currentIndex = all_decks.indexOf(currentDeck);
            var nextIndex = currentIndex + (direction === "Up" ? -1 : 1);

            // Boundary conditions
            if (nextIndex == -1 || nextIndex == all_decks.length) {
                window.scrollBy({ top: direction === "Up" ? -20 : 20, behavior: "smooth" });
                return;
            }

            // Remove 'current' class from the current deck and add it to the next one
            currentDeck.classList.remove("current");
            var nextDeck = all_decks[nextIndex];
            nextDeck.classList.add("current");

            // Set the current selected deck. This is used in the backend to determine which deck is currently selected
            bridgeCommand(`setCurrentDeck:${nextDeck.id}`);

            // Scroll ahead and behind of selected deck first to show neighboring decks too and ensure it is in plain view.
            // First slice the array to get the decks ahead and behind of the selected deck, then scroll to the furthest.
            var scrollToDeckAhead = all_decks.slice(nextIndex - 3, nextIndex + 4).at(direction === "Up" ? 0 : -1);
            var scrollToDeckBehind = all_decks.slice(nextIndex - 3, nextIndex + 4).at(direction === "Up" ? -1 : 0);

            scrollToDeckBehind?.scrollIntoView({ block: "nearest", behavior: "smooth" });
            scrollToDeckAhead?.scrollIntoView({ block: "nearest", behavior: "smooth" });
            break;
        case "ArrowRight":
        case "ArrowLeft":
            selectDeck(currentDeck.id);

            // Simulate click on the collapse/expand link within the selected deck
            var collapseLink = currentDeck.querySelector("td.decktd > a.collapse");
            if (collapseLink) collapseLink.click();
            break;
        case "KeyO":
            selectDeck(currentDeck.id);

            // Simulate click on the options link within the selected deck
            var optsLink = currentDeck.querySelector("td.opts > a");
            if (optsLink) optsLink.click();
            break;
        case "KeyD":
            bridgeCommand("showDecks");
            break;
        case "KeyA":
            bridgeCommand("addNote");
            break;
        case "KeyT":
            bridgeCommand("showStats");
            break;
        case "Enter":
        case "NumpadEnter":
        case "KeyS":
            bridgeCommand(`open:${currentDeck.id}`);
            break;
    }
});

(() => {
    // Create an observer to detect when the current deck goes out of view
    var observer = new IntersectionObserver(handleIntersect, { threshold: 1.0 });

    // Observe the current deck to check if it is not in view the first time the deck browser is loaded
    observer.observe(document.querySelector(currentDeckSelector));

    function handleIntersect(entries, observer) {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) {
                // Element has gone out of view, scroll it into view
                var currentDeck = entry.target;
                var all_decks = Array.from(document.querySelectorAll(all_decks_selector));
                var currentIndex = all_decks.indexOf(currentDeck);

                var scrollToDeckAhead = all_decks.slice(currentIndex - 2, currentIndex + 3).at(0);
                var scrollToDeckBehind = all_decks.slice(currentIndex - 2, currentIndex + 3).at(-1);

                scrollToDeckBehind?.scrollIntoView({ block: "nearest", behavior: "smooth" });
                scrollToDeckAhead?.scrollIntoView({ block: "nearest", behavior: "smooth" });

                // Disconnect the observer since we only need to scroll the deck into view once
                observer.disconnect();
            }
        });
    }

    // Disconnect the observer after 500ms. Because the deck browser might load while the current deck is in view. So no need observe it.
    setTimeout(() => {
        observer.disconnect();
    }, 500);
})();

/**
 * Selects the deck with the given id in the backend. This is important for the backend to determine which deck is currently selected.
 * Equivalent to mw.col.decks.select(currentDeck)
 * @param {number} deckId : The id of the deck to select
 */
function selectDeck(deckId) {
    if (deckId) {
        bridgeCommand("select:" + deckId);
    }
}
