/**
 * TalentYug Data Persistence Helper
 * Handles saving and loading events, guests, and settings to localStorage.
 */

const STORAGE_KEYS = {
    EVENTS: 'ty_events',
    GUESTS: 'ty_guests',
    THEME: 'ty_theme',
    QR_BATCHES: 'ty_qr_batches'
};

const Storage = {
    // --- EVENTS ---
    getEvents: () => {
        const data = localStorage.getItem(STORAGE_KEYS.EVENTS);
        return data ? JSON.parse(data) : [];
    },

    saveEvent: (eventData) => {
        const events = Storage.getEvents();
        // Check if editing existing
        const index = events.findIndex(e => e.id === eventData.id);
        if (index >= 0) {
            events[index] = eventData;
        } else {
            // Assign ID if new
            if (!eventData.id) eventData.id = Date.now().toString();
            events.push(eventData);
        }
        localStorage.setItem(STORAGE_KEYS.EVENTS, JSON.stringify(events));
        return eventData;
    },

    deleteEvent: (id) => {
        let events = Storage.getEvents();
        events = events.filter(e => e.id !== id);
        localStorage.setItem(STORAGE_KEYS.EVENTS, JSON.stringify(events));
    },

    // --- GUESTS ---
    getGuests: () => {
        const data = localStorage.getItem(STORAGE_KEYS.GUESTS);
        // Return dummy data if empty for first time demo
        if (!data) {
            const initial = [
                { id: '1', name: 'Arjun Sharma', email: 'arjun@example.com', status: 'confirmed' },
                { id: '2', name: 'Priya Singh', email: 'priya@example.com', status: 'pending' }
            ];
            localStorage.setItem(STORAGE_KEYS.GUESTS, JSON.stringify(initial));
            return initial;
        }
        return JSON.parse(data);
    },

    saveGuest: (guest) => {
        const guests = Storage.getGuests();
        if (!guest.id) guest.id = Date.now().toString();
        guests.unshift(guest); // Add to top
        localStorage.setItem(STORAGE_KEYS.GUESTS, JSON.stringify(guests));
        return guest;
    },

    deleteGuest: (id) => {
        let guests = Storage.getGuests();
        guests = guests.filter(g => g.id !== id);
        localStorage.setItem(STORAGE_KEYS.GUESTS, JSON.stringify(guests));
    },

    // --- THEME ---
    getTheme: () => {
        return localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
    },

    setTheme: (theme) => {
        localStorage.setItem(STORAGE_KEYS.THEME, theme);
        document.body.setAttribute('data-theme', theme);
    }
};

// Auto-init theme on load
(function () {
    const theme = Storage.getTheme();
    if (theme) document.body.setAttribute('data-theme', theme);
})();
