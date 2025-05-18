import os
from datetime import timedelta

class Config:
    """Application configuration class"""
    # Basic configuration
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # MongoDB configuration
    MONGO_URI = 'mongodb://localhost:27017/community_pulse'
    
    # JWT configuration
    JWT_SECRET_KEY = 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = None  # Set your email username here
    MAIL_PASSWORD = None  # Set your email password here
    MAIL_DEFAULT_SENDER = 'noreply@communitypulse.com'
    
    # Gmail API configuration
    GMAIL_CLIENT_ID = '108536145625-km774t541uevjuas2ur7qdcafld8vqr4.apps.googleusercontent.com'
    GMAIL_CLIENT_SECRET = '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'
    GMAIL_PROJECT_ID = 'newnew-460207'
    GMAIL_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    GMAIL_TOKEN_URI = 'https://oauth2.googleapis.com/token'
    GMAIL_AUTH_PROVIDER_CERT_URL = 'https://www.googleapis.com/oauth2/v1/certs'
    GMAIL_REDIRECT_URIS = 'http://localhost'
    GMAIL_TOKEN_FILE = 'token.json'
    
    # Twilio configuration for SMS
    TWILIO_ACCOUNT_SID = 'ACcde58c008e08783fdedb3a53b9cf83f8'
    TWILIO_AUTH_TOKEN = '4f88cc1172fdaa4e3c4b4e9acff81aca'
    TWILIO_PHONE_NUMBER = '+19128096407'
    
    # Twilio configuration for WhatsApp
    TWILIO_WHATSAPP_NUMBER = '+19128096407'
    
    # Geocoding API configuration
    GEOCODING_API_KEY = 'b058fb8b6ed7419e8ad595db58e22a4f'
