import asyncio
import logging
import os
import sys
from urllib.parse import urljoin, urlparse

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def fetch_html_content(url: str, session: ClientSession) -> str:
    """
    Fetches the HTML content of a URL asynchronously using aiohttp.
    """
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return ""


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


async def extract_team_ids(html_content: str) -> list[str]:
    """
    Extracts team IDs from the HTML content by parsing 'iconface' images.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return [
        img["src"].split("/")[-1].split(".")[0]
        for img in soup.find_all("img", src=lambda src: src and "iconface" in src)
    ]


async def process_team_page(
    team_url: str, dest_dir: str, session: ClientSession
) -> None:
    """
    Processes a team's page by extracting and downloading 'iconface' images asynchronously.
    """
    html_content = await fetch_html_content(team_url, session)
    if not html_content:
        return

    team_ids = await extract_team_ids(html_content)
    tasks = [
        download_image(
            f"https://sortitoutsi.b-cdn.net/uploads/face/{team_id}.png",
            dest_dir,
            session,
        )
        for team_id in team_ids
    ]
    await asyncio.gather(*tasks)


async def main():
    # Get the base URL from command-line arguments
    if len(sys.argv) < 2:
        logging.error("Please provide the base URL as a command-line argument.")
        sys.exit(1)

    base_url = sys.argv[1]
    dest_dir = "."
    os.makedirs(dest_dir, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        # Step 1: Fetch the base page
        html_content = await fetch_html_content(base_url, session)
        if not html_content:
            logging.error(f"Failed to retrieve the base webpage: {base_url}")
            return

        soup = BeautifulSoup(html_content, "html.parser")
        team_links = soup.find_all("a", class_="item-title")

        # Step 2: Download team images and process team pages asynchronously
        tasks = []
        for team_link in team_links:
            team_url = urljoin(base_url, team_link["href"])
            team_id = team_url.split("/")[-1]
            team_image_url = f"https://sortitoutsi.b-cdn.net/uploads/team/{team_id}.png"

            # Download the team image
            tasks.append(download_image(team_image_url, dest_dir, session))

            # Process the team's page
            tasks.append(process_team_page(team_url, dest_dir, session))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
