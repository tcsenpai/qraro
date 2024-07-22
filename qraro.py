import qrcode
from PIL import Image
import zxing

def bin_to_qr(data, chunk_size=100, filename_prefix="qr_code", box_size=10, border=4):
    hex_data = data.hex()
    chunks = [hex_data[i:i+chunk_size] for i in range(0, len(hex_data), chunk_size)]
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks, 1):
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border=border)
        qr.add_data(f"{i}/{total_chunks}:{chunk}")
        qr.make(fit=True)
        print(f"Generating QR code {i}", end="")
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{filename_prefix}_{i}.png")
        print(f"[OK]")

    print(f"Generated {total_chunks} QR codes.")
    print(f"Each QR code except the last one will contain {chunk_size} bytes of data.")
    print(f"The last QR code will contain the remaining bytes of data ({len(chunks[-1]  )} bytes).")

def qr_to_bin(filename_prefix="qr_code"):
    chunks = {}
    i = 1
    reader = zxing.BarCodeReader()

    while True:
        try:
            filename = f"{filename_prefix}_{i}.png"
            print(f"Decoding QR code {i}...", end="")
            barcode = reader.decode(filename)
            print(f"decoded...", end="")
            if barcode and barcode.parsed:
                decoded = barcode.parsed
                chunk_info, chunk_data = decoded.split(':', 1)
                chunk_num, total_chunks = map(int, chunk_info.split('/'))
                chunks[chunk_num] = chunk_data
                print(f"binary data extracted [OK]")
                if chunk_num == total_chunks:
                    break
            else:
                print(f"Error decoding QR code {i}: {barcode.raw}")
                
            i += 1
        except FileNotFoundError:
            break
        except Exception as e:
            print(f"Error decoding QR code {i}: {e}")
            exit(-1)

    if not chunks:
        print("No QR codes found.")
        return None

    hex_data = ''.join(chunks[i] for i in range(1, len(chunks) + 1))
    return bytes.fromhex(hex_data)