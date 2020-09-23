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
    ticket = {'name': name, 'top': ticket_top, 'mid': ticket_mid, 'bot': ticket_bot}
    return ticket

def draw_number():
    drawed_number = random.randint(lowest,largest)
    while drawed_number in drawed_numbers:
        drawed_number = random.randint(lowest,largest)
    drawed_numbers.append(drawed_number)
    if len(drawed_numbers) % 1000 == 0:
        print(len(drawed_numbers))
    for ticket in tickets:
        if drawed_number in ticket['top']:
            ticket['top'].remove(drawed_number)
        if drawed_number in ticket['mid']:
            ticket['mid'].remove(drawed_number)
        if drawed_number in ticket['bot']:
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
        print(len(drawed_numbers))
        print(f"Line: {line_winners}")

def gamecheck(tickets):
    for ticket in tickets:
        if not ticket['top'] and not ticket['mid'] and not ticket['bot']:
            game_winners.append(ticket['name'])
    if game_winners:
        print(len(drawed_numbers))
        print(f"Game: {game_winners}")

def main():
    for i in range(50):
        i = generate_ticket(i)
        tickets.append(i)

    # Game automatically run
    while not game_winners:
        draw_number()

if __name__ == "__main__":
    main()