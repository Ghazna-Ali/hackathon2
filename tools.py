import requests

from bs4 import BeautifulSoup
from crewai.tools import tool
from pypdf import PdfReader


# ============================================================
# PDF CV Extraction Tool
# ============================================================

@tool("Extract CV PDF Text")
def extract_cv_text(file_path: str) -> str:
    """
    Extract readable text from a candidate CV stored as a PDF.

    Args:
        file_path: Path to the CV PDF file.

    Returns:
        Extracted text from all readable PDF pages.
    """

    try:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        extracted_text = "\n\n".join(pages).strip()

        if not extracted_text:
            return (
                "No readable text was found in the PDF. "
                "The CV may be scanned or image-based."
            )

        return extracted_text

    except Exception as error:
        return f"Unable to extract CV text: {error}"


# ============================================================
# Web Research Tool
# ============================================================

@tool("Search Web")
def search_web(query: str) -> str:
    """
    Search the web for publicly available information.

    Args:
        query: Search query.

    Returns:
        A text summary of search results.
    """

    try:
        url = "https://www.google.com/search"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            params={"q": query},
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for result in soup.select("div.MjjYud")[:5]:

            title_element = result.select_one("h3")

            link_element = result.select_one("a")

            if not title_element or not link_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True
            )

            link = link_element.get("href", "")

            snippet_element = result.select_one(
                ".VwiC3b"
            )

            snippet = ""

            if snippet_element:
                snippet = snippet_element.get_text(
                    " ",
                    strip=True
                )

            results.append(
                f"Title: {title}\n"
                f"URL: {link}\n"
                f"Summary: {snippet}"
            )

        if not results:
            return "No useful search results were found."

        return "\n\n".join(results)

    except Exception as error:
        return f"Web search failed: {error}"


# ============================================================
# Job Requirement Extraction Helper
# ============================================================

@tool("Prepare Job Research Query")
def prepare_company_query(
    company_name: str,
    job_title: str
) -> str:
    """
    Create a focused research query for a company and job.

    Args:
        company_name: Organization name.
        job_title: Job title.

    Returns:
        A research query.
    """

    return (
        f"{company_name} {job_title} "
        f"company products services careers "
        f"recent developments"
    )
