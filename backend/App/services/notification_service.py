import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from flask import current_app
from bson import ObjectId
import requests
from app import mongo
from app.utils.mongo_utils import get_user_by_id, get_event_by_id

def send_email_notification(recipient, subject, body):
    """Send an email notification"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@communitypulse.com')
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Log the notification
        mongo.db.notifications.insert_one({
            'type': 'email',
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'sent_at': datetime.utcnow(),
            'status': 'pending'
        })
        
        # In development, just log instead of sending
        if current_app.config.get('TESTING', False):
            print(f"Email to {recipient}: {subject}")
            return True
        
        # Connect to server and send
        server = smtplib.SMTP(
            current_app.config.get('MAIL_SERVER', 'smtp.gmail.com'), 
            current_app.config.get('MAIL_PORT', 587)
        )
        server.starttls()
        server.login(
            current_app.config.get('MAIL_USERNAME', ''), 
            current_app.config.get('MAIL_PASSWORD', '')
        )
        server.send_message(msg)
        server.quit()
        
        # Update notification status
        mongo.db.notifications.update_one(
            {'recipient': recipient, 'subject': subject, 'status': 'pending'},
            {'$set': {'status': 'sent'}}
        )
        
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        
        # Update notification status
        mongo.db.notifications.update_one(
            {'recipient': recipient, 'subject': subject, 'status': 'pending'},
            {'$set': {'status': 'failed', 'error': str(e)}}
        )
        
        return False

def send_sms_notification(phone_number, message):
    """Send an SMS notification using a third-party service"""
    try:
        # Log the notification
        mongo.db.notifications.insert_one({
            'type': 'sms',
            'recipient': phone_number,
            'message': message,
            'sent_at': datetime.utcnow(),
            'status': 'pending'
        })
        
        # In development, just log instead of sending
        if current_app.config.get('TESTING', False):
            print(f"SMS to {phone_number}: {message}")
            return True
        
        # Example using a generic API service
        api_key = current_app.config.get('SMS_API_KEY', '')
        url = "https://api.smsservice.com/send"
        
        payload = {
            "api_key": api_key,
            "to": phone_number,
            "message": message
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Update notification status
        mongo.db.notifications.update_one(
            {'recipient': phone_number, 'message': message, 'status': 'pending'},
            {'$set': {'status': 'sent'}}
        )
        
        return True
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        
        # Update notification status
        mongo.db.notifications.update_one(
            {'recipient': phone_number, 'message': message, 'status': 'pending'},
            {'$set': {'status': 'failed', 'error': str(e)}}
        )
        
        return False

def schedule_event_reminder(event_id, user_id):
    """Schedule a reminder for an event"""
    # Find the interest
    interest = mongo.db.interests.find_one({
        "event_id": ObjectId(event_id),
        "user_id": ObjectId(user_id)
    })
    
    if not interest:
        return False
    
    # Find the event
    event = get_event_by_id(event_id)
    if not event:
        return False
    
    # Find the user
    user = get_user_by_id(user_id)
    if not user:
        return False
    
    # Schedule reminder
    reminder_date = event.get('start_date') - timedelta(days=1)
    
    # Create reminder record
    mongo.db.reminders.insert_one({
        'event_id': ObjectId(event_id),
        'user_id': ObjectId(user_id),
        'reminder_date': reminder_date,
        'status': 'scheduled',
        'created_at': datetime.utcnow()
    })
    
    return True

def send_event_update_notification(event_id, update_type):
    """Send notifications about event changes"""
    # Find the event
    event = get_event_by_id(event_id)
    if not event:
        return False
    
    # Find all interests for this event
    interests = list(mongo.db.interests.find({"event_id": ObjectId(event_id)}))
    
    for interest in interests:
        # Prepare message based on update type
        if update_type == 'update':
            subject = f"Event Update: {event.get('title', '')}"
            body = f"""
            Hello {interest.get('name', '')},
            
            There has been an update to the event "{event.get('title', '')}" that you expressed interest in.
            
            Updated event details:
            - Date: {event.get('start_date').strftime('%A, %B %d, %Y')}
            - Time: {event.get('start_date').strftime('%I:%M %p')} to {event.get('end_date').strftime('%I:%M %p')}
            - Location: {event.get('address', '')}
            - Category: {event.get('category', '')}
            - Description: {event.get('description', '')}
            
            Please check the event page for more details.
            
            Best regards,
            Community Pulse Team
            """
            
            sms_message = f"Update for event '{event.get('title', '')}': New date/time: {event.get('start_date').strftime('%b %d, %I:%M %p')}, New location: {event.get('address', '')}"
        
        elif update_type == 'cancel':
            subject = f"Event Cancelled: {event.get('title', '')}"
            body = f"""
            Hello {interest.get('name', '')},
            
            We regret to inform you that the event "{event.get('title', '')}" that you expressed interest in has been cancelled.
            
            We apologize for any inconvenience this may cause.
            
            Best regards,
            Community Pulse Team
            """
            
            sms_message = f"Event '{event.get('title', '')}' scheduled for {event.get('start_date').strftime('%b %d')} has been cancelled."
        
        # Send notifications based on available contact methods
        if interest.get('email'):
            send_email_notification(interest.get('email'), subject, body)
        
        if interest.get('phone'):
            send_sms_notification(interest.get('phone'), sms_message)
    
    return True

def send_event_status_notification(event_id, status, reason=None):
    """Send notification to organizer about event approval status"""
    # Find the event
    event = get_event_by_id(event_id)
    if not event:
        return False
    
    # Find the organizer
    organizer = get_user_by_id(str(event.get('user_id')))
    if not organizer:
        return False
    
    if status == 'approved':
        subject = f"Event Approved: {event.get('title', '')}"
        body = f"""
        Hello {organizer.get('full_name', '')},
        
        Great news! Your event "{event.get('title', '')}" has been approved and is now visible to the community.
        
        Event details:
        - Date: {event.get('start_date').strftime('%A, %B %d, %Y')}
        - Time: {event.get('start_date').strftime('%I:%M %p')} to {event.get('end_date').strftime('%I:%M %p')}
        - Location: {event.get('address', '')}
        
        Thank you for contributing to the community!
        
        Best regards,
        Community Pulse Team
        """
        
        sms_message = f"Good news! Your event '{event.get('title', '')}' has been approved and is now live on Community Pulse."
    
    elif status == 'rejected':
        subject = f"Event Not Approved: {event.get('title', '')}"
        body = f"""
        Hello {organizer.get('full_name', '')},
        
        We regret to inform you that your event "{event.get('title', '')}" has not been approved.
        
        Reason: {reason or 'The event does not meet our community guidelines.'}
        
        You can edit the event and resubmit it for approval, or contact us if you have any questions.
        
        Best regards,
        Community Pulse Team
        """
        
        sms_message = f"Your event '{event.get('title', '')}' was not approved. Reason: {reason or 'Does not meet guidelines'}. You can edit and resubmit."
    
    # Send notifications based on available contact methods
    if organizer.get('email'):
        send_email_notification(organizer.get('email'), subject, body)
    
    if organizer.get('phone'):
        send_sms_notification(organizer.get('phone'), sms_message)
    
    return True

def send_event_reminders():
    """Send reminders for events happening tomorrow"""
    # Get tomorrow's date
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow + timedelta(days=1), datetime.min.time())
    
    # Find events happening tomorrow
    tomorrow_events = list(mongo.db.events.find({
        "status": "approved",
        "start_date": {
            "$gte": tomorrow_start,
            "$lt": tomorrow_end
        }
    }))
    
    # Send reminders for each event
    for event in tomorrow_events:
        # Find all interests for this event
        interests = list(mongo.db.interests.find({"event_id": event['_id']}))
        
        for interest in interests:
            # Send reminder to each interested user
            subject = f"Reminder: {event.get('title', '')} is tomorrow!"
            body = f"""
            Hello {interest.get('name', '')},
            
            This is a reminder that you have expressed interest in attending "{event.get('title', '')}" tomorrow at {event.get('start_date').strftime('%I:%M %p')}.
            
            Event details:
            - Location: {event.get('address', '')}
            - Category: {event.get('category', '')}
            - Description: {event.get('description', '')}
            
            We look forward to seeing you there!
            
            Best regards,
            Community Pulse Team
            """
            
            # Send notifications based on available contact methods
            if interest.get('email'):
                send_email_notification(interest.get('email'), subject, body)
            
            if interest.get('phone'):
                sms_message = f"Reminder: {event.get('title', '')} is tomorrow at {event.get('start_date').strftime('%I:%M %p')} at {event.get('address', '')}."
                send_sms_notification(interest.get('phone'), sms_message)
    
    return True
