from pathlib import Path
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

BASE_DIR = Path(__file__).resolve().parent
CERTS_DIR = BASE_DIR / "certs"
CERTS_DIR.mkdir(exist_ok=True)

key_path = CERTS_DIR / "saferide.key"
cert_path = CERTS_DIR / "saferide.crt"

# Generar clave privada
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Guardar clave privada
with open(key_path, "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

# Datos del sujeto/emisor (self-signed)
subject = issuer = x509.Name(
    [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "RM"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Santiago"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SafeRide"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ]
)

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName("localhost")]
        ),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

# Guardar certificado
with open(cert_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(f"Certificado generado en: {cert_path}")
print(f"Clave privada generada en: {key_path}")
