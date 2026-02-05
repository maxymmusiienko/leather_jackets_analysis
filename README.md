# Leather Jacket Market Analysis: Data Engineering and Statistical Modeling

## Project Overview
This project focuses on identifying price determinants in the second-hand leather jacket market by aggregating data from local and international e-commerce platforms. The study involves a full data lifecycle: from building robust web scrapers and engineering complex data pipelines to performing econometric modeling and hypothesis testing. The goal is to quantify how branding, item condition, and geographic location influence market value.

---

## Phase 1: Data Acquisition
Data was collected from three distinct sources representing both local and large-scale international markets:
* **eBay:** 11,091 listings (International)
* **Vinted:** 985 listings (International/C2C)
* **OLX:** 1,040 listings (Local)

### Technical Implementation
* **Tools:** Developed using **BeautifulSoup4** for static parsing and **Playwright** for handling dynamic content and JavaScript-heavy pages.
* **Architecture:** Implemented an **Abstract Base Class** for scrapers, ensuring a modular and scalable design. Each store-specific scraper inherits from this base class, promoting code reusability and consistent data output.

---

## Phase 2: Data Engineering and Enrichment
The raw data arrived in varying formats for fields such as price (different currencies), location, and condition.

### The Enrichment Pipeline
* **Enricher Logic:** Created a base `Enricher` class with specific implementations for each platform to standardize currency conversion, geographic coding, and condition mapping.
* **Brand Detection:** Integrated the **FlashText** library to scan listing titles against a predefined dictionary of luxury and mass-market brands, significantly improving processing speed over standard Regex.
* **Consolidation:** Utilized the **Factory Pattern** to merge disparate CSV files into a unified dataset.

### Final Dataset Schema
The pipeline produced a cleaned dataset with the following features:
* `title`, `condition`, `price`, `location` (Original data)
* `price($)`: Normalized USD value.
* `country_code`: ISO 3166-1 alpha-2 codes.
* `store_name`, `store_type`: (Local vs. International).
* `simple_condition`: Categorized into "New" or "Used".
* `brand`, `has_brand`: Extracted branding information.
* `title_length`: Character count for listing titles.

---

## Phase 3: Exploratory Data Analysis (EDA) and Preprocessing
Before modeling, the data underwent rigorous statistical validation.

### Outlier Removal
Applied the **Interquartile Range (IQR)** method to remove price and title length anomalies. A critical domain-specific adjustment was made: the term **"Vintage"** was reclassified from a brand to a description (`has_brand = False`) to prevent skewing the premium brand coefficient.

### Distribution Analysis
* **Log Transformation:** Performed log-transformation on `price($)` and `title_length` to address right-skewness and stabilize variance.
* **Normality Testing:** Validated distributions using **D'Agostino's K^2 test** and **Q-Q plots**.



---

## Phase 4: Hypothesis Testing
Utilized the non-parametric **Mann-Whitney U Test** to compare price distributions across different segments without assuming normality.

* **Geographic Hypothesis:** Tested whether listings from specific regions (e.g., Pakistan vs. Ukraine vs. UK) exhibited statistically significant price differences.
* **Store Type Hypothesis:** Evaluated if "International" platforms command a price premium over "Local" platforms.
* **Branding Impact:** Confirmed that branded items significantly outperform non-branded items in resale value ($p < 0.001$).

---

## Phase 5: Econometric Modeling
An **Ordinary Least Squares (OLS) Regression** was constructed to quantify the impact of each feature on the `log_price`.

### Model Specification
$$\ln(\text{Price}) = \beta_0 + \beta_1 \ln(\text{TitleLength}) + \beta_2 \text{HasBrand} + \beta_3 \text{ConditionUsed} + \epsilon$$

### Model Performance
* **R-squared:** 0.351 (The model explains 35.1% of price variance).
* **F-statistic:** 2127 (Highly significant overall model).

### Key Insights
| Variable | Coefficient | P-value | Interpretation                                                                    |
| :--- | :--- | :--- |:----------------------------------------------------------------------------------|
| **log_title_length** | 0.4508 | 0.000 | A 1% increase in title length correlates to a **45,08%** increase in price.       |
| **has_brand** | 0.2593 | 0.000 | Branded items command a **29.6%** premium over unbranded ones ($e^{0.2593} - 1$). |
| **simple_condition_Used** | -0.5510 | 0.000 | Used items are valued **42.4%** lower than new items ($e^{-0.5510} - 1$).         |

### Model Diagnostics
* **Residual Analysis:** The Residuals vs. Fitted plot showed a horizontal LOWESS line centered at zero, indicating no significant bias in the model.
* **Multicollinearity:** The correlation matrix confirmed that features were sufficiently independent, with the highest correlation (-0.51) between price and condition.



---

## Technical Stack
* **Languages:** Python
* **Data Engineering:** Pandas, NumPy, FlashText
* **Web Scraping:** Playwright, BeautifulSoup4
* **Statistics & ML:** Scipy, Statsmodels
* **Visualization:** Matplotlib, Seaborn

---
*Developed by Maksym Musiienko*