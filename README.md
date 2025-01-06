# Twitter Trends

## Overview
The Twitter Trends application is a Flask-based web application that fetches and displays trending topics from Twitter using Selenium for web scraping. It stores the fetched trends in a MongoDB database along with metadata such as the timestamp and public IP used during the scraping process.

## Features
- Fetch trending topics from Twitter.
- Display the last execution time and public IP used.
- Store historical trends in a MongoDB database.
- User-friendly interface to view current trends and metadata.

## Technologies Used
- **Flask**: Web framework for building the application.
- **Selenium**: For automating web browser interaction and scraping data from Twitter.
- **MongoDB**: NoSQL database for storing trending topics and metadata.
- **JavaScript**: For handling asynchronous requests and updating the UI dynamically.

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- pip (Python package installer)
- MongoDB server running locally

### Clone the Repository

git clone https://github.com/yourusername/twitter-trends.git
cd twitter-trends
