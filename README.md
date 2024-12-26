# python-selenium-browserstack

## Description
This project demonstrates web scraping, API integration, and text processing using Selenium and BrowserStack. The script scrapes articles from the "Opinion" section of the El País website, processes and translates their headers, and performs cross-browser testing on BrowserStack.

## Prerequisites
- Python installed on your system (Python 3.x recommended).
- BrowserStack account credentials (username and access key).

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/aadarsh-nagrath/selenium-wep-scraping-api.git
   cd selenium-wep-scraping-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your BrowserStack credentials:
   ```
   BROWSERSTACK_USERNAME=your_browserstack_username
   BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
   ```
   Use the `.env.example` file as a reference.

## Usage

1. Run the script:
   ```bash
   python web.py
   ```

2. Outputs:
   - Prints the repeated words from the translated headers along with their counts.
   - Prints the headers of the first 5 articles in the "Opinion" section.
   - Downloads the cover images of the articles (if available).

## Assignment Breakdown

### 1. Technical Assignment: Run Selenium Test on BrowserStack
This project addresses the following requirements:

#### Web Scraping:
- Navigates to the El País "Opinion" section.
- Scrapes the first 5 articles, fetching their titles, content, and cover images.

#### API Integration:
- Uses a translation API (e.g., Google Translate API) to translate article headers from Spanish to English.

#### Text Processing:
- Identifies repeated words (occurring more than twice) in the translated headers.

#### Cross-Browser Testing:
- Executes the solution locally and verifies functionality.
- Runs the solution on BrowserStack across 5 parallel threads, testing a combination of desktop and mobile browsers.

### Submission
Upload the completed project source code to GitHub and share the repository link.