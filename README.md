# <u>TIME SERIES BASED RISK ANALYSIS APP FOR CRYPTOCURRENCY TRADING</u>

<img src="Images/Readme images/Intro image.jpeg" width="500" height="300">

|  | GROUP 5 MEMBERS | GITHUB | 
| --- | --- | --- |
| 1. | MATTHEWS TREVOR | https://github.com/Vetre23 |
| 2. | STEPHEN WAWERU | https://github.com/stendewa|
| 3. | CAROL MUNDIA | https://github.com/WairimuMundia |
| 4. | LILIAN MULI | https://github.com/mwikali24 |
| 5. | PETER MAINA | https://github.com/Mr-PeterMaina |

> ### PROJECT OVERVIEW
* As the cryptocurrency market grows, investors face increasing challenges in making informed trading decisions. 
* Our proposed application, CryptoRisk Analyzer, aims to provide a comprehensive risk analysis tool for the top trading cryptocurrencies. 
* By leveraging time series forecasting and machine learning metrics, this app will help users compare cryptocurrencies and assess their potential risks before making investment decisions.

> ### KEY FEATURES
1. Time Series Analysis: Utilize historical price data for top cryptocurrencies (e.g., Bitcoin, Ethereum, Cardano) to identify trends, seasonality, and volatility. This will form the basis for forecasting future prices.
2. Machine Learning Integration: Implement machine learning models, such as ARIMA, LSTM, and regression analysis, to predict future price movements. Metrics such as Mean Squared Error (MSE) will measure the accuracy of these predictions, allowing users to gauge the reliability of forecasts.
3. Risk Assessment Metrics: Calculate risk factors based on volatility, drawdowns, and historical performance. Provide users with an intuitive risk score for each cryptocurrency, helping them to evaluate their risk tolerance.
4. Cryptocurrency Comparison: Users can select two cryptocurrencies for side-by-side comparison. The app will generate a comprehensive report detailing the predicted price movements, risk assessments, and machine learning accuracy metrics (e.g. MSE).
5. User-Friendly Interface: A web-based application with an intuitive UI will allow users to easily navigate through different cryptocurrencies, access analysis reports, and visualize historical trends through interactive graphs and charts.

> ### BENEFITS
* Informed Decision-Making: Equip investors with the necessary tools and insights to make well-informed trading decisions, potentially leading to higher returns.
* Real-Time Updates: Continuous data analysis and updates ensure users receive the most current insights based on market fluctuations.
* Risk Management: Help users understand and mitigate risks associated with cryptocurrency investments, enhancing their overall investment strategy.

> ### TARGET AUDIENCE
1. Individual investors looking to optimize their cryptocurrency portfolios.
2. Financial advisors and analysts seeking reliable tools for crypto asset evaluation.
3. Educational platforms aiming to teach risk analysis and investment strategies in the cryptocurrency space.

> ### DATA SOURCE
* We scraped the data from [CoinGecko](https://www.coingecko.com/en/all-cryptocurrencies).  
* Cryptocurrency that we wanted to focus on were cardano, bitcoin, ethereum, tether, dogecoin, binancecoin, ripple.

> ### PROJECT METHODOLOGY
The project will use the CRISP-DM that is Cross-Industry Standard Process for Data Mining methodology, which has several stages:
   
  * Business understanding   
  * Data Understanding  
  * Data preparation  
  * Modeling  
  * Evaluation  
  * Deployment 

> ### DATA PREPARATION
* We Checked for missing values, duplicates and unique values in each column. 
* We did Log Transformation to reduce the effect of extreme price values and compress the scale.
* Target Variable: **Price**

### EXPLANATORY DATA ANALYSIS
>                       🌟 **UNIVARIATE ANALYSIS OF PRICE FEATURE** 🌟   
| Bitcoin | Dogecoin | Ethereum |
| ---- | ---- | ----|
|![Bitcoin](<Images/Readme images/1. Univariate Analysis/Bitcoin Price_distribution.png>)|![Dogecoin](<Images/Readme images/1. Univariate Analysis/Dogecoin Price_distribution.png>)|![Ethereum](<Images/Readme images/1. Univariate Analysis/Ethereum Price_distribution.png>)|  

| Ripple | Tether | Cardano |
| ---- | ---- | ----|
|![Ripple](<Images/Readme images/1. Univariate Analysis/Ripple Price_distribution.png>)|![Tether](<Images/Readme images/1. Univariate Analysis/Tether Price_distribution.png>)|![Cardano](<Images/Readme images/1. Univariate Analysis/Cardano Price_distribution.png>)| 

>                       🌟 **BIVARIATE ANALYSIS OF PRICE FEATURE** 🌟

| Bitcoin vs Binancecoin | Bitcoin vs Dogecoin | Bitcoin vs Ethereum |
| ---- | ---- | ----|
| ![Bitcoin vs Binancecoin](<Images/Readme images/2. Bivariate Analysis/1. Bitcoin vs Binancecoin.png>) | ![Bitcoin vs Dogecoin](<Images/Readme images/2. Bivariate Analysis/2. Bitcoin vs Dogecoin.png>) | ![Bitcoin vs Ethereum](<Images/Readme images/2. Bivariate Analysis/3. Bitcoin vs Ethereum.png>) |

| Bitcoin vs Ripple | Bitcoin vs Tether | Bitcoin vs Cardano |
| ---- | ---- | ----|
| ![Bitcoin vs Ripple](<Images/Readme images/2. Bivariate Analysis/4. Bitcoin vs Ripple.png>) |![Bitcoin vs Tether](<Images/Readme images/2. Bivariate Analysis/5. Bitcoin vs Tether.png>) | ![Bitcoin vs Cardano](<Images/Readme images/2. Bivariate Analysis/6. Bitcoin vs cardano.png>) |

>                        🌟 **MULTIVARIATE ANALYSIS** 🌟
![Correlation Matrix](<Images/Readme images/3. Multivariate Analysis/Correlation Matrix.png>)
                     
>  ### DATA MODELLING
The models used are:  
  *   ARIMA ➤ Auto Regressive Integrated Moving Average  
  *   SARIMA ➤ Seasonal Auto Regressive Integrated Moving Average 
  *   Prophet Time Series Model  
 
We concluded on the prophet Time Series Model  

> ### CONCLUSION
 * The low MAE and RMSE values indicate that the prophet model delivers accurate forecast for our dataset.  
 * This metrics demonstrates the model's ability to effectively capture underlying trends and patterns, resulting in minimal prediction errors. 



 