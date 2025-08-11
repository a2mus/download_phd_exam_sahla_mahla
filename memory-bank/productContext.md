# Product Context

This file provides a high-level overview of the project and the expected product that will be created. Initially it is based upon projectBrief.md (if provided) and all other available project-related information in the working directory. This file is intended to be updated as the project evolves, and should be used to inform all other modes of the project's goals and context.
2023-11-14 12:00:00 - Log of updates made will be appended as footnotes to the end of this file.
2023-11-15 12:00:00 - Updated with image downloading functionality.

*

## Project Goal

* The PhD Exam Downloader is a Python tool designed to automatically download PhD entrance exam PDFs and embedded images from the sahla-dz.com website. It aims to simplify the process of collecting exam materials for students preparing for PhD entrance exams in Algeria.

## Key Features

* Scrapes the main page to find links to individual exam pages
* Extracts PDF URLs from Google Docs viewer iframes
* Detects and extracts embedded images from iframes and divs
* Downloads PDFs to a specified folder
* Organizes images from each exam in dedicated subfolders
* Handles various URL formats and edge cases
* Provides detailed logging of the download process
* Command-line interface for customization

## Overall Architecture

* The project follows a modular design with a main `PhDExamDownloader` class that handles the core functionality
* Content type detection to differentiate between PDFs and embedded images
* Dedicated methods for handling different content types (PDFs vs. images)
* Organized folder structure for downloaded content
* Command-line interface provided through a separate script
* Error handling and logging throughout the codebase
* Unit tests to verify functionality