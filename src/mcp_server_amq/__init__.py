from .server import serve


def main():
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a LLM model the ability to interact with AmazonMQ API"
    )

    args = parser.parse_args()
    asyncio.run(serve())

if __name__ == "__main__":
    main()
