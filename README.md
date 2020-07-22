from penguin_game import *


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    global mirvah
    mirvah = 1
    # Go over all of my icebergs.
    try:
        if game.turn > game.max_turns / 10:
            mirvah = 5
        if game.turn > game.max_turns / 3:
            mirvah = 8

        for my_iceberg in game.get_my_icebergs():
            if game.turn < 10:
                upgrade(my_iceberg, game)

            else:
                neutral_icebergs = game.get_neutral_icebergs()
                bubble_sort_by_peng(neutral_icebergs, my_iceberg, game)

                enemy_icebergs = game.get_enemy_icebergs()
                bubble_sort_by_peng(enemy_icebergs, my_iceberg, game)

                destination = pick_destination_by_func(my_iceberg, bubble_sort_by_peng, game)

                iceberg_under_attack = get_closest_iceberg_under_attack(my_iceberg, game)

                if destination is None:
                    destination = pick_destination_by_func(my_iceberg, bubble_sort_by_distance, game)

                pick_course_of_action(destination, iceberg_under_attack, my_iceberg, game)
    except:
        pass


def mult_attackers(my_iceberg, game):
    attackers = {}
    friendly_icebergs = game.get_my_icebergs()
    for iceberg in friendly_icebergs[friendly_icebergs.index(my_iceberg):]:
        peng_directed = get_peng_directed(iceberg, game)
        if game.turn < game.max_turns // 6 or game.turn > game.max_turns // 2:
            send_amount = iceberg.penguin_amount // 2
        else:
            send_amount = iceberg.penguin_amount // 3
        print(peng_directed)
        if iceberg.penguin_amount - send_amount + peng_directed > 0:
            attackers[iceberg] = send_amount

    return attackers


def capturable_destination_by_mult(attackers, game):
    for destination in game.get_enemy_icebergs():
        if calculate_num_of_peng_mult(destination, attackers, game) > 0:
            return destination


def calculate_num_of_peng_mult(destination, origin_dict, game):
    total_sent = 0
    total_generated = 0
    cur_distance = 0
    attacker_list = origin_dict.keys()
    bubble_sort_by_distance(attacker_list, destination, game)
    for iceberg in attacker_list:
        cur_distance = iceberg.get_turns_till_arrival(destination) - cur_distance
        total_sent += origin_dict[attacker_list]
        total_generated += cur_distance * destination.penguins_per_turn

    return total_sent - total_generated - destination.penguin_amount


def pick_course_of_action(destination, iceberg_under_attack, my_iceberg, game):
    """Decides what the bot is gonna do (attack, defend, upgrade etc.)"""
    global mirvah

    if destination is None:
        destination = pick_destination_by_func(my_iceberg, bubble_sort_by_distance, game)

    already_sent = False

    if not my_iceberg.already_acted:
        if destination is not None:
            if iceberg_under_attack is not None:
                # If the dest is higher level than berg under attack, try to attack and then to defend
                if (destination.level > iceberg_under_attack.level or
                        (destination.level == iceberg_under_attack.level and destination not in game.get_neutral_icebergs())):
                    if can_attack(destination, my_iceberg, game):
                        attack(destination, my_iceberg, game)
                        already_sent = True
                    elif can_defend(iceberg_under_attack, my_iceberg, game):
                        defend(iceberg_under_attack, my_iceberg, game)
                        already_sent = True
                # If the berg under attack is higher level than the dest, try to defend and then attack
                else:
                    if can_defend(iceberg_under_attack, my_iceberg, game):
                        defend(iceberg_under_attack, my_iceberg, game)
                        already_sent = True
                    elif can_attack(iceberg_under_attack, my_iceberg, game):
                        attack(iceberg_under_attack, my_iceberg, game)
                        already_sent = True
                # Try to upgrade if we can
                upgrade(my_iceberg, game)
            # If dest is not None and berg is None, try to attack and then try to upgrade
            else:
                if can_attack(destination, my_iceberg, game):
                    attack(destination, my_iceberg, game)
                    already_sent = True
                upgrade(my_iceberg, game)
        else:
            if iceberg_under_attack is not None:
                if can_defend(iceberg_under_attack, my_iceberg, game):
                    defend(iceberg_under_attack, my_iceberg, game)
                    already_sent = True
            upgrade(my_iceberg, game)

    if not my_iceberg.already_acted and not already_sent:
        attackers = mult_attackers(my_iceberg, game)
        destination = capturable_destination_by_mult(attackers, game)
        for attacker in attackers:
            send_amount = attackers[attacker]
            print(attacker, "sends", send_amount, "penguins to", destination)
            attacker.send_penguins(destination, send_amount)


