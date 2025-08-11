# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2023-11-14 12:00:00 - Log of updates made.
2023-11-15 12:00:00 - Updated with patterns for image downloading functionality.

*

## Coding Patterns

* Object-Oriented Programming: The project uses a class-based approach with the `PhDExamDownloader` class encapsulating the core functionality
* Error handling with try-except blocks throughout the codebase
* Modular design with separate methods for each step of the process
* Command-line interface using argparse for parameter parsing
* Content type detection and handling with dictionary return values
* Unique folder generation for organizing related content

## Architectural Patterns

* Single Responsibility Principle: Each method in the `PhDExamDownloader` class has a single responsibility
* Dependency Injection: The base URL and destination folder are injected into the `PhDExamDownloader` class
* Command Pattern: The CLI script acts as a command invoker for the downloader
* Strategy Pattern: Different download strategies based on content type (PDF vs. images)
* Factory Method: Content type detection determines which download method to use

## Testing Patterns

* Unit testing with unittest framework
* Mock objects for testing without making actual network requests
* Test fixtures for common test setup