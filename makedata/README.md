<!-- -*- encoding: utf-8 -*- -->

道路データの作り方
==================

1. 連続する直線で道路データを作成して、x,yが列挙されたcsvファイルにする。
2. `dump_spline.py` を使ってスプライン曲線データに変換して、csvファイルに保存。
3. `draw_line_plot.py` で結果をグラフ描画して、正常にスプライン曲線データに変換できたか確認。
4. `make_road_csv.py` で、スプライン曲線データのcsvから、道路用、白線用、周辺の三角形用ポリゴンの座標値を計算して、csvファイルに保存。

```
python dump_spline.py -i INPUT.csv > OUTPUT_spline.csv
python draw_line_plot.py OUTPUT_spline.csv
python make_road_csv.py OUTPUT_spline.csv > OUTPUT_roads.csv
```

最終的に得られた OUTPUT_roads.csv を、`draw_road_iso.py` に渡して使う。

元になる、連続した直線の道路データは、QGIS Desktop 3.22.10 + GSI-VTDownloaderプラグインを使って、現実世界に実在している道路のデータから取得した。

実験用スクリプトについて
------------------------

以下のスクリプトは実験時に使ったスクリプト。道路データの作成には関係しない。

* `draw_line.py` は、連続する直線データが正しく得られているか、Python + pygame を使って表示して確認するためのスクリプト。
* `draw_spline.py` は、scipy を使ってスプライン曲線が得られそうか確認するスクリプト。

