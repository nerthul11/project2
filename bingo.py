import random

drawed_numbers = []
lowest = 0
largest = 90
line_winners = []
game_winners = []
tickets = []
info = {'draw': "", 'announcement': "", 'current_winners': [], 'maxscore': 0, 'endgame': False}

def generate_ticket(name):
    ticket = []
    while len(ticket) < 15:
        number = random.randint(lowest, largest)
        number = f"{number:02}"
        if number not in ticket:
            ticket.append(number)
    ticket_top = ticket[0:5]
    ticket_mid = ticket[5:10]
    ticket_bot = ticket[10:15]
    ticket = {'name': name, 'score': 0, 'top': ticket_top, 'mid': ticket_mid, 'bot': ticket_bot, 'undrawn': 15}
    print(ticket)
    return ticket

def draw_number():
    drawed_number = random.randint(lowest, largest)
    drawed_number = f"{drawed_number:02}"
    while drawed_number in drawed_numbers:
        drawed_number = random.randint(lowest,largest)
        drawed_number = f"{drawed_number:02}"
    drawed_numbers.append(drawed_number)
    multiplier = (largest - lowest) - len(drawed_numbers) + 1
    info['current_winners'] = []
    for ticket in tickets:
        for line in (ticket['top'],ticket['mid'],ticket['bot']):
            if drawed_number in line:
                ticket['score'] += multiplier * (16 - ticket['undrawn'])
                ticket['undrawn'] -= 1
        scorecheck(ticket)
    info['announcement'] = ""
    if not line_winners:
        linecheck(tickets)
    if not game_winners:
        gamecheck(tickets)
    if info['maxscore'] > 0:
        if len(info['current_winners']) > 1:
            info['draw'] = f"The number <span class=number>{drawed_number}</span> was drawn. There are currently {len(info['current_winners'])} current winners (Score: {info['maxscore']})"
        else:
            info['draw'] = f"The number <span class=number>{drawed_number}</span> was drawn. Current winner is {info['current_winners'][0]} (Score: {info['maxscore']})"
    else:
        info['draw'] = f"The number <span class=number>{drawed_number}</span> was drawn."

def linecheck(tickets):
    for ticket in tickets:
        for line in (ticket['top'],ticket['mid'],ticket['bot']):
            linecount = 0
            for number in line:
                if number in drawed_numbers:
                    linecount += 1
                    if linecount == 5:
                        line_winners.append(ticket)
    if line_winners:
        for ticket in line_winners:
            bonus = 25 * ((largest - lowest + 2) - len(drawed_numbers))
            ticket['score'] += bonus
            info['announcement'] = f"Line has been completed! {ticket['name']} obtained {bonus} extra points."
            scorecheck(ticket)

def gamecheck(tickets):
    for ticket in tickets:
        if ticket['undrawn'] == 0:
            game_winners.append(ticket)
    if game_winners:
       for ticket in game_winners:
           bonus = 100 * ((largest - lowest + 2) - len(drawed_numbers))
           ticket['score'] += bonus
           info['announcement'] = f"Game has been completed! {ticket['name']} obtained {bonus} extra points."
           scorecheck(ticket)
           info['endgame'] = True

def scorecheck(ticket):
    if ticket['score'] > info['maxscore']:
        info['maxscore'] = ticket['score']
        info['current_winners'].clear()
        info['current_winners'].append(ticket['name'])
    elif ticket['score'] == info['maxscore']:
        info['current_winners'].append(ticket['name'])

def main():
    # Runs the game automatically with a set number of tickets
    for i in range(50):
        ticket = generate_ticket(i)
        tickets.append(ticket)

    while not game_winners:
        draw_number()

if __name__ == "__main__":
    main()