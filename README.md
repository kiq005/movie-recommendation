# Movie Recommendation
Um sistema inteligente de recomendação de filmes.

# Dados

### Frequência de palavras:
Word | Count | Word | Count
---- | ----- | ---- | -----
the | 12695 | in | 4058
a | 9340 | his | 3883
to | 7849 | is | 3318
and | 7267 | with | 2349
of | 6847 | her | 1968

### Frequência de palavras (Sem _stop words_):
Word | Count | Word | Count
---- | ----- | ---- | -----
life | 804 | two | 538
new | 714 | man | 506
one | 685 | family | 496
young | 629 | find | 473
world | 568 | story | 450

![CLOUD](assets/tokens_cloud.png)

# Clusters

### Jaccard Distance
Método   | Matriz de Distância | Dendrograma
-------- | ------------------- | -----------
Single   | ![](assets/clusters_jaccard_distance_single.png) | ![](assets/dendrogram_jaccard_distance_single.png)
Complete | ![](assets/clusters_jaccard_distance_complete.png) | ![](assets/dendrogram_jaccard_distance_complete.png)
Average  | ![](assets/clusters_jaccard_distance_average.png) | ![](assets/dendrogram_jaccard_distance_average.png)
Ward     | ![](assets/clusters_jaccard_distance_ward.png) | ![](assets/dendrogram_jaccard_distance_ward.png)

### Masi Distance
Método   | Matriz de Distância | Dendrograma
-------- | ------------------- | -----------
Single   | ![](assets/clusters_masi_distance_single.png) | ![](assets/dendrogram_masi_distance_single.png)
Complete | ![](assets/clusters_masi_distance_complete.png) | ![](assets/dendrogram_masi_distance_complete.png)
Average  | ![](assets/clusters_masi_distance_average.png) | ![](assets/dendrogram_masi_distance_average.png)
Ward     | ![](assets/clusters_masi_distance_ward.png) | ![](assets/dendrogram_masi_distance_ward.png)

### Edit Distance
Método   | Matriz de Distância | Dendrograma
-------- | ------------------- | -----------
Single   | ![](assets/clusters_edit_distance_single.png) | ![](assets/dendrogram_edit_distance_single.png)
Complete | ![](assets/clusters_edit_distance_complete.png) | ![](assets/dendrogram_edit_distance_complete.png)
Average  | ![](assets/clusters_edit_distance_average.png) | ![](assets/dendrogram_edit_distance_average.png)
Ward     | ![](assets/clusters_edit_distance_ward.png) | ![](assets/dendrogram_edit_distance_ward.png)

