import sbe
import base64
import struct
import binascii
import datetime


def format_microsecond_timestamp(timestamp_microseconds):
    """
    Convert a microsecond timestamp to a human-readable format.

    Args:
        timestamp_microseconds: Timestamp in microseconds since epoch

    Returns:
        Human-readable datetime string with microsecond precision
    """
    # Convert to seconds for datetime (keeping microseconds precision)
    seconds = timestamp_microseconds / 1_000_000

    # Create datetime object
    dt = datetime.datetime.fromtimestamp(seconds)

    # Format with microseconds
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')

    return formatted_time



# Your base64 string
#base64_data = "EgASJwEAAADMYxogxDEGAPF+8i4LAAAA+PgQABQAwFibwCsAAABQx91fAAAAAIAWjMArAAAAQJoeAgAAAABA1HzAKwAAABDrCQAAAAAAAJJtwCsAAADgkwQAAAAAAMBPXsArAAAAMKoMAAAAAACADU/AKwAAAADMZSgAAAAAQMs/wCsAAAAAdrAQAAAAAMBGIcArAAAAkG8oAAAAAACABBLAKwAAAFC1LAAAAAAAwD3kvysAAADwkJ8RAAAAAID71L8rAAAAsB4EAAAAAABAucW/KwAAAHAaTicAAAAAAHe2vysAAAAgBwITAAAAAMA0p78rAAAAEEBkAAAAAACA8pe/KwAAALAeBAAAAAAAQLCIvysAAADwugQAAAAAAABueb8rAAAAoDegAAAAAADAK2q/KwAAAABsEQ8AAAAAgOlavysAAAAQnN9fAAAAAECnS78rAAAAAMbdKQAAAAAQABQAAJuqwCsAAACQfkuWAAAAAEDducArAAAAQKsTbwAAAACAH8nAKwAAABD9KQ8AAAAAwGHYwCsAAAAAVKdKAAAAAACk58ArAAAA4Ie4DAAAAACAKAbBKwAAAMBFBAAAAAAAwGoVwSsAAABgycEAAAAAAACtJMErAAAAMEo2zAAAAABA7zPBKwAAADCGTQsAAAAAgDFDwSsAAADQoRAAAAAAAMBzUsErAAAAwEUEAAAAAABA+HDBKwAAAGABuA4AAAAAgDqAwSsAAAAwR2YTAAAAAAC/nsErAAAAMNPqBwAAAABAAa7BKwAAAPC6BAAAAAAAwIXMwSsAAADArjsoAAAAAADI28ErAAAAYD0IAAAAAABACuvBKwAAAECMnQkAAAAAgEz6wSsAAADAPV4NAAAAAMCOCcIrAAAA8HF+BgAAAAAHRVRIVVNEVA=="
#base64_data ="GgATJwEAAACTia0n3DEGAOpaaUAPAAAAEVtpQA8AAAD4+BAAEwAADP1emgcAAHhApAwAAAAAwMntXpoHAACQ1gIAAAAAAICH3l6aBwAACFIAAAAAAACAFhhVmgcAAAgM1gEAAAAAwDiGTZoHAAAAAAAAAAAAAIBCskiaBwAAAAAAAAAAAAAAiCVHmgcAAAivLwAAAAAAwCCLOJoHAADIMgAAAAAAAIDeeziaBwAAkGIhBQAAAADAP5UymgcAAAAAAAAAAAAAAKwQC5oHAAAAAAAAAAAAAMDmwACaBwAA8B8JAAAAAABAEWuEmQcAAAAAAAAAAAAAgD/SaJkHAACISkcEAAAAAEDbz1GYBwAAAAAAAAAAAACAAihRmAcAAAAAAAAAAAAAQHvj/ZcHAABAcRwAAAAAAABwyhgVBgAAkOIAAAAAAAAATI6xvAIAAEANAwAAAAAAEAALAEBODF+aBwAA8OFrDQAAAABAa/q3mgcAAAAAAAAAAAAAQHzm55oHAACISkcEAAAAAMAjaxibBwAAAAAAAAAAAACAaYYpmwcAAFjPXwAAAAAAwBH6VJsHAADgzY8DAAAAAAAGzW+cBwAAAAAAAAAAAADA4UsTnQcAAGCUMgEAAAAAwGu/9p0HAAAAAAAAAAAAAIBz2I2eBwAAAAAAAAAAAABA1UGtngcAAIAaBgAAAAAAB0JUQ1VTRFQ="
#base64_data ="EgASJwEAAAD2wrg63DEGADS+a0APAAAA+PgQABQAgKyWnpsHAAAQDooCAAAAAEBqh56bBwAA6IAAAAAAAADA0+6dmwcAALA2AAAAAAAAgJHfnZsHAABYGwAAAAAAAEBGk52bBwAA0O8DAAAAAACASfebmwcAAFgbAAAAAAAAAKHkmpsHAACYOgAAAAAAAMBe1ZqbBwAAOEoAAAAAAADAMaSZmwcAAJg6AAAAAAAAwOm7l5sHAACwNgAAAAAAAICnrJebBwAAeA8PAAAAAAAAwO6UmwcAAIAsAwAAAAAAgCAZlJsHAACwNgAAAAAAAMBHcZObBwAAKCMAAAAAAACA8+eSmwcAAPBVAAAAAAAAwBEDkpsHAABYGwAAAAAAAEC1K4ybBwAA6P0AAAAAAAAAcxyMmwcAAMBdAAAAAAAAAP4CiZsHAABoQgAAAAAAAEAKpIebBwAAyDIAAAAAAAAQABQAwO6lnpsHAAAAR3MYAAAAAACC2qCbBwAAMGcsAAAAAABAxOmgmwcAAFgbAAAAAAAAQOjdoZsHAABYGwAAAAAAAIAq7aGbBwAAWBsAAAAAAADAh7OimwcAAFgbAAAAAAAAAMrCopsHAABYGwAAAAAAAADPrKmbBwAAWBsAAAAAAAAA/N2qmwcAAFgbAAAAAAAAwN3Cq5sHAADgLgAAAAAAAMABt6ybBwAAyDIAAAAAAAAARMasmwcAAGC8TwIAAAAAQIbVrJsHAADIMgAAAAAAAMAu6K2bBwAAcBcAAAAAAAAAJbyymwcAAECccQIAAAAAgMSRs5sHAABQm8UDAAAAAMAGobObBwAAoKN8AwAAAADAYAO2mwcAAGCgNgAAAAAAAKxPtpsHAADg70gAAAAAAAAGsribBwAAqGzLCwAAAAAHQlRDVVNEVA=="
base64_data = "EgASJwEAAAC5l/5I3DEGAJoP6u0DAAAA+PgQABQAAAD6AAAAAAAA2xVZuwQAABj8+QAAAAAAAKmKiLEAAAAw+PkAAAAAAAAhLIjwAgAASPT5AAAAAAAAwEGg0AUAAGDw+QAAAAAAANR51LwHAAB47PkAAAAAAABkkGVyBgAAkOj5AAAAAAAATz24SgcAAKjk+QAAAAAAAPbDCkEEAADA4PkAAAAAAAB9elm6AwAA2Nz5AAAAAAAAOAdD6wUAAPDY+QAAAAAAAEfCiYUFAAAI1fkAAAAAAABkNy6hAwAAINH5AAAAAAAANNpiygUAADjN+QAAAAAAAGoP7qEKAABQyfkAAAAAAABwXaruDAAAaMX5AAAAAAAAeX/3QAYAAIDB+QAAAAAAADhWZwMHAACYvfkAAAAAAABRrXp6FgAAsLn5AAAAAAAAp8JnLhkAAMi1+QAAAAAAAPWb7NUaAAAQABQA6AP6AAAAAAAAMHNV0gIAANAH+gAAAAAAADhLooUEAAC4C/oAAAAAAABXwWYOBAAAoA/6AAAAAAAA4MD8oQYAAIgT+gAAAAAAABpt89AOAABwF/oAAAAAAABRXDDtBwAAWBv6AAAAAAAAxfAq1AQAAEAf+gAAAAAAAIUVRD4GAAAoI/oAAAAAAAAo9AHcDwAAECf6AAAAAAAACVtMPBMAAPgq+gAAAAAAAGjvwzoJAADgLvoAAAAAAABYEMJ6BQAAyDL6AAAAAAAAFdgX+gUAALA2+gAAAAAAAGZCQr0MAACYOvoAAAAAAACTiCzXAwAAgD76AAAAAAAAylOnDQUAAGhC+gAAAAAAALfhXZQGAABQRvoAAAAAAAAJdq0tCgAAOEr6AAAAAAAAq7GQeQcAACBO+gAAAAAAAPlFI8wDAAAIRE9HRVVTRFQ="

