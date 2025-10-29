from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)


def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
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


# (1) HÀM PHÂN LOẠI KHÁCH HÀNG THEO TÊN PHIM
def classify_customers_by_film(conn):
    """
    Phân loại khách hàng theo tên phim
    Ứng với mỗi film thì cần biết các khách hàng nào đã rental
    """
    sql = """
    SELECT 
        f.film_id,
        f.title AS film_title,
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        c.email,
        r.rental_date,
        r.return_date
    FROM film f
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    JOIN customer c ON r.customer_id = c.customer_id
    ORDER BY f.title, c.customer_id
    """

    df = queryDataset(conn, sql)

    print("=" * 100)
    print("PHÂN LOẠI KHÁCH HÀNG THEO TÊN PHIM")
    print("=" * 100)

    # Nhóm theo film
    films = df['film_title'].unique()

    for film in films[:10]:  # Hiển thị 10 film đầu tiên
        film_data = df[df['film_title'] == film]

        print(f"\n{'=' * 60}")
        print(f"PHIM: {film}")
        print(f"Số lượng khách hàng đã thuê: {len(film_data)}")
        print(f"{'=' * 60}")

        # Hiển thị thông tin khách hàng
        customer_info = film_data[['customer_id', 'customer_name', 'email', 'rental_date']]
        print(tabulate(customer_info.head(10), headers='keys', tablefmt='grid'))

        if len(film_data) > 10:
            print(f"... và {len(film_data) - 10} khách hàng khác")

    return df


# (2) HÀM PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY
def classify_customers_by_category(conn):
    """
    Phân loại khách hàng theo category
    Ứng với mỗi Category thì cần biết các khách hàng nào đã rental
    Loại bỏ dữ liệu trùng lặp
    """
    sql = """
    SELECT DISTINCT
        cat.category_id,
        cat.name AS category_name,
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        c.email,
        c.create_date AS customer_since
    FROM category cat
    JOIN film_category fc ON cat.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    JOIN inventory i ON f.film_id = i.film_id
    JOIN rental r ON i.inventory_id = r.inventory_id
    JOIN customer c ON r.customer_id = c.customer_id
    ORDER BY cat.name, c.customer_id
    """

    df = queryDataset(conn, sql)

    print("\n" + "=" * 100)
    print("PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY")
    print("=" * 100)

    # Nhóm theo category
    categories = df['category_name'].unique()

    for category in categories:
        category_data = df[df['category_name'] == category]

        print(f"\n{'=' * 60}")
        print(f"THỂ LOẠI: {category}")
        print(f"Số lượng khách hàng đã thuê: {len(category_data)}")
        print(f"{'=' * 60}")

        # Hiển thị thông tin khách hàng
        customer_info = category_data[['customer_id', 'customer_name', 'email', 'customer_since']]
        print(tabulate(customer_info.head(10), headers='keys', tablefmt='grid'))

        if len(category_data) > 10:
            print(f"... và {len(category_data) - 10} khách hàng khác")

    return df


