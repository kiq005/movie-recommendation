# Source Code
O dataset original está no formato .csv, utilize o programa `csv_to_json.py` para criar uma versão .json, contendo o nome (original e inglês), votos (média e contagem), tagline e sumário.

Utilize o programa `dist_matrix.py` para gerar a matriz de distânciamento com base no sumário dos filmes. Será gerado um arquivo .txt, e outro .npy, que podem ser utilizados para gerar vizualizações.

# Requisitos
Python ≥ 3.4
* nltk
* numpy
* sklearn
* scipy
* matplotlib

# TODO
[ ] Definir arquivos por meio de argumentos do programa
[ ] Corrigir regex de obtenção dos campos do dataset .csv
[ ] Trocar acesso ao sys.argv por biblioteca de manipulação de argumentos

