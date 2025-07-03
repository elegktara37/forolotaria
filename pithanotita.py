# Gives back the possibility of winning depending on the prize

from forolotaria import lottery_numbers

# Prize tier structure
prize_tiers = {
    "50,000€": 1,
    "20,000€": 5,
    "5,000€": 50,
    "1,000€": 500
}

# Total number of lottery tickets is the largest number extracted
total_tickets = max(int(num.replace(" ", "")) for num in lottery_numbers)

# Get how many tickets the user owns
while True:
    try:
        my_tickets = int(input("How many lottery tickets do you own? "))
        if my_tickets <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("That doesn't look like a valid number. Try again.")

print(f"\n📊 Total registered tickets: {total_tickets:,}")
print(f"🎟️  Your tickets: {my_tickets:,}\n")

# Calculate and display odds per tier
print("💰 Your chances of winning by prize tier:\n")
for prize, winners in prize_tiers.items():
    chance = (winners * my_tickets / total_tickets) * 100
    print(f"  • {prize:>7}: {chance:.6f}% chance")
