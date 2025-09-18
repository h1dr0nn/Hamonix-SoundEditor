"""Entry point for launching the Sound Converter application."""

from app.application import run


def main() -> int:
    """Delegate to :func:`app.application.run` for backward compatibility."""

    return run()


if __name__ == "__main__":
    raise SystemExit(main())