def closest_friendly_iceberg(my_iceberg, game):
    """Returns the closest friendly iceberg to a given iceberg"""
    friendly_icebergs = game.get_my_icebergs()
    friendly_icebergs.remove(my_iceberg)
    bubble_sort_by_distance(friendly_icebergs, my_iceberg, game)

    return friendly_icebergs[0]


def attack_amount(destination, my_iceberg, game):
    """Generate the amount of penguins we want to send to an enemy iceberg to capture it"""
    global mirvah
    return calculate_num_of_peng(destination, my_iceberg, game) + mirvah


def can_attack(destination, my_iceberg, game):
    """Returns if you can attack an enemy iceberg (and capture it)"""
    send_amount = attack_amount(destination, my_iceberg, game)
    return my_iceberg.penguin_amount > send_amount and get_peng_directed(my_iceberg, game) - send_amount > 0


def attack(destination, my_iceberg, game):
    """Sends penguins to attack an enemy iceberg"""
    send_amount = attack_amount(destination, my_iceberg, game)
    if can_attack(destination, my_iceberg, game):
        print(my_iceberg, "sends", send_amount, "penguins to", destination)
        my_iceberg.send_penguins(destination, send_amount)


def upgrade(my_iceberg, game):
    """Upgrades the iceberg"""
    if get_peng_after_upgrade(my_iceberg, game) > 0:
        if my_iceberg.can_upgrade():
            my_iceberg.upgrade()


def defense_amount(iceberg_under_attack, game):
    """Returns the amount of penguins we want to send to an iceberg to defend it"""
    return - get_peng_directed(iceberg_under_attack, game) + mirvah


def can_defend(iceberg_under_attack, my_iceberg, game):
    """Returns whether we can defend an iceberg"""
    return my_iceberg.penguin_amount > defense_amount(iceberg_under_attack, game)


def defend(iceberg_under_attack, my_iceberg, game):
    """Sends penguins to defend a friendly iceberg"""
    global mirvah
    send_amount = defense_amount(iceberg_under_attack, game)
    if can_defend(iceberg_under_attack, my_iceberg, game):
        print(my_iceberg, "sends", send_amount, "penguins to", iceberg_under_attack)
        my_iceberg.send_penguins(iceberg_under_attack, send_amount)

def is_iceberg_under_attack(iceberg, game):
    """Returns whether a given iceberg is in risk of being conquered"""
    return get_peng_directed(iceberg, game) < 0

def get_closest_iceberg_under_attack(my_iceberg, game):
    """Returns the closest iceberg which is facing threats"""
    friendly_icebergs = game.get_my_icebergs()
    bubble_sort_by_distance(friendly_icebergs, my_iceberg, game)

    for iceberg in friendly_icebergs:
        if is_iceberg_under_attack(iceberg, game):
            return iceberg


def get_peng_directed(my_iceberg, game):
    """Returns the number of penguins in an iceberg after all groups reach it"""
    all_peng_sent = total_friendly_peng_directed(my_iceberg, game)\
                    - total_enemy_peng_directed(my_iceberg, game)
    total_after_arrival = my_iceberg.penguin_amount + all_peng_sent

    return total_after_arrival


def get_peng_after_upgrade(my_iceberg, game):
    """Returns the amount of penguins an iceberg will have after upgrading"""
    after_upgrade = get_peng_directed(my_iceberg, game) - my_iceberg.upgrade_cost

    return after_upgrade


