var keypressTimeout = -1;

document.addEventListener('keydown', function (event) {
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
            nextDeck.scrollIntoView({ block: 'nearest', behavior: 'smooth' });


            // Clear any existing timeout to reset the timer
            clearTimeout(keypressTimeout);

            console.log(keypressTimeout);

            // Set a new timeout
            keypressTimeout = setTimeout(function () {
                var deckId = nextDeck.id;
                if (deckId) {
                    console.log("Selecting deck ", nextDeck);
                    pycmd("select:" + deckId);
                }
            }, 200); // Wait for 300ms before running the pycmd command
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
            break;
        case 'Enter':
            // Simulate click on the deck link within the selected deck
            var deckLink = currentDeck.querySelector('td.decktd > a.deck');
            if (deckLink) deckLink.click();
            break;

    }
});