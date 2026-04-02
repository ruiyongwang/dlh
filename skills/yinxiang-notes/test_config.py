import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import evernote.edam.notestore.NoteStore as NoteStore
import thrift.transport.THttpClient as THttpClient
import thrift.protocol.TBinaryProtocol as TBinaryProtocol

token = os.getenv('EVERNOTE_TOKEN')
note_store_url = os.getenv('EVERNOTE_NOTESTORE_URL')

print("Token:", token)
print("URL:", note_store_url)
