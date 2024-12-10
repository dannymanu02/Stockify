#!/bin/bash

# Install Java (required by Spark)
apt-get update && apt-get install -y openjdk-11-jdk wget

# Set Java environment variables
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

# Install Spark
SPARK_VERSION=3.4.1
HADOOP_VERSION=3
wget https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
tar -xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /home/site/wwwroot/spark

# Update PATH for Spark
export SPARK_HOME=/home/site/wwwroot/spark
export PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# Start the application
python app.py
