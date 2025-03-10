import os
import time
import numpy as np
import Levenshtein
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from hdbscan import HDBSCAN
from fontTools.ttLib import TTFont
from utils.metadata_handler import get_file_properties
from utils.log import log_message, new_logger

class FontCluster:
    def __init__(self, fontlist):
        self.fontlist = fontlist

        for i in range(0, len(fontlist)):
            ttf = TTFont(fontlist[i]["path"])
            self.fontlist[i]["sfntVersion"] = ttf.sfntVersion
            self.fontlist[i]["tables"] = ttf.keys()

            font_property = get_file_properties(fontlist[i]["path"])
            self.fontlist[i]["Authors"] = font_property.get("Authors")
            self.fontlist[i]["Copyright"] = font_property.get("Copyright")    

        self.table_encoder = self._build_table_encoder()
        self.tfidf_vectorizer_authors = TfidfVectorizer()
        self.tfidf_vectorizer_copyright = TfidfVectorizer()

    # Hàm chính để thực hiện phân cụm font 
    def cluster_fonts(self):
        return self.recursive_clustering(self.fontlist)
    
    # ✅ Tạo bộ mã hóa cho danh sách tables
    def _build_table_encoder(self):
        all_tables = sorted(set(table for font in self.fontlist for table in font["tables"]))
        return {table: idx for idx, table in enumerate(all_tables)}
    
    # ✅ Chuyển sfntVersion thành số
    def _sfnt_to_int(self, sfnt):
        return int.from_bytes(sfnt.encode('latin1'), byteorder='big')
    
    # ✅ Mã hóa danh sách tables (One-Hot Encoding)
    def _encode_tables(self, tables):
        vector = np.zeros(len(self.table_encoder))
        for table in tables:
            vector[self.table_encoder[table]] = 1
        return vector

    # ✅ Trích xuất đặc trưng từ dữ liệu font
    def _extract_features(self):
        authors_text = [font.get("Authors", "") or "" for font in self.fontlist]
        copyright_text = [font.get("Copyright", "") or "" for font in self.fontlist]

        authors_vectors = self.tfidf_vectorizer_authors.fit_transform(authors_text).toarray()
        copyright_vectors = self.tfidf_vectorizer_copyright.fit_transform(copyright_text).toarray()

        feature_vectors = []
        font_names = []

        for idx, font in enumerate(self.fontlist):
            font_vector = [
                self._sfnt_to_int(font["sfntVersion"])  # sfntVersion
            ] + self._encode_tables(font["tables"]).tolist()  # Tables (one-hot)

            font_vector += authors_vectors[idx].tolist()  # Authors
            font_vector += copyright_vectors[idx].tolist()  # Copyright

            feature_vectors.append(font_vector)
            font_names.append(font["name"])

        return np.array(feature_vectors), font_names

    # Tạo ma trận khoảng cách dựa trên Levenshtein Distance
    def compute_distance_matrix(self, fontlist):
        n = len(fontlist)
        distance_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                dist = Levenshtein.distance(fontlist[i]["name"], fontlist[j]["name"])
                distance_matrix[i][j] = dist
                distance_matrix[j][i] = dist  # Ma trận đối xứng
        return distance_matrix

    # Trích xuất thông tin sfntVersion và danh sách tables từ font
    def get_font_properties(self, font):
        try:
            font = TTFont(font["path"])
            sfnt_version = font.sfntVersion
            tables = set(font.keys())
            return sfnt_version, tables
        except Exception as e:
            print(f'❌ Không thể đọc font {font["name"]}: {e}')
            return None, None

    # Kiểm tra tất cả font trong cluster có cùng sfntVersion và tables không 
    def check_cluster_validity(self, cluster):
        if not cluster:
            return False

        first_font = self.get_font_properties(cluster[0])
        if first_font == (None, None):
            return False

        sfnt_version_ref, tables_ref = first_font
        for font in cluster[1:]:
            sfnt_version, tables = self.get_font_properties(font)
            if sfnt_version != sfnt_version_ref or tables != tables_ref:
                return False  # Có sự khác biệt, cần tiếp tục phân cụm
        return True  # Tất cả giống nhau, dừng phân cụm

    # Thực hiện phân cụm đệ quy dựa trên tên font và kiểm tra thuộc tính
    def recursive_clustering(self, fontlist, depth=0, previous_clusters=None, max_depth=10):
        print(f"🔍 Độ sâu {depth}: Đang phân cụm {len(fontlist)} font...")

        if len(fontlist) <= 1 or depth >= max_depth:
            return [fontlist]

        # Lưu trạng thái trước đó của cluster
        if previous_clusters is None:
            previous_clusters = {}

        # Sắp xếp fontlist theo tên font để tạo khóa duy nhất
        cluster_key = tuple(sorted((font["name"]) for font in fontlist))

        if cluster_key in previous_clusters:
            previous_clusters[cluster_key] += 1
            if previous_clusters[cluster_key] >= 4:
                print(f"⚠️ Cụm {cluster_key} không thay đổi sau 4 lần đệ quy. Dừng phân cụm!")
                return [fontlist]
        else:
            previous_clusters[cluster_key] = 1

        # distance_matrix = self.compute_distance_matrix(fontlist)
        feature_matrix, font_names = self._extract_features()

        # Áp dụng thuật toán DBSCAN để nhóm font
        # dbscan = DBSCAN(eps=10, min_samples=2, metric="precomputed")
        # labels = dbscan.fit_predict(distance_matrix)

        hdbscan = HDBSCAN(min_cluster_size=2, metric="euclidean")
        labels = hdbscan.fit_predict(feature_matrix)

        # Gom nhóm các font theo cluster
        clusters = {}
        for idx, label in enumerate(labels):
            if idx >= len(fontlist):
                # print(f"⚠️ Lỗi: idx ({idx}) vượt phạm vi fontlist (size {len(fontlist)})!")
                continue  # Tránh lỗi index out of range

            if label == -1:
                log_message(f"⚠️ Cảnh báo: Font {fontlist[idx]['name']} bị gán nhãn nhiễu (-1), bỏ qua.")
                continue  # Loại bỏ các điểm nhiễu

            if label not in clusters:
                clusters[label] = []
            clusters[label].append(fontlist[idx])

        # Kiểm tra tính hợp lệ của từng cluster
        final_clusters = []
        for cluster in clusters.values():
            if self.check_cluster_validity(cluster):
                final_clusters.append(cluster)
            else:
                # Nếu chưa thỏa điều kiện, tiếp tục đệ quy chia nhỏ
                sub_clusters = self.recursive_clustering(cluster, depth + 1, previous_clusters, max_depth)
                final_clusters.extend(sub_clusters)

        return final_clusters

    
