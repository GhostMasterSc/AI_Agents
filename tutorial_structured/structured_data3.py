import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import logfire
from dotenv import load_dotenv
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
import json
import csv

load_dotenv()
logfire.configure()

model = OpenAIModel(model_name=os.getenv("LLM_MODEL_OPENAI"),
                    base_url=os.getenv("BASE_URL"),
                    api_key=os.getenv("OPENROUTER_API_KEY")
                    )

class Player(BaseModel):
    name: str
    rostered: float
    date: str
    team: str
    position: str

class PlayerList(BaseModel):
    players: list[Player]

async def scrape_espn_data() -> str:
    browser = await launch(headless=True)
    try:
        # Setup page with stealth
        page = await browser.newPage()
        await stealth(page)
        
        # Set headers to look more like a real browser
        await page.setExtraHTTPHeaders({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
        })

        # Navigate to ESPN
        url = "https://fantasy.espn.com/basketball/livedraftresults?leagueId=190"
        logfire.info("Attempting to access URL: {url}", url=url)
        
        await page.goto(url, {'waitUntil': 'networkidle0'})
        
        # Wait for player data to be visible
        await page.waitForSelector('.player-row, .Table__TR', {'timeout': 20000})
        
        # Get the page content
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find player elements
        players = soup.select('.player-row, .Table__TR')
        
        if not players:
            logfire.error("No player data found")
            return ""
            
        # Extract player data
        player_texts = [player.get_text(strip=True) for player in players if player.get_text(strip=True)]
        
        if not player_texts:
            logfire.error("No player text data found")
            return ""
            
        return "\n".join(player_texts)
        
    except Exception as e:
        logfire.error("Error during scraping: {error}", error=str(e))
        return ""
    finally:
        await browser.close()

# Create agent with specific system prompt for parsing ESPN fantasy data
agent = Agent(
    model=model,
    result_type=PlayerList,
    system_prompt="""You are an NBA fantasy expert who extracts player information from ESPN fantasy data.
    Given raw text data from ESPN fantasy basketball, extract information for ALL players in the data.
    For each player, provide:
    - Player name
    - Team
    - Position
    - Roster percentage
    - Current date
    Return the data as a list of players according to the PlayerList model structure."""
)

def save_raw_data(data: str, filename: str = "data/raw_espn_data.csv"):
    """Save raw scraped data to a CSV file"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Split the data into rows
    rows = data.split('\n')
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Raw Data', 'Timestamp'])
        # Write each row with timestamp
        for row in rows:
            if row.strip():  # Only write non-empty rows
                writer.writerow([row, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
    logfire.info(f"Raw data saved to {filename}")

def save_parsed_data(player_data: PlayerList, filename: str = "data/player_data.csv"):
    """Save parsed player data to a CSV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "team", "position", "rostered", "date", "timestamp"
        ])
        
        if not file_exists:
            writer.writeheader()
        
        # Write all players
        for player in player_data.players:
            writer.writerow({
                "name": player.name,
                "team": player.team,
                "position": player.position,
                "rostered": player.rostered,
                "date": player.date,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    logfire.info(f"Parsed data appended to {filename}")

def main():
    # Create new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Scrape the data
        raw_data = loop.run_until_complete(scrape_espn_data())
        if not raw_data:
            logfire.error("Failed to fetch ESPN data")
            return

        # Save raw data as CSV
        save_raw_data(raw_data, "data/raw_espn_data.csv")

        # Parse the data using the agent
        result = agent.run_sync(f"Parse this ESPN fantasy basketball data: {raw_data}")
        
        # Save parsed data as CSV
        save_parsed_data(result.data)
        
        # Log the results
        logfire.notice("Player data parsed:", result=result.data)
        logfire.info("Player name: {name}", name=result.data.players[0].name)
        logfire.info("Team: {team}", team=result.data.players[0].team)
        logfire.info("Position: {position}", position=result.data.players[0].position)
        logfire.info("Rostered: {rostered}%", rostered=result.data.players[0].rostered)
        logfire.info("Date: {date}", date=result.data.players[0].date)
    finally:
        loop.close()

if __name__ == "__main__":
    main()


