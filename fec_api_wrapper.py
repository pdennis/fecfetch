import requests
from colorama import init, Fore, Style
from datetime import datetime
from art import text2art
import sys

init(autoreset=True)

def get_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("API key file not found. Please ensure 'api_key.txt' exists with your API key.")
        exit(1)

def get_totals(api_key, committee_id, **kwargs):
    base_url = "https://api.open.fec.gov/v1/committee/{committee_id}/totals/"
    url = base_url.format(committee_id=committee_id)
    params = {
        "api_key": api_key,
        **kwargs
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def format_number(number):
    return f"${number:,.2f}" if isinstance(number, (int, float)) else number

def format_date(date_str):
    """Extract the date portion from a datetime string."""
    if date_str:
        return date_str.split('T')[0]
    return 'N/A'

def print_formatted(data):
    if data['results']:
        item = data['results'][0]

        # Displaying the PAC name as ASCII art for each word or combined words
        pac_name = item.get('committee_name', 'N/A')
        pac_name_words = pac_name.split()
        longest_word_length = max(len(word) for word in pac_name_words)

        # Combine words if their combined length does not exceed the longest word length
        combined_words = []
        i = 0
        while i < len(pac_name_words):
            current_word = pac_name_words[i]
            next_word = pac_name_words[i + 1] if i + 1 < len(pac_name_words) else ''
            combined_length = len(current_word) + len(next_word) + 1  # +1 for space

            if combined_length <= longest_word_length:
                combined_words.append(current_word + ' ' + next_word)
                i += 2
            else:
                combined_words.append(current_word)
                i += 1

        # Print ASCII art for each combined word
        for combined_word in combined_words:
            word_art = text2art(combined_word, font='tarty2')  # You can choose different fonts
            print(word_art)

        # Print the committee details
        print(f"{Fore.GREEN}{item.get('committee_type_full', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Treasurer:{Style.RESET_ALL} {Fore.CYAN}{item.get('treasurer_name', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}---------------------------------{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Scope{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Filing Frequency:{Style.RESET_ALL} {Fore.CYAN}{item.get('filing_frequency_full', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Last Report Type:{Style.RESET_ALL} {Fore.CYAN}{item.get('last_report_type_full', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Coverage Start Date:{Style.RESET_ALL} {Fore.CYAN}{format_date(item.get('coverage_start_date'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Coverage End Date:{Style.RESET_ALL} {Fore.CYAN}{format_date(item.get('coverage_end_date'))}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Finances{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Cash On Hand Beginning Period:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('cash_on_hand_beginning_period', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Last Cash On Hand End Period:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('last_cash_on_hand_end_period', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Receipts:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('receipts', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Disbursements:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('disbursements', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Last Debts Owed By Committee:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('last_debts_owed_by_committee', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Last Debts Owed To Committee:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('last_debts_owed_to_committee', 'N/A'))}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Independent Expenditures:{Style.RESET_ALL} {Fore.CYAN}{format_number(item.get('independent_expenditures', 'N/A'))}{Style.RESET_ALL}")


def main():
    api_key = get_api_key()
    committee_id = sys.argv[1]
    
    current_year = datetime.now().year
    cycle = current_year if current_year % 2 == 0 else current_year + 1

    filters = {
        "year": [current_year],
        "cycle": [cycle],
        "is_amended": True,
        "per_page": 20,
        "page": 1
    }

    data = get_totals(api_key, committee_id, **filters)
    print_formatted(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fec_api_wrapper.py [Committee ID]")
        sys.exit(1)
    main()
