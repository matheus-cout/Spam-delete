#!/usr/bin/env python3
"""
Gmail Spam Email Deletion Tool
This script connects to Gmail via IMAP and deletes all emails in the Spam folder.
It processes emails in small batches to avoid timeouts.
"""

import imaplib
import socket
import time
import sys
import traceback

# Set a timeout for socket operations
socket.setdefaulttimeout(60)  # 60 seconds timeout

def delete_spam_emails_in_batches(mail, batch_size=10):
    """
    Delete emails in the Spam folder in small batches.

    Args:
        mail (imaplib.IMAP4_SSL): IMAP connection object
        batch_size (int): Number of emails to process in each batch

    Returns:
        int: Number of emails deleted
    """
    # Select the Spam folder
    spam_folder = "[Gmail]/Spam"
    print(f"Selecting folder: {spam_folder}")
    status, _ = mail.select(spam_folder)

    if status != 'OK':
        print(f"Error: Could not select {spam_folder}")
        return 0

    print(f"Successfully selected {spam_folder}")

    # Search for all emails in the Spam folder
    print("Searching for emails...")
    status, data = mail.search(None, 'ALL')

    if status != 'OK':
        print(f"Error: Could not search emails in {spam_folder}")
        return 0

    # Get the list of email IDs
    email_ids = data[0].split()

    if not email_ids:
        print(f"No emails found in {spam_folder}")
        return 0

    total_emails = len(email_ids)
    print(f"Found {total_emails} emails in {spam_folder}")

    # Process emails in batches
    deleted_count = 0
    batch_number = 1

    for i in range(0, total_emails, batch_size):
        batch_ids = email_ids[i:i+batch_size]
        batch_count = len(batch_ids)

        print(f"\nProcessing batch {batch_number} ({batch_count} emails)...")

        try:
            # Mark emails in this batch for deletion
            for email_id in batch_ids:
                try:
                    print(f"  Marking email {email_id.decode()} for deletion...")
                    status, data = mail.store(email_id, '+FLAGS', '\\Deleted')
                    if status == 'OK':
                        deleted_count += 1
                    else:
                        print(f"  Failed to mark email {email_id.decode()} for deletion")
                except Exception as e:
                    print(f"  Error marking email {email_id.decode()}: {e}")

            # Expunge after each batch
            print(f"  Expunging batch {batch_number}...")
            mail.expunge()
            print(f"  Batch {batch_number} processed successfully")

        except Exception as e:
            print(f"Error processing batch {batch_number}: {e}")
            traceback.print_exc()

        batch_number += 1

        # Print progress
        progress = (i + batch_count) / total_emails * 100
        print(f"Progress: {progress:.1f}% ({i + batch_count}/{total_emails})")

    print(f"\nSuccessfully deleted {deleted_count} out of {total_emails} emails from {spam_folder}")
    return deleted_count

def main():
    print("=== Gmail Spam Email Deletion Tool ===")
    print("This tool will delete all emails in your Gmail Spam folder.")
    print("Press Ctrl+C at any time to stop the process.\n")

    # Gmail credentials
    username = "souzasoftm@gmail.com"
    password = "xmxsgunchbfavftq"  # This is an app password, not the actual Gmail password

    try:
        # Connect to Gmail's IMAP server
        start_time = time.time()
        print(f"Connecting to Gmail IMAP server...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        print(f"Connected to imap.gmail.com ({time.time() - start_time:.2f}s)")

        # Login to account
        print(f"Logging in as {username}...")
        mail.login(username, password)
        print(f"Successfully logged in ({time.time() - start_time:.2f}s)")

        # Delete spam emails in batches
        deleted_count = delete_spam_emails_in_batches(mail, batch_size=5)

        # Logout
        print("Logging out...")
        mail.logout()
        print("Logged out successfully")

        # Print summary
        print("\n=== Summary ===")
        print(f"Total emails deleted: {deleted_count}")
        print(f"Total time: {time.time() - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        try:
            mail.logout()
            print("Logged out successfully")
        except:
            pass
    except socket.timeout:
        print("Error: Connection timed out. The operation took too long to complete.")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