binary_message = b"\x12\x00\x12'\x01\x00\x00\x00\xb5\xa5\xd0\x0c\xed1\x06\x00R\xe7\xfe\xee\x03\x00\x00\x00\xf8\xf8\x10\x00\x14\x00\x18\x85\xf8\x00\x00\x00\x00\x00\x00\n\x13\xb9\x01\x00\x00\x000\x81\xf8\x00\x00\x00\x00\x00\x00\xd6\x11~\x03\x00\x00\x00H}\xf8\x00\x00\x00\x00\x00\x00\xd4\xe6o\x14\x02\x00\x00`y\xf8\x00\x00\x00\x00\x00\x00\xec\xfd\x11\xce\x03\x00\x00xu\xf8\x00\x00\x00\x00\x00\x00Y\xcb\xe7o\x06\x00\x00\x90q\xf8\x00\x00\x00\x00\x00\x00\x06{\x82\x08\r\x00\x00\xa8m\xf8\x00\x00\x00\x00\x00\x00\xb6\xd7\xf4|\n\x00\x00\xc0i\xf8\x00\x00\x00\x00\x00\x00!s\xfd\xd8\x03\x00\x00\xd8e\xf8\x00\x00\x00\x00\x00\x00\x93\xff\xbb\xdd\x05\x00\x00\xf0a\xf8\x00\x00\x00\x00\x00\x00\x8foS\x1e\r\x00\x00\x08^\xf8\x00\x00\x00\x00\x00\x00\xafD\xd1r\x0e\x00\x00 Z\xf8\x00\x00\x00\x00\x00\x00%/[\x85\x0c\x00\x008V\xf8\x00\x00\x00\x00\x00\x003\xfe\xafG\t\x00\x00PR\xf8\x00\x00\x00\x00\x00\x00oH\xbam\x02\x00\x00hN\xf8\x00\x00\x00\x00\x00\x00T/\xf0#\x04\x00\x00\x80J\xf8\x00\x00\x00\x00\x00\x00\xf2\xb6\xc7\xd4\n\x00\x00\x98F\xf8\x00\x00\x00\x00\x00\x00\xe53\xb80\r\x00\x00\xb0B\xf8\x00\x00\x00\x00\x00\x00\xba\xd3\x08\xbb\x08\x00\x00\xc8>\xf8\x00\x00\x00\x00\x00\x00\xa4\x85`\x02\x19\x00\x00\xe0:\xf8\x00\x00\x00\x00\x00\x00\xb5y39-\x00\x00\x10\x00\x14\x00\x00\x89\xf8\x00\x00\x00\x00\x00\x00>\xaan\xf6\x07\x00\x00\xe8\x8c\xf8\x00\x00\x00\x00\x00\x00\xeb\xb6F\x87\x08\x00\x00\xd0\x90\xf8\x00\x00\x00\x00\x00\x00\x87\x90(\n\x06\x00\x00\xb8\x94\xf8\x00\x00\x00\x00\x00\x00\x17\xda\xe9+\x08\x00\x00\xa0\x98\xf8\x00\x00\x00\x00\x00\x00A;3\x1c\x07\x00\x00\x88\x9c\xf8\x00\x00\x00\x00\x00\x00\x8aPU\x89\x05\x00\x00p\xa0\xf8\x00\x00\x00\x00\x00\x00\xfc\\#\x93\x04\x00\x00X\xa4\xf8\x00\x00\x00\x00\x00\x00\xcf*~\xf5\n\x00\x00@\xa8\xf8\x00\x00\x00\x00\x00\x00\xe8=\xae\xfa\x03\x00\x00(\xac\xf8\x00\x00\x00\x00\x00\x00\xad\xbb\x11\xdb\t\x00\x00\x10\xb0\xf8\x00\x00\x00\x00\x00\x00\xce\xdf\xac\x87\x18\x00\x00\xf8\xb3\xf8\x00\x00\x00\x00\x00\x00\xdd6\x16\xdd\x0c\x00\x00\xe0\xb7\xf8\x00\x00\x00\x00\x00\x00\xf7{\xfb\xdd\x08\x00\x00\xc8\xbb\xf8\x00\x00\x00\x00\x00\x00\xe4X\xf5\x86\x05\x00\x00\xb0\xbf\xf8\x00\x00\x00\x00\x00\x00\x11\xfdR5\x0f\x00\x00\x98\xc3\xf8\x00\x00\x00\x00\x00\x00\xfcrPp\x1b\x00\x00\x80\xc7\xf8\x00\x00\x00\x00\x00\x00\x85\xd4\x19\xfc\x03\x00\x00h\xcb\xf8\x00\x00\x00\x00\x00\x00K'3\xf4\x06\x00\x00P\xcf\xf8\x00\x00\x00\x00\x00\x00\x91}\xbb\x9c\x0c\x00\x008\xd3\xf8\x00\x00\x00\x00\x00\x00\x07\x99\x11\x92\x0c\x00\x00\x08DOGEUSDT"

# Decode base64 to binary
#binary_data = base64.b64decode(base64_data)
binary_data=binary_message

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

# Move past header
offset = 8

print("\nMessage body:")
# Print each 8-byte segment
while offset < len(binary_data) - 8:  # Leave room for potential symbol at end
    value = struct.unpack_from('<q', binary_data, offset)[0]  # 8 bytes
    print(f"Offset {offset}: Value (8 bytes): {value}")
    offset += 8

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

timestamp_microseconds = 1743744052274613
human_readable_time = format_microsecond_timestamp(timestamp_microseconds)

print(f"Base64 encoded data:")
print(base64_data)
print(f"\nTimestamp {timestamp_microseconds} converted to:")
print(human_readable_time)
