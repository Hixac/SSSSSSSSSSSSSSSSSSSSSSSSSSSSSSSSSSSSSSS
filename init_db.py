import subprocess

from src.server.core.config import settings

def main() -> None:
    args = [ \
            "-e", f"POSTGRES_USER={settings.DB_USER}", \
            "-e", f"POSTGRES_PASSWORD={settings.DB_PASSWORD}", \
            "-e", f"POSTGRES_DB={settings.DB_NAME}", \
            "-p", f"{settings.DB_PORT}:5432", \
            "-d", "postgres", \
            "postgres", "-N", "1000" \
    ]
    cmd = ["docker", "run"]

    _ = subprocess.run(
            cmd + args
    )

if __name__ == "__main__":
    main()
