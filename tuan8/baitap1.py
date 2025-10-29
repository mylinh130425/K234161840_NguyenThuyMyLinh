from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
from tabulate import tabulate
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        # Cấu hình MySQL
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
    return None

def closeConnection(conn):
    if conn is not None:
        conn.close()

def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    if not df.empty:
        df.columns = [i[0] for i in cursor.description]
    return df

# BÀI TẬP 1 - HÀM XUẤT DANH SÁCH CHI TIẾT CUSTOMER THEO CỤM

def export_cluster_details_console(df, cluster_column='cluster'):
    """
    (1) Xuất danh sách chi tiết Customer theo cụm ra console
    """
    print("DANH SÁCH CHI TIẾT KHÁCH HÀNG THEO CỤM - CONSOLE OUTPUT")

    clusters = sorted(df[cluster_column].unique())

    for cluster_num in clusters:
        cluster_data = df[df[cluster_column] == cluster_num]

        print(f"\n{'=' * 80}")
        print(f"CỤM {cluster_num} - Số lượng khách hàng: {len(cluster_data)}")
        print(f"{'=' * 80}")

        # Thống kê cụm
        numeric_columns = ['Age', 'Annual_Income', 'Spending_Score']
        available_numeric = [col for col in numeric_columns if col in df.columns]

        if available_numeric:
            print("Thống kê cụm:")
            for col in available_numeric:
                if col in cluster_data.columns:
                    print(f"  - {col} trung bình: {cluster_data[col].mean():.2f}")

        # Hiển thị chi tiết từng khách hàng
        print(f"\nDanh sách khách hàng trong cụm {cluster_num}:")

        # Hiển thị tất cả các cột trừ cột cluster
        display_columns = [col for col in df.columns if col != cluster_column]

        if len(cluster_data) <= 20:
            print(tabulate(cluster_data[display_columns],
                           headers='keys',
                           tablefmt='grid',
                           maxcolwidths=15))
        else:
            print(tabulate(cluster_data[display_columns].head(20),
                           headers='keys',
                           tablefmt='grid',
                           maxcolwidths=15))
            print(f"... và {len(cluster_data) - 20} khách hàng khác")

def export_cluster_details_web(df, cluster_column='cluster', filename='cluster_results.html'):
    """
    (2) Xuất danh sách chi tiết Customer theo cụm ra file HTML
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kết Quả Phân Cụm Khách Hàng</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background-color: #f5f5f5;
            }
            .header { 
                background-color: #2c3e50; 
                color: white; 
                padding: 20px; 
                text-align: center; 
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .cluster { 
                margin-bottom: 30px; 
                border: 2px solid #3498db; 
                padding: 20px; 
                border-radius: 10px; 
                background-color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .cluster-header { 
                background-color: #3498db; 
                color: white; 
                padding: 15px; 
                border-radius: 5px;
                margin-bottom: 15px;
            }
            .stats { 
                background-color: #ecf0f1; 
                padding: 15px; 
                border-radius: 5px; 
                margin-bottom: 15px;
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 10px;
            }
            th, td { 
                border: 1px solid #bdc3c7; 
                padding: 10px; 
                text-align: left; 
            }
            th { 
                background-color: #34495e; 
                color: white; 
            }
            tr:nth-child(even) { 
                background-color: #f2f2f2; 
            }
            .summary {
                background-color: #e74c3c;
                color: white;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>KẾT QUẢ PHÂN CỤM KHÁCH HÀNG</h1>
            <p>Phân tích dữ liệu khách hàng sử dụng thuật toán K-Means</p>
        </div>
    """

    # Tổng quan
    total_customers = len(df)
    clusters = sorted(df[cluster_column].unique())

    html_content += f"""
        <div class="summary">
            <h2>TỔNG QUAN</h2>
            <p>Tổng số khách hàng: {total_customers}</p>
            <p>Số cụm: {len(clusters)}</p>
        </div>
    """

    # Chi tiết từng cụm
    for cluster_num in clusters:
        cluster_data = df[df[cluster_column] == cluster_num]

        html_content += f"""
        <div class="cluster">
            <div class="cluster-header">
                <h2>CỤM {cluster_num} - {len(cluster_data)} KHÁCH HÀNG</h2>
            </div>
        """

        # Thống kê cụm
        numeric_columns = ['Age', 'Annual_Income', 'Spending_Score']
        available_numeric = [col for col in numeric_columns if col in df.columns]

        if available_numeric:
            html_content += '<div class="stats"><h3>Thống kê cụm:</h3><ul>'
            for col in available_numeric:
                if col in cluster_data.columns:
                    html_content += f'<li><strong>{col}</strong> trung bình: {cluster_data[col].mean():.2f}</li>'
            html_content += '</ul></div>'

        # Bảng chi tiết khách hàng
        html_content += '<h3>Danh sách khách hàng:</h3>'
        html_content += '<table>'

        # Header
        display_columns = [col for col in df.columns if col != cluster_column]
        html_content += '<tr>'
        for col in display_columns:
            html_content += f'<th>{col}</th>'
        html_content += '</tr>'

        # Data rows
        for _, row in cluster_data.iterrows():
            html_content += '<tr>'
            for col in display_columns:
                html_content += f'<td>{row[col]}</td>'
            html_content += '</tr>'

        html_content += '</table>'
        html_content += '</div>'

    html_content += """
        </body>
        </html>
    """

    # Ghi file HTML
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Đã xuất kết quả ra file: {filename}")

