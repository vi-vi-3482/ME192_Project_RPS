
# def match_card(read_card):
#     to_play = None  # default value in case reading fails, this can be used to raise an error later
#     match read_card:
#         case "rock_card":
#             to_play = "paper_block"
#         case "paper_card":
#             to_play = "scissor_block"
#         case "scissors_card":
#             to_play = "rock_block"
#         case _:
#             print("Invalid input")
#
#     print(f"The read card is {read_card}. \nThe block to play is {to_play}.")
#
#     return to_play

def match_card(read_card):
    to_play = None  # default value in case reading fails, this can be used to raise an error later
    if read_card == "rock_card":
        to_play = "paper_block"
    elif read_card == "paper_card":
        to_play = "scissor_block"
    elif read_card == "scissor_card":
        to_play = "rock_block"
    else:
        print("Invalid input")

    print(f"The read card is {read_card}. \nThe block to play is {to_play}.")

    return to_play

def main():
    match_card("scissors_card")

if __name__ == "__main__":
    main()