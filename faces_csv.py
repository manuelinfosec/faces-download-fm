import asyncio
import csv
import logging
import os
import sys
from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def download_image(url: str, dest_dir: str, session: ClientSession) -> None:
    """
    Downloads an image asynchronously if it doesn't already exist in the destination directory.
    """
    filename = os.path.basename(urlparse(url).path)
    file_path = os.path.join(dest_dir, filename)

    if not os.path.exists(file_path):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(await response.read())
                logging.info(f"Downloaded: {filename}")
        except aiohttp.ClientError as e:
            logging.error(f"Failed to download {url}: {e}")
    else:
        logging.info(f"Already exists: {filename}")


def extract_unique_ids_from_csv(csv_file: str) -> list[str]:
    """
    Extracts Unique IDs from a CSV file.
    """
    unique_ids = []
    try:
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            if "Unique ID" not in reader.fieldnames:
                logging.error("CSV file does not contain 'Unique ID' column.")
                sys.exit(1)
            for row in reader:
                unique_ids.append(row["Unique ID"].strip())
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        sys.exit(1)

    return unique_ids


async def main():
    # Check if a CSV file is provided as an argument
    if len(sys.argv) < 2:
        logging.error("Please provide a CSV file as a command-line argument.")
        sys.exit(1)

    csv_file = sys.argv[1]
    dest_dir = "."
    os.makedirs(dest_dir, exist_ok=True)

    # Extract Unique IDs from the CSV file
    unique_ids = extract_unique_ids_from_csv(csv_file)
    if not unique_ids:
        logging.error("No Unique IDs found in the CSV file.")
        return

    async with aiohttp.ClientSession() as session:
        # Generate download tasks for each Unique ID
        tasks = [
            download_image(
                f"https://sortitoutsi.b-cdn.net/uploads/face/{unique_id}.png",
                dest_dir,
                session,
            )
            for unique_id in unique_ids if unique_id == "2000276779"
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
