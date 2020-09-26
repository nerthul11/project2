import random

drawed_numbers = []
lowest = 0
largest = 90
line_winners = []
game_winners = []
tickets = []

def generate_ticket(name):
    ticket = []
    while len(ticket) < 15:
        number = random.randint(lowest, largest)
        if number not in ticket:
            ticket.append(number)
    ticket_top = ticket[0:5]
    ticket_mid = ticket[5:10]
    ticket_bot = ticket[10:15]
    ticket = {'name': name, 'score': 0, 'top': ticket_top, 'mid': ticket_mid, 'bot': ticket_bot}
    return ticket

def draw_number():
    global drawtext
    drawed_number = random.randint(lowest,largest)
    while drawed_number in drawed_numbers:
        drawed_number = random.randint(lowest,largest)
    drawed_numbers.append(drawed_number)
    multiplier = (largest - lowest) - len(drawed_numbers) + 1
    for ticket in tickets:
        remaining = 16 - (len(ticket['top']) + len(ticket['mid']) + len(ticket['bot']))
        if drawed_number in ticket['top']:
            ticket['score'] += multiplier * remaining
            ticket['top'].remove(drawed_number)
        if drawed_number in ticket['mid']:
            ticket['score'] += multiplier * remaining
            ticket['mid'].remove(drawed_number)
        if drawed_number in ticket['bot']:
            ticket['score'] += multiplier * remaining
            ticket['bot'].remove(drawed_number)
    if not line_winners:
        linecheck(tickets)
    if not game_winners:
        gamecheck(tickets)

def linecheck(tickets):
    for ticket in tickets:
        if 0 in (len(ticket['top']),len(ticket['mid']),len(ticket['bot'])):
            line_winners.append(ticket['name'])
    if line_winners:
        for ticket in tickets:
            if ticket['name'] in line_winners:
                ticket['score'] += 25 * ((largest - lowest + 2) - len(drawed_numbers))

def gamecheck(tickets):
    for ticket in tickets:
        if not ticket['top'] and not ticket['mid'] and not ticket['bot']:
            game_winners.append(ticket['name'])
    if game_winners:
       for ticket in tickets:
           if ticket['name'] in game_winners:
                ticket['score'] += 100 * ((largest - lowest + 2) - len(drawed_numbers))

def main():
    # Runs the game automatically with a set number of tickets
    for i in range(50):
        ticket = generate_ticket(i)
        tickets.append(ticket)

    while not game_winners:
        draw_number()

if __name__ == "__main__":
    main()