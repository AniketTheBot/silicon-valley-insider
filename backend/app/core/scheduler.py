from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scraper import fetch_latest_news
from app.services.extractor import extract_graph_from_text
from app.services.graph_store import save_graph_to_neo4j

# Create the scheduler instance
scheduler = AsyncIOScheduler()

async def scheduled_scraping_job():
    """
    This function runs automatically.
    It does the full ETL pipeline: Scrape -> Extract -> Save.
    """
    print("⏰ Cron Job Started: Fetching News...")
    
    try:
        # 1. Scrape
        articles = fetch_latest_news()
        if not articles:
            print("⚠️ No articles found.")
            return

        print(f"📰 Found {len(articles)} articles. Processing...")

        # 2. Process each article
        for article in articles:
            full_text = f"{article['title']}. {article['summary']}"
            
            # Extract
            print(f"🧠 Extracting: {article['title']}...")
            graph_data = extract_graph_from_text(full_text)
            
            # Save
            if graph_data:
                save_graph_to_neo4j(graph_data)
            else:
                print("❌ Extraction failed for this article.")
                
        print("✅ Cron Job Finished successfully.")
        
    except Exception as e:
        print(f"❌ Cron Job Failed: {e}")

def start_scheduler():
    """
    Starts the scheduler loop.
    """
    # Add the job to run every 6 hours
    # For testing, you can change 'hours=6' to 'seconds=60' to see it run every minute!
    scheduler.add_job(scheduled_scraping_job, "interval", hours=6)
    scheduler.start()
    print("⏳ Scheduler started. Scraper will run every 6 hours.")