# CÁC HÀM CLUSTERING

def showHistogram(df, columns):
    plt.figure(1, figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha=0.5)
    plt.xlabel('Number of Clusters'), plt.ylabel('Cluster sum of squared distances')
    plt.show()

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(18, 10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s=100,
                    c=colors[i],
                    label=f'Cluster {i + 1}')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def visualize3DKMeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df,
                        x=columns[0],
                        y=columns[1],
                        z=columns[2],
                        color='cluster',
                        hover_data=hover_data,
                        category_orders={"cluster": range(0, cluster)},
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

# KẾT NỐI DATABASE VÀ THỰC HIỆN CLUSTERING

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Bb13042005')

# Lấy dữ liệu từ cả 2 bảng customer và customer_spend_score
sql2 = """SELECT c.CustomerId, c.Name, c.Gender, c.Age, 
                 cs.Annual_Income, cs.Spending_Score 
          FROM customer c 
          JOIN customer_spend_score cs ON c.CustomerId = cs.CustomerID"""

df2 = queryDataset(conn, sql2)
print("Dữ liệu khách hàng:")
print(df2.head())

colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]

# TRƯỜNG HỢP 1: Gom cụm theo Age và Spending_Score
print("\n" + "=" * 80)
print("TRƯỜNG HỢP 1: GOM CỤM THEO AGE VÀ SPENDING_SCORE")
print("=" * 80)

columns = ['Age', 'Spending_Score']
elbowMethod(df2, columns)

# Giả sử elbow point là 4
cluster = 4
X = df2.loc[:, columns].values
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["cluster_case1"] = labels

print("y_kmeans:", y_kmeans)
print("centroids:", centroids)
print("labels:", labels)

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

# TRIỆU GỌI HÀM BÀI TẬP 1 - TRƯỜNG HỢP 1
print("\nXUẤT KẾT QUẢ TRƯỜNG HỢP 1:")
export_cluster_details_console(df2, 'cluster_case1')
export_cluster_details_web(df2, 'cluster_case1', 'cluster_results_case1.html')

# TRƯỜNG HỢP 2: Gom cụm theo Annual_Income và Spending_Score
print("\n" + "=" * 80)
print("TRƯỜNG HỢP 2: GOM CỤM THEO ANNUAL_INCOME VÀ SPENDING_SCORE")
print("=" * 80)

columns = ['Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

# Giả sử elbow point là 5
cluster = 5
X = df2.loc[:, columns].values
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["cluster_case2"] = labels

print("y_kmeans:", y_kmeans)
print("centroids:", centroids)
print("labels:", labels)

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)

# TRIỆU GỌI HÀM BÀI TẬP 1 - TRƯỜNG HỢP 2
print("\nXUẤT KẾT QUẢ TRƯỜNG HỢP 2:")
export_cluster_details_console(df2, 'cluster_case2')
export_cluster_details_web(df2, 'cluster_case2', 'cluster_results_case2.html')

# TRƯỜNG HỢP 3: Gom cụm 3D theo Age, Annual_Income và Spending_Score
print("\n" + "=" * 80)
print("TRƯỜNG HỢP 3: GOM CỤM 3D THEO AGE, ANNUAL_INCOME VÀ SPENDING_SCORE")
print("=" * 80)

columns = ['Age', 'Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

# Giả sử elbow point là 6
cluster = 6
X = df2.loc[:, columns].values
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["cluster_case3"] = labels

print("y_kmeans:", y_kmeans)
print("centroids:", centroids)
print("labels:", labels)

# Visualize 3D
hover_data = df2.columns
visualize3DKMeans(df2, columns, hover_data, cluster)

# TRIỆU GỌI HÀM BÀI TẬP 1 - TRƯỜNG HỢP 3
print("\nXUẤT KẾT QUẢ TRƯỜNG HỢP 3:")
export_cluster_details_console(df2, 'cluster_case3')
export_cluster_details_web(df2, 'cluster_case3', 'cluster_results_case3.html')

closeConnection(conn)

print("\nHOÀN TẤT BÀI TẬP 1!")
print("Các file HTML đã được tạo:")
print("- cluster_results_case1.html")
print("- cluster_results_case2.html")
print("- cluster_results_case3.html")