#!/usr/bin/env python3
"""
Gmail Spam Email Auto-Deletion Script

This script connects to Gmail via IMAP and deletes all emails in the Spam folder.
It can be scheduled to run periodically to keep your spam folder clean.

Usage:
    python delete_spam_emails.py

Requirements:
    - Python 3.6+
    - Gmail account with IMAP enabled
    - App password for Gmail (if 2FA is enabled)
"""

import imaplib
import email
import time
import logging
import os
from datetime import datetime

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"spam_deletion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Gmail account settings
GMAIL_USERNAME = "souzasoftm@gmail.com"
GMAIL_PASSWORD = "xmxsgunchbfavftq"  # App password, not your regular Gmail password
GMAIL_IMAP_SERVER = "imap.gmail.com"
GMAIL_IMAP_PORT = 993
SPAM_FOLDER = "[Gmail]/Spam"
BATCH_SIZE = 5  # Number of emails to process in each batch

def connect_to_gmail():
    """Connect to Gmail's IMAP server and login."""
    try:
        # Connect to the IMAP server
        logging.info(f"Connecting to {GMAIL_IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER, GMAIL_IMAP_PORT)
        
        # Login to the account
        logging.info(f"Logging in as {GMAIL_USERNAME}...")
        mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        logging.info("Login successful")
        
        return mail
    except Exception as e:
        logging.error(f"Error connecting to Gmail: {e}")
        raise

def delete_spam_emails(mail):
    """Delete all emails in the Spam folder."""
    try:
        # Select the Spam folder
        logging.info(f"Selecting folder: {SPAM_FOLDER}")
        status, messages = mail.select(SPAM_FOLDER, readonly=False)
        
        if status != 'OK':
            logging.error(f"Error selecting {SPAM_FOLDER}: {messages}")
            return 0
        
        # Get the number of emails in the Spam folder
        status, messages = mail.search(None, 'ALL')
        
        if status != 'OK':
            logging.error(f"Error searching for emails: {messages}")
            return 0
        
        # Get the list of email IDs
        email_ids = messages[0].split()
        
        if not email_ids:
            logging.info("No emails found in Spam folder")
            return 0
        
        total_emails = len(email_ids)
        logging.info(f"Found {total_emails} emails in Spam folder")
        
        # Process emails in batches
        deleted_count = 0
        
        for i in range(0, total_emails, BATCH_SIZE):
            batch = email_ids[i:i+BATCH_SIZE]
            batch_size = len(batch)
            
            logging.info(f"Processing batch {i//BATCH_SIZE + 1} ({batch_size} emails)...")
            
            # Mark emails for deletion
            for email_id in batch:
                try:
                    mail.store(email_id, '+FLAGS', '\\Deleted')
                    deleted_count += 1
                    logging.debug(f"Marked email {email_id.decode()} for deletion")
                except Exception as e:
                    logging.error(f"Error marking email {email_id.decode()} for deletion: {e}")
            
            # Permanently delete emails marked for deletion
            mail.expunge()
            
            # Log progress
            progress = min(100, (i + batch_size) / total_emails * 100)
            logging.info(f"Progress: {progress:.1f}% ({i + batch_size}/{total_emails})")
        
        logging.info(f"Successfully deleted {deleted_count} out of {total_emails} emails from Spam folder")
        return deleted_count
    
    except Exception as e:
        logging.error(f"Error deleting spam emails: {e}")
        return 0

def main():
    """Main function to delete spam emails."""
    logging.info("=== Gmail Spam Email Deletion Tool ===")
    start_time = time.time()
    
    try:
        # Connect to Gmail
        mail = connect_to_gmail()
        
        # Delete spam emails
        deleted_count = delete_spam_emails(mail)
        
        # Logout
        mail.logout()
        logging.info("Logged out successfully")
        
        # Log summary
        elapsed_time = time.time() - start_time
        logging.info(f"=== Summary ===")
        logging.info(f"Total emails deleted: {deleted_count}")
        logging.info(f"Total time: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        
    logging.info("Script execution completed")

if __name__ == "__main__":
    main()
