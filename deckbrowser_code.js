const currentDeckSelector = 'tr.deck.current';

document.addEventListener('keydown', function (event) {
    var currentDeck = document.querySelector(currentDeckSelector);
    if (!currentDeck) return;

    currentDeck.scrollIntoView({ block: 'nearest', behavior: 'smooth' });

    switch (event.code) {
        case 'ArrowUp':
        case 'ArrowDown':
            event.preventDefault();

            let direction = event.code === 'ArrowUp' ? "Up" : "Down";

            var decks = Array.from(document.querySelectorAll('tr.deck'));
            var currentIndex = decks.indexOf(currentDeck);
            var nextIndex = currentIndex + (direction === 'Up' ? -1 : 1);

            // Boundary conditions
            if (nextIndex < 0 || nextIndex >= decks.length) { window.scrollBy({ top: direction === 'Up' ? -20 : 20, behavior: 'smooth' }); return; };

            // Remove 'current' class from the current deck and add it to the next one
            currentDeck.classList.remove('current');
            var nextDeck = decks[nextIndex];
            nextDeck.classList.add('current');

            pycmd(`setCurrentDeck:${nextDeck.id}`);

            var scrollToDeckAhead = decks.slice(nextIndex - 3, nextIndex + 4).at(direction === 'Up' ? 0 : -1);
            var scrollToDeckBehind = decks.slice(nextIndex - 3, nextIndex + 4).at(direction === 'Up' ? -1 : 0);

            // Scroll ahead and behind to show neighboring decks too
            scrollToDeckBehind?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            scrollToDeckAhead?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
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
        case 'KeyA':

            // Get the id of the current deck
            var deckId = currentDeck.id;
            // Check if a deckId was found and construct the pycmd
            if (deckId) {
                pycmd("select:" + deckId);
            }

            console.log('deckId :>> ', deckId);
            pycmd('openAddDialog');
            break;
        case 'KeyS':
            // // Get the id of the current deck
            var deckId = currentDeck.id;
            pycmd(`open:${deckId}`);
            break;
        case 'KeyT':
            pycmd("showStats");
            break;
        case 'Enter':
            // Simulate click on the deck link within the selected deck
            var deckLink = currentDeck.querySelector('td.decktd > a.deck');
            if (deckLink) deckLink.click();
            break;
    }
});



var observer = new IntersectionObserver(handleIntersect, { threshold: 1.0 });


observer.observe(document.querySelector(currentDeckSelector));

function handleIntersect(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            // Element has gone out of view, scroll it into view
            entry.target.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            observer.disconnect();
        }
    });
}

