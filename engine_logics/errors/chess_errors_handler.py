
def Error_handler_notation_general(notation, error):
    if len(notation) != 4:
        raise error('Error: Something seems to be wrong, check your import message')
    turn= notation[1]
    if turn != 'w' and turn != 'b':
        raise error('Error: Something is wrong, i cant see whose turn it is')
    castle_availability= notation[2]
    if castle_availability != '-' and not ('Q' in castle_availability or 'K' in castle_availability or 'q' in castle_availability or 'k' in castle_availability):
        raise error('Error: Cant set up castled pieces')
    en_peassant_check= notation[3]
    if len(en_peassant_check) > 2 or en_peassant_check[0] == '-' and len(en_peassant_check) > 1 or len(en_peassant_check) == 2 and (en_peassant_check[1] != '3' and en_peassant_check[1] != '6'):
        raise error('Error: There was a mistake setting up the en_peassant')

def Error_handler_pieces_implementation(rows, error):
    if len(rows) != 8:
        raise error("Error: It seems there is an extra row, or a missing one")
    for row in rows:
        total_sum= 0
        for letter in row:
            if letter.isnumeric(): total_sum+= int(letter)
            else: total_sum+= 1
        if total_sum != 8:
            raise error('Error: One of your rows has missing or extra pieces')
    return