def pick_destination_by_func(my_iceberg, sort_by, game):
    """Generate a iceberg destination"""
    global mirvah
    # Sorts the netural icebergs by the given function (distance or penguin num)
    neutral_icebergs = game.get_neutral_icebergs()
    sort_by(neutral_icebergs, my_iceberg, game)

    # Sorts the enemy icebergs by the given function (distance or penguin num)
    enemy_icebergs = game.get_enemy_icebergs()
    sort_by(enemy_icebergs, my_iceberg, game)

    cur_peng_amount = my_iceberg.penguin_amount

    # Gets an ideal neutral iceberg
    neutral_destination = None
    for iceberg in neutral_icebergs:
        # Checks if we can conquer the iceberg
        if calculate_num_of_peng(iceberg, my_iceberg, game) < cur_peng_amount - mirvah:
            if not neutral_destination:
                neutral_destination = iceberg
            # If we already picked one iceberg, we pick the closest one
            elif (my_iceberg.get_turns_till_arrival(iceberg)
                  < my_iceberg.get_turns_till_arrival(neutral_destination)):
                neutral_destination = iceberg

    enemy_destination = None
    for iceberg in enemy_icebergs:
        # Checks if we can conquer the iceberg
        if calculate_num_of_peng(iceberg, my_iceberg, game) < cur_peng_amount - mirvah:
            if not enemy_destination:
                enemy_destination = iceberg
            # If we already picked one iceberg, we pick the closest one
            elif (my_iceberg.get_turns_till_arrival(iceberg)
                  < my_iceberg.get_turns_till_arrival(enemy_destination)):
                enemy_destination = iceberg

    # Picks the opposite iceberg if both are empty
    if enemy_destination is None:
        return neutral_destination
    if neutral_destination is None:
        return enemy_destination

    # If there is a fitting enemy and neutral iceberg, pick the closest one
    if (my_iceberg.get_turns_till_arrival(enemy_destination)
            > my_iceberg.get_turns_till_arrival(neutral_destination)):
        destination = neutral_destination
    else:
        destination = enemy_destination

    return destination


def total_friendly_peng_directed(destination, game):
    """Returns the total number of friendly penguins directed at the destination"""
    my_peng_headed = 0

    for group in game.get_my_penguin_groups():
        if group.destination == destination:
            my_peng_headed += group.penguin_amount
    return my_peng_headed


def total_enemy_peng_directed(destination, game):
    """Returns the total number of enemy penguins directed at the destination"""
    enemy_peng_headed = 0

    for group in game.get_enemy_penguin_groups():
        if group.destination == destination:
            enemy_peng_headed += group.penguin_amount
    return enemy_peng_headed


def calculate_num_of_peng(destination, origin, game):
    """Calculates the total number of penguins in a destination, by the time penguins from origin arrive"""
    distance = origin.get_turns_till_arrival(destination)
    # Get the amount of friendly penguins directed to the iceberg
    my_peng_headed = total_friendly_peng_directed(destination, game)
    # Get the amount of enemy penguins directed to the iceberg
    enemy_peng_headed = total_enemy_peng_directed(destination, game)
    # If it's friendly we want to subtract the enemy penguins
    if destination in game.get_my_icebergs():
        enemy_peng_headed = - enemy_peng_headed
    # If it's an enemy we want to subtract the friendly penguins
    elif destination in game.get_enemy_icebergs():
        my_peng_headed = - my_peng_headed

    else:
        distance = 0

    return (destination.penguin_amount + destination.penguins_per_turn * distance +
            my_peng_headed + enemy_peng_headed)


def bubble_sort_by_peng(icebergs, origin, game):
    """Sort an array by it's amount of penguins"""
    n = len(icebergs)

    for i in range(n):

        for j in range(0, n - i - 1):

            if calculate_num_of_peng(icebergs[j], origin, game) > \
                    calculate_num_of_peng(icebergs[j + 1], origin, game):
                icebergs[j], icebergs[j + 1] = icebergs[j + 1], icebergs[j]


def bubble_sort_by_distance(icebergs, origin, game):
    """Sort an array by it's distance to an iceberg"""
    n = len(icebergs)

    for i in range(n):

        for j in range(0, n - i - 1):

            if origin.get_turns_till_arrival(icebergs[j]) > origin.get_turns_till_arrival(
                    icebergs[j + 1]):
                icebergs[j], icebergs[j + 1] = icebergs[j + 1], icebergs[j]