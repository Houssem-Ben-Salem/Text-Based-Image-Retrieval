# Text-Based-Image-Retrieval

This project provides a Streamlit-powered interface to search for images from Flickr using Elasticsearch. The application allows users to filter search results by various parameters and view details about each image. It's been designed with scalability in mind, using various optimizations and Elasticsearch features to handle vast amounts of data.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Key Optimizations](#key-optimizations)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Logging](#logging)
6. [Contribution](#contribution)
7. [License](#license)

## Project Structure

- `app.py`: The main Streamlit application. Handles the user interface and interacts with Elasticsearch for search operations.
- `config.py`: Contains configuration details for the application.
- `es_operations.py`: Functions related to Elasticsearch operations, including setting up the index and querying.
- `image_validation.log`: Log file capturing details about image validation processes.
- `image_validator.py`: Logic to validate images before indexing to Elasticsearch.
- `logger_setup.py`: Configurations for setting up logging for the application.
- `main.py`: The main execution script for the application.

## Key Optimizations

### `is_valid` Flag

To ensure the search results are always relevant and valid, images are validated before being indexed into Elasticsearch. The validation process checks several factors, and based on the outcome, an `is_valid` flag is added to each indexed image. This flag:

- Helps in filtering out irrelevant or inappropriate images.
- Significantly boosts the search speed by allowing Elasticsearch to quickly prioritize and return valid images.

By pre-validating and marking images with this flag, we avoid unnecessary compute overhead during search time, leading to faster response times for end-users.

### Scroll API for Large Datasets

Dealing with vast amounts of image data poses challenges in retrieval and indexing. To ensure efficient and consistent retrieval of large datasets from Elasticsearch, we utilize the Elasticsearch Scroll API. Key benefits:

- Allows the application to retrieve large numbers of documents from Elasticsearch without the need for manual pagination.
- Ensures a consistent snapshot of the data is seen during the entire scroll session, even if the underlying data changes.
- Provides a mechanism to handle timeouts and large data fetches without overloading the system.

Using the Scroll API, we can efficiently manage and process vast datasets, ensuring a smooth user experience.

Certainly! Here's a template for a README file that you can use for your GitHub repo:

Certainly! Here's a template for a README file that you can use for your GitHub repo:


## Setup and Installation

1. Ensure you have Python 3.x installed.
2. Clone this repository:
    ```bash
    git clone https://github.com/Houssem-Ben-Salem/Text-Based-Image-Retrieval.git
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

   **Note**: Ensure you have Elasticsearch set up and running.

4. Configure your Elasticsearch parameters in `config.py`.

5. Run the main application:
    ```bash
    streamlit run app.py
    ```

## Usage

- Use `main.py` as the primary entry point if you wish to validate and index images first.
- Directly run `app.py` with Streamlit to start the search interface.

## Logging

- The project utilizes logging to keep track of image validation processes. Check `image_validation.log` for related logs.
- `logger_setup.py` provides a centralized logger configuration.

## Contribution

Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
