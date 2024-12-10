import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, abs, when
from pyspark.sql.types import DateType
import statsmodels.api as sm
import io
import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/home/site/wwwroot/spark"
os.environ["PATH"] += f':{os.environ["SPARK_HOME"]}/bin:{os.environ["SPARK_HOME"]}/sbin'

class dataAnalytics:
    def __init__(self, name):
        self.company_name = name
        self.spark = SparkSession.builder.appName("StockifyAnalytics").master("local[*]").getOrCreate()

    def fetch_company_details(self, name):
        
        import yfinance as yf
        return yf.Ticker(name)

    def get_historical_data(self, name):
        import yfinance as yf
        data = yf.download(name, period="max")
        csv_path = f"/tmp/{name}_historical.csv"
        data.to_csv(csv_path)
        
        spark_df = self.spark.read.csv(csv_path, header=True, inferSchema=True)
        return spark_df

    def plot_closing_prices(self, spark_df):
        pdf = spark_df.select("Date", "Close").orderBy("Date").toPandas()

        plt.figure(figsize=(12, 6))
        cpot = io.BytesIO()
        plt.plot(pdf["Date"], pdf["Close"], label='Close Price')
        plt.title('Stock Closing Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()

        plt.savefig(cpot, format='jpeg')
        plt.close()
        cpot.seek(0)
        return cpot

    def plot_volume_traded(self, spark_df):
        pdf = spark_df.select("Date", "Volume").orderBy("Date").toPandas()

        plt.figure(figsize=(12, 6))
        vtot = io.BytesIO()
        plt.plot(pdf["Date"], pdf["Volume"], label='Volume')
        plt.title('Stock traded volumes Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()

        plt.savefig(vtot, format='jpeg')
        plt.close()
        vtot.seek(0)
        return vtot

    def plot_intraday_diff(self, spark_df):
        spark_df = spark_df.withColumn(
            "intraday_change", abs(col("Close") - col("Open"))
        )
        
        pdf = spark_df.select("Date", "intraday_change").orderBy("Date").toPandas()

        plt.figure(figsize=(12, 6))
        iddot = io.BytesIO()
        plt.plot(pdf["Date"], pdf["intraday_change"], label='Intraday Difference')
        plt.title('Stock Intraday Difference Prices Over Time')
        plt.xlabel('Date')
        plt.ylabel('Difference')
        plt.legend()
        
        plt.savefig(iddot, format='jpeg')
        plt.close()
        iddot.seek(0)
        return iddot

    def plot_intraday_change_trend(self, spark_df):
        spark_df = spark_df.withColumn(
            "intraday_change", abs(col("Close") - col("Open"))
        )

        spark_df = spark_df.withColumn(
            "intraday_change_trend",
            when((col("Close") - col("Open")) > 0, "positive").otherwise("negative")
        )

        pdf = spark_df.select("Date", "intraday_change", "intraday_change_trend").orderBy("Date").toPandas()

        positive_trend = pdf[pdf['intraday_change_trend'] == 'positive']
        negative_trend = pdf[pdf['intraday_change_trend'] == 'negative']

        plt.figure(figsize=(12, 6))
        plt.plot(positive_trend["Date"], positive_trend["intraday_change"], 'g^', label='Positive Change')
        plt.plot(negative_trend["Date"], negative_trend["intraday_change"], 'rv', label='Negative Change')

        idctot = io.BytesIO()
        plt.title('Intraday Change with Trend')
        plt.xlabel('Date')
        plt.ylabel('Intraday Change')
        plt.legend()

        plt.savefig(idctot, format='jpeg')
        plt.close()
        idctot.seek(0)
        return idctot


    def plot_decomposition(self, spark_df):
        pdf = spark_df.select("Date", "Close").orderBy("Date").toPandas()
        pdf = pdf.set_index("Date")

        decomposition = sm.tsa.seasonal_decompose(pdf["Close"], model='additive', period=5)

        plt.figure(figsize=(12, 8))
        dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(pdf["Close"], label='Original')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonality')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residuals')
        plt.legend(loc='upper left')
        plt.tight_layout()
        
        plt.savefig(dec, format='jpeg')
        plt.close()
        dec.seek(0)
        return dec
    
    def get_crisis_covid_data(self, spark_df):
        covid_start = "2020-03-01"
        covid_end = "2021-12-31"
        crisis_start = "2007-07-01"
        crisis_end = "2009-06-30"

        covid_data = spark_df.filter(
            (col("Date") >= covid_start) & (col("Date") <= covid_end)
        )

        crisis_data = spark_df.filter(
            (col("Date") >= crisis_start) & (col("Date") <= crisis_end)
        )

        return crisis_data, covid_data

    def plot_rec_analysis(self, crisis_data):
        pdf = crisis_data.select("Date", "Close", "Volume").orderBy("Date").toPandas()

        plt.figure(figsize=(12, 6))
        crisis_cpot = io.BytesIO()
        plt.plot(pdf["Date"], pdf["Close"], label="Close Price")
        plt.title("Stock Closing Prices During Recession")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.legend()

        plt.savefig(crisis_cpot, format="jpeg")
        plt.close()
        crisis_cpot.seek(0)

        crisis_vtot = io.BytesIO()
        plt.figure(figsize=(12, 6))
        plt.plot(pdf["Date"], pdf["Volume"], label="Volume")
        plt.title("Stock traded volumes During Recession")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()

        plt.savefig(crisis_vtot, format="jpeg")
        plt.close()
        crisis_vtot.seek(0)

        pdf = pdf.set_index("Date")
        decomposition = sm.tsa.seasonal_decompose(pdf["Close"], model="additive", period=5)

        plt.figure(figsize=(12, 8))
        crisis_dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(pdf["Close"], label="Original")
        plt.legend(loc="upper left")
        plt.subplot(412)
        plt.plot(decomposition.trend, label="Trend")
        plt.legend(loc="upper left")
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label="Seasonality")
        plt.legend(loc="upper left")
        plt.subplot(414)
        plt.plot(decomposition.resid, label="Residuals")
        plt.legend(loc="upper left")
        plt.tight_layout()

        plt.savefig(crisis_dec, format="jpeg")
        plt.close()
        crisis_dec.seek(0)

        return crisis_cpot, crisis_vtot, crisis_dec

    def plot_covid_analysis(self, covid_data):
        pdf = covid_data.select("Date", "Close", "Volume").orderBy("Date").toPandas()

        plt.figure(figsize=(12, 6))
        covid_cpot = io.BytesIO()
        plt.plot(pdf["Date"], pdf["Close"], label="Close Price")
        plt.title("Stock Closing Prices During Covid")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.legend()

        plt.savefig(covid_cpot, format="jpeg")
        plt.close()
        covid_cpot.seek(0)

        covid_vtot = io.BytesIO()
        plt.figure(figsize=(12, 6))
        plt.plot(pdf["Date"], pdf["Volume"], label="Volume")
        plt.title("Stock traded volumes During Covid")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()

        plt.savefig(covid_vtot, format="jpeg")
        plt.close()
        covid_vtot.seek(0)

        pdf = pdf.set_index("Date")
        decomposition = sm.tsa.seasonal_decompose(pdf["Close"], model="additive", period=5)

        plt.figure(figsize=(12, 8))
        covid_dec = io.BytesIO()
        plt.subplot(411)
        plt.plot(pdf["Close"], label="Original")
        plt.legend(loc="upper left")
        plt.subplot(412)
        plt.plot(decomposition.trend, label="Trend")
        plt.legend(loc="upper left")
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label="Seasonality")
        plt.legend(loc="upper left")
        plt.subplot(414)
        plt.plot(decomposition.resid, label="Residuals")
        plt.legend(loc="upper left")
        plt.tight_layout()

        plt.savefig(covid_dec, format="jpeg")
        plt.close()
        covid_dec.seek(0)

        return covid_cpot, covid_vtot, covid_dec