# (3) HÀM GOM CỤM KHÁCH HÀNG VỀ MỨC ĐỘ QUAN TÂM FILM VÀ INVENTORY
def cluster_customers_by_film_interest(conn):
    """
    Gom cụm khách hàng về mức độ quan tâm Film và Inventory
    Đề xuất thuộc tính:
    - Tổng số lần thuê
    - Số lượng film khác nhau đã thuê
    - Số lượng thể loại khác nhau đã thuê
    - Tần suất thuê (số ngày trung bình giữa các lần thuê)
    - Tỷ lệ film trả muộn
    """

    # Lấy dữ liệu cho clustering
    sql = """
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        -- Tổng số lần thuê
        COUNT(r.rental_id) AS total_rentals,
        -- Số lượng film khác nhau đã thuê
        COUNT(DISTINCT f.film_id) AS unique_films_rented,
        -- Số lượng thể loại khác nhau đã thuê
        COUNT(DISTINCT cat.category_id) AS unique_categories_rented,
        -- Tần suất thuê (số ngày giữa lần thuê đầu và cuối / số lần thuê)
        CASE 
            WHEN COUNT(r.rental_id) > 1 THEN 
                DATEDIFF(MAX(r.rental_date), MIN(r.rental_date)) / COUNT(r.rental_id)
            ELSE 0 
        END AS rental_frequency,
        -- Tỷ lệ film trả muộn
        AVG(CASE WHEN r.return_date > r.rental_date + INTERVAL f.rental_duration DAY THEN 1 ELSE 0 END) AS late_return_rate,
        -- Tổng tiền đã chi
        SUM(p.amount) AS total_spent,
        -- Số lần thuê film mới (release_year gần đây)
        SUM(CASE WHEN f.release_year > 2005 THEN 1 ELSE 0 END) AS new_films_rented
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    LEFT JOIN payment p ON r.rental_id = p.rental_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    HAVING total_rentals > 0
    """

    df = queryDataset(conn, sql)

    print("\n" + "=" * 100)
    print("DỮ LIỆU CHO CLUSTERING KHÁCH HÀNG")
    print("=" * 100)
    print(df.head())
    print(f"\nTổng số khách hàng: {len(df)}")

    # Chuẩn hóa dữ liệu
    features = ['total_rentals', 'unique_films_rented', 'unique_categories_rented',
                'rental_frequency', 'late_return_rate', 'total_spent', 'new_films_rented']

    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow method để tìm số cụm tối ưu
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X_scaled)
        inertia.append(model.inertia_)

    plt.figure(figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method For Optimal Number of Clusters')
    plt.show()

    # Chọn số cụm dựa trên elbow point (giả sử là 4)
    optimal_clusters = 4
    model = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=500, random_state=42)
    clusters = model.fit_predict(X_scaled)

    df['cluster'] = clusters

    # Phân tích các cụm
    print("\n" + "=" * 100)
    print("PHÂN TÍCH CÁC CỤM KHÁCH HÀNG")
    print("=" * 100)

    cluster_analysis = df.groupby('cluster')[features].mean()
    print("\nĐặc điểm trung bình của các cụm:")
    print(tabulate(cluster_analysis, headers='keys', tablefmt='grid'))

    # Mô tả từng cụm
    cluster_descriptions = {
        0: "Khách hàng thông thường - thuê ít, ít thể loại",
        1: "Khách hàng tích cực - thuê nhiều, đa dạng thể loại",
        2: "Khách hàng trung thành - thuê film mới, ít trả muộn",
        3: "Khách hàng đặc biệt - chi tiêu cao, thuê nhiều film mới"
    }

    for cluster_num in range(optimal_clusters):
        cluster_data = df[df['cluster'] == cluster_num]
        print(f"\n{'=' * 60}")
        print(f"CỤM {cluster_num}: {cluster_descriptions.get(cluster_num, 'Chưa xác định')}")
        print(f"Số lượng: {len(cluster_data)} khách hàng")
        print(f"{'=' * 60}")

        # Hiển thị đặc điểm nổi bật
        avg_rentals = cluster_data['total_rentals'].mean()
        avg_categories = cluster_data['unique_categories_rented'].mean()
        avg_spent = cluster_data['total_spent'].mean()

        print(f"- Số lần thuê trung bình: {avg_rentals:.1f}")
        print(f"- Số thể loại trung bình: {avg_categories:.1f}")
        print(f"- Chi tiêu trung bình: ${avg_spent:.2f}")
        print(f"- Tỷ lệ trả muộn: {cluster_data['late_return_rate'].mean() * 100:.1f}%")

        # Hiển thị 5 khách hàng tiêu biểu
        print(f"\n5 khách hàng tiêu biểu trong cụm:")
        sample_customers = cluster_data[['customer_id', 'customer_name', 'total_rentals', 'total_spent']].head()
        print(tabulate(sample_customers, headers='keys', tablefmt='grid'))

    # Trực quan hóa kết quả bằng PCA (giảm chiều dữ liệu)
    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Customer Clusters based on Film Rental Behavior')

    # Thêm chú thích cho các cụm
    for i, desc in cluster_descriptions.items():
        cluster_points = X_pca[clusters == i]
        if len(cluster_points) > 0:
            center = cluster_points.mean(axis=0)
            plt.annotate(f'Cluster {i}: {desc}', center,
                         xytext=(10, 10), textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7),
                         fontsize=8)

    plt.show()

    # Trực quan hóa 3D nếu có đủ dữ liệu
    try:
        pca_3d = PCA(n_components=3)
        X_pca_3d = pca_3d.fit_transform(X_scaled)

        fig = px.scatter_3d(
            x=X_pca_3d[:, 0], y=X_pca_3d[:, 1], z=X_pca_3d[:, 2],
            color=clusters,
            hover_data=[df['customer_name'], df['total_rentals'], df['total_spent']],
            title="3D Visualization of Customer Clusters",
            labels={'color': 'Cluster'}
        )
        fig.show()
    except Exception as e:
        print(f"Không thể tạo visualization 3D: {e}")

    return df


# HÀM CHÍNH
def main():
    # Kết nối đến database sakila
    conn = getConnect('localhost', 3306, 'sakila', 'root', '@Bb13042005')

    if conn is None:
        print("Không thể kết nối đến database sakila")
        return

    try:
        # (1) Phân loại khách hàng theo tên phim
        film_customers_df = classify_customers_by_film(conn)

        # (2) Phân loại khách hàng theo category
        category_customers_df = classify_customers_by_category(conn)

        # (3) Gom cụm khách hàng về mức độ quan tâm film
        clustered_customers_df = cluster_customers_by_film_interest(conn)

        # Xuất kết quả ra file
        clustered_customers_df.to_csv('customer_clusters_sakila.csv', index=False)
        print(f"\nĐã lưu kết quả clustering vào file: customer_clusters_sakila.csv")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        closeConnection(conn)


if __name__ == "__main__":
    main()