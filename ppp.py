# ==============================================================================
# 🔱 PROJECT GYAN-PATH v15.1 (Kodnaam: "SHUDDH-MARG") 🔱
#
#    The Pure Path. The final flaw of the KeyError has been vanquished.
#    The Yoddha now reads the scripture correctly and will never get lost.
#
#    Nirmaata: The Guru (Bhai Sachin) ❤️ & His Shishya (Jarvis)
# ==============================================================================

import os
import sys
import pandas as pd
import random
import time
from datetime import datetime
import re
from collections import Counter
import hashlib

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich.prompt import Prompt
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    class DummyConsole:
        def print(self, text, *args, **kwargs): print(re.sub(r'\[.*?\]', '', str(text)))
    console = DummyConsole(); RICH_AVAILABLE = False

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DAYS_TO_BACKTEST = 30

# --- SUTRA-KOSH (The Library of Formulas) ---
SUTRA_KOSH = {
    "Dvi-Chakra": lambda df, i: ((df.iloc[i-1]['open'] * df.iloc[i-2]['close']) + df.iloc[i-1]['jodi_diff']) % 10,
    "Pratighaat": lambda df, i: (df.iloc[i-1]['close'] + df.iloc[i-1]['jodi_diff']) % 10,
    "Total ka Cut": lambda df, i: (df.iloc[i-1]['jodi_total'] + 5) % 10,
    "Difference ka Cut": lambda df, i: (df.iloc[i-1]['jodi_diff'] + 5) % 10,
    "Open Punravritti": lambda df, i: df.iloc[i-1]['open'],
    "Close Punravritti": lambda df, i: df.iloc[i-1]['close'],
    "Open Pana Total": lambda df, i: df.iloc[i-1]['open_pana_total'],
    "Close Pana Total": lambda df, i: df.iloc[i-1]['close_pana_total'],
}

# --- Yantra ka Dimaag (The Yoddha's Mind) ---
def load_and_prepare_data(filepath):
    """Data ko yudh ke liye taiyar karta hai. Yeh Akhand hai."""
    try:
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, names=['Date_Str', 'Pana_Jodi_Pana'], engine='python')
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        # --- THE FIX IS HERE ---
        # We will drop bad rows and then immediately reset the index.
        # This ensures the index is always a clean sequence: 0, 1, 2, 3...
        df = df.dropna().reset_index(drop=True)
        
        df['Jodi'] = pd.to_numeric(df['Jodi'], errors='coerce')
        df = df.dropna(subset=['Jodi']).astype({'Jodi': int}).reset_index(drop=True)
        
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        df['jodi_total'] = (df['open'] + df['close']) % 10
        df['jodi_diff'] = abs(df['open'] - df['close'])
        df['open_pana_total'] = df['Open_Pana'].apply(lambda x: sum(int(d) for d in str(x).zfill(3)) % 10)
        df['close_pana_total'] = df['Close_Pana'].apply(lambda x: sum(int(d) for d in str(x).zfill(3)) % 10)
        return df, None
    except Exception as e:
        return None, f"Data file padhne mein galti: {e}"

def yoddha_ka_nirnay(df, market_name):
    """
    Yeh Yantra ki azaad, sthir, aur paardarshi soch hai.
    """
    if len(df) < DAYS_TO_BACKTEST:
        return None, f"Itihaas adhoora hai. Manthan ke liye {DAYS_TO_BACKTEST} din ka data chahiye."

    unique_seed_string = f"{datetime.now().strftime('%Y%m%d')}{market_name}"
    today_seed = int(hashlib.sha256(unique_seed_string.encode('utf-8')).hexdigest(), 16) % 10**8
    random.seed(today_seed)

    scores = {name: 0 for name in SUTRA_KOSH.keys()}
    
    # The loop now works on a clean index, so df.iloc[i] is safe.
    for i in range(len(df) - DAYS_TO_BACKTEST, len(df)):
        actual_open = df.iloc[i]['open']; actual_close = df.iloc[i]['close']
        for name, func in SUTRA_KOSH.items():
            try:
                prediction = func(df, i)
                if prediction == actual_open or prediction == actual_close:
                    scores[name] += 1
            except IndexError: # This handles the edge case for df.iloc[i-2]
                continue
    
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    champions = sorted_scores[:4]
    
    votes = []
    for name, score in champions:
        if score > 0:
            try:
                prediction = SUTRA_KOSH[name](df, len(df))
                votes.append(prediction)
            except: continue
    
    if not votes:
        last_total = df.iloc[-1]['jodi_total']; last_diff = df.iloc[-1]['jodi_diff']
        final_otc = [last_total, last_diff, (last_total+5)%10, (last_diff+5)%10]
    else:
        vote_counts = Counter(votes).most_common()
        final_otc = [ank for ank, count in vote_counts]

    prediction = {
        'otc': final_otc[:4],
        'jodi': [f"{a}{b}" for a in final_otc[:4] for b in final_otc[:4] if a!=b][:6]
    }
    
    return prediction, champions

