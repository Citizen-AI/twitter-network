# https://pythonprogramminglanguage.com/kmeans-text-clustering/

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

from library import clean


def cluster(in_csv_file, num_clusters=12):
    people = pd.read_csv(in_csv_file)
    documents = clean(people['text'].tolist())

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    model = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1, verbose=1)
    model.fit(X)

    clusters = model.labels_.tolist()

    people['cluster'] = clusters

    return people

    # print(people)
    # print(people['cluster'].value_counts())


    # print("Top terms per cluster:")
    # order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    # terms = vectorizer.get_feature_names()
    #
    # cluster_names = []
    # for i in range(num_clusters):
    #     cluster_name = ''
    #     for centroid in order_centroids[i, :10]:
    #         cluster_name += terms[centroid] + ' '
    #     cluster_names.append(cluster_name)
    # print(cluster_names)

    # TODO: Label by medoid https://github.com/letiantian/kmedoids or https://stackoverflow.com/questions/21660937/get-nearest-point-to-centroid-scikit-learn

if __name__ == "__main__":
    df = cluster(OUTPUT_FOLDER + 'mps-people-concat-tweets.csv')
    mps = pd.read_csv(OUTPUT_FOLDER + 'mps.csv')
    mps['cluster'] = df['cluster']
    mps.to_csv(OUTPUT_FOLDER + 'mps-with-cluster.csv', index=False, encoding='utf8')
