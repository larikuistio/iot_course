# iot_course

xml_parser.py was used to download temperature data from FMI. It currently downloads data from the time period 1.1.2016-31.12.2020 as that was the time period used in our project. Changing this requires modification to the code. The temperature values and corresponding dates are output to temperatures.txt

csv_read_test.py reads the power consumption values from electricity_hourly.csv, and calculates the average values for each day. This file is downloaded from https://data.fingrid.fi/open-data-forms/search/fi/?selected_datasets=124 and the time period must mach the temperature data. Results are output to electricity.txt and a plot of the power consumption values as a function of temperature is drawn.

remove_outliers.py removes outliers and draws the data points after that. Results are output to data_no_outliers.txt

data_fit.py fits a polynomial to the data points in data_no_outliers.txt and draws the results. It also prints the coefficients of the polynomial.

prediction.py uses a csv file that is again downloaded from https://data.fingrid.fi/open-data-forms/search/fi/?selected_datasets=124, and downloads temperature data from the corresponding time period. It then predicts the power consumption values for that time period based on the polynomial found before and draws a figure showing the result. The code also prints the RMSE, greatest error, smallest error and average error (percentage) values.
