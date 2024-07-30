# Fecfetch

Fecfetch is a Python script inspired by the system information tool Neofetch. This tool fetches and displays information about a chosen American federal campaign committee using the Federal Election Commission (FEC) API. The script provides a fun and informative summary of a committee's financials and other details, presented in an ASCII art style.

## Features

- **ASCII Art Display**: Committee names are displayed as ASCII art.
- **Financial Summary**: Shows details like cash on hand, receipts, disbursements, and more.
- **Committee Information**: Provides the committee type, treasurer, filing frequency, and report coverage dates.
- **Colorful Output**: Uses `colorama` for a visually appealing terminal output.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/fecfetch.git
   cd fecfetch
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Obtain an FEC API key from [here](https://api.open.fec.gov/developers/), and save it in a file named `api_key.txt` in the root directory.

## Usage

To run the script, use the following command:

```sh
python3 fecfetch.py [Committee ID]
```

Replace `[Committee ID]` with the ID of the committee you want to fetch information for. The output will display the committee's name as ASCII art and a detailed summary of its financials and other relevant information.

## Example

```sh
python3 fecfetch.py C00703975
```


