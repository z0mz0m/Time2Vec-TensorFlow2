import traceback
import logging
import sys
import threading
import sbe
import datetime
import websocket
import rel

# Set up logging once
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sbe_parser.log',
    filemode='a'
)
logger = logging.getLogger('sbe_parser')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Global schema and error tracking
_schema = None
_schema_lock = threading.RLock()
_error_count = 0
_error_types = {}


def load_schema():
    """Load the SBE schema (if not already loaded)"""
    global _schema

    with _schema_lock:
        if _schema is not None:
            return _schema

        try:
            with open('stream_1_0.xml', 'r') as f:
                _schema = sbe.Schema.parse(f)
            logger.info("SBE schema loaded successfully")
            return _schema
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Failed to load SBE schema: {e}")
            logger.error(f"Traceback: {error_trace}")
            return None


# Load schema at module initialization
_schema = load_schema()


def on_message(ws, message):
    """WebSocket message handler"""
    if isinstance(message, bytes):
        print("received binary message:",message)
        try:
            if _schema is None:
                # Try loading schema again if it failed initially
                if load_schema() is None:
                    logger.error("Cannot process message - SBE schema not available")
                    return
            print("starting decode binary message:")
            # Process the message with the schema
            #decoder = _schema.get_message_decoder(message)
            decoded_data = _schema.decode(message)
            print("decoded binary message:", decoded_data)

            # Print symbol information
            symbol_info = decoded_data.value.get('symbol', {})
            if symbol_info:
                print("\nSymbol section:")
                print(f"Symbol length field (1 byte): {symbol_info['length']}")

                if isinstance(symbol_info['varData'], bytes):
                    symbol = symbol_info['varData'].decode('utf-8')
                elif isinstance(symbol_info['varData'], int):
                    symbol = chr(symbol_info['varData'])
                else:
                    symbol = str(symbol_info['varData'])

                print(f"Symbol data ({len(symbol)} bytes): {symbol}")
                print(f"Total symbol section length: {1 + len(symbol)} bytes")  # length byte + data

            print("\nFull decoded message structure:")
            for key, value in decoded_data.value.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"{key}: {value}")

        except Exception as e:
            global _error_count, _error_types

            # Track error type
            error_type = type(e).__name__
            if error_type not in _error_types:
                _error_types[error_type] = 1
            else:
                _error_types[error_type] += 1

            _error_count += 1

            # Full logging for first few errors
            if _error_count <= 10:
                error_trace = traceback.format_exc()
                logger.error(f"Error #{_error_count}: {e}")
                logger.error(f"Traceback: {error_trace}")

                # Log message details
                if isinstance(message, bytes):
                    logger.error(f"Message sample (hex): {message[:50].hex()}")
            elif _error_count % 100 == 0:
                # Periodic summary
                logger.error(f"Total of {_error_count} errors. Types: {_error_types}")



def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)

    custom_headers = {
        'User-Agent': 'My User Agent',
        'Authorization': 'Bearer your-token-here',
        'X-MBX-APIKEY': 'e6EIY7HRHkTFJlsBsAi2ICQ6oEh71HvqbJH1p96h29BqBpVLL6rM0vBUZyODitps'
    }



    ws = websocket.WebSocketApp("wss://stream-sbe.binance.com/stream?streams=btcusdt@depth20/btcusdt@depth",
                              header=custom_headers,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()