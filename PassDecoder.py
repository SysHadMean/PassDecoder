import sys
import zlib
import pprint
import argparse
import logging
# Modules tiers (Pillow, Pyzbar, base45, cbor2)
import PIL.Image
import pyzbar.pyzbar
import base45
import cbor2


log = logging.getLogger(__name__)


def _setup_logger() -> None:
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(log_formatter)
    console_handler.propagate = False
    logging.getLogger().addHandler(console_handler)
    # log.setLevel(logging.DEBUG)
    log.setLevel(logging.INFO)


def main() -> None:
    parser = argparse.ArgumentParser(description='EU COVID Vaccination Passport Decoder')
    parser.add_argument('--image-file', metavar="IMAGE-FILE",
                        help='Image to read QR-code from')
    args = parser.parse_args()
    _setup_logger()

    covid_cert_data = None
    image_file = None
    if args.image_file:
        image_file = args.image_file

    if image_file:
        data = pyzbar.pyzbar.decode(PIL.Image.open(image_file))
        cert = data[0].data.decode()
        b45data = cert.replace("HC1:", "")
        zlibdata = base45.b45decode(b45data)
        cbordata = zlib.decompress(zlibdata)
        decoded = cbor2.loads(cbordata)
        print("Header\n----------------");
        pprint.pprint(cbor2.loads(decoded.value[0]))
        print("\nPayload\n----------------");
        pprint.pprint(cbor2.loads(decoded.value[2]))
        print("\nSignature ?\n----------------");
        print(decoded.value[3])
    else:
        log.error("Input parameters: Need either --image-file")
        exit(2)


if __name__ == '__main__':
    main()