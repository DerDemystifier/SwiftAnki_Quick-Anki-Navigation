document.addEventListener('keydown', function (event) {
    var currentDeck = document.querySelector('tr.deck.current');
    if (!currentDeck) return;

    switch (event.code) {
        case 'ArrowUp':            
        case 'ArrowDown':
            event.preventDefault();
			
			let direction = event.code === 'ArrowUp' ? "Up" : "Down";

            var decks = Array.from(document.querySelectorAll('tr.deck'));
            var currentIndex = decks.indexOf(currentDeck);
            var nextIndex = currentIndex + (direction === 'Up' ? -1 : 1);

            // Boundary conditions
            if (nextIndex < 0 || nextIndex >= decks.length) { window.scrollBy({ top: direction === 'Up' ? -10 : 10, behavior: 'smooth' }); return };

            // Remove 'current' class from the current deck and add it to the next one
            currentDeck.classList.remove('current');
            var nextDeck = decks[nextIndex];
            nextDeck.classList.add('current');
			
			var scrollToDeck = decks[nextIndex + (direction === 'Up' ? -3 : 3)];

            // Scroll into view if out of viewport
            nextDeck.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
			
			// Scroll ahead to show neighbors too
			scrollToDeck?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
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
            // Get the id of the current deck
            var deckId = currentDeck.id;
            // Check if a deckId was found and construct the pycmd
            if (deckId) {
                pycmd("select:" + deckId);
            }
        case 'Enter':
            // Simulate click on the deck link within the selected deck
            var deckLink = currentDeck.querySelector('td.decktd > a.deck');
            if (deckLink) deckLink.click();
            break;
    }
});