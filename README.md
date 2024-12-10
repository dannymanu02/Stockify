# Stockify: A Flask Application for Stock Analysis

Stockify is a Flask-based web application that provides comprehensive stock analysis using data from Yahoo Finance. The application generates various plots, including closing prices, traded volumes, intraday differences, and trend analysis during key financial events such as the 2008 recession and the COVID-19 pandemic.

## Features

- **Company Overview**: Get detailed information about a company using its stock ticker symbol.
- **Stock Analysis**: Visualize stock performance over time with various plots:
  - Closing Prices Over Time
  - Traded Volumes Over Time
  - Intraday Difference Prices Over Time
  - Intraday Difference Trends
  - Decomposition of Closing Prices (Trend, Seasonality, Residuals)
  - Analysis During Recession (2008-09)
  - Analysis During COVID-19 Pandemic

## Technology Stack

- **Python**: Core programming language
- **Flask**: Web framework used for building the application
- **Yahoo Finance**: Data source for historical stock data
- **Matplotlib**: Library for creating static, animated, and interactive visualizations
- **Statsmodels**: Used for statistical modeling and time series analysis
- **Pandas**: Data manipulation and analysis library
- **Azure App Services**: Hosting platform for the web application

## Getting Started

### Prerequisites

- Python 3.x installed on your local machine
- Virtualenv for creating isolated Python environments
- Git for version control

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/stockify.git
    cd stockify
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    - Create a `.env` file in the root directory.
    - Add any necessary environment variables. For example:
    
    ```
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```

5. **Run the application locally**:

    ```bash
    flask run
    ```

6. **Open your browser** and navigate to `http://127.0.0.1:5000/` to see the application running locally.

## Deployment on Azure App Services

To deploy this application on Azure App Services, follow these steps:

1. **Create an Azure App Service**:

   - Log in to the [Azure Portal](https://portal.azure.com/).
   - Create a new App Service and select the appropriate subscription, resource group, and service plan.
   - Choose the runtime stack (Python 3.x) and deploy the application.

2. **Set up deployment from GitHub**:

   - Navigate to the "Deployment Center" in your Azure App Service.
   - Choose GitHub as the deployment source and authenticate your GitHub account.
   - Select your repository and branch.

3. **Configure Application Settings**:

   - Go to "Configuration" in your Azure App Service.
   - Add the environment variables listed in your `.env` file (e.g., `FLASK_ENV`, `SECRET_KEY`).

4. **Deploy the application**:

   - Azure App Service will automatically deploy your application from the selected GitHub repository.
   - After deployment, your application will be accessible via the provided Azure URL.

## Acknowledgments

- Thanks to the developers of [Flask](https://flask.palletsprojects.com/), [Matplotlib](https://matplotlib.org/), [Pandas](https://pandas.pydata.org/), and [Statsmodels](https://www.statsmodels.org/) for their amazing libraries.
- Data provided by [Yahoo Finance](https://finance.yahoo.com/).

## Contact

For any questions or suggestions, feel free to open an issue or contact me via [danielmanu02@gmail.com](mailto:danielmanu02@gmail.com).
