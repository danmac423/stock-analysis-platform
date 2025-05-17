import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class AlphaVantageFundamentalAnalyser:
    """
    A class to fetch, clean, and analyse fundamental stock data from Alpha Vantage.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    KNOWN_STRING_FIELDS_OVERVIEW = {
        "Symbol",
        "AssetType",
        "Name",
        "Description",
        "CIK",
        "Exchange",
        "Currency",
        "Country",
        "Sector",
        "Industry",
        "Address",
        "FiscalYearEnd",
        "LatestQuarter",
        "DividendDate",
        "ExDividendDate",
        "OfficialSite",
    }

    KNOWN_STRING_FIELDS_REPORTS = {
        "fiscalDateEnding",
        "reportedCurrency",
        "reportTime",
        "reportedDate",
    }

    QUARTERLY_REPORT_CONFIGS = {
        "income_statement": {
            "raw_key": "income_statement",
            "list_key": "quarterlyReports",
            "output_key": "quarterly_income_statement",
        },
        "balance_sheet": {
            "raw_key": "balance_sheet",
            "list_key": "quarterlyReports",
            "output_key": "quarterly_balance_sheet",
        },
        "cash_flow": {
            "raw_key": "cash_flow",
            "list_key": "quarterlyReports",
            "output_key": "quarterly_cash_flow",
        },
        "earnings": {
            "raw_key": "earnings",
            "list_key": "quarterlyEarnings",
            "output_key": "quarterly_earnings",
        },
    }

    def __init__(self, ticker: str):
        """
        Initializes the analyser with a stock ticker.
        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").
        Raises:
            ValueError: If the Alpha Vantage API key is not found in environment variables.
        """
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("API key for Alpha Vantage is not set in environment variables (ALPHA_VANTAGE_API_KEY).")
        self.ticker = ticker.upper()
        self.raw_data = {}

    def _fetch_from_api(self, function_name: str, **kwargs: dict) -> dict:
        """
        Fetches data from the Alpha Vantage API for a given function and ticker.
        Handles common request errors and returns a dictionary.
        Args:
            function_name (str): The Alpha Vantage function name (e.g., "OVERVIEW").
            **kwargs (dict): Additional parameters for the API request.
        Returns:
            dict: The JSON response from the API if successful, or an error dictionary
                  (e.g., {"request_error": "Timeout", ...}) if an error occurs.
        """
        params = {
            "function": function_name,
            "symbol": self.ticker,
            "apikey": self.api_key,
            **kwargs,
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.Timeout:
            return {"request_error": "Timeout", "details": f"Function: {function_name}, Ticker: {self.ticker}"}
        except requests.exceptions.HTTPError as e:
            error_details = e.response.text if e.response else str(e)
            return {
                "request_error": "HTTPError",
                "details": error_details,
                "status_code": e.response.status_code if e.response else None,
            }
        except requests.exceptions.RequestException as e:
            return {"request_error": "RequestException", "details": str(e)}
        except json.JSONDecodeError:
            return {
                "json_error": "Failed to decode JSON",
                "details": response.text[:200]
                if "response" in locals() and hasattr(response, "text")
                else "No response text",
            }

    def _fetch_all_data(self):
        """
        Fetches all core fundamental data (overview, income statement, balance sheet,
        cash flow, and earnings) for the ticker and stores it in `self.raw_data`.
        """

        self.raw_data["overview"] = self._fetch_from_api("OVERVIEW")
        self.raw_data["income_statement"] = self._fetch_from_api("INCOME_STATEMENT")
        self.raw_data["balance_sheet"] = self._fetch_from_api("BALANCE_SHEET")
        self.raw_data["cash_flow"] = self._fetch_from_api("CASH_FLOW")
        self.raw_data["earnings"] = self._fetch_from_api("EARNINGS")

    def _parse_value(self, value):
        """
        Parses a raw string value from the API into a more usable Python type.
        - Converts "None", "-", "N/A" (case-insensitive) to Python `None`.
        - Converts numeric strings (potentially with commas) to `int` or `float`.
        - Returns other strings as is (stripped).
        - Returns non-string, non-numeric types as is.
        Args:
            value: The value to parse.
        Returns:
            The parsed value (int, float, str, or None).
        """
        if isinstance(value, (int, float)):
            return value
        if not isinstance(value, str):
            return value

        val_stripped = value.strip()
        if val_stripped.lower() in ("none", "-", "n/a", ""):
            return None
        try:
            val_no_commas = val_stripped.replace(",", "")
            if "." in val_no_commas:
                return float(val_no_commas)
            return int(val_no_commas)
        except ValueError:
            return val_stripped

    def _clean_dict(self, data_dict: dict, known_string_fields: set) -> dict:
        """
        Cleans a dictionary by parsing its values using `_parse_value`.
        Values for keys specified in `known_string_fields` are treated as strings
        (or become `None` if they represent missing data like "None").
        Other values are parsed according to `_parse_value`.
        Args:
            data_dict (dict): The dictionary to clean.
            known_string_fields (set): A set of keys whose values should primarily be treated as strings.
        Returns:
            dict: A new dictionary with cleaned values. Returns the input if not a dict.
        """
        if not isinstance(data_dict, dict):
            return data_dict

        cleaned_dict = {}
        for key, original_value in data_dict.items():
            if key in known_string_fields:
                if isinstance(original_value, str) and original_value.strip().lower() in ("none", "-", "n/a", ""):
                    processed_value = None
                else:
                    processed_value = original_value
            else:
                processed_value = self._parse_value(original_value)

            if processed_value is not None:
                cleaned_dict[key] = processed_value
        return cleaned_dict

    def _process_overview_data(self) -> dict:
        """
        Retrieves and cleans the overview data from self.raw_data.
        Returns:
            dict: The cleaned overview data.
        """
        raw_overview = self.raw_data.get("overview", {})
        return self._clean_dict(raw_overview, self.KNOWN_STRING_FIELDS_OVERVIEW)

    def _process_single_quarterly_report(self, report_config: dict, n_quarters: int) -> list:
        """
        Processes a single type of quarterly report based on its configuration.
        Retrieves the raw data, extracts the list of reports, slices it, and cleans each item.
        Args:
            report_config (dict): The configuration for the specific quarterly report
                                 (e.g., an item from QUARTERLY_REPORT_CONFIGS).
            n_quarters (int): The number of recent quarters to include.
        Returns:
            list: A list of cleaned quarterly report dictionaries.
        """
        raw_key = report_config["raw_key"]
        list_key = report_config["list_key"]

        raw_report_data_full = self.raw_data.get(raw_key, {})

        quarterly_reports_list = raw_report_data_full.get(list_key, [])
        if not isinstance(quarterly_reports_list, list):
            quarterly_reports_list = []

        recent_n_reports = quarterly_reports_list[:n_quarters]

        cleaned_reports = []
        for report_item in recent_n_reports:
            if isinstance(report_item, dict):
                cleaned_reports.append(self._clean_dict(report_item, self.KNOWN_STRING_FIELDS_REPORTS))

        return cleaned_reports

    def get_fundamental_data(self, n_quarters: int = 4) -> dict:
        """
        Fetches, cleans, and structures all fundamental data for the ticker.
        This version assumes successful API calls and well-formed data for simplification,
        meaning it does not explicitly check for error keys (e.g. 'request_error') in
        the raw_data before processing, relying on `_fetch_from_api` to return
        at least an empty dict or a dict with an error message.
        Args:
            n_quarters (int): The number of recent quarters to include for quarterly reports.
        Returns:
            dict: A dictionary containing cleaned "overview" and "quarterly_*" reports.
                  If API calls failed, the corresponding entries might contain error dicts
                  from `_fetch_from_api` or be empty lists/dicts.
        """
        self._fetch_all_data()

        cleaned_fundamental_data = {}

        cleaned_fundamental_data["overview"] = self._process_overview_data()

        for _, config_details in self.QUARTERLY_REPORT_CONFIGS.items():
            output_key = config_details["output_key"]
            cleaned_fundamental_data[output_key] = self._process_single_quarterly_report(
                report_config=config_details, n_quarters=n_quarters
            )

        return cleaned_fundamental_data
