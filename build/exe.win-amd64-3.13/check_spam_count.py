#!/usr/bin/env python3
"""
Gmail Spam Folder Checker

This script connects to Gmail via IMAP and checks the number of emails in the Spam folder.
It's a simpler alternative to the deletion script that can be used to monitor your spam folder.

Usage:
    python check_spam_count.py
"""

import imaplib
import time
import logging
import sys
import credential_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Obter data e hora atual para o log
log_timestamp = time.strftime('%Y%m%d_%H%M%S')

# Gmail account settings
GMAIL_IMAP_SERVER = "imap.gmail.com"
SPAM_FOLDER = "[Gmail]/Spam"

def check_spam_with_credentials(username, password):
    """
    Connect to Gmail and check the number of emails in the Spam folder using provided credentials.

    Args:
        username (str): Gmail email address
        password (str): Gmail app password
    """
    try:
        # Start timer
        start_time = time.time()

        # Connect to Gmail
        logging.info(f"Connecting to {GMAIL_IMAP_SERVER}...")
        print(f"Connecting to {GMAIL_IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)

        # Login
        logging.info(f"Logging in as {username}...")
        print(f"Logging in as {username}...")
        mail.login(username, password)
        logging.info("Login successful")
        print("Login successful")

        # Select the Spam folder
        logging.info(f"Selecting folder: {SPAM_FOLDER}")
        print(f"Selecting folder: {SPAM_FOLDER}")
        status, messages = mail.select(SPAM_FOLDER, readonly=True)

        if status != 'OK':
            logging.error(f"Error selecting {SPAM_FOLDER}: {messages}")
            print(f"Error selecting {SPAM_FOLDER}: {messages}")
            mail.logout()
            return

        # Get the number of emails
        status, messages = mail.search(None, 'ALL')

        if status != 'OK':
            logging.error(f"Error searching for emails: {messages}")
            print(f"Error searching for emails: {messages}")
            mail.logout()
            return

        # Count emails
        email_ids = messages[0].split()
        email_count = len(email_ids)

        # Log the result
        logging.info(f"Number of emails in {SPAM_FOLDER}: {email_count}")
        print(f"Number of emails in {SPAM_FOLDER}: {email_count}")

        # If there are emails, show some information about the most recent ones
        if email_count > 0:
            # Show info for up to 5 most recent emails
            num_to_show = min(5, email_count)
            logging.info(f"\nShowing information for the {num_to_show} most recent spam emails:")
            print(f"\nShowing information for the {num_to_show} most recent spam emails:")

            # Get the most recent email IDs (they are at the end of the list)
            recent_ids = email_ids[-num_to_show:]

            for email_id in reversed(recent_ids):
                # Fetch email headers
                status, data = mail.fetch(email_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')

                if status != 'OK':
                    logging.error(f"Error fetching email {email_id.decode()}")
                    print(f"Error fetching email {email_id.decode()}")
                    continue

                # Parse headers
                header_data = data[0][1].decode('utf-8', errors='replace')

                # Extract basic information
                from_line = next((line for line in header_data.split('\r\n') if line.startswith('From: ')), 'From: Unknown')
                subject_line = next((line for line in header_data.split('\r\n') if line.startswith('Subject: ')), 'Subject: No Subject')
                date_line = next((line for line in header_data.split('\r\n') if line.startswith('Date: ')), 'Date: Unknown')

                # Log email info
                logging.info(f"ID: {email_id.decode()}")
                logging.info(f"{from_line}")
                logging.info(f"{subject_line}")
                logging.info(f"{date_line}")
                logging.info("-" * 50)

                print(f"ID: {email_id.decode()}")
                print(f"{from_line}")
                print(f"{subject_line}")
                print(f"{date_line}")
                print("-" * 50)

        # Logout
        mail.logout()
        logging.info("Logged out successfully")
        print("Logged out successfully")

        # Log execution time
        elapsed_time = time.time() - start_time
        logging.info(f"Script execution time: {elapsed_time:.2f} seconds")
        print(f"Script execution time: {elapsed_time:.2f} seconds")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        raise

def check_spam_folder():
    """Connect to Gmail and check the number of emails in the Spam folder."""

    # Obter credenciais do Gmail usando o gerenciador de credenciais
    print("\nPor favor, forneça suas credenciais do Gmail:")
    username, password = credential_prompt.get_credentials()

    # Usar a função com as credenciais obtidas
    check_spam_with_credentials(username, password)

if __name__ == "__main__":
    logging.info("=== Gmail Spam Folder Checker ===")
    check_spam_folder()
    logging.info("Script execution completed")
