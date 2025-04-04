import websocket
import rel
import sbe
import struct
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='websocket_errors.log',  # Log to a file
    filemode='a'  # Append mode
)
logger = logging.getLogger('websocket_handler')


def on_message(ws, message):
    try:

        if isinstance(message, bytes):
            print("Received binary message:", message)
            binary_data = message

            print(f"\nTotal buffer length: {len(binary_data)} bytes")

            # Print header information
            offset = 0
            print("\nHeader section:")
            block_length = struct.unpack_from('<H', binary_data, offset)[0]  # 2 bytes
            print(f"Block Length (2 bytes): {block_length}")

            template_id = struct.unpack_from('<H', binary_data, offset + 2)[0]  # 2 bytes
            print(f"Template ID (2 bytes): {template_id}")

            schema_id = struct.unpack_from('<H', binary_data, offset + 4)[0]  # 2 bytes
            print(f"Schema ID (2 bytes): {schema_id}")

            version = struct.unpack_from('<H', binary_data, offset + 6)[0]  # 2 bytes
            print(f"Version (2 bytes): {version}")




            # Load the schema
            with open('stream_1_0.xml', 'r') as f:
                schema = sbe.Schema.parse(f)

            # Decode the binary data
            decoded_data = schema.decode(binary_data)

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

            # Print raw bytes at the end for verification
            print("\nRaw bytes of last section:")
            last_bytes = binary_data[-10:]  # Show last 20 bytes
            print(' '.join(f'{b:02x}' for b in last_bytes))
            print("UTF-8 decoded: " + last_bytes.decode('utf-8'))

        else:
            print("Received text message:", message)

    except Exception as e:
        # Capture the full stack trace
        error_trace = traceback.format_exc()
        logger.error(f"Error in on_message: {e}")
        logger.error(f"Traceback: {error_trace}")
        logger.error(f"Message that caused error (type: {type(message)})")
        # Don't let the exception propagate and crash the thread




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
        'X-MBX-APIKEY': '...'
    }



    ws = websocket.WebSocketApp("wss://stream-sbe.binance.com/ws/btcusdt@trade",
                                header=custom_headers,
                                on_open=on_open,
                              on_message=on_message,
                                on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()