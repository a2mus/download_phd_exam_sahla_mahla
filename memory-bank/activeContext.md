# Active Context

This file tracks the project's current status, including recent changes, current goals, and open questions.
2023-11-14 12:00:00 - Log of updates made.
2023-11-15 12:00:00 - Updated with image downloading functionality.

*

## Current Focus

* The project is currently complete with enhanced functionality implemented
* The downloader can scrape the main page, find exam pages, extract PDF URLs or embedded images, and download them
* Images from a single exam are organized in dedicated subfolders
* Command-line interface is available for customization

## Recent Changes

* Enhanced the `PhDExamDownloader` class to detect and download embedded images from iframes and divs
* Added functionality to organize images from each exam in dedicated subfolders
* Updated the default destination folder to use the specified exams folder
* Updated CLI and README to reflect the new image downloading capabilities

## Open Questions/Issues

* The website structure might change in the future, requiring updates to the scraping logic
* Image extraction might need refinement for different iframe structures
* Error handling could be improved for specific edge cases
* Performance optimization might be needed for large numbers of PDFs and images
* Image quality and format detection could be improved