rooms = {
    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': ['key']
    },
    'Kitchen': {
        'north': 'Hall',
        'item': ['knife', 'potion']
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'item': ['monster']
    },
    'Garden': {
        'north': 'Dining Room',
        'item': ['monster']
    }
}