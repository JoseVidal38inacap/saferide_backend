#!/usr/bin/env python
import os
import sys
import ssl

# --- Parche de compatibilidad para Python 3.13 + django-sslserver ---
# django-sslserver usa ssl.wrap_socket (eliminado en 3.13) con muchos kwargs
# antiguos (ssl_version, cert_reqs, etc.). Aquí recreamos esa función usando
# SSLContext.wrap_socket y simplemente ignoramos los kwargs que ya no existen.
if not hasattr(ssl, "wrap_socket"):
    def _compat_wrap_socket(sock, keyfile=None, certfile=None,
                            server_side=False, **kwargs):
        # Eliminar argumentos que SSLContext.wrap_socket no soporta
        kwargs.pop("ssl_version", None)
        kwargs.pop("cert_reqs", None)
        kwargs.pop("ca_certs", None)
        kwargs.pop("ssl_version", None)
        # Estos sí existen en SSLContext.wrap_socket:
        #   server_side, do_handshake_on_connect, suppress_ragged_eofs,
        #   server_hostname

        if server_side:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            if certfile:
                ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
        else:
            # Cliente genérico
            ctx = ssl.create_default_context()

        return ctx.wrap_socket(sock, server_side=server_side, **kwargs)

    ssl.wrap_socket = _compat_wrap_socket
# --- Fin parche ---


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saferide_backend.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