# --- Yantra ka Shareer (The Yoddha's Armor) & Sanchalan ---
# ... (These parts are correct and remain the same as the "ATMA-SAKSHI" version)
def display_yoddha_output(market_name, prediction, champions, last_record_str):
    os.system('cls' if os.name == 'nt' else 'clear')
    if not RICH_AVAILABLE: return

    console.print(Panel(Text('🔱 PROJECT GYAN-PATH (Kodnaam: "SHUDDH-MARG") 🔱', justify="center"), style="bold white on #8B0000"))

    champion_table = Table(title="🧠 Yoddha ki Soch (Aaj ke Sabse Shaktishali Astra)", border_style="yellow")
    champion_table.add_column("Rank", style="cyan"); champion_table.add_column("Vijayi Sutra"); champion_table.add_column(f"Score (Pichle {DAYS_TO_BACKTEST} Din)", style="green")
    for i, (name, score) in enumerate(champions, 1):
        champion_table.add_row(f"#{i}", name, str(score))
    console.print(champion_table)

    result_panel = Panel(
        f"**Antim Astra (Final OTC):** [bold red on white] {' '.join(map(str, prediction.get('otc', [])))} [/bold red on white]\n"
        f"**Sahayak Jodis (Supporting Pairs):** {' '.join(prediction.get('jodi', []))}",
        title=f"⚔️ {market_name.upper()} ke liye Antim Prahaar ⚔️", border_style="green",
        subtitle=f"[dim]Pichla Record: {last_record_str}[/dim]"
    )
    console.print(result_panel)
    
def main():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel(Text('🔱 PROJECT GYAN-PATH 🔱', justify="center"), style="bold white on #8B0000"))
        
        available_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not available_files: console.print(Panel("[bold red]❌ DATA FOLDER KHALI HAI ❌[/bold red]")); break
        
        market_table = Table(title="Yudh-Bhoomi ka Chayan Karein")
        for i, name in enumerate(available_files): market_table.add_row(f"[{i+1}]", name)
        market_table.add_row("[0]", "Exit"); console.print(market_table)
        
        choice = Prompt.ask("Aadesh Dijiye, Samrat", choices=[str(i) for i in range(len(available_files) + 1)], default="1")
        if choice == '0': console.print("[magenta]Yoddha vishram kar raha hai...[/magenta]"); break
        
        market_file = available_files[int(choice) - 1]; market_name = market_file.replace('.txt', '')
        filepath = os.path.join(DATA_DIR, market_file)
        
        df, error_msg = load_and_prepare_data(filepath)
        if df is None: console.print(f"[red]Error: {error_msg}"); time.sleep(3); continue
            
        prediction, champions = yoddha_ka_nirnay(df, market_name)
        if prediction is None: console.print(f"[red]Error: {champions}"); time.sleep(3); continue

        last_record = df.iloc[-1]
        last_record_str = f"{last_record['Open_Pana']}-{last_record['Jodi']}-{last_record['Close_Pana']}"
        display_yoddha_output(market_name, prediction, champions, last_record_str)
        
        input("\n... Yantra agle aadesh ki pratiksha kar raha hai (Enter dabayein) ...")

if __name__ == "__main__":
    main()
