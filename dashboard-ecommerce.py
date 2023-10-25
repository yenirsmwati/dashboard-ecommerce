import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import io
import requests
sns.set(style='dark')

st.title('E-Commerce Dashboard')

st.caption('This is a simple dashboard of e-commerce public dataset. You can see the raw data at this link')
st.markdown("[Click here to visit Public Data E-Commerce](https://drive.google.com/file/d/1MsAjPM7oKtVfJL_wRp1qmCajtSG1mdcK/view)")

# Load data
# Get the raw GitHub URL
url1 = 'https://raw.githubusercontent.com/yenirsmwati/dashboard-ecommerce/main/merge_payment_df.csv'
url2 = 'https://raw.githubusercontent.com/yenirsmwati/dashboard-ecommerce/main/merge_product_df.csv'
url3 = 'https://raw.githubusercontent.com/yenirsmwati/dashboard-ecommerce/main/merge_review_df.csv'


# Fetch the data from the GitHub URLs
response1 = requests.get(url1)
response2 = requests.get(url2)
response3 = requests.get(url3)

# Create file-like objects from the fetched content
file_payment = io.StringIO(response1.content.decode('utf-8'))
file_product = io.StringIO(response2.content.decode('utf-8'))
file_review = io.StringIO(response3.content.decode('utf-8'))

# Read the relative paths
data_review = pd.read_csv(file_review)
data_payment = pd.read_csv(file_payment)
data_product = pd.read_csv(file_product)

#best&worst product
most_sold_product = data_product.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).reset_index().head(10)
most_sold_product = most_sold_product.rename(columns={"order_id": "order"})

least_sold_product = data_product.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=True).reset_index().head(10)
least_sold_product = least_sold_product.rename(columns={"order_id": "order"})

st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order", y="product_category_name", data=most_sold_product.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="order", y="product_category_name", data=least_sold_product.sort_values(by="order", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

with st.expander("Explanation"):
    st.write("""
        The product that buyers are 
        most interested in is the **bed_bath_table** category
        with a total of **9417** sold
        and the products that were sold the least 
        were products in the **security_and_services**
        category, which only sold **2**.""")


st.subheader("Most Common Payment")
#Payment
#Menghitung jumlah penggunaan setiap metode pembayaran
payment_counts = data_payment['payment_type'].value_counts()

payment_count_df = pd.DataFrame({'payment_type': payment_counts.index,'count': payment_counts.values})

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="payment_type", y="count", data=payment_count_df.head(5), palette=colors, ax=ax)
ax.set_ylabel("Count", fontsize=30)
ax.set_xlabel("Payment Type", fontsize=30)
ax.set_title("Most Common Payment", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)


with st.expander("Explanation"):
    st.write("""
        The type of payment most 
        frequently used is a **credit card**
        reaching **86.769** transactions.""")

st.subheader("Customer Review")
# Review

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Calculate satisfaction metrics
product_satisfaction = data_review.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False).reset_index().head(5)
satisfied_customers = data_review[data_review['review_score'] >= 2]['order_id'].nunique()
total_customers = data_review['order_id'].nunique()
satisfied_percentage = (satisfied_customers / total_customers) * 100
unsatisfied_customers = total_customers - satisfied_customers

# Create satisfaction table
satisfaction_table = pd.DataFrame({'Review': ['Puas', 'Tidak Puas'],
                                   'Number Customer': [satisfied_customers, unsatisfied_customers]})

# Create a pie chart
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig1, ax1 = plt.subplots()
ax1.pie(satisfaction_table['Number Customer'], labels=satisfaction_table['Review'], colors=colors, autopct='%1.1f%%')
ax1.set_title('Customer Review')

# Create a bar plot
fig2, ax2 = plt.subplots()
sns.barplot(x="product_category_name", y="review_score", data=product_satisfaction.head(5), palette=colors, ax=ax2)
ax2.set_ylabel("Review Score")
ax2.set_xlabel("Product Category")
ax2.set_title("Satisfaction Product", loc="center", fontsize = 20)
ax2.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=40)

# Display plots side by side
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)

with st.expander("Explanation"):
    st.write("""
        Based on customer reviews, 
        most customers are satisfied 
        with the products they purchase, with **88%**
        of buyers feeling satisfied. The product with the 
        highest average rating is the product in the **cds_dvd_musical**
        category, with an average rating of **4,6**.""")