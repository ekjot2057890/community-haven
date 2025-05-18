from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
import logging
from app import mongo
from app.services.notification_service import send_event_reminders

logger = logging.getLogger(__name__)

def check_and_send_reminders():
    """Check for scheduled reminders and send them"""
    logger.info("Running scheduled task: check_and_send_reminders")
    send_event_reminders()

def cleanup_old_events():
    """Archive events that are more than 30 days old"""
    logger.info("Running scheduled task: cleanup_old_events")
    
    # Get date 30 days ago
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Find old events
    result = mongo.db.events.update_many(
        {"end_date": {"$lt": thirty_days_ago}, "status": {"$ne": "archived"}},
        {"$set": {"status": "archived"}}
    )
    
    logger.info(f"Archived {result.modified_count} old events")

def init_scheduler(app):
    """Initialize the background task scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule daily job to check for upcoming events and send reminders
    # Run at midnight every day
    scheduler.add_job(
        func=lambda: app.app_context().push() and check_and_send_reminders(),
        trigger='cron',
        hour=0,
        minute=0,
        id='check_and_send_reminders'
    )
    
    # Schedule weekly job to clean up old events
    # Run every Sunday at 1:00 AM
    scheduler.add_job(
        func=lambda: app.app_context().push() and cleanup_old_events(),
        trigger='cron',
        day_of_week='sun',
        hour=1,
        minute=0,
        id='cleanup_old_events'
    )
    
    # Start the scheduler
    scheduler.start()
    
    logger.info("Background scheduler initialized with tasks")
    
    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())
